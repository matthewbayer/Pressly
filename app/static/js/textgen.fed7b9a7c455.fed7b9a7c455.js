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

		window.setTimeout(function() {
		console.log("test");
	}, 10000);

    	//var preloader = $('.spinner-wrapper');
		//preloader.fadeIn();
		$("#submit-btn-spinner").addClass("spinner-border");
		$("#submit-btn-spinner").addClass("spinner-border-sm");
		$("#generate-btn").prop("disabled",true);
		$("#sample-generate-btn").prop("disabled",true);
		$("#generate-btn-text").text("Processing...");
		$("#progress-bar").css("width", "0%");
		$("#progress-full").attr("hidden", false);
		
		
		var request_id = null;
		function id_callback(id){
			request_id = id;
		}
		// Send in request
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

	$('#sample-generate-btn').on('click', function(){
		//const datepicker = window.bootstrap-datepicker;
		//console.log(datepicker);
		var pr_notes = document.getElementById('notes');
		var descriptions = document.getElementById('description');
		var location = document.getElementById('location');
		var date = document.getElementById('date');

		$('#location').val("Boston, MA");
		$('#date').val("02/01/2022");
		$('#pr_title').val("Pressly Releases Press Release Writing Assistant");
		$("#description").val(`Pressly is an internet company using cutting-edge AI technology to help companies write press releases and other external communications.`);
		$("#notes").val(`Announcing the release of its flagship product, the Press Release Assistant.
The Press Release Assistant generates professional-looking press releases at the click of a button.
Creates a full industry report from a company description + a short outline.
Leverages modern neural networks for high quality text generation.
Offers a much simpler user experience than competitors, leading to increased use.
The company is continuing to grow and expand the features its product can provide.
Pressly is in its first year of operations.
The product has earned strong reviews from famous authors such as Ernest Hemingway and Mark Twain.
Sold with a tiered subscription model, billed monthly.
Pressly plans to expand into email assistants, along with investor updates.`);
	$("#description").trigger("change");
	$("#notes").trigger("change");
	//setDate(date, new Date(2022, 1, 1));


    });
    

})(jQuery);