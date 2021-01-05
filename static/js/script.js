$(document).ready(function(){
    $('.sidenav').sidenav({edge: "right"});
    $(".dropdown-trigger").dropdown({ hover: false });
    $('input#username, input#password').characterCounter();
  });