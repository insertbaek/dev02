const ApiError = require('../utils/ApiError');
const catchAsync = require('../utils/catchAsync');
const createUser = catchAsync(async (req, res) => {
    res.status(201).send(user);
});

const getUsers = catchAsync(async (req, res) => {
    const result = {}
    res.send(result);
});

const getUser = catchAsync(async (req, res) => {
    const user = false;
    if (!user) {
        throw new ApiError(401, 'User not found');
    }
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