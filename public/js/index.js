var socket = io('/maze');
var uuid = "";

//임시 아이디 생성 및 불러오기
if (localStorage.getItem('uuid')) {
  uuid = localStorage.getItem('uuid')
} else {
  uuid = Math.random().toString(24);
  uuid = uuid.substr(-8);
  localStorage.setItem('uuid', uuid);
}

//유저 정보
var user = {
  "uuid": uuid,
  "nick": "basic",
  "rank": 0,
  "token": "A",
  "connecting":""
};

$('#access-id').text(uuid);

//대기실 새로고침 버튼
$('#btn-reset').click(() => {
  var roomListWrapper = document.getElementById('roomListWrapper');
  while (roomListWrapper.firstChild) { //wrapper에 있는 기존 방 리스트를 모두 삭제
    roomListWrapper.removeChild(roomListWrapper.firstChild);
  }
  socket.emit('roomListLoad');
});

//방 생성 버튼
$('#btn-make-room').click(() => {
  socket.emit("makeRoom");
});

//유저 접속 정보 전달
socket.emit("login", user);

//유저 재접속 - 기존 userList에 저장된 정보 받아옴
socket.on("newUserCheck",function(data){
  user = data;
  socket.emit("userUpdate",user);
})

//방 생성 완료
socket.on('makeRoomSuccess', function (roomData, userData) {
  user = userData;

  socket.emit("userUpdate",userData);
  socket.emit("enterRoomPage", userData);
  location.href = '/room?id=' + roomData.id; //해당 방으로 이동 처리
});

//방 리스트 요청
socket.emit('roomListLoad');

//방 리스트 노출
socket.on('roomList', function (data) {
  roomListAppend(data); // 방 리스트 
});

//방 리스트 생성 
function roomListAppend(data) {
  var roomListWrapper = document.getElementById('roomListWrapper');

  if (roomListWrapper != undefined) {
    var statement = '';

    data.forEach(function (el) {
      statement += '<li class="list-group-item" data-room="' + el.id + '">' + el.name + '<button type="button" class="btn-enter btn btn-secondary btn-sm" data-room="' + el.id + '">입장</button></li>';
    });

    roomListWrapper.insertAdjacentHTML('beforeend', statement);

    var roomName = document.querySelectorAll('.btn-enter')

    for (var i = 0; i < roomName.length; i++) {
      //방 입장    
      roomName[i].addEventListener('click', function () {
        roomCheck(this);
      });
    }
  }

  function roomCheck(element) {
    var roomId = element.getAttribute('data-room');
    var data = {
      'room': roomId,
      'user': user
    };
    //인원 체크
    socket.emit("checkRoom", data);
  }

  socket.on('checkRoomFlag', function (flag, data) {
    if(flag == true){
      socket.emit('enterRoom',data);
      location.href='/room?id=' + data.room; 
    }else{ 
      alert("인원초과로 들어가실 수 없습니다."); 
    } 
  });
}