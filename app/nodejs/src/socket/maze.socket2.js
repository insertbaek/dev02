let roomList = [];
let userList = [];
let connected = true;

const mazeNSSocket = (io, mazeNs, socket) => {
    var user = null;
    //유저 접속 데이터 받음

    socket.on("login", function (data) {
        user = data;
        let newJoinFlag = checkUserList(user.uuid) //접속 check flag 값 받아옴

        if (newJoinFlag) { //처음 접속
            userList.push(user);
        }
        socket.emit('resUser', user);
    });

    socket.on('existJoin', function () {
        // console.log("______existJoin : " + JSON.stringify(user));
        // console.log(user.connecting)
        if (user.connecting !== '' && user != null) {
            socket.join(user.connecting)
        }
    })


    //현재 생성된 roomList 출력
    socket.on('roomListLoad', function () {
        socket.emit('roomList', roomList)
    });


    //새로운 방 등록
    socket.on('makeRoom', function () {
        var newRoomId = Math.random().toString(24);
        var newRoomName = 'test 들어오세요_' + Math.floor(Math.random() * 100);

        if (user !== null) {
            user.connecting = newRoomId;

            var newRoom = {
                'id': newRoomId,
                'name': newRoomName,
                'turn': 0, //전체 턴 수
                'state': false, //게임 시작 여부
                'startTime':"",
                'totalTime':0,
                'userList': []
            };

            roomList.push(newRoom);
            socket.emit('makeRoomSuccess', newRoom);
        } else {
            socket.emit('maekeRoomError');
        }
    });


    //방 인원체크
    socket.on('checkRoom', function (data) {
        let room = getRoomElement(data.room);

        if (room == null) {
            socket.emit('roomListReload', 'delete')
        } else {
            let joinRoom = getCheckRoomUser(room.id, user.uuid)
            let flag = true;

            console.log("룸 ㅣ "+ JSON.stringify(room));
            

            user.connecting = room.id;
            setUserData(user.uuid, "connecting", user.connecting)

            // console.log('checkRoom ' + JSON.stringify(room))
            console.log('[checkRoom checking] ' + JSON.stringify(getUserElement(user.uuid)))
            console.log("😙😙😙😙😙😙😙😙😙😙😙😙😙😙😙😙😙😙😙😙😙😙");
            // console.log("in room user exisxts : " + joinRoom);
            if (room.userList.length < 2) {
                flag = true;
            } else {
                //이미 있는 user인지 체크
                if (joinRoom === false) {
                    flag = false;
                } else {
                    console.log("user reconnection");
                    flag = true;
                }
            }
            socket.emit('checkRoomFlag', flag, data.room);
        }

    });


    //room에 있는 user 정보 전송
    socket.on('reqData', function (data) {
        var getUser = getUserElement(data); //유저리스트에서 유저 찾고
        var room = getRoomElement(getUser.connecting)
        console.log("getUserConnecting : " + getUser.connecting);
        socket.emit('resData', getUser)
    });


    //접속한 방 이름 전송
    socket.on('getRoomName', function (roomId) {
        var room = getRoomElement(roomId);
        var roomName = room.name;
        socket.emit('sendRoomName', roomName);
    })


    //방 입장
    socket.on('enterRoom', async (data) => {
        let room = getRoomElement(data);
        let joinRoom = getCheckRoomUser(room.id, user.uuid)

        console.log('========= join room : ' + joinRoom)

        if (joinRoom) {
            console.log("이미 입장한 유저");
        } else {
            if (user.connecting !== room.id) {
                user.connecting = room.id;
                setUserData(user.uuid, "connecting", user.connecting)
            }
            socket.join(room.id);
            user.last_connect = room.id;
            room.userList.push(user)
        }

        if (room.userList.length >= 2) {
            mazeNs.to(room.id).emit('joinUser', room.userList)
        }
        // console.log("enterRoomUser : " + JSON.stringify(room.userList))
        console.log("enterRoomUser : " + JSON.stringify(user))
        socket.emit('enterRoomSuccess', room)
        // console.log("data : " + JSON.stringify(room));
        console.log("............................. enterRoom End................................")
    });


    //게임 포기, 방 나가기
    socket.on('leaveRoom', function (data, type) {
        var room = getRoomElement(data);
        // console.log(JSON.stringify(room));

        socket.leave(data);
        setRoomUserUpdate(room, user)
        user.connecting = "";
        setUserData(user, "connecting", user.connecting)
        setRoomUserState(room.id, user.uuid, false)
        setUserData(user.uuid, "state", false)
        setRoomUpdate(room.id, "state", false)

        if (type == "giveup") {
            //패배처리 소스 추가 필요
            //시간 처리도 0으로 만들 소스 필요
            socket.to(data).emit('giveUpUserSuccess');
        } else {
            socket.to(data).emit('leaveUserSuccess');
        }

        socket.emit('roomListReload', "exit")

        // console.log(JSON.stringify(room))
        connected = false;
    });


    socket.on('disconnecting', (reason) => {

    });


    //연결 종료
    socket.on('disconnect', (reason) => {
        // console.log("user disconnect");
        var clear = setTimeout(() => {
            if (user != null && user.last_connect != '') {
                // console.log("last : " + user.last_connect)
                let room = getRoomElement(user.last_connect)
                let clientCount = '';

                if (room != null) {
                    clientCount = room.userList.length;
                }

                // console.log(room)
                // console.log(room.userList.length)
                // console.log('===========================')

                if (clientCount == 0) {
                    deleteRoom(room)
                }
            }
        }, 3000);

        // if (connected) {
        //     clearTimeout(clear);
        // }
    });


    // socket.on('countUser', function(roomId){
    //     var room = getRoomElement(roomId);
    //     mazeNs.in(roomId).fetchSockets().then((sockets) => {
    //         mazeNs.to(roomId).emit('sendCountUser', sockets.length, room)
    //         });
    //         console.log("^^^^^^^^^^^^countUser^^^^^^^^^^^^^^")
    // })


    socket.on('startState', function (state, roomId) {
        let room = getRoomElement(roomId);
        // console.log("startState : "+ room);

        setRoomUserState(roomId, user.uuid, state)
        setUserData(user.uuid, "state", state)

        if (room.userList[0].state == true && room.userList[1].state == true) {
            room.userList[0].turn = true;
            room.userList[1].turn = false;
            mazeNs.to(roomId).emit('gameStart', room.turn, room.userList, true)
        }

        // console.log("room state상태 : " + JSON.stringify(room))
    })


    socket.on('timeStart', function (roomId, turn, run) {
        let room = getRoomElement(roomId)
        let date = new Date();
        let gameTime = "";
        let startTime = "";
        let clearTimer;
        // let totalPlayTime = 0;
        let flag = false;

        if(room.startTime == ""){
            startTime = date;
            setRoomUpdate(roomId, "startTime", startTime)
        }else{
            startTime = room.startTime;
        }
        console.log("run :"+ run)
        setRoomUpdate(roomId, "turn", turn)
        if(run === true){
            setRoomUpdate(roomId, "state", true)
            flag = true;
            
            console.log("====================timeStart",JSON.stringify(getRoomElement(roomId)));
            clearTimer = setInterval(() => {
                Timer()
            }, 1000)
        }else{
            flag = false; 
            clearInterval(clearTimer)
            console.log("clearTimer :" + clearTimer);
            flag = true;
            clearTimer = setInterval(() => {
                Timer()
            }, 1000)
        }

        console.log(flag)
        

        Timer = () =>{
            if(flag == true){
                let time = Math.floor(((date - new Date()) / 1000) % 60);
                let roundPlayTime = -(Math.floor(((startTime - new Date()) / 1000) % 60)); //턴 체인지 시 주는 여유시간 때문에 +1초씩 누적해서 밀려남.
                let sumPlayTime = "";
                gameTime = 60 + time;
                if (gameTime == 0) {
                    clearInterval(clearTimer)
                    mazeNs.to(roomId).emit('turnout', room.userList);
                    sumPlayTime = room.totalTime + roundPlayTime;
                    console.log(sumPlayTime);
                    setRoomUpdate(roomId, "totalTime", sumPlayTime)
                }

                console.log(roundPlayTime);
                mazeNs.to(roomId).emit('timer', gameTime)

            }
        }
    })


    //run == true: 바로 실행, false : 초기화 후 실행
    socket.on('turnChange', function (run) {
        //room.userList에서 
        console.log("==================turnChange===================")
        let room = getRoomElement(user.connecting)

        for(var i=0; i<room.userList.length; i++){
            var turnFlag = room.userList[i].turn;
            room.userList[i].turn = !turnFlag
        }
        // console.log(JSON.stringify(room.userList));
        mazeNs.to(room.id).emit('gameStart', room.turn, room.userList, run)
    })


    //user = null로 인한 에러
    socket.on('error', function () {
        var room = getRoomElement(user.connecting);
        deleteRoom(getRoomElement(user.connecting))
        setRoomUserUpdate(room, user)
        setUserData(user.uuid, "connecting", "")
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
        let getUser = null;
        for (var i = 0; i < userList.length; i++) {
            if (userList[i].uuid === userId) {
                getUser = userList[i];
                break;
            }
        }
        return getUser
    }

    //해당 방에 있는 유저 state값 변경
    setRoomUserState = (roomId, uuid, state) => {
        var room = getRoomElement(roomId);
        let getUser = null;
        console.log("setRoomUserState : "+ roomId, JSON.stringify(room))
        for (var i = 0; i < room.userList.length; i++) {
            if (room.userList[i].uuid === uuid) {
                room.userList[i].state = state;
                break;
            }
        }
    }

    //방 정보 업데이트
    setRoomUpdate = (roomId, type, data) => {
        var room = null;
        for (var i = 0; i < roomList.length; i++) {
            if (roomList[i].id === roomId) {
                roomList[i][type] = data;
                break;
            }
        }
    }


    //방 userList - user 중복 체크
    getCheckRoomUser = (roomId, uuid) => {
        var room = getRoomElement(roomId);
        var flag = false;
        if (room != null) {
            for (var i = 0; i < room.userList.length; i++) {
                console.log("user " + (i + 1) + ": " + room.userList[i].uuid + "/" + uuid)
                if (room.userList[i].uuid === uuid) {
                    flag = true;
                    break;
                }
            }
        }
        return flag;
    }

    //유저리스트에서 해당 유저 입장 방 정보 변경
    setUserData = (userId, type, data) => {
        console.log("String TYPE : " + type)
        for (var i = 0; i < userList.length; i++) {
            if (userList[i].uuid === userId) {
                userList[i][type] = data;
                console.log("type : " + JSON.stringify(userList[i]))
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
        for (var i = 0; i < roomList.length; i++) {
            if (roomList[i] == room) {
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
                user = userList[i];
                return false;
            }
        }
        return true;
    }

}

module.exports = { mazeNSSocket };