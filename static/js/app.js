// UI helpers
const totalInvoices = 12;
function showModal(id){document.getElementById(id).classList.add('active');}
function hideModal(id){document.getElementById(id).classList.remove('active');}

// Demographics
document.getElementById('demo-form').addEventListener('submit',e=>{
  e.preventDefault();
  const data={ age_range:age_range.value, gender:gender.value, education:education.value };
  fetch('/record_demographics',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)})
    .then(r=>r.json()).catch(console.error).then(()=>hideModal('demo-modal'));
});

let currentInvoice=0;
function selectInvoice(round){ currentInvoice=round;
  fetch('/select_invoice',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({round})})
    .then(r=>r.json()).catch(console.error).then(data=>{
      // render invoice
      const pane=document.getElementById('invoice-details'); pane.classList.add('active');
      pane.innerHTML = `
        <div class='budget-bar'>Budget: $${data.budget.toFixed(2)} | Points: ${data.points}</div>
        <div class='invoice-card'>
          <img src='${data.logo_url}' class='invoice-logo'/>
          <h3>${data.company}</h3>
          <p>${data.address}</p>
          <table class='invoice-details'>
            <tr><th>Invoice #</th><td>${data.invoice_id}</td></tr>
            <tr><th>Date</th><td>${data.invoice_date}</td></tr>
            <tr><th>Due</th><td>${data.due_date}</td></tr>
            <tr><th>Amount</th><td>$${data.amount_due.toFixed(2)}</td></tr>
          </table>
          <p><strong>${data.message}</strong></p>
          <div class='reading-pane-actions'>
            <button onclick="action('pay')">Pay Now</button>
            <button onclick="action('plan')">Request Plan</button>
            <button onclick="action('ask')">Ask Question</button>
            <button onclick="action('archive')">Archive</button>
          </div>
        </div>`;
  });
}

function action(type){
  if(type==='plan'){ showModal('plan-modal'); return; }
  if(type==='ask'){ showModal('question-modal'); return; }
  sendAction(type,null);
}

function sendAction(type,detail){
  fetch('/record_action',{method:'POST',headers:{'Content-Type':'application/json'},
    body:JSON.stringify({round:currentInvoice, action:type, plan:detail, question:detail})
  }).then(r=>r.json()).catch(console.error).then(data=>{
    // update budget display
    // proceed to next or block modal
    if(currentInvoice %3===0 && currentInvoice<totalInvoices) showModal('block-modal');
    else if(currentInvoice===totalInvoices) showModal('final-modal');
    else {document.getElementById(`invoice-item-${currentInvoice}`).remove();}
  });
}

// Plan modal
document.getElementById('plan-form').addEventListener('submit',e=>{
  e.preventDefault();
  const detail = installments.value + ' installments';
  hideModal('plan-modal'); sendAction('plan',detail);
});

// Question modal
document.getElementById('question-form').addEventListener('submit',e=>{
  e.preventDefault();
  const detail = question_text.value;
  hideModal('question-modal'); sendAction('ask',detail);
});

// Block survey
document.getElementById('block-submit').addEventListener('click',()=>{
  const rating=parseInt(block_rating.value);
  fetch('/record_block_survey',{method:'POST',headers:{'Content-Type':'application/json'},
    body:JSON.stringify({round:currentInvoice, rating})
  }).then(_=>{ hideModal('block-modal'); document.getElementById(`invoice-item-${currentInvoice}`).remove(); });
});

// Final survey
document.getElementById('final-submit').addEventListener('click',()=>{
  const data={ q1:parseInt(final_q1.value), q2:final_q2.value, q3:final_q3.value, comments:final_comments.value };
  fetch('/record_final_survey',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)})
    .then(_=>{ hideModal('final-modal'); document.body.innerHTML='<h2>Thank you!</h2>' });
});

function refreshInvoices(){fetch('/refresh_invoices',{method:'POST'}).then(_=>location.reload()).catch(console.error);} 