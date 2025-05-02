// static/js/app.js

// --- Global state ---
const demographics = {};
let currentEmail = null;
let currentRound = null;
let currentCompany = null;
let ratings = {};
const companyMap = {};

// --- Initialization functions ---
function setupDemoForm() {
  const form = document.getElementById('demo-form');
  form.addEventListener('submit', e => {
    e.preventDefault();
    demographics.age_range = document.getElementById('age_range').value;
    demographics.gender    = document.getElementById('gender').value;
    demographics.education  = document.getElementById('education').value;
    demographics.location   = document.getElementById('location').value.trim();
    document.getElementById('demo-modal').classList.remove('active');
    document.getElementById('rules-modal').classList.add('active');
  });
}

function initMessageList() {
  const items = document.querySelectorAll('#invoice-list .message-item');
  items.forEach(item => {
    const companyName = item.querySelector('div').textContent.trim();
    const round = parseInt(item.id.split('-').pop());
    if (!companyMap[companyName]) {
      companyMap[companyName] = [];
    }
    companyMap[companyName].push({ round, element: item });
  });
  Object.values(companyMap).forEach(arr => {
    arr.sort((a,b) => a.round - b.round);
    arr.forEach((o, i) => {
      if (i > 0) o.element.style.display = 'none';
      o.element.addEventListener('click', () => selectInvoice(o.round));
    });
  });
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

function setupFinalSurvey() {
  document.getElementById('final-submit').addEventListener('click', () => {
    const q1 = document.getElementById('final_q1').value;
    const q2 = document.getElementById('final_q2').value;
    const q3 = document.getElementById('final_q3').value;
    const comments = document.getElementById('final_comments').value.trim();
    fetch('/record_final_survey', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ q1, q2, q3, comments })
    }).then(() => showThankYou())
      .catch(err => console.error('Final survey error', err));
  });
}

// --- Core Interaction ---
function selectInvoice(round) {
  fetch('/select_invoice', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ round })
  })
    .then(res => res.json())
    .then(data => {
      currentEmail = data;
      currentRound = data.round;
      currentCompany = data.company;
      renderEmail(data);
    })
    .catch(err => console.error('Select invoice error', err));
}

function renderEmail(email) {
  const pane = document.getElementById('invoice-details');
  pane.innerHTML = `
    <img src="${email.logo_url}" alt="${email.company} logo" />
    <h3>${email.company}</h3>
    <p>${email.address}</p>
    <div class="email-body">${email.message.replace(/\n/g, '<br>')}</div>
    <div class="actions">
      <button onclick="onAnswerEmail('pay')">Pay Now</button>
      <button onclick="onAnswerEmail('delay')">Delay Payment</button>
      <button onclick="onAnswerEmail('contest')">Contest Invoice</button>
    </div>
  `;
+  // make the reading pane visible
+  pane.classList.add('active');
}

function onAnswerEmail(action) {
  fetch('/record_action', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ round: currentRound, action })
  })
    .then(res => res.json())
    .then(() => {
      document.getElementById('rating-modal').classList.add('active');
    })
    .catch(err => console.error('Record action error', err));
}

function checkAllRated() {
  const total = document.querySelectorAll('.scale-group').length;
  if (Object.keys(ratings).length === total) {
    document.getElementById('submit-scales').disabled = false;
  }
}

function submitRatings() {
  fetch('/record_block_survey', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ round: currentRound, rating: ratings })
  })
    .then(res => res.json())
    .then(() => {
      document.getElementById('rating-modal').classList.remove('active');
      resetRatings();
      // hide answered
      const answeredEl = document.getElementById(`invoice-item-${currentRound}`);
      answeredEl.style.display = 'none';
      // reveal next in company
      const arr = companyMap[currentCompany];
      const idx = arr.findIndex(o => o.round === currentRound);
      if (idx >= 0 && idx < arr.length - 1) {
        const nextObj = arr[idx + 1];
        nextObj.element.style.display = '';
        const badge = document.createElement('span');
        badge.classList.add('badge');
        badge.textContent = ` (Part ${idx + 2})`;
        nextObj.element.querySelector('div').appendChild(badge);
      }
      // clear pane
      document.getElementById('invoice-details').innerHTML = '';
      // if done
      const remaining = document.querySelectorAll('#invoice-list .message-item')
        .length - document.querySelectorAll('#invoice-list .message-item[style*="display: none"]').length;
      if (remaining === 0) {
        document.getElementById('final-modal').classList.add('active');
      }
    })
    .catch(err => console.error('Record rating error', err));
}

function resetRatings() {
  ratings = {};
  document.getElementById('submit-scales').disabled = true;
  document.querySelectorAll('.bubble.selected').forEach(b => b.classList.remove('selected'));
}

function showThankYou() {
  document.getElementById('final-modal').classList.remove('active');
  document.getElementById('invoice-details').innerHTML = '<h2>Thank you for participating!</h2>';
}

// --- DOM Ready ---
document.addEventListener('DOMContentLoaded', () => {
  setupDemoForm();
  document.getElementById('start-game').addEventListener('click', () => {
    document.getElementById('rules-modal').classList.remove('active');
  });
  initMessageList();
  setupRatingBubbles();
  document.getElementById('submit-scales').addEventListener('click', submitRatings);
  setupFinalSurvey();
});
