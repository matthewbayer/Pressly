(function($) {
  $('#generate-btn').on('click', function(){
    var pr_notes = document.getElementById('notes');
    var title = document.getElementById('pr_title');
    var descriptions = document.getElementById('description');
    var location = document.getElementById('location');
    var date = document.getElementById('date');
    
    //var pr_details = []
    //var company_descriptions = [];
    //Array.prototype.forEach.call(pr_notes, function(field) {
    //  pr_details.push(field.value);
    //});

    //Array.prototype.forEach.call(descriptions, function(field) {
    //  company_descriptions.push(field.value);
    //});
    data_to_send = {
        "title": title.value,
        "company_descriptions": descriptions.value,
        "pr_details": pr_notes.value,
        "location": location.value,
        "date": date.value
    }

    var preloader = $('.spinner-wrapper');
    preloader.fadeIn();

    $.ajax({
      type: "POST",
      url: "/app/press-release/",
      data: JSON.stringify(data_to_send),
      datatype: "json",
      success: function (data) {
          preloader.fadeOut();
          var textarea = document.getElementById("txtEditor");

          $("#txtEditor").val(data["generated_text"]);
          $("#txtEditor").trigger("change");
          $("#generate-btn").text("Try Another Generation");
          if (parseInt(data["num_credits"]) > 0) {
            $("#credits_left").text("Uses 1 generation credit. Credits left: " + data["num_credits"]);
          }
          else{
            $("#credits_left").replaceWith('<p id="credits_left" style="color: red">Out of generation credits. Increase your plan or contact support.</p>');
            $("#generate-btn").prop("disabled",true);;
          }

          
      }
    });
    
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

    $('#location').val("Boston");
    $('#date').val("01/01/2022");
    $('#pr_title').val("Pressly Releases Press Release Writing Assistant");
    $("#description").val(`- Pressly is an internet company using cutting-edge AI technology to help companies write press releases and other external communications.`);
    $("#notes").val(`- Announcing the release of its flagship product, the Press Release Assistant
- The Press Release Assistant generates professional-looking press releases at the click of a button
- Creates a full industry report from a company description + a short outline
- Leverages modern neural networks for high quality text generation
- Offers a much simpler user experience than competitors, leading to increased use
- The company is continuing to grow and expand the features its product can provide
- Pressly is in its first year of operations
- The product has earned strong reviews from famous authors such as Ernest Hemingway and Mark Twain
- Sold with a tiered subscription model, billed monthly
- Pressly plans to expand into email assistants, along with investor updates`);
    $("#description").trigger("change");
    $("#notes").trigger("change");
    //setDate(date, new Date(2022, 1, 1));


    });
    

})(jQuery);