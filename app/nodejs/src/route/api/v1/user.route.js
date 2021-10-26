const express = require('express');
const router = express.Router();
const userController = require('../../../controller/user.controller');

router
    .route('/')
    .post(userController.createUser)
    .get(userController.getUsers);

router
    .route('/:userId')
    .get(userController.getUser)
    .patch(userController.updateUser)
    .delete(userController.deleteUser);

module.exports = router;