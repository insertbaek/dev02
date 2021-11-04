let roomList = [];
let userList = [];
let connected = true;

const mazeNSSocket = (io, mazeNs, socket) => {
    var user = null;
    //유저 접속 데이터 받음
    //io.socketsJoin("lobby");

    socket.on("login", function (data) {
        user = data;
        let newJoinFlag = checkUserList(user.uuid) //접속 check flag 값 받아옴

        if (newJoinFlag) { //처음 접속
            userList.push(user);
        }
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

            user.connecting = newRoomId;

            var newRoom = {
                'id': newRoomId,
                'name': newRoomName,
                'userList':[]
            };

            roomList.push(newRoom);

            socket.emit('makeRoomSuccess', newRoom);
        } else {
            socket.emit('maekeRoomError');
        }
    });


    //방 인원체크
    socket.on('checkRoom', function (data) {
        var room = getRoomElement(data.room);
        console.log("checkRoom: "+room)
        //console.log("clientCount: "+mazeNs.adapter.rooms.get(room.id).size)
        var flag = true;
        //user.roomCheckFlag = getRoomUser(data.room, data.user);
        console.log('checkRoom '+JSON.stringify(room))
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
        user.connecting = roomId
        setUserData(user.uuid, user.connecting)
        //mazeNs.socketsJoin(user.connecting)
        console.log(user)
    });


    //room에 있는 user 정보 전송
    socket.on('reqData', function (data) {
        console.log(data)
        var getUser = getUserElement(data); //유저리스트에서 유저 찾고
        //user.roomCheckFlag = getRoomUser(getUser.connecting, getUser.uuid)
        socket.emit('resData', getUser)
    });

    //방 입장
    socket.on('enterRoom', async (data)=> {

        let room = getRoomElement(data);
        user.connecting = room.id;
        let joinRoom = getRoomUser(room.id, user.uuid)
        if(joinRoom)
        {
            console.log("이미 입장한 유저");
        }
        else
        {
            console.log(room.id)
            mazeNs.socketsJoin(room.id);
            room.userList.push(user)
            mazeNs.in(room.id).fetchSockets().then((sockets)=>{
                socket.emit('count', sockets.length)
            })
        }

        //console.log(clients)
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
    socket.on('disconnect',async (reason) => {
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
        let getUser = null;
        for (var i = 0; i < userList.length; i++) {
            if (userList[i].uuid === userId) {
                getUser = userList[i];
                break;
            }
        }
        return getUser
    }

    //방 userList - user 중복 체크
    getRoomUser = (roomId, uuid) => {
        var room = getRoomElement(roomId);
        var flag = false;
        if(room != null)
        {
            for (var i = 0; i < room.userList.length; i++) {
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
                user = userList[i];
                return false;
            }
        }
        return true;
    }

    var clientsCount = async function(roomId) {
        var userCount = await mazeNs.fetchSockets();
        // if(!userCount.length) {
        //     throw new Error('socket is not found');
        // }
        // return Array.from(userCount[0].rooms);
        return userCount
    }

}

module.exports = { mazeNSSocket };