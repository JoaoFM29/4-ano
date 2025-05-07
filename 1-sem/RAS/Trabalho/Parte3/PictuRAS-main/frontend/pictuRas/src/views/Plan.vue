<template>
    <div class="plan-layout">
        <Navbar id="nav"></Navbar>

        <div class="plan-container">
            <div v-for="plan in plans" :key="plan.name" class="plan-box"
                :class="{ active: isCurrentPlan(plan.id), [`${plan.type}-plan`]: true }">

                <h2>{{ plan.name }}</h2>
                <ul>
                    <li>Price: {{ plan.price }} €</li>
                    <li>Type: {{ plan.type }}</li>
                </ul>
                <h3>{{ plan.price }} €</h3>

                <div v-if="isCurrentPlan(plan.id)">
                    <button disabled>Current Plan</button>
                </div>
                <button v-else-if="plan.name === 'free'" @click="cancelPlan(plan.name, plan.price, plan.type, plan.id)"
                    :class="`${plan.type}-plan-btn`">
                    Cancel Subscription
                </button>
                <button v-else @click="choosePlan(plan.name, plan.price, plan.type, plan.id)"
                    :class="`${plan.type}-plan-btn`">
                    Proceed to payment →
                </button>
            </div>
        </div>
    </div>
</template>

<script>
import Navbar from '../components/Navbar.vue';
import axios from 'axios';
import { useStripeStore } from '../stores/StripeStore';

export default {
    name: 'Plan',
    components: {
        Navbar
    },
    data() {
        return {
            plans: [], // Store fetched plans here
            currentUserPlanId: null
        };
    },
    methods: {
        isCurrentPlan(planId) {
            return this.currentUserPlanId === planId;
        },
        choosePlan(plan, amount, planType, planId) {
            this.$router.push({
                path: '/payment',
                query: {
                    amount: amount,
                    planName: plan,
                    planId: planId
                }
            });
        },
        async cancelPlan(plan, amount, planType, planId) {
            const stripeStore = useStripeStore();
            try {
                stripeStore.setPlanID(planId);
                await stripeStore.updateUserPlan();
                alert('Subscription cancelled successfully');
                window.location.reload();
            } catch (error) {
                console.error('Error cancelling plan susbcription:', error);
            }
        },
        async fetchPlans() {
            try {
                const response = await axios.get(`${import.meta.env.VITE_API_GATEWAY}/api/plans`, {
                    withCredentials: true
                });
                this.plans = response.data;
            } catch (error) {
                console.error('Error fetching plans:', error);
            }
        },
        async getCurrentPlan() {
            const stripeStore = useStripeStore();
            try {
                this.currentUserPlanId = await stripeStore.getUserPlan();
            } catch (error) {
                console.error('Error getting current plan:', error);
                this.currentUserPlanId = null;
            }
        }
    },
    created() {
        this.fetchPlans(); // Fetch plans when the component is created
        this.getCurrentPlan(); // Get the current user's plan
    }
};
</script>

<style scoped>
.plan-container {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 20px;
    justify-items: center;
    padding: 2rem;
}

.plan-box {
    background: white;
    padding: 2rem;
    border-radius: 8px;
    box-shadow: rgba(0, 0, 0, 0.25) 0px 4px 6px;
    text-align: center;
    width: 300px;
    height: 350px;
    transition: transform 0.3s ease;
}

/* Plan type styles */
.free-plan h2,
.free-plan h3,
.free-plan button {
    color: #007bff;
    /* Blue */
}

.monthly-plan h2,
.monthly-plan h3,
.monthly-plan button {
    color: #8a2be2;
    /* Purple */
}

.annual-plan h2,
.annual-plan h3,
.annual-plan button {
    color: #d415cb;
    /* Pink */
}

.daily-plan h2,
.daily-plan h3,
.daily-plan button {
    color: #451e43;
    /* Pink */
}

.plan-box h2 {
    font-size: 1.5rem;
    margin-bottom: 1rem;
}

.plan-box ul {
    list-style-type: none;
    padding: 0;
    margin-bottom: 1rem;
}

.plan-box ul li {
    margin: 0.5rem 0;
}

.plan-box button {
    color: white;
    padding: 0.5rem 1rem;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.3s ease;
}

.free-plan-btn {
    background-color: #007bff;
    /* Blue for free plan */
}

.monthly-plan-btn {
    background-color: #8a2be2;
    /* Purple for monthly plan */
}

.annual-plan-btn {
    background-color: #d415cb;
    /* Pink for annual plan */
}

.daily-plan-btn {
    background-color: #451e43;
    /* Pink for annual plan */
}

.plan-box button:hover {
    background-color: #0056b3;
    /* Darker blue on hover */
}

.plan-box button[disabled] {
    background-color: #d3d3d3;
    cursor: not-allowed;
}

.plan-box.active {
    background-color: #e3f2fd;
    /* Light blue for active plan */
}

.free-plan.active {
    background-color: #d0e7ff;
    /* Light blue */
}

.monthly-plan.active {
    background-color: #d6bbe4;
    /* Light purple */
}

.annual-plan.active {
    background-color: #fcbade;
    /* Light pink */
}

.daily-plan.active {
    background-color: #b88fa5;
    /* Light pink */
}
</style>
