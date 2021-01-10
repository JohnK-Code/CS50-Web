document.addEventListener("DOMContentLoaded", function () {
  // Use buttons to toggle between views
  document
    .querySelector("#inbox")
    .addEventListener("click", () => load_mailbox("inbox"));
  document
    .querySelector("#sent")
    .addEventListener("click", () => load_mailbox("sent"));
  document
    .querySelector("#archived")
    .addEventListener("click", () => load_mailbox("archive"));
  document.querySelector("#compose").addEventListener("click", compose_email);

  // By default, load the inbox
  load_mailbox("inbox");

  // calls function to send email when form submited
  document.querySelector("#compose-form").onsubmit = () => {
    send_email();
  };
});


function compose_email() {
  // Show compose view and hide other views
  document.querySelector("#emails-view").style.display = "none";
  document.querySelector("#email-view").style.display = "none";
  document.querySelector("#compose-view").style.display = "block";
  document.querySelector('#title').innerHTML = "New Email"

  // Clear out composition fields
  document.querySelector("#compose-recipients").value = "";
  document.querySelector("#compose-subject").value = "";
  document.querySelector("#compose-body").value = "";
}


function load_mailbox(mailbox) {
  // Show the mailbox and hide other views
  document.querySelector("#emails-view").style.display = "block";
  document.querySelector("#compose-view").style.display = "none";
  document.querySelector("#email-view").style.display = "none";
  // Clear email-view div of it's contents so no open emails are repeated if reopened
  document.querySelector("#email-view").innerHTML = "";

  // Show the mailbox name
  document.querySelector("#emails-view").innerHTML = `<h3>${
    mailbox.charAt(0).toUpperCase() + mailbox.slice(1)
  }</h3>`;

  // Fetch and display each mailboxs contents - By John
  fetch(`/emails/${mailbox}`)
    .then((response) => response.json())
    .then((emails) => {
      emails.forEach((email) => {
        let new_email = document.createElement("div");
        new_email.id = `${email.id}`;
        if (email.read == true) {
          new_email.className = "new_email read";
        } else {
          new_email.className = "new_email unread";
        }
        document.querySelector("#emails-view").appendChild(new_email);

        // Used to open email when clicked in mailbox 
        new_email.addEventListener("click", function () {
          open_email(email.id);
          read_email(email.id);
        });

        let user_email = document.querySelector("#email_address").textContent;
        // Check if user sent or recived email so correct info displayed in inbox or sent mailbox
        if (user_email == email.sender) {
          let recipient = document.createElement("div");
          recipient.id = "recipient";
          recipient.innerHTML = `<strong>Recipient: </strong> ${email.recipients}`;
          new_email.appendChild(recipient);
        } else {
          let sender = document.createElement("div");
          sender.id = "sender";
          sender.innerHTML = `<strong>Sender: </strong> ${email.sender}`;
          new_email.appendChild(sender);
        }

        let subject = document.createElement("div");
        subject.id = "subject";
        subject.innerHTML = `<strong>Subject: </strong> ${email.subject}`;

        let timestamp = document.createElement("div");
        timestamp.id = "timestamp";
        timestamp.innerHTML = `<strong>Date: </strong> ${email.timestamp}`;

        new_email.appendChild(subject);
        new_email.appendChild(timestamp);
      });
    });
}


