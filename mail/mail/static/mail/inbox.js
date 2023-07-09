document.addEventListener('DOMContentLoaded', function() {
  /*window.onpopstate = (event) => {
    if ('compose' in event.state)
      compose_email();
    else if ('mailbox' in event.state)
      load_mailbox(event.state.mailbox);
    else if ('email' in event.state)
      load_email(event.state.email);
  }*/

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').onclick = () => load_mailbox('sent');
  document.querySelector('#archived').onclick = () => load_mailbox('archive');
  document.querySelector('#compose').onclick = () => compose_email();

  // Compose form submission
  document.querySelector('#compose-form').onsubmit = () => send_email();

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {
  // Add history
  //history.pushState({compose: true}, "", "compose");

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#big-email-view').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox, message) {
  // Add history
  //history.pushState({mailbox: mailbox}, "", mailbox);

  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#big-email-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `
    <h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>
    <h5 id='emails-message'></h5>
    `;

  // If there's a message, show it
  if (message) {
    document.querySelector('#emails-message').innerHTML = message;
  }

  fetch(`/emails/${mailbox}`)
  .then(request => request.json())
  .then(emails => {
    for (email of emails) {
      render_email(email);
    }
  });
}

// Renders a single small email box for the emails-view
function render_email(email) {
  const email_box = document.createElement('div');
  email_box.className = "row col-12 border border-2 border-dark pt-2 pb-2 px-1 pointer";
  email_box.innerHTML = `
    <div class="col-auto"><strong>${email.sender}</strong></div>
    <div class="col-auto">${email.subject}</div>
    <div class="col-auto ml-auto text-muted">${email.timestamp}</div>
    `;
  // Turn read emails grey
  if (email.read) {
    email_box.style.backgroundColor = 'whitesmoke';
  }
  email_box.onclick = () => load_email(email.id);
  document.querySelector('#emails-view').append(email_box);
}

// Loads the big email view, this is the onclick property for the small email boxes
function load_email(email_id) {
  //history.pushState({email: email_id}, "", `email=${email_id}`);

  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#big-email-view').innerHTML = '';
  document.querySelector('#big-email-view').style.display = 'block';

  fetch(`/emails/${email_id}`, {
    method: 'PUT',
    body: JSON.stringify({
      read: true
    })
  })

  fetch(`/emails/${email_id}`)
  .then(response => response.json())
  .then(email => {
    const big_email_box = document.createElement('div');
    big_email_box.className="container border border-2 border-dark bg-light p-2"
    big_email_box.innerHTML=`
      <div class='row mb-2'>
        <div class='col-auto lead'>${email.subject}</div>
      </div>
      <div class='row'>
        <div class='col-auto text-strong'>Sender: ${email.sender}</div>
        <div class='col-auto ml-auto text-muted'>${email.timestamp}</div>
      </div>
      <div class='m-3'>${email.body}</div>
      <div class='row'>
        <div class='col-auto ml-auto'>Sent to: ${`${email.recipients}`.replace(',', ', ')}</div>
      </div>
      `;
    
    const buttons_div = document.createElement('div');
    buttons_div.className = 'row mt-3';
    buttons_div.id = 'big-email-buttons';
      
    const archive_button = document.createElement('button');
    archive_button.className = (email.archived) ? 'btn btn-danger col-auto ml-auto mr-2' : 'btn btn-primary col-auto ml-auto mr-2';
    archive_button.id = 'email-button-archive';
    archive_button.innerHTML = (email.archived) ? 'Unarchive' : 'Archive';
    archive_button.onclick = () => {
      fetch(`emails/${email_id}`, {
        method: 'PUT',
        body: JSON.stringify({
          archived: (!email.archived)
        })
      })
      .then(response => load_mailbox('inbox'));
    }
  
    const reply_button = document.createElement('button');
    reply_button.className = "btn btn-primary col-auto"
    reply_button.id = 'email-button-reply';
    reply_button.innerHTML = 'Reply';
    reply_button.onclick = () => {
      compose_email();
      document.querySelector('#compose-recipients').value = email.sender;
      if (email.body) {
        document.querySelector('#compose-body').value = `On ${email.timestamp} ${email.sender} wrote: ${email.body}`;
      }
      const reply_expression = /^Re:.+/;
      if (!email.subject.match(reply_expression)) {
        document.querySelector('#compose-subject').value = 'Re: ' + email.subject;
      } else {
        document.querySelector('#compose-subject').value = email.subject;
      }

    }

    buttons_div.append(archive_button, reply_button);

    document.querySelector('#big-email-view').append(big_email_box, buttons_div);
  })
}

// This is the onsubmit function for the email compose form
function send_email() {
  // Submit POST request to send email
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
      recipients: `${document.querySelector('#compose-recipients').value}`,
      subject: `${document.querySelector('#compose-subject').value}`,
      body: `${document.querySelector('#compose-body').value}`
    })
  })
  .then(response => response.json())
  .then(result => {
    console.log(result)
    if ('error' in result) {
      document.querySelector('#compose-error').innerHTML = "Error: " + result['error'];
    }
    else {
      // Go to sent mailbox with a success message
      load_mailbox('sent', result.message);
    }
  })

  // Don't redirect after submitting form
  return false;
}