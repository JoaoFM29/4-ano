const express = require('express');

const rawBodyMiddleware = express.raw({ type: 'application/json' });

const validateWebhook = (req, res, next) => {
    if (req.headers['stripe-signature']) {
        return next();
    }
    res.status(400).json({ error: 'Invalid webhook signature' });
};

module.exports = {
    rawBodyMiddleware,
    validateWebhook
};