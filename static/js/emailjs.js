// Contact form on click to fire sendmail()
$("#contact-form-submit").click(function () {
    if ($("#user").val() == $("#validation").val()) {
      $("#contact-form-submit").hide();
      $("#message-sending-spinner").show();
      if ($("#contact-message").val() == "") {
        $("#message-sending-spinner").hide();
        alert("Message is empty. Please write something.");
      } else {
        sendMail();
        return false;
      }
    } else {
      alert("Validation was incorrect")
      return false
    }});
  
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
  };