
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

var stat = new Array();
    stat[0] = "<span style='color:rgb(155,155,155)'>Saturat</span>";
    stat[1] = "<span style='background-color:rgb(255,255,255);color:rgb(0,0,0)'>Availab</span>";
    stat[2] = "<span style='color:rgb(255,255,255)'>HighDem</span>";
    stat[3] = "<span style='text-decoration:underline;color:rgb(70,70,70)'>Unavail</span>";


function getRandomInt(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}


$( document ).ready(function() {


	$("#show_1").css({opacity: 0.0, visibility: "visible"}).animate({opacity: 1.0},100);

	
	if ($("#show_1").css('visibility') == 'visible') {
    	$("#show_2").delay( 800 ).css({opacity: 0.0, visibility: "visible"}).animate({opacity: 1.0},100);
    } 
	if ($("#show_2").css('visibility') == 'visible') {
        $("#show_3").delay( 600 ).css({opacity: 0.0, visibility: "visible"}).animate({opacity: 1.0},100);
    } 

    for(i=0; i<countries.length-1; i++){  
    		comp_num=getRandomInt(0, 4)			
  			list ="<div class='col-sm-12 row' style='visibility:hidden' id='"+countries[i]+"'><div class='col-sm-1'>"+countries[i]+"</div><div class='col-sm-1'>"+Math.round(Math.random() * 100)+"%</div><div class='col-sm-1'>"+Math.round(Math.random() * 100)+"%</div><div class='col-sm-1'>"+Math.round(Math.random() * 100)+"%</div><div class='col-sm-1'>"+Math.round(Math.random() * 100)+"%</div><div class='col-sm-1'>"+Math.round(Math.random() * 100)+"%</div><div class='col-sm-1'>"+Math.round(Math.random() * 100)+"%</div><div class='col-sm-2'>"+company[comp_num]+" "+Math.round(Math.random() * 100)+"%</div><div class='col-sm-2'>"+stat[getRandomInt(0, 3)]+"</div><div class='col-sm-1'>"+stat[getRandomInt(0, 3)]+"</div></div>";
        	$("#countries_list").append(list);
        	list = "";

        	if(i>0){
        		if ($("#"+countries[i-1]).css('visibility') == 'visible') {
        			$("#"+countries[i]).delay(600*(i+Math.random())).css({opacity: 0.0, visibility: "visible"}).animate({opacity: 1.0},100);
        		}
    		}else{
    			$("#"+countries[i]).delay(800).css({opacity: 0.0, visibility: "visible"}).animate({opacity: 1.0},100);
    		}

       }


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

    setInterval(function() {
      console.log("callPage");
      //$("#goToStart").click();
      window.location.href = "/start";
    },10000);
});

var stateCallback = function(data) {
  $('#issue-message').html('');
  if (data.overall == 'ready') {
    $('#offers').show();
    $('#issues').hide();
  } else if (data.overall == 'water') {
    window.location.replace("http://localhost:5000/water_request/");
  } else {
    $('#issues').show();
    $('#offers').hide();
    $('#issue-message').append(data.message);
  } 
};