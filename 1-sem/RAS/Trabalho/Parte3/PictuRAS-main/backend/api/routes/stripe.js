const express = require('express');
const StripeController = require('../controllers/stripe.js');
const router = express.Router();

// Route for creating a payment intent
router.post('/create-payment-intent', StripeController.createPaymentIntent);

// Route for handling Stripe webhooks
router.post('/webhook', express.raw({ type: 'application/json' }), StripeController.handleWebhook);

module.exports = router;