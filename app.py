import os
from flask import Flask, request, jsonify, render_template, make_response, send_file
from flask_migrate import Migrate
from models import db, Session, Demographics, Invoice
from simulation import generate_invoices
import csv
import io
import uuid

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = os.getenv('SECRET_KEY')
    db.init_app(app)
    Migrate(app, db)

    @app.before_request
    def ensure_session():
        sid = request.cookies.get('session_id')
        if not sid:
            sid = uuid.uuid4().hex
            sess = Session(session_id=sid)
            db.session.add(sess)
            # populate invoices
            for inv in generate_invoices():
                inv['session_id'] = sid
                db.session.add(Invoice(**inv))
            db.session.commit()
            resp = make_response()
            resp.set_cookie('session_id', sid, httponly=True)
            return resp
    @app.route('/')
    def index():
        sid = request.cookies.get('session_id')
        sess = Session.query.get(sid)
        invoices = Invoice.query.filter_by(session_id=sid).all()
        return render_template('index.html', invoices=invoices, budget=sess.budget, points=sess.points)

    @app.route('/record_demographics', methods=['POST'])
    def record_demographics():
        data = request.json
        sid = request.cookies.get('session_id')
        demo = Demographics(session_id=sid, **data)
        db.session.add(demo)
        db.session.commit()
        return jsonify(success=True)

    @app.route('/select_invoice', methods=['POST'])
    def select_invoice():
        data = request.json; sid = request.cookies.get('session_id')
        inv = Invoice.query.filter_by(session_id=sid, round=data['round']).first()
        # mark open_time if desired...
        sess = Session.query.get(sid)
        return jsonify(invoice={
            'company':inv.company, 'logo_url':inv.logo_url, 'address':inv.address,
            'invoice_id':inv.invoice_id, 'invoice_date':inv.invoice_date,
            'due_date':inv.due_date, 'principle':inv.principle,
            'tone':inv.tone, 'message':inv.message, 'coupon':inv.coupon,
            'amount_due':inv.amount_due
        }, budget=sess.budget, points=sess.points)

    @app.route('/record_action', methods=['POST'])
    def record_action():
        data = request.json; sid = request.cookies.get('session_id')
        inv = Invoice.query.filter_by(session_id=sid, round=data['round']).first()
        sess = Session.query.get(sid)
        action = data['action']
        if action == 'pay':
            sess.budget -= inv.amount_due
            pts = {'mild':2,'firm':5,'final':10}[inv.tone]
            sess.points += pts
            inv.receipt_code = uuid.uuid4().hex[:8]
            inv.action_choice = 'pay'
        elif action == 'archive':
            penalty = inv.amount_due * .05
            sess.budget -= penalty
            inv.action_choice = 'archive'
        elif action == 'plan':
            inv.plan_details = data.get('plan')
            installments = int(data.get('plan').split()[0])
            sess.points -= installments
            inv.action_choice = 'plan'
        elif action == 'ask':
            inv.question_text = data.get('question')
            inv.action_choice = 'ask'
        db.session.commit()
        return jsonify(budget=sess.budget, points=sess.points, receipt=inv.receipt_code)

    @app.route('/record_block_survey', methods=['POST'])
    def record_block_survey():
        d = request.json; sid = request.cookies.get('session_id')
        inv = Invoice.query.filter_by(session_id=sid, round=d['round']).first()
        inv.block_rating = d['rating']
        db.session.commit()
        return jsonify(success=True)

    @app.route('/record_final_survey', methods=['POST'])
    def record_final_survey():
        d = request.json; sid = request.cookies.get('session_id')
        invs = Invoice.query.filter_by(session_id=sid).order_by(Invoice.round).all()
        last = invs[-1]
        last.final_q1 = d['q1']; last.final_q2 = d['q2']
        last.final_q3 = d['q3']; last.final_comments = d['comments']
        db.session.commit()
        return jsonify(success=True)

    @app.route('/refresh_invoices', methods=['POST'])
    def refresh():
        sid = request.cookies.get('session_id')
        Invoice.query.filter_by(session_id=sid).delete()
        for inv in generate_invoices(): inv['session_id']=sid; db.session.add(Invoice(**inv))
        db.session.commit()
        return jsonify(success=True)

    @app.route('/download-data')
    def download_data():
        sid = request.args.get('session_id') or request.cookies.get('session_id')
        invoices = Invoice.query.filter_by(session_id=sid).all()
        demos = Demographics.query.filter_by(session_id=sid).all()
        buf = io.StringIO()
        writer = csv.writer(buf)
        # write invoice CSV header
        writer.writerow(['id','session_id','company','round','action_choice','amount_due','plan_details','question_text','receipt_code','block_rating','final_q1','final_q2','final_q3','final_comments'])
        for inv in invoices:
            writer.writerow([inv.id, inv.session_id, inv.company, inv.round, inv.action_choice, inv.amount_due, inv.plan_details, inv.question_text, inv.receipt_code, inv.block_rating, inv.final_q1, inv.final_q2, inv.final_q3, inv.final_comments])
        buf.seek(0)
        return send_file(io.BytesIO(buf.read().encode()), mimetype='text/csv', attachment_filename='invoices.csv')

    # Dev-only: download all data across sessions
    @app.route('/download-data-all')
    def download_data_all():
        # Export both demographics and invoice tables for all sessions
        demos = Demographics.query.all()
        invoices = Invoice.query.all()
        zip_buf = io.BytesIO()
        with zipfile.ZipFile(zip_buf, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # demographics.csv
            demo_buf = io.StringIO()
            demo_writer = csv.writer(demo_buf)
            demo_writer.writerow(['id','session_id','age_range','gender','education','submitted_at'])
            for d in demos:
                demo_writer.writerow([d.id, d.session_id, d.age_range, d.gender, d.education, d.submitted_at.isoformat()])
            zipf.writestr('demographics.csv', demo_buf.getvalue())
            # invoices.csv
            inv_buf = io.StringIO()
            inv_writer = csv.writer(inv_buf)
            inv_writer.writerow(['id','session_id','company','round','action_choice','amount_due','plan_details','question_text','receipt_code','block_rating','final_q1','final_q2','final_q3','final_comments'])
            for inv in invoices:
                inv_writer.writerow([inv.id, inv.session_id, inv.company, inv.round, inv.action_choice, inv.amount_due, inv.plan_details, inv.question_text, inv.receipt_code, inv.block_rating, inv.final_q1, inv.final_q2, inv.final_q3, inv.final_comments])
            zipf.writestr('invoices.csv', inv_buf.getvalue())
        zip_buf.seek(0)
        return send_file(zip_buf, mimetype='application/zip', attachment_filename='all_data.zip')

    return app

if __name__=='__main__':
    create_app().run()