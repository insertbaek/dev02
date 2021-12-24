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
  "connecting": "",
  "last_connect": "",
  "state": false, //게임 시작 버튼 클릭 여부
  "turn": false //turn 체크
};


//유저 접속 정보 전달
socket.emit("login", user);

//대기실 재접속 일 때 유저 정보 받아오기
socket.on('resUser', function (data) {
  user = data;
  // console.log(user);
})



//방 생성 완료
socket.on('makeRoomSuccess', function (roomData, userData) {
  console.log(userData);
  user = userData;
  location.href = '/room?id=' + roomData.id; //해당 방으로 이동 처리
});


//방 리스트 요청
socket.emit('roomListLoad');


//방 리스트 노출
socket.on('roomList', function (data) {
  roomListAppend(data); // 방 리스트 
});


//삭제된 방 클릭
socket.on('roomListReload', function(type){
  if(type == 'delete'){
    alert("삭제된 방입니다. 다른 방을 골라주세요.");
  }
  location.reload();
});


//이미 접속 중인 방 존재
socket.on('sendRoomName', function(sendRoomName){
  alert("현재 [" + sendRoomName + "] 방에 접속중입니다.\n 방 나가기 후 다른 방 접속이 가능합니다.");
});


//방 입장 인원체크 후 이동
socket.on('checkRoomFlag', function (flag, data) {
  if (flag == true) {
    location.href = '/room?id=' + data;
  } else {
    alert("인원초과로 들어가실 수 없습니다.");
  }
});


//방 생성 user == null error
socket.on('maekeRoomError', function () {
  alert("유저 정보가 상이합니다. 다시 실행해주세요.");
  location.href = "/";
})



//********************************************************************************** */



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
  if (user.connecting !== '') {
    socket.emit('getRoomName',user.connecting)
  } else {
    //방생성
    socket.emit("makeRoom");
  }
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
        var roomId = this.getAttribute('data-room');
        var data = {
          'room': roomId,
          'user': user
        };
        //이미 접속해있는 방이 있는 지 확인
        if (user.connecting !== '' && user.connecting !== roomId) {
          socket.emit('getRoomName',user.connecting)
        } else {
          //인원 체크
          socket.emit("checkRoom", data);
        }
      });
    }
  }
}