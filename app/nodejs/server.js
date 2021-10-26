// modules init
const express = require('express');
const app = express();
const http = require('http').createServer(app);
const io = require('socket.io')(http);
const os = require('os');

const mazeNs = io.of('/maze'); //mazeNamespace
const mazeNsAdapter = mazeNs.adapter;
var roomList = [];
var userList = [];
var connected = true;
var newJoinFlag = true;

function getServerIp() {
    var ifaces = os.networkInterfaces();
    var result = '';

    for (var dev in ifaces) {
        var alias = 0;
        ifaces[dev].forEach(function (details) {
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

app.use('/css', express.static(PUBLIC_DIR + '/css'));
app.use('/js', express.static(PUBLIC_DIR + '/js'));

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


mazeNs.on('connection', (socket) => {
    var user = null;
    //유저 접속 데이터 받음
    socket.on("login", function (data) {
        user = data;
        checkUserList(data.uuid) //접속 check flag 값 받아옴

        if (newJoinFlag) { //처음 접속
            console.log("처음 접속");
            userList.push(user);
        } else {
            console.log("재접속");
        }

        // console.log('userList : ' + JSON.stringify(userList))
    });


    //현재 생성된 roomList 출력
    socket.on('roomListLoad', function () {
        socket.emit('roomList', roomList)
    });


    //새로운 방 등록
    socket.on('makeRoom', function () {
        var newRoomId = Math.random().toString(24);
        var newRoomName = 'test 들어오세요_' + Math.floor(Math.random() * 100);

        user.connecting = newRoomId;
        setUserData(user.uuid, newRoomId)
        console.log('userList : ' + JSON.stringify(userList))

        var newRoom = {
            'id': newRoomId,
            'name': newRoomName,
            'userList': [user]
        };

        roomList.push(newRoom);
        socket.join(newRoomId);

        socket.emit('makeRoomSuccess', newRoom, user);
    });

    //방 인원체크
    socket.on('checkRoom', function (data) {
        console.log('data : ' + JSON.stringify(data));

        var room = getRoomElement(data.room);
        var flag = true;
        var userCheckFlag = getRoomUser(data.room, user.uuid);

        if (room.userList.length < 2) {
            flag = true;
        } else {
            //이미 있는 user인지 체크
            if (userCheckFlag === false) {
                flag = false;
            } else {
                console.log("user reconnection");
                flag = true;
            }
        }
        socket.emit('checkRoomFlag', flag, data.room);
    });

    //방 입장
    socket.on('enterRoom', function (data) {
        user.connecting = data;
        var room = getRoomElement(user.connecting);
        var userCheckFlag = getRoomUser(user.connecting, user.uuid);

        console.log("userFlag"+userCheckFlag);
        console.log("data"+data);
        console.log("usre.connecting"+user.connecting);
        
        //이미 있는 user인지 체크
        if (userCheckFlag === false) {
            socket.join(user.connecting);
            room.userList.push(user);
            setUserData(user.uuid, user.connecting)
        } else {
            console.log("user exists(insertUser)");
        }
        console.log('room' + JSON.stringify(room))
    });


    //room에 있는 user 정보 전송
    socket.on('reqData', function (data) {
        checkUserList(data)
        console.log('reqData : ' + JSON.stringify(user))
        socket.emit('resData', user)
    })

    
    socket.on('leaveRoom', function(data){
        var room = getRoomElement(data);

        socket.leave(data);
        setRoomUserUpdate(room,user)

        console.log(JSON.stringify(room))

        socket.to(data).emit('leaveUserSuccess');
    })


    socket.on('disconnecting', (reason) => {
        connected = false;
    });


    //연결 종료
    socket.on('disconnect', (reason) => {
        console.log("user disconnect");
        // console.log(user);

        if (connected) {
            clearTimeout(clear);
        }
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

    //전체 유저리스트에서 유저 객체 찾기
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

        roomList.forEach((room) => {
            room.userList.forEach((users) => {
                if (users.uuid == uuid) {
                    flag = true;
                }
            })
        });
        return flag;
    }

    //유저리스트에서 해당 유저 입장 방 정보 변경
    setUserData = (userId, roomId) => {
        for (var i = 0; i < userList.length; i++) {
            if (userList[i].uuid === userId) {
                userList[i].connecting = roomId;
                break;
            }
        }
    }

    //유저 방 퇴장 시 방 유저 정보에서 해당 유저 삭제
    setRoomUserUpdate = (room, user) => {
        for(var i = 0; i < room.userList.length; i++){
            if(room.userList[i] === user){
                room.userList.splice(i,1);
                break;
            }
        }
    }

    //user 대기실 첫 접속 체크
    checkUserList = (uuid) => {
        for (var i = 0; i < userList.length; i++) {
            //접속 시 해당 유저 처음 접속인지 재접속인지 체크
            if (userList[i].uuid === uuid) {
                newJoinFlag = false;
                user = userList[i];
                break;
            }
        }
    }
});

