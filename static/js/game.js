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


function offset(el) {
    var rect = el.getBoundingClientRect(),
    scrollLeft = window.pageXOffset || document.documentElement.scrollLeft,
    scrollTop = window.pageYOffset || document.documentElement.scrollTop;
    return { top: rect.top + scrollTop, left: rect.left + scrollLeft }
}





function placeTile(lists, currentPlayer) {
  var board = $('.board');
  var rack1 = $('.rack1');
  var rack2 = $('.rack2');
  var others = $('.others');

  board.empty();
  rack1.empty();
  rack2.empty();
  others.empty();
  var p1List = [];
  var p2List = [];
  var x = 0
  lists.forEach(list => {
  var top = parseFloat(list[0]).toFixed(2).toString() + 'px'
  var left = parseFloat(list[1]).toFixed(2).toString() + 'px';
  if (list[5]=='tb'){
  board.append(`<div class = 'tiles' id="${list[2]}" style='position:absolute; left:${left}; top:${top};'> <h3 style='color:${list[3]}'>${list[4]}</h3> </div>`)
} else if (list[5]=='p1'){
  rack1.append(`<div class = 'tiles players' id="${list[2]}"> <h3 style='color:${list[3]}'>${list[4]}</h3> </div>`)
  p1List.push(list[2])
}
else if (list[5]=='p2'){
  rack2.append(`<div class = 'tiles players' id="${list[2]}"> <h3 style='color:${list[3]}'>${list[4]}</h3> </div>`)
  p2List.push(list[2])
}
  else if (x < 20) {
  others.append(`<div class = 'tiles  other' id="${list[2]}"> <h3 style='color:${list[3]}'> </h3></div>`);
  x +=1
  };

})

var turn = $('#playerTurn')
turn.text(currentPlayer)

var boardOffset = offset(board[0]);
if(rack1.length != 0){
  var rack1Offset = offset(rack1[0]);
} else{
  var rack1Offset = offset(rack2[0]);
}

var boardLeft= boardOffset.left
var boardTop= boardOffset.top
var rack1Left= rack1Offset.left
var rack1Top= rack1Offset.top

//function that sends data about draging
$('.tiles').draggable({
  start: function(event){
    let td = $(this)[0];
    let tileId = td.id;
    let startVal = $(this).position();
    let left = startVal['left']
    let top = startVal['top']
    left = Math.round(left)
    top = Math.round(top)
    left = left.toFixed(1)
    top = top.toFixed(1)

    $.ajax({
        url : "",
        type : "GET",
        data : { 'lewa' : left, 'gora':top,
                  'tid' : tileId},
        success : function(json) {

        },
            error : function() {}
    });
  }
},{
 stop: function(event, ui){
  let td = $(this)[0];
  let tileId = td.id;
  let stopVal = $(this).position();
  if (p1List.includes(tileId) || p2List.includes(tileId)) {
    if (stopVal['top']>-100 && p1List.includes(tileId)){
    stopVal['top']=2
    stopVal['left']=2
  } else if  (stopVal['top']>-100 && p2List.includes(tileId)) {
    stopVal['top'] =3
    stopVal['left']=3
} else {
  stopVal['top'] = Math.round((stopVal['top']+rack1Top-boardTop+boardLeft-5))
  stopVal['left'] = Math.round((stopVal['left']+rack1Left-boardLeft+boardTop/2-5))
}
}

let left = stopVal['left']
let top = stopVal['top']
left = Math.round(left)
top = Math.round(top)
left = left.toFixed(1)
top = top.toFixed(1)
  $.ajax({
      url : "",
      type : "GET",
      data : { 'left' : left, 'to':top,
                't' : tileId},
      success : function(json) {
        update()
      },
          error : function() {}
  });

},
});
};

$('#changePlayer').click(()=>{
$.ajax({
    url : "",
    type : "GET",
    data : { 'p' : '1'},
    success : function(json) {
      setTimeout(update(), 1000)
    },
        error : function() {}
});
})

$('#undo').click(()=>{
$.ajax({
    url : "",
    type : "GET",
    data : {'undo':true},
    success : function(json) {
      setTimeout(update(), 500)
    },
        error : function() {}
});
})


function update(){
  console.log('update')
$.ajax({
    url : "",
    type : "GET",
    data : { },

    success : function(json) {
      placeTile(json['tiles_positions'], json['currentPlayer']);
      refresh(json['refresh_info'])
},
        error : function() {}
})
}

const refresh = (refreshInfo) => {
  setTimeout(()=>{
    if (refreshInfo){
    update()}}, 2000)
}

update()
