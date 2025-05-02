from sqlalchemy import Column, String, Integer, Float, DateTime, Text, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class Session(Base):
    __tablename__ = 'sessions'
    session_id = Column(String, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    budget = Column(Float, default=1000.0)
    points = Column(Integer, default=0)
    demographics = relationship('Demographics', back_populates='session', uselist=False)
    invoices = relationship('Invoice', back_populates='session')

class Demographics(Base):
    __tablename__ = 'demographics'
    id = Column(Integer, primary_key=True)
    session_id = Column(String, ForeignKey('sessions.session_id'), unique=True)
    age_range = Column(String)
    gender = Column(String)
    education = Column(String)
    submitted_at = Column(DateTime, default=datetime.utcnow)
    session = relationship('Session', back_populates='demographics')

class Invoice(Base):
    __tablename__ = 'invoices'
    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String, ForeignKey('sessions.session_id'))
    round = Column(Integer)
    company = Column(String)
    logo_url = Column(String)
    address = Column(String)
    invoice_id = Column(String)
    invoice_date = Column(String)
    due_date = Column(String)
    amount_due = Column(Float)
    principle = Column(String)
    tone = Column(String)
    message = Column(Text)
    open_time = Column(Float, nullable=True)
    action_choice = Column(String, nullable=True)
    plan_details = Column(String, nullable=True)
    question_text = Column(Text, nullable=True)
    block_rating = Column(Integer, nullable=True)
    final_q1 = Column(Integer, nullable=True)
    final_q2 = Column(String, nullable=True)
    final_q3 = Column(String, nullable=True)
    final_comments = Column(Text, nullable=True)
    session = relationship('Session', back_populates='invoices')