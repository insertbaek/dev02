var socket = io('/maze');
var uuid = "";
var user = {};

//임시 아이디 불러오기
uuid = localStorage.getItem('uuid');


//server에 id 전송 
socket.emit('reqData',uuid)


//server에서 user정보 받아 옴
socket.on('resData',function(data){
    user = data;
    $("#roomName").text(user.connecting);
})

//포기 버튼
$('#btn-exit-room').click(() => {
    if(confirm("게임을 포기하시겠습니까?")){
        socket.emit("leaveRoom", user.connecting);
        // location.href="/";
    }
});

socket.on('leaveUserSuccess', function(){
    console.log('leaveUserSuccess');
    alert("상대방이 게임을 포기하였습니다.");
});