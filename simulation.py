import random
import datetime
import uuid
import random, datetime, uuid

COMPANIES = [
    {"name":"Acme Solutions, Inc.",    "logo_url":"/static/img/acme-logo.png",    "address":"123 Elm St, Metropolis, NY"},
    {"name":"Brightside Technologies", "logo_url":"/static/img/brightside-logo.png","address":"456 Oak Ave, Sunnyvale, CA"},
    {"name":"Greenfield Co.",         "logo_url":"/static/img/greenfield-logo.png","address":"789 Pine Rd, Austin, TX"},
    {"name":"Nova Financial",         "logo_url":"/static/img/nova-logo.png",      "address":"321 Maple Blvd, Chicago, IL"}
]

# --- now full email templates per principle (mild, firm, final) ---
PRINCIPLES = {
    "loss aversion": [
        # mild
        """Dear {name} Customer,

Please find attached invoice #{invoice_id} for €{amount:.2f}, due on {due_date}.

We kindly remind you that settling this amount by the due date will help you avoid any late fees. Timely payments ensure uninterrupted service and protect your credit standing.

If you need any assistance or wish to discuss payment options, please reach out at your earliest convenience.

Best regards,
{company} Billing Team""",
        # firm
        """Dear {name} Customer,

This is a reminder that invoice #{invoice_id} for €{amount:.2f}, due on {due_date}, has not yet been paid.

Please note that a late fee of 5% will be applied if payment is not received within 48 hours. To prevent any additional charges, we urge you to remit payment promptly.

We appreciate your prompt attention to this matter and are available to help if you encounter any issues.

Sincerely,
{company} Billing Team""",
        # final
        """Dear {name} Customer,

FINAL NOTICE: Invoice #{invoice_id} for €{amount:.2f}, originally due on {due_date}, remains outstanding.

Immediate payment is required to avoid suspension of your account and referral to collections. Please make payment today to prevent further action.

Thank you for your urgent attention.

Regards,
{company} Billing Team"""
    ],
    "scarcity": [
        # mild
        """Dear {name} Customer,

Your invoice #{invoice_id} for €{amount:.2f}, due on {due_date}, is ready for payment.

As a token of appreciation, we’re offering a 2% early-payment discount for those who settle within 5 days. This limited-time offer helps you save and supports our operations.

Don’t miss out—take advantage of this benefit by paying early.

Warm regards,
{company} Billing Team""",
        # firm
        """Dear {name} Customer,

Invoice #{invoice_id} for €{amount:.2f} is due on {due_date}.

Only 10 spots remain for our early-bird discount—act quickly to secure your savings. Once those spots are gone, the standard amount applies.

We value your business and encourage you to pay now to enjoy this exclusive rate.

Best,
{company} Billing Team""",
        # final
        """Dear {name} Customer,

URGENT: Invoice #{invoice_id} for €{amount:.2f}, due on {due_date}, is pending.

This is your last chance to qualify for our 2% early-payment discount. After today, that opportunity expires and late fees will apply.

Please remit payment immediately to lock in your savings.

Thank you,
{company} Billing Team"""
    ],
    "social proof": [
        # mild
        """Dear {name} Customer,

Invoice #{invoice_id} for €{amount:.2f} is due on {due_date}.

Already, over 60% of our clients have paid on time—join them to keep your account in good standing. Early payments help us serve you and your peers better.

We appreciate your timely action.

Cheers,
{company} Billing Team""",
        # firm
        """Dear {name} Customer,

Your invoice #{invoice_id} for €{amount:.2f}, due on {due_date}, is outstanding.

Last week, 80% of customers in your region settled their bills promptly. To maintain that community standard, please pay yours today.

Thank you for being part of our valued customer network.

Regards,
{company} Billing Team""",
        # final
        """Dear {name} Customer,

FINAL REMINDER: Invoice #{invoice_id} for €{amount:.2f}, due on {due_date}, remains unpaid.

Nearly 95% of your peers have already completed their payments—don’t be left behind. Please pay immediately to align with the majority and avoid late fees.

Sincerely,
{company} Billing Team"""
    ],
    "urgency": [
        # mild
        """Dear {name} Customer,

Invoice #{invoice_id} for €{amount:.2f} is due on {due_date}.

We encourage you to pay as soon as possible to keep everything on schedule. Prompt action ensures no disruption to your service.

Feel free to contact us if you need extra time.

All the best,
{company} Billing Team""",
        # firm
        """Dear {name} Customer,

Your invoice #{invoice_id} for €{amount:.2f}, due on {due_date}, needs your attention.

A late fee will be added if payment is not received within 2 days. Please act now to prevent extra charges.

We’re here to help if you require assistance.

Thank you,
{company} Billing Team""",
        # final
        """Dear {name} Customer,

FINAL ALERT: Invoice #{invoice_id} for €{amount:.2f}, originally due {due_date}, is now severely overdue.

Immediate payment is mandatory to avoid service interruption and further penalties. Please settle your account within 24 hours.

Thank you for your prompt action.

Best regards,
{company} Billing Team"""
    ]
}
# ------------------------------------------------------------------

def generate_invoices(num_rounds=12):
    invoices = []
    today = datetime.date.today()
    round_no = 1

    for comp in COMPANIES:
        principle = random.choice(list(PRINCIPLES.keys()))
        msgs = PRINCIPLES[principle]
        for idx, tone in enumerate(['mild','firm','final']):
            inv_date = today - datetime.timedelta(days=random.randint(3,10))
            due_date = inv_date + datetime.timedelta(days=random.randint(7,21))
            amount = round(random.uniform(50,500),2)
            invoice_id = str(uuid.uuid4())[:8]
            due_str = due_date.strftime('%d %B %Y')

            # --- Build full_msg from the chosen template ---
            full_msg = msgs[idx].format(
                name=comp['name'],
                company=comp['name'],
                invoice_id=invoice_id,
                amount=amount,
                due_date=due_str
            )
            # ---------------------------------------------------

            invoices.append({
                "round": round_no,
                "company": comp["name"],
                "logo_url": comp["logo_url"],
                "address": comp["address"],
                "invoice_id": invoice_id,
                "invoice_date": inv_date.isoformat(),
                "due_date": due_date.isoformat(),
                "amount_due": amount,
                "coupon": "SAVE5" if random.random()>0.3 else None,
                "principle": principle,
                "tone": tone,
                "message": full_msg,
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
