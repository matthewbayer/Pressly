(function($) {
	$('#generate-btn').on('click', function(){
    	var status = document.getElementById('notes');
		data_to_send = {
			"status": status.value
		}

    	//var preloader = $('.spinner-wrapper');
		//preloader.fadeIn();
		$("#submit-btn-spinner").addClass("spinner-border");
		$("#submit-btn-spinner").addClass("spinner-border-sm");
		$("#generate-btn").prop("disabled",true);
		$("#sample-generate-btn").prop("disabled",true);
        $("#generate-btn-text").text("Uploading...");
		console.log("begin");
		// Send in request
		
        window.setTimeout(function() {
            $.ajax({
                type: "POST",
                url: "/api/submit_data/",
                contentType: "application/json",
                data: JSON.stringify(data_to_send),
                datatype: "json",
                async: false,
                success: function(data) {
                    console.log("complete");
                    $("#submit-btn-spinner").removeClass("spinner-border");
                    $("#submit-btn-spinner").removeClass("spinner-border-sm");
                    $("#generate-btn-text").text("Submit Data");
                    $("#generate-btn").prop("disabled",false);
                    $("#sample-generate-btn").prop("disabled",false);
                }
            });
        }, 	10);
        
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

		$('#pr_title').val("Pressly Releases Press Release Writing Assistant");
		$("#notes").val(`Eating hay, drinking water.`);
	    $("#notes").trigger("change");
	//setDate(date, new Date(2022, 1, 1));


    });
    

})(jQuery);