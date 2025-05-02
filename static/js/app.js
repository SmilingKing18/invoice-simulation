// --- Global state ---
const demographics = {};
let allEmails = [];           // populate from server
let emailQueue = [];
let currentEmailIndex = 0;
let ratings = {};

// --- On DOM ready ---
document.addEventListener('DOMContentLoaded', () => {
  setupDemoForm();
  filterEmailQueue();
  // ... any other init you had …
});

// Demographics form
function setupDemoForm() {
  document.getElementById('demo-form').addEventListener('submit', e => {
    e.preventDefault();
    demographics.age_range = document.getElementById('age_range').value;
    demographics.gender    = document.getElementById('gender').value;
    demographics.education  = document.getElementById('education').value;
    demographics.location   = document.getElementById('location').value.trim();

    document.getElementById('demo-modal').classList.remove('active');
    showRulesModal();
  });
}

// Rules modal
function showRulesModal() {
  document.getElementById('rules-modal').classList.add('active');
}
document.getElementById('start-game').addEventListener('click', () => {
  document.getElementById('rules-modal').classList.remove('active');
  loadNextEmail();
});

// Filter one per company
function filterEmailQueue() {
  const seen = new Set();
  emailQueue = allEmails.filter(email => {
    if (seen.has(email.company)) return false;
    seen.add(email.company);
    return true;
  });
}

// Load & render next
function loadNextEmail() {
  if (currentEmailIndex >= emailQueue.length) {
    return showEndOfGame();
  }
  renderEmail(emailQueue[currentEmailIndex]);
}

// When user answers (pay/delay/contest)
function onAnswerEmail(action) {
  // record action…
  // then show rating modal:
  document.getElementById('rating-modal').classList.add('active');
}

// Rating bubbles setup
const groups = document.querySelectorAll('.scale-group');
groups.forEach(group => {
  const q = group.dataset.question;
  const container = group.querySelector('.scale');
  for (let i = 1; i <= 5; i++) {
    const b = document.createElement('div');
    b.classList.add('bubble');
    b.textContent = i;
    b.dataset.value = i;
    container.appendChild(b);
    b.addEventListener('click', () => {
      container.querySelectorAll('.bubble').forEach(x => x.classList.remove('selected'));
      b.classList.add('selected');
      ratings[q] = i;
      checkAllRated();
    });
  }
});

function checkAllRated() {
  if (Object.keys(ratings).length === groups.length) {
    document.getElementById('submit-scales').disabled = false;
  }
}

document.getElementById('submit-scales').addEventListener('click', () => {
  saveResponse({
    emailId: emailQueue[currentEmailIndex].id,
    ratings,
    demographics
  });
  // reset
  groups.forEach(g => g.querySelectorAll('.bubble').forEach(b => b.classList.remove('selected')));
  document.getElementById('submit-scales').disabled = true;
  ratings = {};
  currentEmailIndex++;
  document.getElementById('rating-modal').classList.remove('active');
  loadNextEmail();
});

// Utility: enrich each email with fullBody
function enrichEmails() {
  emailQueue.forEach(email => {
    email.fullBody = `
Dear ${email.recipientName || 'Customer'},

Please find attached invoice #${email.invoiceNumber} for €${email.amount.toFixed(2)},
due on ${new Date(email.dueDate).toLocaleDateString('en-GB', {
  day: 'numeric', month: 'long', year: 'numeric'
})}.

You are currently in the top 10% of our earliest payers—thank you for your promptness!
Timely payments help us keep serving you better. Let us know if you have any questions.

Best regards,
The Billing Team
    `;
  });
}

// Call enrichEmails() after filterEmailQueue()
