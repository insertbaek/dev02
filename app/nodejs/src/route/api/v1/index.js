const express = require('express');
const userRoute = require('./user.route');
const docsRoute = require('./docs.route');
const router = express.Router();

const defaultRoutes =
[
    {
        path: '/user',
        route: userRoute,
    },
    {
        path: '/docs',
        route: docsRoute,
    },
];
defaultRoutes.forEach((route) => {
    router.use(route.path, route.route);
});

module.exports = router;