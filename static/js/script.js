$(document).ready(function () {
  $(".sidenav").sidenav({ edge: "right" });
  $(".dropdown-trigger").dropdown({ hover: false });
  $(".dropdown-trigger-main").dropdown();
  $(".parallax").parallax();
  $("#instruction").characterCounter();
  $("select").formSelect();
  $("#copyright").text(new Date().getFullYear());
  $("#contact-form-fail").hide();
  $("#contact-form-confirmation").hide();
});

$("#contact-form-submit").click(function () {
  if ($("#contact-message").val() == "") {
    $("#contact-form-fail").show();
  } else {
    $("#contact-form-confirmation").show();
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
      $("#contact-form-confirmation").show();
    },
    function (error) {
      alert("message not sent, please try again");
    }
  );
  return false;
}
