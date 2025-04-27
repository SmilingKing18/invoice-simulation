import random
import time

def generate_invoices(num_rounds=5):
    reminders = [
        {"name": "Loss Aversion", "principle": "loss aversion", "message": "Alert: Your account is at risk of service interruption if the invoice is not paid by tomorrow. Avoid extra fees by paying now."},
        {"name": "Reciprocity", "principle": "reciprocity", "message": "Thank you for your loyalty! As a token of our appreciation, settle your invoice today and receive a discount on your next service."},
        {"name": "Social Proof", "principle": "social proof", "message": "Notice: 80% of your peers have already paid their invoices. Join them to continue enjoying uninterrupted service."},
        {"name": "Combined: Loss Aversion & Social Proof", "principle": "loss aversion, social proof", "message": "Urgent: Most clients have already paid, and if you delay, you risk additional charges and service interruption."},
        {"name": "Combined: Reciprocity & Social Proof", "principle": "reciprocity, social proof", "message": "We value your business and many of your peers have paid promptly. Settle this invoice now and receive an exclusive discount on your next order."},
        {"name": "Early Bird Discount", "principle": "scarcity", "message": "Act now to take advantage of our early bird discount before it expires."},
        {"name": "Limited Time Offer", "principle": "scarcity", "message": "This is a limited time offer. Settle your invoice now to secure your benefits."},
        {"name": "Customer Appreciation", "principle": "reciprocity", "message": "We appreciate your continued support. Settle your invoice and enjoy special perks on your next order."},
        {"name": "Loyalty Bonus", "principle": "reciprocity", "message": "Your loyalty matters. Pay your invoice now and earn extra rewards for your future purchases."},
        {"name": "Exclusive Deal", "principle": "exclusivity", "message": "You're one of our valued customers. Settle this invoice to access an exclusive deal tailored for you."},
        {"name": "Priority Service", "principle": "authority", "message": "Ensure priority service by settling your invoice promptly. Don’t miss out on our premium support."},
        {"name": "Fast Track", "principle": "efficiency", "message": "Experience a fast track process by paying your invoice immediately. Your efficiency is rewarded."},
        {"name": "Upgrade Opportunity", "principle": "aspiration", "message": "Unlock an upgrade opportunity by settling your invoice now and enjoy enhanced benefits."},
        {"name": "Time-Sensitive Reminder", "principle": "urgency", "message": "Time is running out. Avoid service interruption by paying your invoice without delay."},
        {"name": "Proactive Savings", "principle": "loss aversion", "message": "Don't miss out on potential savings. Settle your invoice now to avoid extra fees."},
        {"name": "VIP Treatment", "principle": "social proof", "message": "Join our VIP circle by paying your invoice promptly and enjoy top-tier services."},
        {"name": "Smart Choice", "principle": "rational decision-making", "message": "Make the smart choice by settling your invoice now. It’s the best decision for your account."},
        {"name": "Optimal Performance", "principle": "performance", "message": "Keep your account running at optimal performance. Settle your invoice promptly."},
        {"name": "Risk-Free Option", "principle": "safety", "message": "Eliminate any risk of service interruption by paying your invoice immediately."},
        {"name": "Special Invitation", "principle": "exclusivity", "message": "You're specially invited to take advantage of a unique offer by settling your invoice today."}
    ]
    invoices = []
    for i in range(num_rounds):
        reminder = random.choice(reminders)
        invoice = {
            "round": i+1,
            "name": reminder["name"],
            "principle": reminder["principle"],
            "message": reminder["message"],
            "open_time": None,
            "response_time": None,
            "response": None,
            "relationship_rating": None,
        }
        invoices.append(invoice)
    return invoices