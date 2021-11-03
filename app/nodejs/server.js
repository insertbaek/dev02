// modules init
const express = require('express');
const app = express();
const http = require('http').createServer(app);
const io = require('socket.io')(http);
const os = require('os');
const routes = require('./src/route/api/v1');

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

// parse json request body
app.use(express.json());
// parse urlencoded request body
app.use(express.urlencoded({ extended: true }));

app.use('/css', express.static(PUBLIC_DIR + '/css'));
app.use('/js', express.static(PUBLIC_DIR + '/js'));

/* api */
app.use('/v1', routes);

/* main */
app.get('/', (req, res) => {
    res.sendFile(PUBLIC_DIR + '/index.html');
});

/* maze */
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
            // console.log("처음 접속");
            userList.push(user);
        } else {
            // console.log("재접속");
        }

        // console.log('접속 user : ' + JSON.stringify(user))
    });


    //현재 생성된 roomList 출력
    socket.on('roomListLoad', function () {
        socket.emit('roomList', roomList)
    });


    //새로운 방 등록
    socket.on('makeRoom', function () {
        var newRoomId = Math.random().toString(24);
        var newRoomName = 'test 들어오세요_' + Math.floor(Math.random() * 100);

        if (user !== null) {
            user.roomCheckFlag = false;

            var newRoom = {
                'id': newRoomId,
                'name': newRoomName,
                'userList': [user]
            };

            mazeNs.socketsJoin(newRoomId);
            roomList.push(newRoom);

            socket.emit('makeRoomSuccess', newRoom, user);
        } else {
            socket.emit('maekeRoomError');
        }
    });


    //방 인원체크
    socket.on('checkRoom', function (data) {
        var room = getRoomElement(data.room);
        var flag = true;
        user.roomCheckFlag = getRoomUser(data.room, user.uuid);

        if (room.userList.length < 2) {
            flag = true;
        } else {
            //이미 있는 user인지 체크
            if (user.roomCheckFlag === false) {
                flag = false;
            } else {
                console.log("user reconnection");
                flag = true;
            }
        }
        socket.emit('checkRoomFlag', flag, data.room);
    });

    socket.on('beforeEnterRoom', function (roomId) {
        user.connecting = roomId;
        setUserData(user.uuid, roomId)
    });


    //room에 있는 user 정보 전송
    socket.on('reqData', function (data) {
        console.log("userList : " + JSON.stringify(userList));
        console.log("uuid : " + data);
        getUserElement(data); //유저리스트에서 유저 찾고
        
        console.log(" 들어간 유저 정보 : " + JSON.stringify(user));
        user.roomCheckFlag = getRoomUser(user.connecting, user.uuid)

        if (user == null) {
            socket.emit('error')
            socket.emit('errorMessage')
        } else {
            socket.emit('resData', user)
            console.log('reqData : ' + JSON.stringify(user))
        }

    });


    //방 입장
    socket.on('enterRoom', function (data) {
        var room = getRoomElement(user.connecting);

        //이미 있는 user인지 체크
        if (user.roomCheckFlag === false) {
            mazeNs.socketsJoin(user.connecting);
            console.log("joinroom :"+ JSON.stringify(socket.rooms));
            var clientCount = io.of('/maze').in(data).fetchSockets();
            var clientCount2 = io.of("/maze").in(data).allSockets();
            var clientCount3 = io.of("/maze").allSockets();
            // console.log("clientCount: "+JSON.stringify(clientCount))
            // console.log("clientCount2: "+JSON.stringify(clientCount2))
            var CC = clientsCount(data)
            let clientsInRoom = 0;
            if (io.sockets.adapter.rooms.has(room)) clientsInRoom = io.sockets.adapter.rooms.get(room).size
            console.log('clientRoom : '+clientsInRoom)
            console.log('clientCount : '+JSON.stringify(clientCount))
            console.log('clientCount2 : '+JSON.stringify(clientCount2))
            console.log('clientCount3 : '+JSON.stringify(clientCount3))
            console.log('clientCount4 : '+ JSON.stringify(CC))
            console.log(io.of('/maze').sockets.get())

            room.userList.push(user);
        } else {
            console.log("user exists(insertUser)유저가 이미 있음.");
        }
        // console.log('room' + JSON.stringify(room))
        // console.log('userList : ' + JSON.stringify(userList));
    });




    // socket.on('leaveRoom', function(data){
    //     var room = getRoomElement(data);

    //     socket.leave(data);
    //     setRoomUserUpdate(room,user)
    //     user.connecting = "";
    //     setUserData(user,user.connecting);


    //     console.log(JSON.stringify(room))

    //     socket.to(data).emit('leaveUserSuccess');
    // });

    //user = null로 인한 에러
    socket.on('error', function () {
        var room = getRoomElement(user.connecting);
        deleteRoom(getRoomElement(user.connecting))
        setRoomUserUpdate(room, user)
        setUserData(user.uuid, "")
    });

    socket.on('disconnecting', (reason) => {
        connected = false;
    });


    //연결 종료
    socket.on('disconnect', (reason) => {
        // console.log("user disconnect");
        // console.log(user);

        //방에 들어있는 인원이 몇 명인지 찾기 . 연결된 socket 수
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
    }

    //방 userList - user 중복 체크
    getRoomUser = (roomId, uuid) => {
        var room = getRoomElement(roomId);
        var flag = false;

        for (var i = 0; i < room.userList.length; i++) {
            if (room.userList[i].uuid === uuid) {
                flag = true;
                break;
            }
        }
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
        for (var i = 0; i < room.userList.length; i++) {
            if (room.userList[i] === user) {
                room.userList.splice(i, 1);
                break;
            }
        }
    }

    // 방 삭제 
    deleteRoom = (room) => {
        for (var i = 0; i < roomList; i++) {
            if (roomList[i] === room) {
                roomList.splice(i, 1);
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

    var clientsCount = async function(roomId) {
        var userCount = await io.of('/maze').fetchSockets();
        // if(!userCount.length) {
        //     throw new Error('socket is not found');
        // }
        // return Array.from(userCount[0].rooms);
        return userCount 
    }

});

