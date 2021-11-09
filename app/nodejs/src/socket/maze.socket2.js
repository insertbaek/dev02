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
        console.log(user);
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
            socket.emit('roomListReload')
        } else {
            let joinRoom = getCheckRoomUser(room.id, user.uuid)
            let flag = true;




            user.connecting = room.id;

            setUserData(user.uuid, user.connecting)

            console.log('checkRoom ' + JSON.stringify(room))
            console.log("in room user exisxts : " + joinRoom);
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
        console.log("data : " + room);

        let joinRoom = getCheckRoomUser(room.id, user.uuid)


        if (joinRoom) {
            console.log("이미 입장한 유저");
            // mazeNs.in(room.id).fetchSockets().then((sockets) => {
            //     console.log(sockets.length);
            // })

        } else {
            if (user.connecting !== room.id) {
                user.connecting = room.id;
                setUserData(user.uuid, user.connecting)
            }

            socket.join(room.id);
            user.last_connect = room.id;
            room.userList.push(user)

            // mazeNs.in(room.id).fetchSockets().then((sockets) => {
            //     console.log(sockets.length);
            // })

            // mazeNs.in(room.id).fetchSockets().then((sockets) => {
            //     socket.emit('count', sockets.length)
            // })
        }
        if (room.userList.length >= 2) {
            socket.in(room.id).emit('joinUser', room.userList)
            socket.emit('joinUser', room.userList)
        }

    });

    socket.on('leaveRoom', function (data, type) {
        var room = getRoomElement(data);

        socket.leave(data);
        setRoomUserUpdate(room, user)
        user.connecting = "";
        setUserData(user, user.connecting);

        if (type == "giveup") {
            //패배처리 소스 추가 필요
            socket.to(data).emit('giveUpUserSuccess');
        } else {
            socket.to(data).emit('leaveUserSuccess')
        }

        console.log(JSON.stringify(room))
        connected = false;
    });


    socket.on('disconnecting', (reason) => {

    });


    //연결 종료
    socket.on('disconnect', (reason) => {
        // console.log("user disconnect");
        var clear = setTimeout(() => {
            if (user != null && user.last_connect != '') {
                console.log("last : " + user.last_connect)
                let room = getRoomElement(user.last_connect)
                let clientCount = '';

                if (room != null) {
                    clientCount = room.userList.length;
                }

                // mazeNs.in(user.last_connect).fetchSockets().then((sockets) => {
                //     clientCount = sockets.length;
                // })

                // console.log(room)
                // console.log(room.userList.length)
                // console.log('===========================')

                if (clientCount == 0) {
                    deleteRoom(room)
                }
            }
        }, 5000); //최종적으로 세션으로 체크해야할지 고민

        // if (connected) {
        //     clearTimeout(clear);
        // }
    });

    socket.on('startState', function (state, roomId) {
        let room = getRoomElement(roomId);
        setRoomUserState(room, user.uuid, state)

        if(room.userList[0].state == true && room.usrList[1].state == true){
            socket.emit('gaemStart')
        }
        console.log("room state상태 : " + room)
    })



    //user = null로 인한 에러
    socket.on('error', function () {
        var room = getRoomElement(user.connecting);
        deleteRoom(getRoomElement(user.connecting))
        setRoomUserUpdate(room, user)
        setUserData(user.uuid, "")
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
    setRoomUserState = (room, uuid, state) => {
        let getUser = null;
        for (var i = 0; i < room.userList.length; i++) {
            if (room.userList[i].uuid === uuid) {
                    room.userList[i].state = state;
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