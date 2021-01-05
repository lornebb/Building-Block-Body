$(document).ready(function(){
    $('.sidenav').sidenav({edge: "right"});
    $(".dropdown-trigger").dropdown({ hover: false });
    $('.parallax').parallax();
    $('input#username, input#password').characterCounter();
  });