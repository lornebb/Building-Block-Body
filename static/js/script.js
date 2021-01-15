$(document).ready(function () {
  $(".sidenav").sidenav({ edge: "right" });
  $(".parallax").parallax();
  $("input").characterCounter();
  $("select").formSelect();
  $("#year").text(new Date().getFullYear());
  $("#contact-form-fail").hide();
  $("#contact-form-confirmation").hide();
  $("#message-sending-spinner").hide();
  $('.tooltipped').tooltip();
  $('.modal').modal();
});
