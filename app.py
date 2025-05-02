import os, uuid, time
from flask import Flask, render_template, request, jsonify, make_response
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from dotenv import load_dotenv
from models import Base, Session as SessionModel, Demographics, Invoice
from simulation import generate_invoices

# Load config
load_dotenv()
DB_URL = os.getenv('DATABASE_URL', 'sqlite:///data.db')
SECRET_KEY = os.getenv('FLASK_SECRET', str(uuid.uuid4()))

# Setup app & DB
app = Flask(__name__)
app.secret_key = SECRET_KEY
engine = create_engine(DB_URL, echo=False, future=True)
Base.metadata.create_all(engine)
SessionLocal = scoped_session(sessionmaker(bind=engine))

def get_or_create_session(sid):
    db = SessionLocal()
    sess = db.get(SessionModel, sid)
    if not sess:
        sess = SessionModel(session_id=sid)
        db.add(sess)
        db.commit()
    return sess, db

@app.route('/')
def index():
    sid = request.cookies.get('session_id') or str(uuid.uuid4())
    sess, db = get_or_create_session(sid)
    # Initialize invoices if first visit
    if not sess.invoices:
        templates = generate_invoices(num_rounds=12)
        for inv in templates:
            db.add(Invoice(session_id=sid, **inv))
        db.commit()
    invoices = db.query(Invoice).filter_by(session_id=sid).order_by(Invoice.round).all()
    resp = make_response(render_template('index.html', invoices=invoices,
        budget=sess.budget, points=sess.points))
    resp.set_cookie('session_id', sid, httponly=True)
    return resp

@app.route('/record_demographics', methods=['POST'])
def record_demographics():
    data = request.json
    sid = request.cookies.get('session_id')
    sess, db = get_or_create_session(sid)
    if sess.demographics:
        return jsonify({'error': 'Already submitted'}), 400
    demo = Demographics(session_id=sid, age_range=data['age_range'],
                         gender=data['gender'], education=data['education'])
    db.add(demo); db.commit()
    return jsonify({'message': 'Demographics recorded'})

@app.route('/select_invoice', methods=['POST'])
def select_invoice():
    sid = request.cookies.get('session_id')
    rnd = request.json['round']
    db = SessionLocal()
    inv = db.query(Invoice).filter_by(session_id=sid, round=rnd).one()
    if not inv.open_time:
        inv.open_time = time.time(); db.commit()
    sess = db.get(SessionModel, sid)
    return jsonify({
      'round':inv.round,'company':inv.company,'logo_url':inv.logo_url,
      'address':inv.address,'invoice_id':inv.invoice_id,'invoice_date':inv.invoice_date,
      'due_date':inv.due_date,'amount_due':inv.amount_due,'message':inv.message,
      'budget': sess.budget, 'points': sess.points
    })

@app.route('/record_action', methods=['POST'])
def record_action():
    data = request.json; sid = request.cookies.get('session_id')
    db = SessionLocal()
    inv = db.query(Invoice).filter_by(session_id=sid, round=data['round']).one()
    sess = db.get(SessionModel, sid)
    action = data['action']
    inv.action_choice = action
    if action=='pay':
        sess.budget -= inv.amount_due
        sess.points += 10 if inv.tone=='mild' else 5 if inv.tone=='firm' else 2
    elif action=='archive':
        penalty = inv.amount_due * 0.05
        sess.budget -= penalty
    inv.plan_details = data.get('plan',None)
    inv.question_text = data.get('question',None)
    db.commit()
    return jsonify({'budget':sess.budget,'points':sess.points})

@app.route('/record_block_survey', methods=['POST'])
def record_block_survey():
    data = request.json; sid = request.cookies.get('session_id')
    db = SessionLocal()
    inv = db.query(Invoice).filter_by(session_id=sid, round=data['round']).one()
    inv.block_rating = data['rating']; db.commit()
    return jsonify({'message':'Block rating saved'})

@app.route('/record_final_survey', methods=['POST'])
def record_final_survey():
    data = request.json; sid = request.cookies.get('session_id')
    db = SessionLocal()
    last = db.query(Invoice).filter_by(session_id=sid).order_by(Invoice.round.desc()).first()
    last.final_q1 = data['q1']; last.final_q2=data['q2'];
    last.final_q3=data['q3']; last.final_comments=data['comments']
    db.commit()
    return jsonify({'message':'Final survey saved'})

if __name__=='__main__':
    from waitress import serve
    serve(app, host='0.0.0.0', port=8080)