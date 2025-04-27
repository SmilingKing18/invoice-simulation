// Modal controls
function showModal(id){ document.getElementById(id).classList.add('active'); }
function hideModal(id){ document.getElementById(id).classList.remove('active'); }

// Initialize demographics modal
document.getElementById('demo-form').addEventListener('submit', e => {
  e.preventDefault();
  const data = { age_range: age_range.value, gender: gender.value, education: education.value };
  fetch('/record_demographics',{ method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(data) })
    .then(r=>r.json()).catch(console.error).then(()=> hideModal('demo-modal'));
});

let currentInvoice;
function selectInvoice(round){ currentInvoice=round;
  fetch('/select_invoice',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({round})})
    .then(r=>r.json()).catch(console.error).then(data=>{
      document.getElementById('invoice-title').innerText=`Invoice ${data.round}: ${data.name}`;
      document.getElementById('invoice-message').innerText=data.message;
      document.getElementById('invoice-details').classList.add('active');
  });
}

function recordResponse(choice){
  fetch('/record_response',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({round:currentInvoice,response:choice})})
    .then(r=>r.json()).catch(console.error).then(()=>{
      document.querySelectorAll('.scale-group .scale').forEach(container=>{
        container.innerHTML='';
        for(let i=1;i<=5;i++){
          const star=document.createElement('i'); star.className='fa fa-circle'; star.dataset.value=i;
          star.addEventListener('click',()=>{ container.querySelectorAll('i').forEach(s=>s.classList.remove('selected')); star.classList.add('selected'); checkScales(); });
          container.appendChild(star);
        }
      });
      document.getElementById('submit-scales').disabled=true;
      showModal('rating-modal');
  });
}

function checkScales(){
  const ok=[...document.querySelectorAll('.scale-group')].every(g=>g.querySelector('.selected'));
  document.getElementById('submit-scales').disabled=!ok;
}

document.getElementById('submit-scales').addEventListener('click',()=>{
  const payload={round:currentInvoice};
  document.querySelectorAll('.scale-group').forEach(g=>{
    const key=g.dataset.question;
    payload[key]=parseInt(g.querySelector('.selected').dataset.value);
  });
  fetch('/record_scales',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)})
    .then(r=>r.json()).catch(console.error).then(()=>{
      hideModal('rating-modal');
      document.getElementById(`invoice-item-${currentInvoice}`).remove();
      document.getElementById('invoice-details').classList.remove('active');
  });
});

function refreshInvoices(){
  fetch('/refresh_invoices',{method:'POST'}).then(_=>location.reload()).catch(console.error);
}