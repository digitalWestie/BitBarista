
var countries = new Array();
    countries[0] = "Brazil";
    countries[1] = "Vietnam";
    countries[2] = "Colombia";
    countries[3] = "Indonesia";
    countries[4] = "Ethiopia";
    countries[5] = "India";
    countries[6] = "Mexico";
    countries[7] = "Guatemala";
    countries[8] = "Peru";
    countries[9] = "Honduras";
    countries[10] = "IvoryCoast";
    countries[11] = "CostaRica";
    countries[12] = "ElSalvador";
    countries[13] = "Nicaragua";
    countries[14] = "PNGuinea";
    countries[15] = "Ecuador";

var company = new Array();
	company[0] = "";
	company[1] = "P&G";
	company[2] = "SaraLee";
	company[3] = "Nestle";
	company[4] = "Kraft";

var stat = new Array();
    stat[0] = "<span style='color:rgb(0,255,0)'>Sat</span>";
    stat[1] = "<span style='background-color:rgb(0,255,0);color:rgb(0,0,0)'>Avail</span>";
    stat[2] = "<span style='color:rgb(0,255,0)'>HiDem</span>";
    stat[3] = "<span style='text-decoration:underline;color:rgb(70,70,70)'>Unavail</span>";


function showDiv() {
   // If there are hidden divs left
    if($('div:hidden').length) {
        // Fade the first of them in
        $('div:hidden:first').fadeIn();
        // And wait one second before fading in the next one
        setTimeout(showDiv, 1000);
    }
}


function getRandomInt(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}


$( document ).ready(function() {

	/*$("#show").each(function() {
		var elem = $(this);
		if (elem.css('visibility') == 'hidden') {
            	//elem.css('visibility', 'visible');
        	} 
	});*/   
    

	$("#show_1").css({opacity: 0.0, visibility: "visible"}).animate({opacity: 1.0},100);

	
	if ($("#show_1").css('visibility') == 'visible') {
    	$("#show_2").delay( 800 ).css({opacity: 0.0, visibility: "visible"}).animate({opacity: 1.0},100);
    } 
	if ($("#show_2").css('visibility') == 'visible') {
        $("#show_3").delay( 600 ).css({opacity: 0.0, visibility: "visible"}).animate({opacity: 1.0},100);
    } 

	
    //console.log( $("#country").html() );

    for(i=0; i<countries.length-1; i++){  
    		comp_num=getRandomInt(0, 4)			
  			list ="<div class='col-sm-12 row' style='visibility:hidden' id='"+countries[i]+"'><div class='col-sm-1'>"+countries[i]+"</div><div class='col-sm-1'>"+Math.round(Math.random() * 100)+"%</div><div class='col-sm-1'>"+Math.round(Math.random() * 100)+"%</div><div class='col-sm-1'>"+Math.round(Math.random() * 100)+"%</div><div class='col-sm-1'>"+Math.round(Math.random() * 100)+"%</div><div class='col-sm-1'>"+Math.round(Math.random() * 100)+"%</div><div class='col-sm-1'>"+Math.round(Math.random() * 100)+"%</div><div class='col-sm-2'>"+company[comp_num]+" "+Math.round(Math.random() * 100)+"%</div><div class='col-sm-1'>"+stat[getRandomInt(0, 3)]+"</div><div class='col-sm-1'>"+stat[getRandomInt(0, 3)]+"</div></div>";
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


     setInterval(function() {
     	$("#goToStart").click();
     },10000);

   	function fadeSwitchElements(id1, id2)
	{
    	var element1 = $('#' + id1);
 	    var element2 = $('#' + id2);

    	if(element1.is(':visible'))
    	{
        	element1.fadeToggle(500);
        	element2.fadeToggle(500);
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

	//console.log ($('#status').css('background-color'));

	/*$('#status').each(function() {
  	  var elem = $(this);
    	setInterval(function() {
        	if (elem.css('background-color') == 'rgb(0, 255, 0)') {
            	elem.css('background-color', 'rgb(255, 0, 0)');
        	} else if (elem.css('background-color') == 'rgb(255, 0, 0)') {
            		elem.css('background-color', 'rgb(255, 255, 0)');
        	} else {
            		elem.css('background-color', 'rgb(0, 255, 0)');
        	}
        	    
    	}, 200);
	});*/
	
});

