/* Template: Tivo - SaaS App HTML Landing Page Template
   Author: Inovatik
   Created: Sep 2019
   Description: Custom JS file
*/


(function($) {
    "use strict"; 
	
	/* Preloader */
	$(window).on('load', function() {
		var preloaderFadeOutTime = 500;
		function hidePreloader() {
			var preloader = $('.spinner-wrapper');
			setTimeout(function() {
				preloader.fadeOut(preloaderFadeOutTime);
			}, 500);
		}
        hidePreloader();
       
        $.ajaxSetup({
            headers: {
                'X-CSRFTOKEN': $('meta[name="csrf-token"]').attr('content')
            }
        });
	});

	
	/* Navbar Scripts */
	// jQuery to collapse the navbar on scroll
    $(window).on('scroll load', function() {
		if ($(".navbar").offset().top > 60) {
			$(".fixed-top").addClass("top-nav-collapse");
		} else {
			$(".fixed-top").removeClass("top-nav-collapse");
		}
    });

	// jQuery for page scrolling feature - requires jQuery Easing plugin
	$(function() {
		$(document).on('click', 'a.page-scroll', function(event) {
			var $anchor = $(this);
			$('html, body').stop().animate({
				scrollTop: $($anchor.attr('href')).offset().top
			}, 600, 'easeInOutExpo');
			event.preventDefault();
		});
	});

    // closes the responsive menu on menu item click
    $(".navbar-nav li a").on("click", function(event) {
    if (!$(this).parent().hasClass('dropdown'))
        $(".navbar-collapse").collapse('hide');
    });


    /* Image Slider - Swiper */
    var imageSlider = new Swiper('.image-slider', {
        autoplay: {
            delay: 2000,
            disableOnInteraction: false
		},
        loop: true,
        spaceBetween: 30,
        slidesPerView: 5,
		breakpoints: {
            // when window is <= 580px
            580: {
                slidesPerView: 1,
                spaceBetween: 10
            },
            // when window is <= 768px
            768: {
                slidesPerView: 2,
                spaceBetween: 20
            },
            // when window is <= 992px
            992: {
                slidesPerView: 3,
                spaceBetween: 20
            },
            // when window is <= 1200px
            1200: {
                slidesPerView: 4,
                spaceBetween: 20
            },

        }
    });


    /* Text Slider - Swiper */
	var textSlider = new Swiper('.text-slider', {
        autoplay: {
            delay: 6000,
            disableOnInteraction: false
		},
        loop: true,
        navigation: {
			nextEl: '.swiper-button-next',
			prevEl: '.swiper-button-prev'
		}
    });


    /* Video Lightbox - Magnific Popup */
    $('.popup-youtube, .popup-vimeo').magnificPopup({
        disableOn: 700,
        type: 'iframe',
        mainClass: 'mfp-fade',
        removalDelay: 160,
        preloader: false,
        fixedContentPos: false,
        iframe: {
            patterns: {
                youtube: {
                    index: 'youtube.com/', 
                    id: function(url) {        
                        var m = url.match(/[\\?\\&]v=([^\\?\\&]+)/);
                        if ( !m || !m[1] ) return null;
                        return m[1];
                    },
                    src: 'https://www.youtube.com/embed/%id%?autoplay=1'
                },
                vimeo: {
                    index: 'vimeo.com/', 
                    id: function(url) {        
                        var m = url.match(/(https?:\/\/)?(www.)?(player.)?vimeo.com\/([a-z]*\/)*([0-9]{6,11})[?]?.*/);
                        if ( !m || !m[5] ) return null;
                        return m[5];
                    },
                    src: 'https://player.vimeo.com/video/%id%?autoplay=1'
                }
            }
        }
    });


    /* Details Lightbox - Magnific Popup */
	$('.popup-with-move-anim').magnificPopup({
		type: 'inline',
		fixedContentPos: false, /* keep it false to avoid html tag shift with margin-right: 17px */
		fixedBgPos: true,
		overflowY: 'auto',
		closeBtnInside: true,
		preloader: false,
		midClick: true,
		removalDelay: 300,
		mainClass: 'my-mfp-slide-bottom'
	});
    
    
    /* Move Form Fields Label When User Types */
    // for input and textarea fields
    $("input, textarea").keyup(function(){
		if ($(this).val() != '') {
			$(this).addClass('notEmpty');
		} else {
			$(this).removeClass('notEmpty');
		}
    });


    /* Sign Up Form */
    //$("#signUpForm").validator().on("submit", function(event) {
    //	if (event.isDefaultPrevented()) {
            // handle the invalid form...
    //        sformError();
    //        ssubmitMSG(false, "Please fill all fields!");
    //    }// else {
            // everything looks good!
            //event.preventDefault();
            //ssubmitForm();
        //}
    //});

    function ssubmitForm() {
        // initiate variables with form content
		var email = $("Email").val();
        var firstname = $("#First\\ name").val();
        var lastname = $("#Last\\ name").val();
        var password1 = $("#Password").val();
        var password2 = $("#Password confirmation").val();
        var terms = $("#sterms").val();
        $.ajax({
            type: "POST",
            url: "/sign-up/",
            data: {
                "email": email,
                "first_name": firstname,
                "last_name": lastname,
                "password1": password1,
                "password2": password2, 
                "terms": terms,
            },
            datatype: "json",
            success: function (data) {
                $('#header').html(data);
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
	}

    function sformSuccess() {
        $("#signUpForm")[0].reset();
        ssubmitMSG(true, "Sign Up Submitted!");
        $("input").removeClass('notEmpty'); // resets the field label after submission
    }

    function sformError() {
        $("#signUpForm").removeClass().addClass('shake animated').one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function() {
            $(this).removeClass();
        });
	}

    function ssubmitMSG(valid, msg) {
        if (valid) {
            var msgClasses = "h3 text-center tada animated";
        } else {
            var msgClasses = "h3 text-center";
        }
        $("#smsgSubmit").removeClass().addClass(msgClasses).text(msg);
    }


    /* Log In Form
    $("#logInForm").validator().on("submit", function(event) {
    	if (event.isDefaultPrevented()) {
            // handle the invalid form...
            lformError();
            lsubmitMSG(false, "Please fill all fields!");
        } else {
            // everything looks good!
            event.preventDefault();
            lsubmitForm();
        }
    });

    function lsubmitForm() {
        // initiate variables with form content
		var email = $("#lemail").val();
		var password = $("#lpassword").val();
        
        $.ajax({
            type: "POST",
            url: "php/loginform-process.php",
            data: "email=" + email + "&password=" + password, 
            success: function(text) {
                if (text == "success") {
                    lformSuccess();
                } else {
                    lformError();
                    lsubmitMSG(false, text);
                }
            }
        });
	}*/

    function lformSuccess() {
        $("#logInForm")[0].reset();
        lsubmitMSG(true, "Log In Submitted!");
        $("input").removeClass('notEmpty'); // resets the field label after submission
    }

    function lformError() {
        $("#logInForm").removeClass().addClass('shake animated').one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function() {
            $(this).removeClass();
        });
	}

    function lsubmitMSG(valid, msg) {
        if (valid) {
            var msgClasses = "h3 text-center tada animated";
        } else {
            var msgClasses = "h3 text-center";
        }
        $("#lmsgSubmit").removeClass().addClass(msgClasses).text(msg);
    }


    /* Newsletter Form 
    $("#newsletterForm").validator().on("submit", function(event) {
    	if (event.isDefaultPrevented()) {
            // handle the invalid form...
            nformError();
            nsubmitMSG(false, "Please fill all fields!");
        } else {
            // everything looks good!
            event.preventDefault();
            nsubmitForm();
        }
    });

    function nsubmitForm() {
        // initiate variables with form content
		var email = $("#nemail").val();
        var terms = $("#nterms").val();
        $.ajax({
            type: "POST",
            url: "php/newsletterform-process.php",
            data: "email=" + email + "&terms=" + terms, 
            success: function(text) {
                if (text == "success") {
                    nformSuccess();
                } else {
                    nformError();
                    nsubmitMSG(false, text);
                }
            }
        });
	}

    function nformSuccess() {
        $("#newsletterForm")[0].reset();
        nsubmitMSG(true, "Subscribed!");
        $("input").removeClass('notEmpty'); // resets the field label after submission
    }

    function nformError() {
        $("#newsletterForm").removeClass().addClass('shake animated').one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function() {
            $(this).removeClass();
        });
	}*/

    function nsubmitMSG(valid, msg) {
        if (valid) {
            var msgClasses = "h3 text-center tada animated";
        } else {
            var msgClasses = "h3 text-center";
        }
        $("#nmsgSubmit").removeClass().addClass(msgClasses).text(msg);
    }
    

    /* Privacy Form */
    $("#privacyForm").validator().on("submit", function(event) {
    	if (event.isDefaultPrevented()) {
            // handle the invalid form...
            pformError();
            psubmitMSG(false, "Please fill all fields!");
        } else {
            // everything looks good!
            event.preventDefault();
            psubmitForm();
        }
    });

    function psubmitForm() {
        // initiate variables with form content
		var name = $("#pname").val();
		var email = $("#pemail").val();
        var select = $("#pselect").val();
        var terms = $("#pterms").val();
        
        $.ajax({
            type: "POST",
            url: "php/privacyform-process.php",
            data: "name=" + name + "&email=" + email + "&select=" + select + "&terms=" + terms, 
            success: function(text) {
                if (text == "success") {
                    pformSuccess();
                } else {
                    pformError();
                    psubmitMSG(false, text);
                }
            }
        });
	}

    function pformSuccess() {
        $("#privacyForm")[0].reset();
        psubmitMSG(true, "Request Submitted!");
        $("input").removeClass('notEmpty'); // resets the field label after submission
    }

    function pformError() {
        $("#privacyForm").removeClass().addClass('shake animated').one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function() {
            $(this).removeClass();
        });
	}

    function psubmitMSG(valid, msg) {
        if (valid) {
            var msgClasses = "h3 text-center tada animated";
        } else {
            var msgClasses = "h3 text-center";
        }
        $("#pmsgSubmit").removeClass().addClass(msgClasses).text(msg);
    }
    

    /* Back To Top Button */
    // create the back to top button
    $('body').prepend('<a href="body" class="back-to-top page-scroll">Back to Top</a>');
    var amountScrolled = 700;
    $(window).scroll(function() {
        if ($(window).scrollTop() > amountScrolled) {
            $('a.back-to-top').fadeIn('500');
        } else {
            $('a.back-to-top').fadeOut('500');
        }
    });


	/* Removes Long Focus On Buttons */
	$(".button, a, button").mouseup(function() {
		$(this).blur();
    });
    

    /* Add additional text inputs for newsletter notes*/
    function getPressNoteCount() {
        return document.getElementsByClassName('form-control addl_notes').length;
    }

    var max_pr_notes = 10;
    var last_placeholder = 1;
    var template = '<div class="input-group"><input type="text" name="pr_details" class="form-control  newsletter_note addl_notes" maxlength="200"></div>';
    var minusButton = '<div class="input-group-append"><button class="btn btn-danger delete-field fixed-width addl_notes newsletter_note" id="basic-addon">-</button></div>';
    var plusButton =  '<div class="input-group-append"><button class="btn btn-success add-field fixed-width addl_notes newsletter_note" id="basic-addon">+</button></div>';
    var pressrelease_placeholders = ["Added 500 customers in the past year...", "Raised a Series C...", "Hired 30 new employees...", "Quote from CEO...", "Reached $1 million in revenue...", "Closed 3 new partnerships..."];


    $('.fields').on('click', ".add-field", function() {
        var num_notes = getPressNoteCount();
        var inputs = document.getElementsByClassName('add-field');
        var buttonToChange = inputs[inputs.length - 1];
        $(buttonToChange).replaceWith($(minusButton));

        var temp = $(template).insertBefore('#help-block');
        var input_box = temp[0].childNodes[0];
        console.log(num_notes);
        input_box.setAttribute("placeholder", pressrelease_placeholders[last_placeholder]);
        last_placeholder = (last_placeholder + 1) % pressrelease_placeholders.length;
        if (num_notes + 1 == max_pr_notes){
            temp.append(minusButton);
        }
        else{
            temp.append(plusButton);
        }
    });

    $('.fields').on('click', '.delete-field', function(){
        console.log($(this).closest('.input-group'));
        $(this).closest('.input-group').remove();
        var plusses = document.getElementsByClassName('add-field');

        /* If we've just deleted the last note possible, re-add the plus button */
        if (plusses.length == 0){
            var minuses = document.getElementsByClassName('delete-field');
            var buttonToChange = minuses[minuses.length - 1];
            $(buttonToChange).replaceWith($(plusButton));
        }

    });


    var max_company_notes = 5;
    var last_company_placeholder = 1;
    var company_template = '<div class="input-group"><input type="text" name="company_description" class="form-control newsletter_note addl_notes2" maxlength="200"></div>';
    var minusCompanyButton = '<div class="input-group-append"><button class="btn btn-danger delete-field2 fixed-width addl_notes2 newsletter_note" id="basic-addon">-</button></div>';
    var plusCompanyButton =  '<div class="input-group-append"><button class="btn btn-success add-field2 fixed-width addl_notes2 newsletter_note" id="basic-addon">+</button></div>';
    var company_placeholders = ["Acme Inc. is a multinational corporation serving...", "ABC Technologies is a Boston-based technology company...", "XYZ, LLC delivers widgets to..."];
    
    /* Add additional text inputs for newsletter notes*/
     function getCompanyNoteCount() {
        return document.getElementsByClassName('form-control addl_notes2').length;
    }

    $('.fields2').on('click', ".add-field2", function() {
        var num_notes = getCompanyNoteCount();
        var inputs = document.getElementsByClassName('add-field2');
        var buttonToChange = inputs[inputs.length - 1];
        $(buttonToChange).replaceWith($(minusCompanyButton));

        var temp = $(company_template).insertBefore('#help-block2');
        var input_box = temp[0].childNodes[0];
        console.log(num_notes);
        input_box.setAttribute("placeholder", company_placeholders[last_company_placeholder]);
        last_company_placeholder = (last_company_placeholder + 1) % company_placeholders.length;
        if (num_notes + 1 == max_company_notes){
            temp.append(minusCompanyButton);
        }
        else{
            temp.append(plusCompanyButton);
        }
    });

    $('.fields2').on('click', '.delete-field2', function(){
        console.log($(this).closest('.input-group'));
        $(this).closest('.input-group').remove();
        var plusses = document.getElementsByClassName('add-field2');

        /* If we've just deleted the last note possible, re-add the plus button */
        if (plusses.length == 0){
            var minuses = document.getElementsByClassName('delete-field2');
            var buttonToChange = minuses[minuses.length - 1];
            $(buttonToChange).replaceWith($(plusCompanyButton));
        }

    });

})(jQuery);