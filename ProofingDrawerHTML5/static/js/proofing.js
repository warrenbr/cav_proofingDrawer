/* 
 * Custom javascript for the proofing drawer user interface
 */

// the maximum and minimum tempuratures this thing will support
var rangeMax = 110; //fahrenheit, of course
var rangeMin = 70; //fahrenheit, of course

// the seconds counter for the timer (initialized at zero, seems sensible)
var seconds = 0;
// whether or not the timer is paused
var paused = true;
// whether or not the time interval is already set (otherwise the timer goes super fast!)
var intervalSet = false;

$(document).ready(function() {
	
	//make the proofing button load the proofing page
	$("#proofing-button").click(function() {
		window.location.href='ProofingPage';
		return false;
	});

	//make the recipes button load the recipes page
	$("#recipes-button").click(function() {
		window.location.href='recipes.html';
		return false;
	});

	//make the back button go back a page
	$("#backarrow").click(function() {
		window.history.back();
	});
	
	//make the temp plus button turn up the temp (as long as it is within the appropriate range)
	$("#tempPlus").click(function() {

		//Extract the current set tempurature from the document (and trim off the units)
		setTemp = $("#setTemp").html();
		setTemp = Number(setTemp.substring(0,4));
		if (setTemp < rangeMax) {
			$("#setTemp").text((setTemp + 1) + ".0°F");
		}

	});

	//make the temp minus button turn down the temp (as long as it is within the appropriate range)
	$("#tempMinus").click(function() {

		//Extract the current set tempurature from the document (and trim off the units)
		setTemp = $("#setTemp").html();
		setTemp = Number(setTemp.substring(0,4));
		if (setTemp > rangeMin) {
			$("#setTemp").text((setTemp - 1) + ".0°F");
		}
	
	});

	$("#lightbulb").click(function() {
		
		//if the light is off, turn on the light
		if ($("#lightbulb").attr("src") == "../static/img/lightbulb-gray.svg") {
			$("#lightbulb").attr("src", "../static/img/lightbulb-yellow.svg");
			paused = false;
			startTime();
			//send the ajax post request to turn the real light bulb on
			$.post("/ProofingPage/proofOn");			
		} else { //it's on, so turn it off
			$("#lightbulb").attr("src", "../static/img/lightbulb-gray.svg");
			paused = true;
			//send the ajax post request to turn the real light bulb off
			$.post("/ProofingPage/proofOff");
		}
	});
	
	function startTime() {
		if (!intervalSet) { //make sure the interval isn't already running
			setInterval(setTime, 1000);
			setInterval(updateTempHumid, 3000);
			intervalSet = true;
		}

		//runs on 1 sec interval, increments the seconds and updates the document
		function setTime() {
			if (!paused) {
				++seconds;
				$("#seconds").html(pad(seconds % 60));
				$("#minutes").html(pad(Math.floor((seconds / 60) % 60)));
				$("#hours").html(pad(Math.floor(seconds / 60 / 60)));
			}
		}

		//function that fetches the tempurature and humidity from server via ajax and updates it in the DOM
		//   (this is called in an interval that begins when the setTime interval begins)
		function updateTempHumid() {
			$.get("ProofingPage/getTemp", function(data) {
				$("#actualTemp").html(data + "°F");
			});
			$.get("ProofingPage/getHumid", function(data) {
				$("#humidity").html(data + "%");
			});
		}
		
		//pads val with a zero if it's a single digit (looks better)
		function pad(val) {
			var valString = val + "";
			if (valString.length < 2) {
				return "0" + valString;
			} else {
				return valString;
			}
		}
	} //end startTime() function

	//function to reset the timer when the reset button is clicked
	$("#timeResetButton").click(function() {
		seconds = 0;
		$("#hours").html("00");
		$("#minutes").html("00");
		$("#seconds").html("00");
	});

	
}); //end of document ready function
