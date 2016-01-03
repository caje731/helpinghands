$(function() {
// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

// Replace the "partner" text on 2nd page with the first name
$('input.firstName').keyup("keyup", function() {
    $('.cName').html($('.firstName').val());
});

$('.help').popover();
//$('.progress-bar').css("width", "20%");

// Show the Terms and Conditions page if required
$('a.tnc_link').click(function(eventObject){
    window.open(window.location.protocol + '//' + window.location.host + '#TOU');
});

// Handle the form submit action
$('.submit').click(function() {
    event.preventDefault();
    
    // Give a modal-like feeling
    var darken = '<div class="darken" style="display:none;"></div>';
    $('body').prepend(darken);

    $(".darken").delay().show(0).animate({
      opacity: 0.8
    }, "fast");
    
    // Show the thanks button
    $('.thanks').removeClass('hide').addClass('fadeInDownBig');
    
    // Submit the form data
    $.ajax('.', {
        type : 'POST',
        headers: { 'X-CSRFToken' : csrftoken },
        data: {
          'first_name': $('.answer1')[0].innerHTML,
          'last_name': $('.answer2')[0].innerHTML,
          'email': $('.answer3')[0].innerHTML,
          'phone': $('.answer4')[0].innerHTML,
          'ref_id': $('.answer5')[0].innerHTML
      }
    });
});

var img_cnt = $('li.activate').index() + 1;
var img_amt = $('li.form-group').length;
$('.img_cnt').html(img_cnt);
$('.img_amt').html(img_amt);
var progress = ($('.img_cnt').text() / $('.img_amt').text()) * 100;
$('.progress-bar').css("width", progress + "%");
$('.form-control').keyup(function() {
    $('.nxt').removeClass("hide fadeOutDown").addClass("fadeInUp");
});

$('.nxt').click(function() {
    $('.nxt').removeClass("fadeInUp").addClass('fadeOutDown');

    if ($('.progress-form li').hasClass('activate')) {

      $('p.alerted').removeClass('fadeInLeft').addClass('fadeOutUp');

      var $activate = $('li.activate');
      var $inactive = $('li.inactive');
      $activate.removeClass("fadeInRightBig activate").addClass('fadeOutLeftBig');
      $inactive.removeClass("hide inactive").addClass("activate fadeInRightBig").next().addClass('inactive');

      var img_cnt = $('li.activate').index() + 1;

      var img_amt = $('li.form-group').length;
      $('.img_cnt').html(img_cnt);
      $('.img_amt').html(img_amt);
      var progress = ($('.img_cnt').text() / $('.img_amt').text()) * 100;
      $('.progress-bar').css("width", progress + "%");

      if ($('.img_cnt').html() == $('.img_amt').html()) {

        $('.count, .nxt').hide();
        $('.submit').removeClass("hide");

      }

    } //End Else

  });

});

$(function() {

  $('#q1fn').keyup(function() {
    var nameValue = $(this).val();
    $('.answer1').html(nameValue);
  });

  $('#q1ln').keyup(function() {
    var nameValue = $(this).val();
    $('.answer2').html(nameValue);
  });

  $('#q2e').keyup(function() {
    var nameValue = $(this).val();
    $('.answer3').html(nameValue);
  });

  $('#q2p').keyup(function() {
    var nameValue = $(this).val();
    $('.answer4').html(nameValue);
  });

  $('#q3id').keyup(function() {
    var nameValue = $(this).val();
    $('.answer5').html(nameValue);
  });

});