function open_email(email_id) {
  // function used to display email and all it's contents 
  // display email div and hide mailbox and compose div's
  document.querySelector("#emails-view").style.display = "none";
  document.querySelector("#compose-view").style.display = "none";
  document.querySelector("#email-view").style.display = "block";

  const email_view = document.querySelector("#email-view");

  fetch(`/emails/${email_id}`) // fetch contents of specific email to be opened and displayed on page
    .then(response => response.json())
    .then((email) => {
      let open_email = document.createElement("div");
      open_email.id = "open_email";

      let sender = document.createElement("div");
      sender.innerHTML = `<strong>Sender: </strong>${email.sender}`;
      open_email.appendChild(sender);

      let recipient = document.createElement("div");
      recipient.innerHTML = `<strong>Recipients: </strong>${email.recipients}`;
      open_email.appendChild(recipient);

      let subject = document.createElement("div");
      subject.innerHTML = `<strong>Subject: </strong>${email.subject}`;
      open_email.appendChild(subject);

      let timestamp = document.createElement("div");
      timestamp.innerHTML = `<strong>Date: </strong>${email.timestamp}`;
      open_email.appendChild(timestamp);

      let pre = document.createElement('pre');
      pre.innerHTML = email.body;
      let body = document.createElement("div");
      body.id = "email_body";
      body.appendChild(pre);
      open_email.appendChild(body);

      // buttons used to set archived to true or false
      let email_address = document.querySelector("#email_address").textContent;
      if (email.archived == true) {
        // unarchive button code
        let unarchived = document.createElement("button");
        unarchived.id = "unarchived_button";
        unarchived.className = "btn btn-sm btn-outline-primary";
        unarchived.innerHTML = "Unarchive Email";
        unarchived.addEventListener('click', function(){
          unarchive_email(email.id);
        })
        open_email.appendChild(unarchived);

        // reply button code 
        let reply = document.createElement("button");
        reply.id = "reply_button";
        reply.className = "btn btn-sm btn-outline-danger";
        reply.innerHTML = "Reply";
        reply.addEventListener('click', function(){
          reply_email(email.id);
        })
        open_email.appendChild(reply);
      } else if (email.archived == false && email_address != email.sender){
        // archive button code
        let archived = document.createElement("button");
        archived.id = "archived_button";
        archived.className = "btn btn-sm btn-outline-primary";
        archived.innerHTML = "Archive Email";
        archived.addEventListener('click', function(){
          archive_email(email.id);
        })
        open_email.appendChild(archived);

        // reply button code 
        let reply = document.createElement("button");
        reply.id = "reply_button";
        reply.className = "btn btn-sm btn-outline-danger";
        reply.innerHTML = "Reply";
        reply.addEventListener('click', function(){
          reply_email(email.id);
        })
        open_email.appendChild(reply);
      }

      email_view.appendChild(open_email);
    });
}


function read_email(email_id) {
  // function used to mark email as read
  fetch(`/emails/${email_id}`, {
    method: "PUT",
    body: JSON.stringify({
      read: true,
    }),
  });
}


function archive_email(email_id) {
  // function used to mark email as archived
  fetch(`/emails/${email_id}`, {
    method: "PUT",
    body: JSON.stringify({
      archived: true,
    }),
  });
  setTimeout(function(){load_mailbox("inbox"); }, 300) 
}


function unarchive_email(email_id) {
  // functioned used to mark email as unarchived
  fetch(`/emails/${email_id}`, {
    method: "PUT",
    body: JSON.stringify({
      archived: false,
    }),
  });
  setTimeout(function(){load_mailbox("inbox"); }, 300) 
}


function send_email() {
  // function used to post email to recipient - added by John
  const recipient = document.querySelector("#compose-recipients").value;
  const subject = document.querySelector("#compose-subject").value;
  const body = document.querySelector("#compose-body").value;

  event.preventDefault();
  fetch("/emails", {
    method: "POST",
    body: JSON.stringify({
      recipients: recipient,
      subject: subject,
      body: body,
    }),
  }).then((response) =>
    console.log(`Email 'SEND' request - ${response.status}`)
  );
  setTimeout(function(){load_mailbox("sent"); }, 300) 
}


function reply_email(email_id) {
  // function used to view email reply form 
  // Show compose view and hide other views
  document.querySelector("#emails-view").style.display = "none";
  document.querySelector("#email-view").style.display = "none";
  document.querySelector("#compose-view").style.display = "block";
  document.querySelector('#title').innerHTML = "Reply"

  // fetch contents of email so it can be added to the form for replying
  fetch(`/emails/${email_id}`)
  .then(response => response.json())
  .then(email => {
    document.querySelector("#compose-recipients").value = `${email.sender}`;
    // check if email subject already contains reply text
    if(email.subject.substring(0,3) == "Re:"){
      document.querySelector("#compose-subject").value = `${email.subject}`; 
    }else{
      document.querySelector("#compose-subject").value = `Re: ${email.subject}`;
    }
    document.querySelector("#compose-body").value = `

----------------------------------------------
On ${email.timestamp} ${email.sender} wrote: 
${email.body}`;
  })
}