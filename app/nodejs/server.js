<<<<<<< HEAD
// module init
const app = require('express')();
const http = require('http').createServer(app);
const io = require('socket.io')(http);

// variable init
const ROOT_DIR = "/home/dev02.01";
const APP_DIR = ROOT_DIR + "/app";
const PYTHON_DIR = APP_DIR + "/python";
const NODEJS_DIR = APP_DIR + "/nodejs";
const PUBLIC_DIR = ROOT_DIR + "/public";

/* nodejs -> python */
const spawn = require('child_process').spawn;
const exec = require('child_process').exec;
const python = spawn('python', [PYTHON_DIR + '/welcome.py']);
python.stdout.on('data', (data) => {
	let returnStr = data.toString('utf-8');
	console.log(returnStr)
});
/* nodejs -> python */

app.get('/', (req, res) => {
	res.sendFile(PUBLIC_DIR + '/index.html');
});

http.listen(3000, () => {
	console.log('Connected at 3000')
});

io.on('connection', (socket)=>{
    socket.on('request_message', (msg) => {
        io.emit('response_message', msg);
    });

    socket.on('disconnect', async () => {
        console.log('user disconnected');
    });
});

=======
// modules init
const app = require('express')();
const http = require('http').createServer(app);
const io = require('socket.io')(http);

// variables init
const ROOT_DIR = "/home/dev02.01";
const APP_DIR = ROOT_DIR + "/app";
const PYTHON_DIR = APP_DIR + "/python";
const NODEJS_DIR = APP_DIR + "/nodejs";
const PUBLIC_DIR = ROOT_DIR + "/public";

/* nodejs -> python */
const spawn = require('child_process').spawn;
const exec = require('child_process').exec;
const python = spawn('python', [PYTHON_DIR + '/welcome.py']);
python.stdout.on('data', (data) => {
	let returnStr = data.toString('utf-8');
	console.log(returnStr)
});
/* nodejs -> python */

app.get('/', (req, res) => {
	res.sendFile(PUBLIC_DIR + '/index.html');
});

http.listen(3000, () => {
	console.log('Connected at 3000')
});

io.on('connection', (socket)=>{
    socket.on('request_message', (msg) => {
        io.emit('response_message', msg);
    });

    socket.on('disconnect', async () => {
        console.log('user disconnected');
    });
});

>>>>>>> 29beadbb8d335074f508f9ad26e3d734ac67bfe5
