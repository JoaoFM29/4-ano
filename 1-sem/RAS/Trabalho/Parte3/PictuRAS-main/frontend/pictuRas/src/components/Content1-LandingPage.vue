<template>
  <div class="content1-layout" ref="content1">

    <!-- Coluna da Esquerda -->
    <div class="left1-column">
      <div class="content1-wrapper">
        <div class="logo1-container">
          <img src="../assets/logo.png" alt="Logo" class="logo1" />
          <span class="app-name">PictuRAS</span>
        </div>
        <h1 class="title">Edit at the speed of your imagination</h1>
        <p class="description">
          Give wings to your creativity with the most advanced image editing app ever made.
          Transform your photos with a single click and achieve stunning, professional-level results.
        </p>
        <p>
          Start now for free and explore premium features at an unbeatable price. Unlock your full
          creative potential with PictuRAS for only €15.00/month (VAT included). Let your imagination
          lead the way. Terms apply.
        </p>
        <Button1 @click="goProject" label="Start Now" />
      </div>
    </div>

    <!-- Coluna da Direita -->
    <div class="right1-column">
      <video
        ref="videoElement"
        class="video-bg"
        :autoplay="isPlaying"
        :loop="true"
        :muted="true"
        playsinline
        @play="handlePlay"
        @pause="handlePause"
      >
        <source src="../assets/VideoLanding.mp4" type="video/mp4" />
        Your browser does not support the video element.
      </video>
      <VideoControlButton
        :isPlaying="isPlaying"
        :bottom="'20px'"
        :right="'20px'"
        @toggle="emitToggleVideo"
      />
    </div>
  </div>
</template>

<script>
import Button1 from './Button-style1.vue';
import VideoControlButton from './VideoControlButton.vue';

export default {
  name: 'Content1',
  components: { Button1, VideoControlButton },
  props: {
    isPlaying: {
      type: Boolean,
      required: true,
    },
  },
  emits: ['toggleVideo', 'content1Visible'],
  mounted() {
    window.addEventListener('scroll', this.checkVisibility);
  },
  beforeDestroy() {
    window.removeEventListener('scroll', this.checkVisibility);
  },
  methods: {
    emitToggleVideo() {
      const video = this.$refs.videoElement;

      // Toggle play/pause state for the video
      if (this.isPlaying) {
        video.pause();
      } else {
        video.play();
      }

      // Emit event to notify parent
      this.$emit('toggleVideo');
    },

    checkVisibility() {
      const rect = this.$refs.content1.getBoundingClientRect();
      const isVisible = rect.bottom > 0;
      this.$emit('content1Visible', isVisible);
    },
    goProject() {

        this.$router.push(`/projects`);

    }
  },
};
</script>


<style scoped>

.content1-layout {
    grid-area: content;
    display: grid;
    grid-template-columns: 50% 50%; 
    height: 80vh;
  }

  .left1-column {
      padding: 1rem;
      display: flex;
      align-items:center;
      justify-content: right;
  }

  .content1-wrapper {
    margin-right: 18%;
    max-width: 55%; 
    text-align: justify;
}


.content1-wrapper p{
  text-align: justify;
}

.logo1-container {
    display: flex;
    align-items: center; 
    margin-bottom: 1rem;
}

.logo1 {
    width: 50px;
    height: 50px; 
    margin-right: 1rem; 
}

.app-name {
    font-size: 1.2rem;
    font-weight: bold;
    color: #333;
}


.title {
    font-size: 2rem;
    font-weight: bold;
    margin-bottom: 1rem;
    color: #333;
    font-family:Verdana, Geneva, Tahoma, sans-serif;
    background: linear-gradient(
        82.3deg,
        #000000 0%, 
        #ff00ff8e 24.8%,
        #ff660093 50.3%,
        #ffcc00bd 80%
    );
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent; 
    background-clip: text; 
    
}

.right1-column {
    background-color: #fff; 
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative; 
}

.video-bg {
    width: 100%;
    height: 100%;
    object-fit: cover; 
    top: 0;
    left: 0;
}
</style>
  