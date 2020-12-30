if (!localStorage.getItem("counter")) { // checks if counter is not in local storage and creates it if it's not there
  localStorage.setItem("counter", 0);
}

function count() { // count function increments counter variable by one when run and displays the value in the h1 element
  let counter = localStorage.getItem("counter"); // sets counter variable to local counter value
  counter++; // increments counter variable 
  document.querySelector("h1").innerHTML = counter; // displays counter value in h1 element
  localStorage.setItem("counter", counter); // updates local counter value with value from counter variable

  if (counter % 10 === 0) { // displays an alert every time the counter varible is a multiple of 10
    alert(`Count is now ${counter}`);
  }
}

document.addEventListener("DOMContentLoaded", function () { // runs code in function once DOM loaded
  document.querySelector('h1').innerHTML = localStorage.getItem('counter'); // set h1 elements value to local storages counter value
  document.querySelector("button").onclick = count; // runs count function when button element clicked

  // setInterval(count, 1000); // run count function every 1000 milliseconds - 1 second
});
