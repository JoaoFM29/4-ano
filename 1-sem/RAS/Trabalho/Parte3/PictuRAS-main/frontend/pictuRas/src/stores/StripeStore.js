import { defineStore } from 'pinia';
import axios from 'axios';

const api = import.meta.env.VITE_API_GATEWAY;

export const useStripeStore = defineStore('stripe', {
    state: () => ({
        clientSecret: '',
        errorMessage: '',
        planID: '',
    }),
    actions: {
        async createPaymentIntent(amount) {
            try {
                const response = await axios.post(`${api}/api/create-payment-intent`, {
                    amount: Math.round(amount * 100),
                });

                this.clientSecret = response.data.clientSecret;
                return this.clientSecret;
            } catch (error) {
                console.error('Error creating payment intent:', error);
                this.errorMessage = 'Failed to initialize payment: ' + error.message;
                throw error;
            }
        },
        setPlanID(planID) {
            this.planID = planID;
        },
        async updateUserPlan() {
            try {
                const response = await axios.put(
                    `${api}/api/user/plan`,
                    { plan: this.planID },
                    {
                        withCredentials: true  
                    }
                );
                return response.data;
            } catch (error) {
                console.error('Error updating user plan:', error);
                throw new Error('Failed to update user plan');
            }
        },
        async getUserPlan() {
            try {
                const response = await axios.get(`${api}/api/profile`,{ withCredentials: true } );
                return response.data.plan;
            } catch (error) {
                console.error('Error getting user plan:', error);
                throw new Error('Failed to get user plan');
            }
        }
    },
});
