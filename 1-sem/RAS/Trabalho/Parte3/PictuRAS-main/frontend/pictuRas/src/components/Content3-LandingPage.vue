<template>
    <div class="content3-layout">
      <div class="content3-wrapper">
        <img src="../assets/logo.png" alt="Logo" class="content3-logo" />
        <h2 class="content3-title">Need a quick edit?</h2>
        <h3 class="content3-subtitle">We provide advanced tools to make your life easier.</h3>
        <p class="content3-description">
          Explore the latest tools for cropping, resizing, and customizing images.
          Create unique and stunning designs easily and quickly.
        </p>
        <Button2 :onClick="myFunction">See all resources</Button2>
      </div>
    </div>
  </template>
  
  <script>
  import Button2 from './Button-style2.vue';
  
  export default {
    name: 'Content3',
    components: { Button2 },
    methods: {
      myFunction() {
        console.log('See all resources clicked!');
      },
    },
  };
  </script>
  

  <style scoped>

  /* Content 3 */

.content3-layout {
    background-color: rgba(255, 174, 0, 0.534);
    background: linear-gradient(90deg, #ff00ffcc, #ff6600c2, #ffcc00); 
    display: flex;
    justify-content: center;
    align-items: center;
    height: 60vh;
    font-family: 'Adobe Clean', adobe-clean, 'Trebuchet MS', sans-serif;
  }

.content3-wrapper {
  text-align: center;
  width: 70%;
  height: 70%;
  margin: auto;
}

.content3-logo {
  width: 80px;
  height: 80px;
  margin-bottom: 1rem;
}

.content3-title {
  font-size: 2rem;
  font-weight: bold;
  margin-bottom: 0.5rem;
}

.content3-subtitle {
  font-size: 1.5rem;
  margin-bottom: 1rem;
  font-weight: bold;
  font-weight: 400;
}

.content3-description {
  font-size: 1rem;
  margin-bottom: 4rem;
  line-height: 1.5;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
}
</style>