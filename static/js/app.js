// static/js/app.js

// --- Global state ---
const demographics = {};
let allEmails = [];           // will be populated from server
let emailQueue = [];
let currentEmailIndex = 0;
let ratings = {};

// --- Helper functions ---

function setupDemoForm() {
  const demoForm = document.getElementById('demo-form');
  demoForm.addEventListener('submit', e => {
    e.preventDefault();
    demographics.age_range = document.getElementById('age_range').value;
    demographics.gender    = document.getElementById('gender').value;
    demographics.education  = document.getElementById('education').value;
    demographics.location   = document.getElementById('location').value.trim();
    document.getElementById('demo-modal').classList.remove('active');
    showRulesModal();
  });
}

function showRulesModal() {
  document.getElementById('rules-modal').classList.add('active');
}

function filterEmailQueue() {
  const seen = new Set();
  emailQueue = allEmails.filter(email => {
    if (seen.has(email.company)) return false;
    seen.add(email.company);
    return true;
  });
}

function renderEmail(email) {
  const pane = document.getElementById('invoice-details');
  pane.innerHTML = `
    <img src='${email.logo_url}' alt='${email.company} logo' />
    <h3>${email.company}</h3>
    <p>${email.address}</p>
    <div class='email-body'>${email.message.replace(/\n/g,'<br>')}</div>
    <div class='actions'>
      <button onclick='onAnswerEmail("pay")'>Pay Now</button>
      <button onclick='onAnswerEmail("delay")'>Delay Payment</button>
      <button onclick='onAnswerEmail("contest")'>Contest Invoice</button>
    </div>
  `;
}

function loadNextEmail() {
  if (currentEmailIndex >= emailQueue.length) {
    return showEndOfGame();
  }
  renderEmail(emailQueue[currentEmailIndex]);
}

function onAnswerEmail(action) {
  document.getElementById('rating-modal').classList.add('active');
}

function setupRatingBubbles() {
  const groups = document.querySelectorAll('.scale-group');
  groups.forEach(group => {
    const q = group.dataset.question;
    const container = group.querySelector('.scale');
    for (let i = 1; i <= 5; i++) {
      const bubble = document.createElement('div');
      bubble.classList.add('bubble');
      bubble.textContent = i;
      bubble.dataset.value = i;
      container.appendChild(bubble);
      bubble.addEventListener('click', () => {
        container.querySelectorAll('.bubble').forEach(b => b.classList.remove('selected'));
        bubble.classList.add('selected');
        ratings[q] = i;
        checkAllRated();
      });
    }
  });
}

function checkAllRated() {
  if (Object.keys(ratings).length === document.querySelectorAll('.scale-group').length) {
    document.getElementById('submit-scales').disabled = false;
  }
}

function submitRatings() {
  saveResponse({
    round: emailQueue[currentEmailIndex].round,
    ratings,
    demographics
  });
  document.getElementById('rating-modal').classList.remove('active');
  resetRatings();
  currentEmailIndex++;
  loadNextEmail();
}

function resetRatings() {
  ratings = {};
  document.getElementById('submit-scales').disabled = true;
  document.querySelectorAll('.bubble.selected').forEach(b => b.classList.remove('selected'));
}

function setupPlanForm() {
  document.getElementById('plan-form').addEventListener('submit', e => {
    e.preventDefault();
    const installments = document.getElementById('installments').value;
    document.getElementById('plan-modal').classList.remove('active');
  });
}

function setupQuestionForm() {
  document.getElementById('question-form').addEventListener('submit', e => {
    e.preventDefault();
    const question = document.getElementById('question_text').value.trim();
    document.getElementById('question-modal').classList.remove('active');
  });
}

function setupFinalSurvey() {
  document.getElementById('final-submit').addEventListener('click', () => {
    const final_q1 = document.getElementById('final_q1').value;
    const final_q2 = document.getElementById('final_q2').value;
    const final_q3 = document.getElementById('final_q3').value;
    const final_comments = document.getElementById('final_comments').value.trim();
    document.getElementById('final-modal').classList.remove('active');
    showThankYou();
  });
}

function showEndOfGame() {
  document.getElementById('final-modal').classList.add('active');
}

function showThankYou() {
  const pane = document.getElementById('invoice-details');
  pane.innerHTML = '<h2>Thank you for participating!</h2>';
}

function saveResponse(data) {
  console.log('Saving response', data);
}

// --- Initialization ---
document.addEventListener('DOMContentLoaded', () => {
  setupDemoForm();
  document.getElementById('start-game').addEventListener('click', () => {
    document.getElementById('rules-modal').classList.remove('active');
    loadNextEmail();
  });
  setupRatingBubbles();
  document.getElementById('submit-scales').addEventListener('click', submitRatings);
  setupPlanForm();
  setupQuestionForm();
  setupFinalSurvey();

  fetch('/api/invoices')
    .then(response => response.json())
    .then(data => {
      allEmails = data;
      filterEmailQueue();
    })
    .catch(err => console.error('Error loading invoices:', err));
});