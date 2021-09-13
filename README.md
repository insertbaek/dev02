개발연구소 2연구소 공통 연구과제

1. 서버구성
 - OS
  CentOS 7 64bit

 - APP
   apache
   Python 3.9.6
   node.js 14.17.6
   MySQL 8.0.25

 - WAS
   HOME : /home/dev02.01/public
   GIT HOME : /home/dev02.01
   www : 192.168.56.14

 - 접속정보
   os : root / dkdldpadkdl
   mysql root : root / dkdldpadkdl
   mysql user : dev02 / IBqwe123!@# / 192.168.56.14

2. 개발환경
 - ssh-keygen (box)
   root@ib-dev02> ssh-keygen (실행 후 입력 없이 모두 엔터)
   root@ib-dev02> cat ~/.ssh/id_rsa.pub (현재 초기설정에 의한 파일 존재하므로 덮어쓰기 선택, 결과 복사 후 메신저로 전달)

 - ssh-keygen (desktop)
   git-bash.exe 실행 (윈도우 검색 선택 후 "git-bash" 검색)
   cd .ssh
   ssh-keygen -t rsa -b 4096
   cat id_rsa.pub
   내용 복사 후 메신저
