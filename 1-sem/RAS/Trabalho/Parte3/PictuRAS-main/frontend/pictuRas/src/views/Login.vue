<template>
  <div class="login-layout">

    <!-- navbar  -->
    <Navbar id="nav"></Navbar>

    <!-- Login  -->
    <div class="login-container">
      <div class="login-box">
        <img src="../assets/logo.png" alt="Logo" class="login-logo" />
        <form @submit.prevent="handleLogin" class="login-form-group ">
          <Inputs
            id="email"
            type="email"
            placeholder="Email"
            v-model="email"
            required
          />
          <Inputs
            id="password"
            type="password"
            placeholder="Password"
            v-model="password"
            required
          />
          <Button1 type="submit" label="Login" />
        </form>

        <!-- Links para Forget Password e Sign Up -->
        <div class="login-links">
          <a href="/forgot-password" class="link">Forgot Password?</a>
          <a href="/register" class="link">Sign Up</a>
        </div>

        <!-- <GoogleButton label="Continue with Google" /> -->
      </div>
    </div>
  </div>


</template>


 <!-- Logic--> 
<script>
  import Navbar from '../components/Navbar.vue';
  import Inputs from "../components/Inputs.vue";
  import Button1 from "../components/Button-style1.vue";
  import GoogleButton from "../components/GoogleButton.vue"; 
  import Toastify from "toastify-js";
  import "toastify-js/src/toastify.css";
  import axios from 'axios';
  const api = import.meta.env.VITE_API_GATEWAY;

  export default {
    name: 'Login',
    components: {
        Navbar,
        Inputs,
        Button1,
        GoogleButton,
    },
    data() {
    return {
      email: "",
      password: "",
    };
  },
  methods: {
    async sendLogin(){
      try{
            const possibleUser = {
            username:this.email,
            password: this.password
          };
            const response = await axios.post(`${api}/api/login`,possibleUser, {
                  withCredentials: true, // Ensure credentials are sent with the request
                });
                this.$router.push('/projects'); // Navigate to the projects page
          }catch(e){
              alert("Password or username is incorrect")
          }

    },
    async handleLogin() {

      if (!this.email || !this.password) {
                Toastify({
                    text: '⚠️ Please fill in all required fields!',
                    duration: 3000, 
                    close: true,
                    gravity: "bottom",
                    position: "right", 
                    backgroundColor: "White", 
                    stopOnFocus: true, 
                    style:{
                        fontWeight: "bold",
                        boxShadow: "0px 4px 6px rgba(0, 0, 0, 0.3)",
                        color: "black",
                    }
                }).showToast();
                return;
            }
            await this.sendLogin();
      
    },
  },
  };
</script>



<!-- CSS-->
<style scoped>

.login-layout{
  max-height: 100%;
  overflow: hidden;
}

.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f7f7f7;
}

.login-box {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: rgba(0, 0, 0, 0.25) 0px 54px 55px, rgba(0, 0, 0, 0.12) 0px -12px 30px, rgba(0, 0, 0, 0.12) 0px 4px 6px, rgba(0, 0, 0, 0.17) 0px 12px 13px, rgba(0, 0, 0, 0.09) 0px -3px 5px;
  text-align: center;
  width: 100%;
  max-width: 400px;
  height: 60%;
}

.login-logo {
  max-width: 200px;
  margin-bottom: 1rem;
}

.login-form-group {
  margin-bottom: 2rem;
}

.login-links {
  margin-top: 1rem;
  align-self: center;
  justify-self: center;
  display: flex;
  width: 80%;
  margin-bottom: 2em;
  justify-content: space-between;
  margin-left: auto;
  margin-right: auto;
  padding-right: 2em;
}


.link {
  position: relative;
  text-decoration: none;
  color: black; /* Remove a cor azul dos links */
  font-size: 0.9rem;
  font-weight: 500;
  overflow: hidden;
}

.link::after {
  content: '';
  position: absolute;
  left: 0;
  bottom: 0;
  width: 0;
  height: 2px;
  background-color: black;
  transition: width 0.5s ease;
}

.link:hover::after {
  width: 100%; /* Aumenta a largura do sublinhado ao passar o mouse */
}


</style>