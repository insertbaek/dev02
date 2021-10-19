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

//유저 접속 정보 전달
socket.emit("login", user);



//유저 재접속 - 기존 userList에 저장된 정보 받아옴
socket.on("newUserCheck",function(data){
  user = data;
  socket.emit("userUpdate",user);
})
