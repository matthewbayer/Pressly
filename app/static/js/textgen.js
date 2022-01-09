(function($) {
  $('#generate-btn').on('click', function(){
    var pr_notes = document.getElementsByClassName('form-control addl_notes');
    var descriptions = document.getElementsByClassName('form-control addl_notes2');
    
    var pr_details = []
    var company_descriptions = [];
    Array.prototype.forEach.call(pr_notes, function(field) {
      pr_details.push(field.value);
    });

    Array.prototype.forEach.call(descriptions, function(field) {
      company_descriptions.push(field.value);
    });
    data_to_send = {
        "company_descriptions": company_descriptions,
        "pr_details": pr_details,
    }
    $.ajax({
      type: "POST",
      url: "/app/",
      data: JSON.stringify(data_to_send),
      datatype: "json",
      success: function (data) {
          //$("#txtEditor").Editor("setText", data["generated_text"]);
          var textarea = document.getElementById("txtEditor");
          console.log(textarea);
          $("#txtEditor").val(data["generated_text"]);
          //textarea.val(data["generated_text"]);
          textarea.style.height = (textarea.scrollHeight)+"px";
          //auto_grow(("#txtEditor"));
          $("#credits_left").text("Uses 1 generation credit. Credits left: " + data["num_credits"]);
      }
      //success: function(data) {
      //    if (data.result == "success") {
      //        sformSuccess();
      //    } else {
      //        sformError();
      //        ssubmitMSG(false, data.result);
      //   }
      //}
    });
    
  });

  $('#txtEditor').on('input', function(){
    var textarea = document.getElementById("txtEditor");
    textarea.style.height = "5px";
    textarea.style.height = (textarea.scrollHeight)+"px";
  });

})(jQuery);