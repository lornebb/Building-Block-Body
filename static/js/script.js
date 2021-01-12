$(document).ready(function () {
  $(".sidenav").sidenav({ edge: "right" });
  $(".parallax").parallax();
  $("#instruction").characterCounter();
  $("select").formSelect();
  $("#copyright").text(new Date().getFullYear());
  $("#contact-form-fail").hide();
  $("#contact-form-confirmation").hide();
  $("#message-sending-spinner").hide();
  $('.tooltipped').tooltip();
});

$("#contact-form-submit").click(function () {
  $("#contact-form-submit").hide();
  $("#message-sending-spinner").show();
  if ($("#contact-message").val() == "") {
    $("#message-sending-spinner").hide();
    alert("Message is empty. Please write something.");
  } else {
    sendMail();
    return false;
  }
});

/**
 * emailJS API - when submit on contact form is sent,
 * EmailJS API is used to send the email to the developer directly
 * */
function sendMail() {
  emailjs.init("user_NLgvc4Mu5hpwy6V4uUBBn");
  const templateParams = {
    user: $("#user").val(),
    message: $("#contact-message").val(),
  };
  emailjs.send("lorneashley_gmail_com", "work_it_out", templateParams).then(
    function (response) {
      $("#message-sending-spinner").hide();
      $("#contact-form-confirmation").show();
      alert("message sent")
      // $("#contact-form-confirmation").show();
    },
    function (error) {
      alert("message not sent, please try again");
    }
  );
  return false;
}
