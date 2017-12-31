/*
 * Custom javascript for removing recipes from the recipes page
 */

$(document).ready(function() {

	var breadNumber = -1;
	
	$("[id^=ask-delete-bread-]").click(function() {
		breadNumber = $(this).val();

		//testing thing -- remove later
		console.log("remove clicked for bread: " + breadNumber);
		
		$("#myModal").modal('show');
	});

	$("#delete-bread").click(function() {
		if (breadNumber > 0) {

			//testing thing -- remove later
			console.log("trying to delete bread: " + breadNumber);

			// $.post("/ProofingPage/remove/"+breadNumber, function(data) {
			// 	console.log("POST returned data: " + data);
			// });
			
			// commented out because we are changing to POST request -- delete if that works later.
			$.ajax({
				url: '/RecipesPage/remove/'+breadNumber,
				type: 'POST',
				success: function(result) {
					// Do nothing with the result, lol

					//testing thing -- remove later
					// console.log("Result from POST: " + result);
					location.reload();
				}
			});

			//testing thing -- remove later
			console.log("POST sent to: " + '/RecipesPage/remove/'+breadNumber);
			
			breadNumber = -1;
		}
	});
		
}); //end of document ready function
