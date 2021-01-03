$(document).ready(function(){
    $('.sidenav').sidenav({edge: "right"});
    $(".dropdown-trigger").dropdown();
    $('input#username, input#password').characterCounter();
  });