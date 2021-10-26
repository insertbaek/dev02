const ApiError = require('../utils/ApiError');
const catchAsync = require('../utils/catchAsync');
const createUser = catchAsync(async (req, res) => {
    //req.body -> post 등 방식 데이터 가져오기
    console.log(req.body)
    res.status(201).send(user);
});

const getUsers = catchAsync(async (req, res) => {
    //req.query -> get 방식 데이터 가져오기
    console.log(req.query)
    const result = {}
    res.send(result);
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