<template>
    <button
      :type="type"
      class="custom-button1"
      @click="onClick"
    >
      <span class="button-content1">{{ label }}</span>
    </button>
  </template>
  
<script>
  export default {
    name: "Button1",
    props: {
      type: {
        type: String,
        default: "button", 
      },
      label: {
        type: String,
        default: "", 
      },
    },
    emits: ["click"],
    methods: {
      onClick(event) {
        this.$emit("click", event); 
      },
    },
  };
</script>
  
<style scoped>
    .custom-button1 {
        position: relative;
        overflow: hidden;
        height: 3rem;
        padding: 0 3rem;
        border-radius: 1.5rem;
        background: #3d3a4e;
        background-size: 400%;
        color: #fff;
        border: none;
        cursor: pointer;
        margin-top: 2em;
    }
  
  
    .custom-button1:hover::before {
        transform: scaleX(1);
    }

    .button-content1 {
        position: relative;
        z-index: 1;
    }

    .custom-button1::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        transform: scaleX(0);
        transform-origin: 0 50%;
        width: 100%;
        height: inherit;
        border-radius: inherit;
        background: linear-gradient(90deg, #ff00ffcc, #ff6600c2, #ffcc00); 
        transition: all 0.475s;
    }
</style>
  