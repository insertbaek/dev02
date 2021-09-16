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
	console.log('Connected at 3000');
});

io.on('connection', (socket)=>{
    socket.on('request_message', (msg) => {
        io.emit('response_message', msg);
    });

    socket.on('disconnect', async () => {
        console.log('user disconnected');
    });
});

var os = require('os');

  

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

  

console.log(getServerIp());