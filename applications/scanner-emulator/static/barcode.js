const app = Vue.createApp({
    delimiters: ['[[', ']]'],
    data() {
        return {
            message: 'Hello, vue'
        }
    }
})

function currentTime() {
  var date = new Date(); /* creating object of Date class */
  var hour = date.getUTCHours();
  var min = date.getUTCMinutes();
  var sec = date.getUTCSeconds();
  hour = updateTime(hour);
  min = updateTime(min);
  sec = updateTime(sec);
  document.getElementById("clock").innerText = hour + ":" + min + ":" + sec + " - UTC"; /* adding time to the div */
    var t = setTimeout(function(){ currentTime() }, 1000); /* setting timer */
}

function updateTime(k) {
  if (k < 10) {
    return "0" + k;
  }
  else {
    return k;
  }
}

currentTime(); /* calling currentTime() function to initiate the process */