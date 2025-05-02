from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid

db = SQLAlchemy()

class Session(db.Model):
    session_id = db.Column(db.String, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    budget = db.Column(db.Float, default=1000.0)
    points = db.Column(db.Integer, default=0)
    demographics = db.relationship('Demographics', backref='session', uselist=False)
    invoices = db.relationship('Invoice', backref='session', lazy=True)

class Demographics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String, db.ForeignKey('session.session_id'), nullable=False)
    age_range = db.Column(db.String)
    gender = db.Column(db.String)
    education = db.Column(db.String)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)

class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String, db.ForeignKey('session.session_id'), nullable=False)
    round = db.Column(db.Integer)
    company = db.Column(db.String)
    logo_url = db.Column(db.String)
    address = db.Column(db.String)
    invoice_id = db.Column(db.String, default=lambda: uuid.uuid4().hex[:8])
    invoice_date = db.Column(db.String)
    due_date = db.Column(db.String)
    principle = db.Column(db.String)
    tone = db.Column(db.String)
    message = db.Column(db.Text)
    coupon = db.Column(db.String, nullable=True)
    amount_due = db.Column(db.Float)
    action_choice = db.Column(db.String, nullable=True)
    plan_details = db.Column(db.String, nullable=True)
    question_text = db.Column(db.Text, nullable=True)
    receipt_code = db.Column(db.String, nullable=True)
    block_rating = db.Column(db.Integer, nullable=True)
    final_q1 = db.Column(db.Integer, nullable=True)
    final_q2 = db.Column(db.String, nullable=True)
    final_q3 = db.Column(db.String, nullable=True)
    final_comments = db.Column(db.Text, nullable=True)