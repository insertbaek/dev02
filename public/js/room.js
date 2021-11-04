var socket = io('/maze');
var uuid = '';
var user = null;
// var userFlag = '';
// var userConnecting = '';

//임시 아이디 불러오기
uuid = localStorage.getItem('uuid');


//server에 id 전송 
socket.emit('reqData',uuid);
 

//server에서 user정보 받아 옴
socket.on('resData',function(data){
    console.log(data);
    user = data;
    $("#roomName").text(user.connecting);
    // var data = {
    //     'room':{
    //         'id':user.connecting
    //     },
    //     'user':user
    // }
    socket.emit("enterRoom", user.connecting);
});

//setInterval(function(){socket.emit('count')},3000)
socket.on('count',function(data){
    alert(data)
})
//포기 버튼
// $('#btn-exit-room').click(() => {
//     if(confirm("게임을 포기하시겠습니까?")){
//         socket.emit("leaveRoom", user.connecting);
//         // location.href="/";
//     }
// });


socket.on('errorMessage',function(){
    alert("입장이 제대로 진행되지 않았습니다. 다시 입장해주세요.");
    location.href="/";
})


// socket.on('leaveUserSuccess', function(){
//     console.log('leaveUserSuccess');
//     alert("상대방이 게임을 포기하였습니다.");
// });

socket.on('error', function(data){
    alert(data.content);
    location.href = '/';
})