// frontend/app.js
const API = "http://localhost:8000";

async function syncEmails() {
  const res = await fetch(`${API}/sync_emails`, { method: 'POST' });
  const data = await res.json();
  alert(`Synced ${data.synced} emails`);
  loadEmails();
}

async function loadEmails() {
  const res = await fetch(`${API}/emails`);
  const emails = await res.json();
  const container = document.getElementById("emails");
  container.innerHTML = "";
  emails.forEach(e=>{
    const el = document.createElement("div");
    el.className = "email";
    el.innerHTML = `
      <strong>${e.subject}</strong> <small>from: ${e.sender}</small><br/>
      <em>class: ${e.classification}</em>
      <p>${e.snippet || ''}</p>
      <div id="draft-${e.message_id}">
        ${e.draft ? `<pre>${e.draft}</pre><button onclick="sendDraft('${e.message_id}')">Send</button>` : `<button onclick="generateDraft('${e.message_id}')">Generate Draft</button>`}
      </div>
    `;
    container.appendChild(el);
  });
}

async function generateDraft(message_id) {
  const tone = "professional";
  const res = await fetch(`${API}/draft`, {
    method: 'POST',
    headers: {'Content-Type':'application/json'},
    body: JSON.stringify({message_id, tone, extra_instructions: ""})
  });
  const data = await res.json();
  document.getElementById(`draft-${message_id}`).innerHTML = `<pre>${data.draft}</pre><button onclick="sendDraft('${message_id}')">Send</button>`;
}

async function sendDraft(message_id) {
  const draftText = document.querySelector(`#draft-${message_id} pre`).innerText;
  const res = await fetch(`${API}/send`, {
    method: 'POST',
    headers: {'Content-Type':'application/json'},
    body: JSON.stringify({message_id, draft_text: draftText})
  });
  const j = await res.json();
  alert('Sent (simulated) ' + message_id);
  loadEmails();
}

document.getElementById("syncBtn").addEventListener("click", syncEmails);
window.onload = loadEmails;
