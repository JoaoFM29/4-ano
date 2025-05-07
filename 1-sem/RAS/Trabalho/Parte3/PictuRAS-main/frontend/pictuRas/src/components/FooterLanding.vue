<template>
    <footer v-show="showFooter" class="footer">
      <div class="footer-content">
        <img src="../assets/logo.png" alt="Logo" class="footer-logo" />
        <div class="footer-text">
          <h3>PictuRAS</h3>
          <p>
            Create incredible images, detailed drawings and spectacular art.
            Plans start at €15.00/month including VAT. Annual plan, charges
            months.
          </p>
        </div>
        <div class="footer-buttons">
            <Button1 @click="goProject" label="Start Now" />
        </div>
      </div>
    </footer>
  </template>
  
  <script>

    import Button1 from '../components/Button-style1.vue';
  export default {
    name: "Footer",
    components: {
        Button1,
    },
    props: {
      showFooter: {
        type: Boolean,
        required: true,
      },
    },

    method:{
      goProject() {
        this.$router.push(`/projects`);
      }
    }
  };
  </script>
  
  <style scoped>
  .footer {
    position: fixed;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 15vh;
    background-color: #000;
    color: white;
    box-shadow: 0 -4px 6px rgba(0, 0, 0, 0.1);
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 10px 20px;
    z-index: 1000; 
    transform: translateY(0); 
    transition: transform 0.3s ease-in-out;
  }
  
  .footer-content {
    display: flex;
    align-items: center;
    gap: 1rem;
    width: 70%;
  }
  
  .footer-logo {
    width: 50px;
    height: 50px;
    background-color: white;
    border-radius: 50%;
  }
  
  .footer-text {
    flex: 1;
  }
  
  .footer-text h3 {
    font-size: 1rem;
    font-weight: bold;
    margin-bottom: 5px;
  }
  
  .footer-text p {
    font-size: 0.9rem;
    line-height: 1.2;
  }
  
  .footer-buttons {
    display: flex;
    gap: 10px;
  }
  
  .footer-button {
    padding: 10px 15px;
    border: 2px solid white;
    border-radius: 20px;
    font-size: 0.9rem;
    cursor: pointer;
    transition: all 0.3s ease;
  }
  
  .footer-button.outline {
    background-color: transparent;
    color: white;
  }
  
  .footer-button.outline:hover {
    background-color: white;
    color: black;
  }
  
  .footer-button.primary {
    background-color: #007bff;
    color: white;
    border: none;
  }
  
  .footer-button.primary:hover {
    background-color: #0056b3;
  }
  </style>
  