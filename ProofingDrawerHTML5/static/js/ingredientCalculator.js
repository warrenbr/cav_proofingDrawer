
/*
 * Custom javascript for calculating ingredient amounts based on the number of lbs of bread you want to make
 */

function calculateIngredients() {

	var breadYield = $("#breadYield").html();
	var desiredAmount = $("#lbs-input").val();
	var origVals = [];
	var counter = 0;

	$('.origVals').each(function() {
		origVals.push($(this).html());
	});

	$('.ingredientAmount').each(function() {
		
		var newAmount = (origVals[counter] * desiredAmount) / breadYield;
		counter++;
		
		$(this).html(newAmount.toFixed(3));
	});
}
