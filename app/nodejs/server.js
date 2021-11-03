// modules init
const express = require('express');
const app = express();
const http = require('http').createServer(app);
const { io } = require('./src/socket');
const os = require('os');
const routes = require('./src/route/api/v1');

io.attach(http);

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


