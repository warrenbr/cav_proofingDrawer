/*
 * Custom JS to make the New Recipe form dynamically add or remove ingredients and notes.
 */ 

$(document).ready(function() {

	//variable to hold the number of ingredient fields in the form (starts at 4 because there are 4 in the form)
	var ingredientCounter = 4;
	//variable to hold the number of note fields in the form (starts at 2 because there are 2 in the form)
	var noteCounter = 2;

	//This adds another ingredient field to the form when the "Add Another Ingredient" button is clicked
	$("#addIngredient").click(function () {
		ingredientCounter++;
		$("#ingredients-holder").append(
			'<div class="row spaced-row" id="ingredient-'+ ingredientCounter +'">' +
				'<div class="col-sm-8">' +
				'<h3><b>INGREDIENT</b></h3>' +
				'<input name="ingredientName-'+ ingredientCounter +'" class="form-control ingredientName" type="text">' +
				'</div>' +
				'<div class="col-sm-4">' +
				'<div class="row">' + 
				'<h3><b>AMOUNT (lbs.)</b></h3>' +
				'<span class="stupid-damn-form-span">' +
				'<input name="ingredientAmount-'+ ingredientCounter +'" class="form-control ingredientAmount" type="number" min="0" step="any" value="0.25">' +
				'</span>' +
				'</div>' +
				'</div>' +
				'</div>'
		);
	});

	//This adds another note field to the form when the "Add Another Note" button is clicked
	$("#addNote").click(function () {
		noteCounter++;
		$("#noteHolder").append(
				'<div class="row spaced-row" id=noteRow-'+ noteCounter +'>' +
				'<textarea name="note-'+ noteCounter +'" class="form-control" rows="2"></textarea>' +
				'</div>'
		);
	});
	
	//This removes the bottom ingredient when one of the "X" buttons is clicked. It removes the bottom ingredient for
	//    any of the X buttons so that the numbers in the field ID's stay correct.
	$("#removeIngredient").click(function () {
		$("#ingredient-"+ingredientCounter).remove();
		if (ingredientCounter > 0) {
			ingredientCounter--;
		}
	});

	//This removes the bottom note when the "remove note" button is clicked. It removes the bottom note and decrements
	//    the counter so that the numbered labels are always accurate.
	$("#removeNote").click(function() {
		$("#noteRow-"+noteCounter).remove();
		if (noteCounter > 0) {
			noteCounter--;
		}
	});
	
});
