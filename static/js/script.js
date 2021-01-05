$(document).ready(function(){
    $('.sidenav').sidenav({edge: "right"});
    $(".dropdown-trigger").dropdown({ hover: false });
    $('.dropdown-trigger-main').dropdown();
    $('.parallax').parallax();
    $('input#username, input#password').characterCounter();
    $("#copyright").text(new Date().getFullYear());
  });