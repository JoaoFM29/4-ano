<!-- PaymentForm.vue -->
<template>
    <div class="payment-form">
        <div class="order-summary">
            <h3>Order Summary</h3>
            <div class="plan-details">
                <div class="selected-plan">
                    <span class="label">Selected Plan:</span>
                    <span class="value">{{ planName }}</span>
                </div>
                <div class="total-amount">
                    <span class="label">Total Amount:</span>
                    <span class="value">{{ amount.toFixed(2) }}€</span>
                </div>
            </div>
        </div>

        <div v-show="loading" class="loading">
            Loading payment form...
        </div>
        <div v-show="!loading">
            <form @submit.prevent="handleSubmit">
                <div ref="paymentElement" class="payment-element"></div>
                <LoadingButton :loading="processing" :disabled="!stripe || processing" class="pay-button">
                    Pay {{ amount.toFixed(2) }}€
                </LoadingButton>
                <div v-if="errorMessage" class="error-message">
                    {{ errorMessage }}
                </div>
            </form>
        </div>
    </div>
</template>

<script>
import { loadStripe } from '@stripe/stripe-js';
import LoadingButton from './LoadingButton.vue';
import { useStripeStore } from '../stores/StripeStore';

export default {
    name: 'PaymentForm',
    components: {
        LoadingButton
    },
    props: {
        amount: {
            type: Number,
            required: true
        },
        planName: {
            type: String,
            required: true
        },
        planId: {
            type: String,
            required: true
        }
    },
    data() {
        return {
            stripe: null,
            elements: null,
            loading: true,
            processing: false,
            errorMessage: '',
        };
    },
    async mounted() {
        const stripeStore = useStripeStore();
        try {
            this.stripe = await loadStripe('pk_test_51QgoxwFpyquVPMmLaU6S8izTAjKmlZNmlKaP1zoU4u3P1dcZwiHkc2ENEGyAJR8FrasD28ACG9lR53wdtMMLVHwn00e13yJ07b');
            const clientSecret = await stripeStore.createPaymentIntent(this.amount);

            this.elements = this.stripe.elements({
                clientSecret,
                appearance: {
                    theme: 'stripe',
                    variables: { colorPrimary: '#0066cc' },
                },
            });

            const paymentElement = this.elements.create('payment');
            paymentElement.mount(this.$refs.paymentElement);
            this.loading = false;
        } catch (error) {
            this.errorMessage = stripeStore.errorMessage;
            this.loading = false;
        }
    },
    methods: {
        async handleSubmit() {
            if (!this.stripe || !this.elements) {
                console.error('Stripe or elements not initialized');
                return;
            }

            this.processing = true;
            this.errorMessage = '';
            const stripeStore = useStripeStore();

            try {
                // First attempt the payment confirmation
                const { error } = await this.stripe.confirmPayment({
                    elements: this.elements,
                    redirect: 'if_required',
                    confirmParams: {
                        return_url: `${window.location.origin}/payment/result?planId=${this.planId}`,
                    },
                });

                if (error) {
                    console.error('Payment error:', error);
                    this.errorMessage = error.message;
                    this.$router.push('/payment/result?status=failure');
                    return;
                }

                // If we get here, payment was successful without redirect
                try {
                    console.log('Payment successful, updating plan:', this.planId);
                    stripeStore.setPlanID(this.planId);
                    await stripeStore.updateUserPlan();
                    this.$router.push('/payment/result?status=success');
                } catch (planError) {
                    console.error('Plan update error:', planError);
                    this.errorMessage = 'Payment succeeded, but plan update failed. Please contact support.';
                    this.$router.push('/payment/result?status=failure');
                }
            } catch (error) {
                console.error('Payment processing error:', error);
                this.errorMessage = 'Payment failed. Please try again.';
                this.$router.push('/payment/result?status=failure');
            } finally {
                this.processing = false;
            }
        },
    },
};
</script>

<style scoped>
.payment-form {
    width: 100%;
    max-width: 600px;
    margin: 0 auto;
}

.order-summary {
    background: #f8f9fa;
    border-radius: 8px;
    padding: 1.5rem;
    margin-bottom: 2rem;
}

.order-summary h3 {
    margin: 0 0 1rem;
    color: #333;
}

.plan-details {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
}

.selected-plan,
.total-amount {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.label {
    color: #666;
}

.value {
    font-weight: 600;
    color: #333;
}

.total-amount .value {
    color: #0066cc;
    font-size: 1.2rem;
}

.loading {
    text-align: center;
    padding: 2rem;
    color: #666;
}

.payment-element {
    margin-bottom: 1.5rem;
    padding: 1rem;
    border-radius: 8px;
    background: white;
}

.pay-button {
    width: 100%;
    padding: 0.75rem;
    background-color: #0066cc;
    color: white;
    border: none;
    border-radius: 4px;
    font-size: 1rem;
    cursor: pointer;
    transition: background-color 0.2s;
}

.pay-button:disabled {
    background-color: #ccc;
    cursor: not-allowed;
}

.error-message {
    margin-top: 1rem;
    padding: 0.75rem;
    border-radius: 4px;
    background-color: #fee2e2;
    color: #dc3545;
    text-align: center;
}
</style>