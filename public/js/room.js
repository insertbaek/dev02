var socket = io('/maze');
var uuid = '';
var user = null;


//임시 아이디 불러오기
uuid = localStorage.getItem('uuid');


//server에 id 전송 
socket.emit('reqData',uuid);
 

//server에서 user정보 받아 옴
socket.on('resData',function(data){
    user = data;
    $("#roomName").text(user.connecting);
    $("#player1-name").text(user.uuid);
    socket.emit("enterRoom", user.connecting);

    var clear = setTimeout(() => {
        socket.emit('existJoin')
    }, 10); 
});


//setInterval(function(){socket.emit('count')},3000)
socket.on('count',function(data){
    alert(data)
})


//상대방 입장
socket.on('joinUser', function(userList){
    let player2 = "";
    for(var i = 0; i < userList.length; i++){
        if(userList[i].uuid != user.uuid){
            player2 = userList[i].uuid;
            break;
        }
    }
    $('#player2-name').text(player2)
    $('#btn-player1-start').removeClass('disabled');
    $('#btn-player2-start').removeClass('disabled');
    $('#btn-player2-start').css('cursor','dafult');
})


//입장 Error Message
socket.on('errorMessage',function(){
    alert("입장이 제대로 진행되지 않았습니다. 다시 입장해주세요.");
    location.href="/";
})


//상대방 게임 포기 시 
socket.on('giveUpUserSuccess', function(){
    alert("상대방이 게임을 포기하였습니다.");
});


//상대가 방을 나갔을 때
socket.on('leaveUserSuccess', function(){
    $('#player2-name').text('대기중')
    //시작하기 버튼 다시 비활성화 만들기
})


socket.on('gaemStart', function(){
    
})


//에러 : 수정 필요
socket.on('error', function(data){
    alert(data.content);
    location.href = '/';
})

//********************************************************************************** */


// 나가기 버튼
$('#btn-leave-room').click(() => {
    if(confirm("방을 나가시겠습니까?")){
        socket.emit("leaveRoom", user.connecting, "leave");
        location.href="/";
    }
});

// 포기 버튼
$('#btn-give-up').click(() => {
    if(confirm("게임을 포기하시면 패배로 처리됩니다\n게임을 포기하시겠습니까?")){
        socket.emit("leaveRoom", user.connecting, "giveup");
        location.href="/";
    }
});


//1번 플레이어 게임 시작 버튼
document.getElementById('btn-player1-start').addEventListener('click', function(){
    socket.emit('startState', true, user.connecting);
    this.classList.remove('btn-warning');
    this.classList.add('btn-danger');
});


