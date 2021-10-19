// modules init
const express = require('express');
const app = express();
const http = require('http').createServer(app);
const io = require('socket.io')(http);
const os = require('os');  

const mazeNs = io.of('/maze'); //mazeNamespace
const mazeNsAdapter = mazeNs.adapter;
var roomList=[];
var userList=[];
var connected = true;
var newJoinFlag = true;



function getServerIp() {
    var ifaces = os.networkInterfaces();
    var result = '';

    for (var dev in ifaces) {
        var alias = 0;
        ifaces[dev].forEach(function(details) {
            if (details.family == 'IPv4' && details.internal === false) {
                result = details.address;
                ++alias;
            }
        });
    }

    return result;
}

// variables init
if (getServerIp() == '192.168.56.14') {
    var ROOT_DIR = "/home/dev02.01";
} else {
    var ROOT_DIR = "/DEV02";
}
var APP_DIR = ROOT_DIR + "/app";
var PYTHON_DIR = APP_DIR + "/python";
var NODEJS_DIR = APP_DIR + "/nodejs";
var PUBLIC_DIR = ROOT_DIR + "/public";

/* nodejs -> python */
const spawn = require('child_process').spawn;
const exec = require('child_process').exec;
const python = spawn('python', [PYTHON_DIR + '/welcome.py']);
python.stdout.on('data', (data) => {
    let returnStr = data.toString('utf-8');
    console.log(returnStr)
});
/* nodejs -> python */

app.use('/css', express.static(PUBLIC_DIR+'/css'));
app.use('/js', express.static(PUBLIC_DIR+'/js'));

/* main */
app.get('/', (req, res) => {
    res.sendFile(PUBLIC_DIR + '/index.html');
});

app.get('/maze', (req, res) => {
    res.sendFile(PUBLIC_DIR + '/maze.html');
});

/* room */
app.get('/room', (req, res) => {
	res.sendFile(PUBLIC_DIR + '/room.html');
    // console.log(req.params);
});

http.listen(3000, () => {
    console.log('Connected at 3000');
});
	console.log('Connected at 3000');
});

io.on('connection', (socket) => {
    socket.on('request_message', (msg) => {
        io.emit('response_message', msg);
mazeNs.on('connection', (socket)=>{
    var user = null;


    //유저 접속 데이터 받음
    socket.on("login", function(data){

        checkUserList(data.uuid) //접속 check flag 값 받아옴

        if (newJoinFlag) { //처음 접속
            // console.log("처음 접속");
            user = data;
            userList.push(user);
        }else{
            // console.log("재접속");
            socket.emit("newUserCheck",getUserElement(data.uuid));
        }
        console.log(user);
    })

    // user 재접속 시 user 정보 userList 정보로 받아 업데이트
    socket.on("userUpdate",function(data){
        user = data;
    })

    //현재 생성된 roomList 출력
    socket.on('roomListLoad', function() {
        socket.emit('roomList', roomList)
    });

    //새로운 방 등록
    socket.on('makeRoom', function() {
        var newRoomId = Math.random().toString(24);
        var newRoomName = 'test 들어오세요_' + Math.floor(Math.random()*100);
        var beforeUser = getUserElement(user.uuid);

        user.connecting = newRoomId;
        beforeUser.connecting = newRoomId;

        var newRoom = {
            'id': newRoomId,
            'name': newRoomName,
            'userList': [user]
        }
        roomList.push(newRoom);
        socket.join(newRoom.id);

        socket.emit('makeRoomSuccess', newRoom, user);
    });

    //방 인원체크
    socket.on('checkRoom',function(data){
        var room = getRoomElement(data.room);
        var flag = true;
        var userCheckFlag = getRoomUser(data.room, data.user.uuid);

        if(room.userList.length < 2){
            flag = true;
        }else{
            //이미 있는 user인지 체크
            if(userCheckFlag == false){
                flag = false;
            }else{
                console.log("user reconnection");
                flag = true;
            }
        }
        socket.emit('checkRoomFlag',flag,data);
    })

    //방 입장
    socket.on('enterRoom', function(data){
        var room = getRoomElement(data.room);
        var user = data.user;
        var userCheckFlag = getRoomUser(data.room, user.uuid);

        //이미 있는 user인지 체크
        if(userCheckFlag == false){
            socket.join(data.room);
            user.connecting = data.room;
            room.userList.push(user);
        }else{
            console.log("user exists(insertUser)");
        }
    });

    socket.on('disconnecting', (reason) => {
        connected = false;
        // console.log("connected",connected);
        // console.log("socket.rooms",socket.rooms);
    });

    socket.on('disconnect', async() => {
        console.log('user disconnected');
    //연결 종료
    socket.on('disconnect', async (reason) => {
        console.log("user disconnect");
        // if(){ //새로고침일 때

        // }else{ // 뒤로 나가기 했을 때
        //     //방에서도 퇴장
        // }


        var clear = setTimeout(() => {
            if (!connected && user != null) { //리프레시인지 종료인지 체크
                // var clients = mazeNs.adapter.rooms.get(user.connnecting);

                var clients = io.of('/mazeNS').in(user.connnecting).allSockets();
                // clients.then((dd)=>{
                //     console.log(dd)
                // });
                var room = getRoomElement(user.connecting) // 현재 소켓의 방 체크
                var clientCount = clients != undefined ? clients.size : null;
                // console.log("client",clients);
                // console.log("size",clientCount);
                // if(clientCount != null && clientCount == 0 ){
                //     console.log("방이 있고, 0명이다.");
                // }else{
                //     console.log("방이 x")
                // }
            };
        }, 1000);

        if (connected) {
            clearTimeout(clear);
        }
    });
});

//방 찾기
getRoomElement = (roomId) => {
    var room = null;
    for (var i = 0; i < roomList.length; i++) {
        if (roomList[i].id === roomId) {
            room = roomList[i];
            break;
        }
    }
    return room;
}

//전체 유저리스트에서 유저 찾기
getUserElement = (userId) => {
    var user = null;
    for (var i = 0; i < userList.length; i++) {
        if (userList[i].uuid === userId) {
            user = userList[i];
            break;
        }
    }
    return user;
}

//방 userList - user 중복 체크
getRoomUser = (roomId, uuid) => {
    var room = getRoomElement(roomId);
    var flag = false;

    roomList.forEach((room)=>{
        room.userList.forEach((users)=>{
            if(users.uuid == uuid){
                flag = true;
            }
        })
    });

    return flag;
}

//user 대기실 첫 접속 체크
checkUserList = (uuid) => {
    for (var i = 0; i < userList.length; i++) {
        //접속 시 해당 유저 처음 접속인지 재접속인지 체크
        if (userList[i].uuid === uuid) {
            newJoinFlag = false;
            break;
        }
    }
}