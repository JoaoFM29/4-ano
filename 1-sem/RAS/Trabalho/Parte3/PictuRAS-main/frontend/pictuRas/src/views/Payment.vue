<template>
    <div class="main-layout">
        <Navbar id="nav"></Navbar>
        <div class="payment-container">
            <img src="../assets/logo.png" >
            <h2>Complete Your Payment</h2>
            <PaymentForm :amount="amount" :planName="planName" :planId="planId"/>
        </div>
    </div>
</template>

<script>
import Navbar from '../components/Navbar.vue';
import PaymentForm from '../components/PaymentForm.vue';

export default {
    name: 'Payment',
    components: {
        Navbar,
        PaymentForm
    },
    data() {
        return {
            amount: parseFloat(this.$route.query.amount) || 0,
            planName: this.$route.query.planName || '',
            planId: this.$route.query.planId || ''
        };
    },
    created() {
    }
};
</script>   

<style scoped>
.main-layout {
    background-color: rgb(255, 255, 255);
}

.payment-container {
    max-width: 600px;
    margin: 2rem auto;
    padding: 2rem;
    box-shadow: rgba(0, 0, 0, 0.25) 0px 54px 55px, 
                 rgba(0, 0, 0, 0.12) 0px -12px 30px, 
                 rgba(0, 0, 0, 0.12) 0px 4px 6px, 
                 rgba(0, 0, 0, 0.17) 0px 12px 13px, 
                 rgba(0, 0, 0, 0.09) 0px -3px 5px;
    border-radius: 8px;
    display: flex;
    flex-direction: column;
    align-items: center;
}

.payment-container img{
    width: 100px;
    margin-bottom: 2rem;
}

h2 {
    text-align: center;
    margin-bottom: 2rem;
    color: #333;
}
</style>