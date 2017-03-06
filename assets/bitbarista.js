function getRandomInt(min, max) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

var stateCallback = function(data) {
  $('#issue-message').html('');
  if (data.overall == 'ready') {
    $('#offers').show();
    $('#issues').hide();
  } else if (data.overall == 'water') {
    window.location.replace("http://localhost:5000/water_request/");
  } else if (data.overall == 'empty_grinds') {
    window.location.replace("http://localhost:5000/empty_grinds/");
  } else if (data.overall == 'off') {
    window.location.replace("http://localhost:5000/standby/");
  } else if (data.overall == 'warmup') {
    window.location.replace("http://localhost:5000/warmup/");
  } else if (data.overall == 'disconnected') {
    window.location.replace("http://localhost:5000/disconnected/");
  } else {
    window.location.replace("http://localhost:5000/error/");
  }
};

$(document).ready(function(){

  $('.blink').each(function() {
    var elem = $(this);
    setInterval(function() {
      if (elem.css('visibility') == 'hidden') {
        elem.css('visibility', 'visible');
      } else {
         elem.css('visibility', 'hidden');
      }
    }, 100);
  });

});

var logAction = function(description){
  //Logging to http://datadrop.wolframcloud.com/
  //NB databins only last 30 days
  $.ajax({ 
    url: 'https://datadrop.wolframcloud.com/api/v1.0/Add?bin=jxFDUPr6',
    method: "POST",
    data: {
      timestamp: (new Date).toString(), 
      location: window.location.toString(),
      description: description
    },
    dataType: "json",
    success: function(data){ console.log(data) }
  });
};