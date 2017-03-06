var countries = new Array();
    countries[0] = "Brazil";
    countries[1] = "Vietnam";
    countries[2] = "Colombi";
    countries[3] = "Indone";
    countries[4] = "Ethiop";
    countries[5] = "India";
    countries[6] = "Mexico";
    countries[7] = "Guatema";
    countries[8] = "Peru";
    countries[9] = "Hondura";
    countries[10] = "IvoryC";
    countries[11] = "CostaRi";
    countries[12] = "ElSalva";
    countries[13] = "Nicarag";
    countries[14] = "PNGuine";
    countries[15] = "Ecuador";
    countries[16] = "Thailan";
    countries[17] = "Tanzani";
    countries[18] = "DominRe";
    countries[19] = "Kenya";
    countries[20] = "Venezuela";
    /*countries[21] = "Cameroon";
    countries[22] = "Philippin";
    countries[23] = "DRepCongo";
    countries[24] = "Burundi";
    countries[25] = "Madagascar";
    countries[26] = "Haiti";
    countries[27] = "Rwanda";
    countries[28] = "Guinea";
    countries[29] = "Cuba";*/

var company = new Array();
	company[0] = "";
	company[1] = "P&G";
	company[2] = "SaraLe";
	company[3] = "Nestle";
	company[4] = "Kraft";

$( document ).ready(function() {
  $("#show_1").css({opacity: 0.0, visibility: "visible"}).animate({opacity: 1.0},100);

  if ($("#show_1").css('visibility') == 'visible') {
    $("#show_2").delay( 800 ).css({opacity: 0.0, visibility: "visible"}).animate({opacity: 1.0},100);
  } 

  if ($("#show_2").css('visibility') == 'visible') {
    $("#show_3").delay( 600 ).css({opacity: 0.0, visibility: "visible"}).animate({opacity: 1.0},100);
  } 

  $('.supply-row').each(function(i,e){ 
    if(i>0){
      $(e).delay(600*(i+Math.random())).css({opacity: 0.0, visibility: "visible"}).animate({opacity: 1.0},100);
    } else {
      $(e).delay(800).css({opacity: 0.0, visibility: "visible"}).animate({opacity: 1.0},100);
    }
  });

  setInterval(function() {
    window.location.href = "/start";
  },10000);
});

var stateCallback = function(data) {
  alert('state callback');
  $('#issue-message').html('');
  if (data.overall == 'ready') {
    $('#offers').show();
    $('#issues').hide();
  } else if (data.overall == 'water') {
    window.location.replace("http://localhost:5000/water_request/");
  } else if (data.overall == 'empty_grinds') {
    window.location.replace("http://localhost:5000/empty_grinds/");
  } else {
    $('#issues').show();
    $('#offers').hide();
    $('#issue-message').append(data.message);
  } 
};
