const ApiError = require('../utils/ApiError');
const catchAsync = require('../utils/catchAsync');

var ROOT_DIR = "/DEV02";
var APP_DIR = ROOT_DIR + "/app";
var ROUTE_DIR = APP_DIR + "/python/route";

const createUser = catchAsync(async (req, res) => {
    //req.body -> post 방식 데이터 가져오기
    const spawn = require('child_process').spawn;
    const python = spawn('python', [ROUTE_DIR+'/route.py',Object.values(req.body)]);
    python.stdout.on('data', function(pythonResult){
        let returnStr = pythonResult.toString('utf-8');
        console.log(returnStr)
        res.status(201).send(pythonResult.toString());
    });
});

const getUsers = catchAsync(async (req, res) => {
    //req.query -> get 방식 데이터 가져오기
    const spawn = require('child_process').spawn;
    const python = spawn('python', [ROUTE_DIR+'/route.py',Object.values(req.query)]);
    python.stdout.on('data', function(pythonResult){
        let returnStr = pythonResult.toString('utf-8');
        console.log(returnStr)
        res.status(201).send(pythonResult.toString());
    });
});

const getUser = catchAsync(async (req, res) => {
    //req.params.parm -> url param 데이터 가져오기
    const user = {};
    // if (!user) {
    //     throw new ApiError(401, 'User not found');
    // }
    console.log(req.params.userId)
    res.send(user);
});

const updateUser = catchAsync(async (req, res) => {
    const user = {};
    res.send(user);
});

const deleteUser = catchAsync(async (req, res) => {

    res.status(200).send();
});

module.exports = {
    createUser,
    getUsers,
    getUser,
    updateUser,
    deleteUser,
};