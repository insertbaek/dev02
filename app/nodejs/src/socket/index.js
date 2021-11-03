const { mazeNSSocket } = require('./maze.socket2');
const io = require('socket.io')({
    cors: {
        origin: 'http://localhost:3000',
        methods: ['GET', 'POST'],
        allowedHeaders: ['my-custom-header'],
        credentials: true,
    },
    pingInterval: 10000,
    pingTimeout: 5000,
});
const mazeNs = io.of('/maze'); //mazeNamespace

mazeNs.on('connection', (socket) => {
    mazeNSSocket(io, mazeNs, socket)
});

module.exports = { io };