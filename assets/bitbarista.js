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
  } else {
    $('#issues').show();
    $('#offers').hide();
    $('#issue-message').append(data.message);
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
