<template>
    <button :style="buttonStyle" @click="toggleVideo" class="video-control">
      <span v-if="isPlaying">
        <font-awesome-icon icon="fa-solid fa-pause" />
      </span>
      <span v-else>
        <font-awesome-icon icon="play" />
      </span>
    </button>
  </template>
  

  <script>
  export default {
    name: "VideoControlButton",
    props: {
      bottom: {
        type: String,
        default: "15px", 
      },
      right: {
        type: String,
        default: "15px", 
      },
      isPlaying: {
        type: Boolean,
        required: true,
      },
    },
    emits: ["toggle"],
    computed: {
      buttonStyle() {
        return {
          position: "absolute",
          bottom: this.bottom,
          right: this.right,
          zIndex: 10,
          backgroundColor: "rgba(0, 0, 0, 0.5)",
          color: "white",
          border: "none",
          padding: "10px 15px",
          width: "40px",
          height: "40px",
          borderRadius: "50%",
          cursor: "pointer",
          fontSize: "1em",
          transition: "background-color 0.3s",
        };
      },
    },
    methods: {
      toggleVideo() {
        this.$emit("toggle");
      },
    },
  };
  </script>

<style>

.video-control:hover {
  background-color: rgba(0, 0, 0, 0.8) !important;
}

</style>
  