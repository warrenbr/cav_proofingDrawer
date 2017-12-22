/*
 * Custom javascript for navigation throughout the web interface (because normal navigation isn't cool enough!)
 */

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
	
}); //end of document ready function
