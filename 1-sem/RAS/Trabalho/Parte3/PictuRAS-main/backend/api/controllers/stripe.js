const stripeService = require('../services/stripe');

class StripeController {
    async createPaymentIntent(req, res) {
        try {
            const { amount, currency, paymentMethods } = req.body;
    
            if (!amount) {
                return res.status(400).json({ error: 'Amount is required' });
            }
    
            const paymentIntent = await stripeService.createPaymentIntent(amount);
            
            res.json({
                clientSecret: paymentIntent.client_secret
            });
        } catch (error) {
            console.error('Payment Intent Error:', error);
            res.status(500).json({ error: error.message });
        }
    }

    async handleWebhook(req, res) {
        try {
            const sig = req.headers['stripe-signature'];
            const event = await stripeService.constructWebhookEvent(req.body, sig);

            // Handle different webhook events
            switch (event.type) {
                case 'payment_intent.succeeded':
                    const paymentIntent = event.data.object;
                    // Handle successful payment
                    console.log('Payment succeeded:', paymentIntent.id);
                    break;

                case 'payment_intent.payment_failed':
                    const failedPayment = event.data.object;
                    // Handle failed payment
                    console.log('Payment failed:', failedPayment.id);
                    break;

                default:
                    console.log(`Unhandled event type: ${event.type}`);
            }

            res.json({ received: true });
        } catch (error) {
            console.error('Webhook Error:', error);
            res.status(400).json({ error: error.message });
        }
    }
}

module.exports = new StripeController();