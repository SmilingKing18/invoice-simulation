# simulation.py
import random
from datetime import datetime, timedelta
import uuid

COMPANIES = [
    { 'company': 'Acme Corp',    'logo_url': '/static/logo_acme.png', 'address': '123 Main St.' },
    { 'company': 'Globex Inc',   'logo_url': '/static/logo_globex.png','address': '456 Elm St.' },
    { 'company': 'Soylent Co',   'logo_url': '/static/logo_soylent.png','address': '789 Oak St.' },
    { 'company': 'Initech LLC',  'logo_url': '/static/logo_initech.png','address': '246 Pine St.' },
]

PRINCIPLES = {
    'loss_aversion': [
        "Don't miss out—pay today!",
        "Your past-due balance is growing.",
        "Final notice before extra fees apply!"
    ],
    'reciprocity': [
        "Thanks for being a valued customer—please settle.",
        "We appreciate your prompt payment history.",
        "We value your continued partnership—last reminder!"
    ],
    # add more principles...
}


def generate_invoices():
    invoices = []
    today = datetime.utcnow().date()
    for c in COMPANIES:
        principle = random.choice(list(PRINCIPLES.keys()))
        msgs = PRINCIPLES[principle]
        for idx, tone in enumerate(['mild','firm','final'], start=1):
            inv_date = today - timedelta(days=random.randint(3,10))
            due_date = inv_date + timedelta(days=random.randint(7,21))
            amount = round(random.uniform(50,500),2)
            coupon = 'SAVE5' if random.random() < .3 else None
            invoices.append({
                'company': c['company'],
                'logo_url': c['logo_url'],
                'address': c['address'],
                'invoice_id': uuid.uuid4().hex[:8],
                'invoice_date': inv_date.isoformat(),
                'due_date': due_date.isoformat(),
                'principle': principle,
                'tone': tone,
                'message': msgs[idx-1],
                'coupon': coupon,
                'amount_due': amount,
                'round': len(invoices)+1
            })
    return invoices