document.addEventListener('DOMContentLoaded', () => {
    const list = document.getElementById('message-list');
    const invoiceCard = document.getElementById('invoice-card');
    const statusBudget = document.getElementById('status-budget');
    const statusPoints = document.getElementById('status-points');
  
    // Modal elements
    const modals = document.querySelectorAll('.modal');
    const openModal = id => document.getElementById(id).classList.add('active');
    const closeModal = id => document.getElementById(id).classList.remove('active');
    const closeAllModals = () => modals.forEach(m => m.classList.remove('active'));
  
    // Keep track of current round and completed count
    let currentRound;
    let completedCount = 0;
  
    // Initialize survey scales (block survey)
    document.querySelectorAll('#modal-block-survey .scale').forEach(scaleEl => {
      const scale = scaleEl.dataset.scale;
      for (let i = 1; i <= 5; i++) {
        const bubble = document.createElement('div');
        bubble.className = 'bubble';
        bubble.dataset.value = i;
        bubble.addEventListener('click', () => {
          // Deselect others
          scaleEl.querySelectorAll('.bubble').forEach(b => b.classList.remove('selected'));
          bubble.classList.add('selected');
        });
        scaleEl.append(bubble);
      }
    });
  
    // Render invoice data into card
    const renderInvoice = (invoice, budget, points) => {
      invoiceCard.classList.remove('hidden');
      document.getElementById('card-logo').src = invoice.logo_url;
      document.getElementById('card-company').textContent = invoice.company;
      document.getElementById('card-address').textContent = invoice.address;
      document.getElementById('card-invoice-id').textContent = invoice.invoice_id;
      document.getElementById('card-invoice-date').textContent = invoice.invoice_date;
      document.getElementById('card-due-date').textContent = invoice.due_date;
      document.getElementById('card-message').textContent = invoice.message;
  
      const couponEl = document.getElementById('card-coupon');
      if (invoice.coupon) {
        document.getElementById('card-coupon-code').textContent = invoice.coupon;
        couponEl.classList.remove('hidden');
      } else {
        couponEl.classList.add('hidden');
      }
  
      document.getElementById('card-amount').textContent = invoice.amount_due.toFixed(2);
  
      // Actions metadata
      document.getElementById('action-pay-cost').textContent = `-$${invoice.amount_due.toFixed(2)}`;
      const pointsMap = { mild: 2, firm: 5, final: 10 };
      document.getElementById('action-pay-points').textContent = pointsMap[invoice.tone];
  
      // Update status
      statusBudget.textContent = budget.toFixed(2);
      statusPoints.textContent = points;
  
      // Attach actions
      ['pay', 'plan', 'ask', 'archive'].forEach(action => attachAction(action, invoice.round));
    };
  
    // Generic action handler
    const attachAction = (action, round) => {
      const btn = document.getElementById(`action-${action}`);
      btn.onclick = () => {
        closeAllModals();
        if (action === 'plan') return openModal('modal-plan');
        if (action === 'ask') return openModal('modal-question');
        // pay or archive
        fetch('/record_action', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ round, action })
        })
        .then(res => res.json())
        .then(data => {
          statusBudget.textContent = data.budget.toFixed(2);
          statusPoints.textContent = data.points;
          if (action === 'pay') {
            document.getElementById('receipt-code').textContent = data.receipt;
            openModal('modal-receipt');
          }
        });
      };
    };
  
    // Demographics submission
    document.getElementById('form-demographics').onsubmit = e => {
      e.preventDefault();
      const form = e.target;
      const data = { age_range: form.age_range.value, gender: form.gender.value, education: form.education.value };
      fetch('/record_demographics', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) })
        .then(() => { closeModal('modal-demographics'); openModal('modal-rules'); });
    };
  
    // Rules modal close
    document.getElementById('rules-close').onclick = () => closeModal('modal-rules');
  
    // Plan submission
    document.getElementById('form-plan').onsubmit = e => {
      e.preventDefault();
      const plan = e.target.plan.value;
      fetch('/record_action', { method:'POST', headers:{ 'Content-Type':'application/json'}, body:JSON.stringify({ round: currentRound, action:'plan', plan }) })
        .then(res => res.json()).then(data => { statusPoints.textContent = data.points; closeModal('modal-plan'); });
    };
  
    // Question submission
    document.getElementById('form-question').onsubmit = e => {
      e.preventDefault();
      const question = e.target.question.value;
      fetch('/record_action', { method:'POST', headers:{ 'Content-Type':'application/json'}, body:JSON.stringify({ round: currentRound, action:'ask', question }) })
        .then(() => closeModal('modal-question'));
    };
  
    // Receipt close
    document.getElementById('receipt-close').onclick = () => closeModal('modal-receipt');
  
    // Block Survey submission
    document.getElementById('form-block-survey').onsubmit = e => {
      e.preventDefault();
      // gather ratings
      const ratings = {};
      document.querySelectorAll('#modal-block-survey .scale').forEach(scaleEl => {
        const key = scaleEl.dataset.scale;
        const selected = scaleEl.querySelector('.bubble.selected');
        ratings[key] = selected ? parseInt(selected.dataset.value) : null;
      });
      fetch('/record_block_survey', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ round: currentRound, ratings })
      }).then(() => {
        closeModal('modal-block-survey');
        // if all 12 done, open final survey
        if (++completedCount === 12) openModal('modal-final-survey');
      });
    };
  
    // Final Survey submission
    document.getElementById('form-final-survey').onsubmit = e => {
      e.preventDefault();
      const form = e.target;
      const data = {
        q1: parseInt(form.q1.value),
        q2: form.q2.value,
        q3: form.q3.value,
        comments: form.comments.value
      };
      fetch('/record_final_survey', { method:'POST', headers:{ 'Content-Type':'application/json' }, body:JSON.stringify(data) })
        .then(() => { closeModal('modal-final-survey'); alert('Thanks for completing the study!'); });
    };
  
    // Invoice selection
    list.addEventListener('click', async e => {
      const li = e.target.closest('li'); if (!li) return;
      currentRound = li.dataset.round;
      const res = await fetch('/select_invoice', { method: 'POST', headers:{ 'Content-Type':'application/json' }, body: JSON.stringify({ round: currentRound }) });
      const { invoice, budget, points } = await res.json();
      renderInvoice(invoice, budget, points);
      li.remove();
      completedCount++;
      // every 3 invoices
      if (completedCount % 3 === 0 && completedCount < 12) openModal('modal-block-survey');
      // if last processed and final not shown here, will show in block handler above
    });
  
    // On first load
    openModal('modal-demographics');
  });