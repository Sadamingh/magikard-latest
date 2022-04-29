setTimeout(myURL, 5000);

function myURL(){
   window.location.href = '/';
}

var x = setInterval(function() {
  var seconds = document.getElementById("demo").innerHTML;
  seconds--;
  document.getElementById("demo").innerHTML = seconds;
}, 1000);
