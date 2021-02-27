$(function() {
// This function gets cookie with a given name
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

/*
The functions below will create a header with csrftoken
*/

function csrfSafeMethod(method) {
// these HTTP methods do not require CSRF protection
return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
function sameOrigin(url) {
// test that a given url is a same-origin URL
// url could be relative or scheme relative or absolute
var host = document.location.host; // host + port
var protocol = document.location.protocol;
var sr_origin = '//' + host;
var origin = protocol + sr_origin;
// Allow absolute or scheme relative URLs to same origin
return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
    (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
    // or any other URL that isn't scheme relative or absolute i.e relative.
    !(/^(\/\/|http:|https:).*/.test(url));
}

$.ajaxSetup({
beforeSend: function(xhr, settings) {
    if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
        // Send the token to same-origin, relative URLs only.
        // Send the token only if the method warrants CSRF protection
        // Using the CSRFToken value acquired earlier
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
}
});
});






function placeTile(lists) {
  var board = $('.board');
  var rack1 = $('.rack1');
  var rack2 = $('.rack2');
  var others = $('.others');
  // console.log(board.position(), board.width(), board.height())
  //

  board.empty();
  rack1.empty();
  rack2.empty();
  others.empty();
  lists.forEach(list => {
  var top = list[0] + 'px'
  var left = list[1] + 'px'
  if (list[5]=='tb'){
  board.append(`<div class = 'tiles' id="${list[2]}" style='position:absolute; left:${left}; top:${top};'> <h3 style='color:${list[3]}'>${list[4]}</h3> </div>`)
} else if (list[5]=='p1'){
  rack1.append(`<div class = 'tiles players' id="${list[2]}"> <h3 style='color:${list[3]}'>${list[4]}</h3> </div>`)
}
else if (list[5]=='p2'){
  rack2.append(`<div class = 'tiles players' id="${list[2]}"> <h3 style='color:${list[3]}'>${list[4]}</h3> </div>`)
}
  else {
  others.append(`<div class = 'tiles  other' id="${list[2]}"> <h3 style='color:${list[3]}'> </h3></div>`)
  };

})

//function that sends data about draging
$('.tiles').draggable({
 stop: function(event, ui){
  var td = $(this)[0];
  var tileId = td.id;
  var stopVal = $(this).position();
  console.log(stopVal)
  $.ajax({
      url : "",
      type : "GET",
      data : { 'position' : stopVal,
                'tile' : tileId },
      success : function(json) {},
          error : function() {}
  });
},
});
};



document.addEventListener('mousemove', (event) => {
	console.log(`Mouse X: ${event.clientX}, Mouse Y: ${event.clientY}`);
});





function update(){
$.ajax({
    url : "",
    type : "GET",
    data : { },

    success : function(json) {
      placeTile(json['tiles_positions'])

},
        error : function() {}
})
}


$(document).ready(function(){
  window.setInterval(()=>{update()}, 2000)
})
