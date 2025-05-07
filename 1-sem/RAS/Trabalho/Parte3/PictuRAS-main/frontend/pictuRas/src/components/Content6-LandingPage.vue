<template>
    <div class="Content6-layout" ref="content6">
      <div class="promotion-content">
        <!-- Logo -->
        <img src="../assets/logo.png" alt="Logo" class="promotion-logo" />
        <!-- Title -->
        <h2 class="promotion-title">PictuRAS</h2>
        <!-- Subtitle -->
        <h3 class="promotion-subtitle">Start with PictuRAS. Finish with something extraordinary.</h3>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: "Content6",
    emits: ['content6Visible'],
    mounted() {
      
      this.$nextTick(() => {
        if (this.$refs.content6) {
          window.addEventListener("scroll", this.checkVisibility);
          this.checkVisibility(); 
        }
      });
    },
    beforeDestroy() {
        window.removeEventListener('scroll', this.checkVisibility);
    },
    methods:{
        checkVisibility() {
            const rect = this.$refs.content6.getBoundingClientRect();
            const isVisible = rect.bottom > 0;
            this.$emit('content6Visible', isVisible);
        },
    },
  };
  </script>
  
  <style scoped>
  .Content6-layout{
    background-color: #222;
    color: white;
    padding: 2rem;
    text-align: center;
    border-radius: 10px;
    width: 100%;
    height: 30vh;
    padding-bottom: 5vh;
    margin: 2rem auto;
    font-family: Arial, Helvetica, sans-serif;
  }
  
  .promotion-content {
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  
  .promotion-logo {
    width: 60px;
    height: 60px;
    margin-bottom: 1rem;
    background-color: white;
    border-radius: 50%;
  }
  
  .promotion-title {
    font-size: 1.5rem;
    font-weight: bold;
    margin-bottom: 0.5rem;
  }
  
  .promotion-subtitle {
    font-size: 1.2rem;
    font-weight: bold;
    margin-bottom: 1rem;
  }
  
  .promotion-description {
    font-size: 1rem;
    line-height: 1.5;
    margin-bottom: 1rem;
    max-width: 500px;
  }
  
  .promotion-pricing {
    font-size: 0.9rem;
    font-weight: 700;
    margin-bottom: 1.5rem;
  }
  
  .promotion-buttons {
    display: flex;
    gap: 1rem;
  }
  
  .promotion-button {
    padding: 0.8rem 1.5rem;
    border-radius: 20px;
    font-size: 0.9rem;
    cursor: pointer;
    transition: all 0.3s ease;
  }
  
  .promotion-button.outline {
    background-color: transparent;
    color: white;
    border: 2px solid white;
  }
  
  .promotion-button.outline:hover {
    background-color: white;
    color: #222;
  }
  
  .promotion-button.primary {
    background-color: #007bff;
    color: white;
    border: none;
  }
  
  .promotion-button.primary:hover {
    background-color: #0056b3;
  }
  </style>
  