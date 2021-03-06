window.addEventListener("load", function () {
    var socket = io('/maze');
    var uuid = '';
    var user = null;
    var pressNum = 0;

    //임시 아이디 불러오기
    uuid = localStorage.getItem('uuid');


    //server에 id 전송 
    socket.emit('reqData', uuid);


    //server에서 user정보 받아 옴
    socket.on('resData', function (data) {
        user = data;
        $("#roomName").text(user.connecting);
        $("#player1-name").text(user.uuid);
        socket.emit("enterRoom", user.connecting);
    });


    //입장 완료
    socket.on('enterRoomSuccess', function (room) {
        let clear = setTimeout(() => {
            socket.emit('existJoin')
        }, 10);

        var data = {
            url: '/v1/user', 
            method: 'patch',
            data: '?uuid=' + uuid
          }
          ApiHelper(data).then(res => {
            // console.log(res)
            //유저 정보
            user = {
              "uuid": res.uuid,
              "nick": res.nick,
              "rank": res.rank,
              "token": res.token,
              "connecting": res.connecting,
              "last_connect": res.last_connect,
              "state": res.state, //게임 시작 버튼 클릭 여부
              "turn": res.turn //turn 체크
            };
          }).catch(e => {
          })

        if (user.state == true) { //새로고침에 true로 되어있으면 버튼 true로 보이게
            $('#btn-player1-start').removeClass('disabled');
            $('#btn-player1-start').removeClass('btn-warning');
            $('#btn-player1-start').addClass('btn-danger');
        }

        let player2 = "대기중";
        let flag = false;

        for (var i = 0; i < room.userList.length; i++) {
            if (room.userList[i].uuid != user.uuid) {
                player2 = room.userList[i].uuid;
            } else {
                flag = user.turn;
            }
        }

        $('#player2-name').text(player2);
        if (room.state !== true) {
            $('#btn-player1-start').css('display', 'block');
            $('#btn-player2-start').css('display', 'block');
        } else {
            checkUserTurn(flag)
        }
        console.log(user);
    })


    //상대방 입장
    socket.on('joinUser', function (userList) {
        let player2 = "";
        for (var i = 0; i < userList.length; i++) {
            if (userList[i].uuid != user.uuid) {
                player2 = userList[i].uuid;
                break;
            }
        }
        $('#player2-name').text(player2);
        $('#btn-player1-start').css('disply','block');
        $('#btn-player1-start').removeClass('disabled');
        $('#btn-player2-start').css('disply', 'block');
        $('#btn-player2-start').css('cursor', 'dafult');
    })


    //입장 Error Message
    socket.on('errorMessage', function () {
        alert("입장이 제대로 진행되지 않았습니다. 다시 입장해주세요.");
        location.href = "/";
    })


    //게임 시작
    socket.on('gameStart', function (turn, data) {
        console.log(turn);
        if (turn == 0) {
            $('#btn-player2-start').removeClass('btn-warning');
            $('#btn-player2-start').addClass('btn-danger');
            $('#btn-player2-start').removeClass('disabled');

            var clear = setTimeout(() => {
                console.log("------game start-------");
                $('#btn-player1-start').css('display', 'none');
                $('#btn-player2-start').css('display', 'none');
                $('#btn-give-up').css('display', 'block');
                $('#btn-leave-room').css('display', 'none');
            }, 500);

        } else {
            $('#btn-player1-start').css('display', 'none');
            $('#btn-player2-start').css('display', 'none');
        }

        var flag = true;

        data.forEach(function (user) {
            if (user.uuid == this.user.uuid) {
                flag = user.turn
            }
        })

        turn++;

        if (flag) {
            console.log("my turn")
            socket.emit('timeStart', user.connecting, turn)
        }

        checkUserTurn(flag)
    })


    //타이머 작동
    socket.on('timer', function (time) {
        $('#game-time').text(time + "초");
    })


    //턴 변경
    socket.on('turnout', function (data) {
        console.log("------turn change-------")
        //턴 바꾸는 emit 보내기
        var flag = true

        data.forEach(function (user) {
            if (user.uuid == this.user.uuid) {
                flag = user.turn
            }
        })

        if (flag) {
            socket.emit('turnChange', true)
        }
    })


    //게임 종료 : 총 플레이타임 시간 초과 
    socket.on('timeOver', function () {
        alert("총 플레이시간 초과\nplay 종료");
        socket.emit('timeStart', user.connecting, "", true);
    })


    //상대방 게임 포기 시 : 게임 진행 중
    socket.on('giveUpUserSuccess', function () {
        socket.emit('timeStart', user.connecting, "", true)
        alert("상대방이 게임을 포기하였습니다.");

        $('#btn-give-up').css('display', 'none');
        $('#btn-leave-room').css('display', 'block');

        // var clear = setTimeout(() => {
        //     location.reload();
        // }, 3000);
    });


    //상대가 방을 나갔을 때 : 게임 시작 전
    socket.on('leaveUserSuccess', function () {
        $('#player2-name').text('대기중');
        $('#btn-player1-start').addClass('disabled');
        $('#btn-player1-start').addClass('btn-warning');
        $('#btn-player1-start').removeClass('btn-danger');
        socket.emit('startState', false, user.connecting);
    })



    //에러 : 수정 필요
    socket.on('error', function (data) {
        alert(data.content);
        location.href = '/';
    })

    //********************************************************************************** */


    // 나가기 버튼
    $('#btn-leave-room').click(() => {
        if (confirm("방을 나가시겠습니까?")) {
            socket.emit("leaveRoom", user.connecting, "leave");
            location.href = "/";
        }
    });

    // 포기 버튼
    $('#btn-give-up').click(() => {
        if (confirm("게임을 포기하시면 패배로 처리됩니다\n게임을 포기하시겠습니까?")) {
            socket.emit("leaveRoom", user.connecting, "giveup");
            location.href = "/";
        }
    });


    //1번 플레이어 게임 시작 버튼
    $('#btn-player1-start').click(() => {
        socket.emit('startState', true, user.connecting);
        $('#btn-player1-start').removeClass('btn-warning');
        $('#btn-player1-start').addClass('btn-danger');
    });


    checkUserTurn = (flag) => {
        var names = $('.game-name');
        var names_text = names.find('span:eq(1)');

        if (flag) {
            names.each(function (e, el) {
                if (user.uuid == $(el).find('span:eq(1)').text()) {
                    $(el).css('border', '3px solid red')
                } else {
                    $(el).css('border', 'none')
                }
            })
            startTurn()
        } else {
            names.each(function (e, el) {
                if (user.uuid == $(el).find('span:eq(1)').text()) {
                    $(el).css('border', 'none')
                } else {
                    $(el).css('border', '3px solid red')
                }
            })
            endTurn()
        }
    }

    startTurn = () => {

        $(document).bind('keydown', function (event) {
            if (event.which === 37, 38, 39, 40 && pressNum < 2) { //37:왼,38:위,39:오,40:아래
                //api 실행
                // let result = "";
                // if(result == true){
                    pressNum++;
                // }else{
                //     socket.emit('turnChange', false)
                //     pressNum = 0;
                // }
            } else if (pressNum == 2) {
                //turnchange함수 실행
                socket.emit('turnChange', false)
                pressNum = 0;
            }
        })
    }

    endTurn = () => {
        $(document).unbind('keydown');
    }
});
