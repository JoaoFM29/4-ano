<template>
    <button class="custom-button2" @click="handleClick">
      <slot />
    </button>
  </template>
  
  <script>
  export default {
    name: "Button2",
    props: {
      onClick: {
        type: Function,
        default: null,
      },
    },
    methods: {
      handleClick(event) {
        if (this.onClick) {
          this.onClick(event);
        }
      },
    },
  };
  </script>
  
  <style scoped>
  .custom-button2 {
    padding: 10px 20px;
    font-size: 1rem;
    font-weight: bold;
    color: #000; 
    background-color: transparent; 
    border: 2px solid #000; 
    border-radius: 20px; 
    cursor: pointer;
    transition: all 0.3s ease; 
  }
  
  .custom-button2:hover {
    background-color: #000; 
    color: #fff;
  }
  </style>