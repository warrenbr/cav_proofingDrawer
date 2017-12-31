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
			$.ajax({
				url: '/RecipesPage/remove/'+breadNumber,
				type: 'POST',
				success: function(result) {
					// Do nothing with the result, just reload the page
					//location.reload();
					window.location.replace("/RecipesPage");
				}
			});
			breadNumber = -1;
		}
	});
		
}); //end of document ready function
