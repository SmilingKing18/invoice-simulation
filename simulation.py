import random
import datetime
import uuid

COMPANIES = [
  {"name":"Acme Solutions, Inc.", "logo_url":"/static/img/acme-logo.png", "address":"123 Elm St, Metropolis, NY"},
  {"name":"Brightside Technologies", "logo_url":"/static/img/brightside-logo.png", "address":"456 Oak Ave, Sunnyvale, CA"},
  {"name":"Greenfield Co.", "logo_url":"/static/img/greenfield-logo.png", "address":"789 Pine Rd, Austin, TX"},
  {"name":"Nova Financial", "logo_url":"/static/img/nova-logo.png", "address":"321 Maple Blvd, Chicago, IL"}
]

PRINCIPLES = {
  "loss aversion": [
    "Friendly reminder: please settle your invoice by the due date to avoid any fees.",
    "Alert: Payment overdue. Additional charges will apply after tomorrow.",
    "Final Notice: Your account is flagged; immediate payment required or service will be suspended."
  ],
  "reciprocity": [
    "Thank you! Please pay your invoice at your convenience.",
    "As a token of appreciation, settle today to receive 5% off your next order.",
    "Exclusive offer: settle now for a 10% loyalty bonus on your next purchase."
  ],
  "social proof": [
    "Notice: 80% of your peers have already paid their invoices.",
    "Most clients in your area paid on time last month.",
    "Congratulations: you’re in the top 10% earliest payers—keep it up!"
  ],
  "urgency": [
    "Time is running out. Avoid interruption by paying today.",
    "2 days left before late fees apply.",
    "FINAL: Payment must be received within 24 hours or service terminates."
  ]
}


def generate_invoices(num_rounds=12):
    invoices = []
    today = datetime.date.today()
    companies = COMPANIES  # exactly 4
    round_no = 1

    for comp in companies:
        principle = random.choice(list(PRINCIPLES.keys()))
        msgs = PRINCIPLES[principle]
        for idx, tone in enumerate(['mild','firm','final']):
            inv_date = today - datetime.timedelta(days=random.randint(3,10))
            due_date = inv_date + datetime.timedelta(days=random.randint(7,21))
            amount = round(random.uniform(50,500),2)
            invoice_id = str(uuid.uuid4())[:8]
            invoices.append({
                "round": round_no,
                "company": comp["name"],
                "logo_url": comp["logo_url"],
                "address": comp["address"],
                "invoice_id": invoice_id,
                "invoice_date": inv_date.isoformat(),
                "due_date": due_date.isoformat(),
                "amount_due": amount,
                "principle": principle,
                "tone": tone,
                "message": msgs[idx],
                # tracking fields:
                "open_time": None,
                "action_choice": None,
                "plan_details": None,
                "question_text": None,
                "block_rating": None,
                "final_q1": None,
                "final_q2": None,
                "final_q3": None,
                "final_comments": None
            })
            round_no += 1
    return invoices