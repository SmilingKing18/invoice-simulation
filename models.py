from sqlalchemy import Column, String, Integer, Float, DateTime, Text, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class Session(Base):
    __tablename__ = 'sessions'
    session_id = Column(String, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
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
    name = Column(String)
    principle = Column(String)
    message = Column(Text)
    open_time = Column(Float, nullable=True)
    response_time = Column(Float, nullable=True)
    response_choice = Column(String, nullable=True)
    urgency = Column(Integer, nullable=True)
    arousal = Column(Integer, nullable=True)
    persuasion = Column(Integer, nullable=True)
    trust = Column(Integer, nullable=True)
    session = relationship('Session', back_populates='invoices')