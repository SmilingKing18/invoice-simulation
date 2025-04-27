import os, uuid, time
from flask import Flask, render_template, request, jsonify, make_response
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from dotenv import load_dotenv
from models import Base, Session as SessionModel, Demographics, Invoice
from simulation import generate_invoices

# Load config\load_dotenv()
DB_URL = os.getenv('DATABASE_URL', 'sqlite:///data.db')
SECRET_KEY = os.getenv('FLASK_SECRET', str(uuid.uuid4()))

# Setup app & database
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
    if not sess.invoices:
        templates = generate_invoices(num_rounds=5)
        for inv in templates:
            db.add(Invoice(
                session_id=sid,
                round=inv['round'],
                name=inv['name'],
                principle=inv['principle'],
                message=inv['message']
            ))
        db.commit()
    invoices = db.query(Invoice).filter_by(session_id=sid).order_by(Invoice.round).all()
    resp = make_response(render_template('index.html', invoices=invoices))
    resp.set_cookie('session_id', sid, httponly=True)
    return resp

@app.route('/record_demographics', methods=['POST'])
def record_demographics():
    data = request.json
    sid = request.cookies.get('session_id')
    sess, db = get_or_create_session(sid)
    if sess.demographics:
        return jsonify({'error': 'Already submitted'}), 400
    demo = Demographics(
        session_id=sid,
        age_range=data['age_range'],
        gender=data['gender'],
        education=data['education']
    )
    db.add(demo)
    db.commit()
    return jsonify({'message': 'Demographics recorded'})

@app.route('/select_invoice', methods=['POST'])
def select_invoice():
    sid = request.cookies.get('session_id')
    rnd = request.json['round']
    db = SessionLocal()
    inv = db.query(Invoice).filter_by(session_id=sid, round=rnd).one()
    if not inv.open_time:
        inv.open_time = time.time()
        db.commit()
    return jsonify({
        'round': inv.round,
        'name': inv.name,
        'principle': inv.principle,
        'message': inv.message
    })

@app.route('/record_response', methods=['POST'])
def record_response():
    sid = request.cookies.get('session_id')
    data = request.json
    db = SessionLocal()
    inv = db.query(Invoice).filter_by(session_id=sid, round=data['round']).one()
    if inv.response_choice:
        return jsonify({'error': 'Already responded'}), 400
    inv.response_choice = data['response']
    inv.response_time = time.time()
    db.commit()
    return jsonify({'message': 'Response saved'})

@app.route('/record_scales', methods=['POST'])
def record_scales():
    sid = request.cookies.get('session_id')
    data = request.json
    db = SessionLocal()
    inv = db.query(Invoice).filter_by(session_id=sid, round=data['round']).one()
    inv.urgency    = data['urgency']
    inv.arousal    = data['arousal']
    inv.persuasion = data['persuasion']
    inv.trust      = data['trust']
    db.commit()
    return jsonify({'message': 'Ratings saved'})

@app.route('/refresh_invoices', methods=['POST'])
def refresh_invoices():
    sid = request.cookies.get('session_id')
    sess, db = get_or_create_session(sid)
    # delete old and regenerate
    db.query(Invoice).filter_by(session_id=sid).delete()
    db.commit()
    templates = generate_invoices(num_rounds=5)
    for inv in templates:
        db.add(Invoice(session_id=sid, round=inv['round'], name=inv['name'], principle=inv['principle'], message=inv['message']))
    db.commit()
    return jsonify({'message': 'Invoices refreshed'})

if __name__ == '__main__':
    from waitress import serve
    serve(app, host='0.0.0.0', port=8080)