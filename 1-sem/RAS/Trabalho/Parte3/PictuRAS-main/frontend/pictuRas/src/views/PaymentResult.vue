<template>
  <div class="main-layout">
    <Navbar id="nav"></Navbar>
    <div class="payment-result">
      <div v-if="status === 'success'" class="payment-success">
        <h1>Payment Successful</h1>
        <p>Your transaction was successful. Thank you for your payment!</p>
        <button @click="goHome">Back to Profile Page</button>
      </div>

      <div v-if="status === 'failure'" class="payment-failure">
        <h1>Payment Failed</h1>
        <p>Unfortunately, your payment could not be processed. Please try again.</p>
        <button @click="retryPayment">Retry Payment</button>
      </div>
    </div>
  </div>
</template>

<script>
import Navbar from '../components/Navbar.vue';

export default {
  name: 'PaymentResult',
  components: {
    Navbar,
  },
  data() {
    return {
      status: 'pending', // status can be 'success', 'failure', or 'pending'
    };
  },
  mounted() {
    // Check the URL for the success or failure status
    const status = this.$route.query.status; // The status will come from the query params
    if (status === 'success') {
      this.status = 'success';
    } else if (status === 'failure') {
      this.status = 'failure';
    }
  },
  methods: {
    goHome() {
      this.$router.push('/profile'); // Redirect to profile page
    },
    retryPayment() {
      this.$router.push('/payment'); // Redirect to payment page to retry
    },
  },
};
</script>

<style scoped>
.main-layout {
  background-color: rgb(255, 255, 255);
}

.payment-result {
  width: 100%;
  display: flex;
  justify-content: center;
  margin-top: 10vh;
}

.payment-success,
.payment-failure {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 40px;
  padding: 20px;
  padding: 60px 100px;
  box-shadow: rgba(0, 0, 0, 0.25) 0px 54px 55px,
    rgba(0, 0, 0, 0.12) 0px -12px 30px,
    rgba(0, 0, 0, 0.12) 0px 4px 6px,
    rgba(0, 0, 0, 0.17) 0px 12px 13px,
    rgba(0, 0, 0, 0.09) 0px -3px 5px;
  border-radius: 20px;

}

.payment-success h1,
p,
.payment-failure h1,
p {
  margin: 0;
}

button {
  padding: 10px 20px;
  background-color: #0066cc;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #005bb5;
}
</style>