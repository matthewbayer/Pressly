(function($) {
	$('#generate-btn').on('click', function(){
    	var iot = document.getElementById('txtEditor');
    
		//var pr_details = []
		//var company_descriptions = [];
		//Array.prototype.forEach.call(pr_notes, function(field) {
		//  pr_details.push(field.value);
		//});

		//Array.prototype.forEach.call(descriptions, function(field) {
		//  company_descriptions.push(field.value);
		//});

    	//var preloader = $('.spinner-wrapper');
		//preloader.fadeIn();
		$("#submit-btn-spinner").addClass("spinner-border");
		$("#submit-btn-spinner").addClass("spinner-border-sm");
		$("#generate-btn").prop("disabled",true);
		$("#sample-generate-btn").prop("disabled",true);
		$("#generate-btn-text").text("Processing...");
		
		
		var request_id = null;
		function id_callback(id){
			request_id = id;
		}
		// Send in request
		window.setTimeout(function() {		}, 	10);
			$.ajax({
				type: "POST",
				url: "/api/press-release/",
				contentType: "application/json",
				datatype: "json",
				async: false,
				success: function (data) {
					id_callback(data["id"]);
				}
			});


		console.log(request_id);

		var num_polls = 0;
		const time_to_fill_progress_bar = 50;

		poll = function() {
			$.ajax({
				type: 'GET',
				url: '/api/press-release/?id='+request_id,
				async: false,
				success: function(data) {
					if (data["status"] == "PENDING") {
						num_polls++;
						progress = Math.min(100 * num_polls / time_to_fill_progress_bar, 90);
						$("#progress-bar").css("width", progress + "%");


						setTimeout(function(){
							poll();
						}, 1000);
					}
					else if (data["status"] == "COMPLETE" || data["status"] == "ERROR") {
						var textarea = document.getElementById("txtEditor");
						if (data["status"] == "COMPLETE"){
							$("#txtEditor").val(data["generated_text"]);
						}
						else{
							$("#txtEditor").val(data["error_msg"]);
						}
						
						$("#progress-full").attr("hidden", true);
						$("#submit-btn-spinner").removeClass("spinner-border");
						$("#submit-btn-spinner").removeClass("spinner-border-sm");
						$("#sample-generate-btn").prop("disabled",false);
						$("#txtEditor").trigger("change");
						$("#generate-btn").text("Try Another Generation");
						if (parseInt(data["num_credits"]) > 0) {
							$("#credits_left").text("Uses 1 generation credit. Credits left: " + data["num_credits"]);
							$("#generate-btn").prop("disabled",false);
						}
						else{
							$("#credits_left").replaceWith('<p id="credits_left" style="color: red">Out of generation credits. Increase your plan or contact support.</p>');
							$("#generate-btn").prop("disabled",true);
						}
						//preloader.fadeOut();
					}
			  	}
			});
		  }
		poll();
  	});

	$('.custom-editor').on('change keyup paste update', function(){
		var textarea = $(this);
		textarea.height("5px");
		textarea.height(textarea.prop('scrollHeight'));
	});

    

})(jQuery);