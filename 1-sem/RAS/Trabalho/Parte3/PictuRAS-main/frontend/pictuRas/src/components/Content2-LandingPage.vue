<template>
    <div class="content2-layout">
      <div class="content2-wrapper">
        <!-- Conteúdo da coluna esquerda -->
        <div class="left2-column">
          <div class="video2-container">
            <video ref="videoElement" class="video-bg2" autoplay muted loop playsinline>
              <source src="../assets/RecorteImagem.mp4" type="video/mp4" />
              Your browser does not support the video element.
            </video>
            <VideoControlButton
            :isPlaying="isPlaying"
            :bottom="'15px'"
            :right="'85%'"
            @toggle="emitToggleVideo"
          />
          </div>
        </div>
  
        <!-- Conteúdo da coluna direita -->
        <div class="right2-column">
          <p class="p2">Crop image</p>
          <h2 class="title2">Make instant edits</h2>
          <p class="p21">
            Discover advanced tools to precisely crop, adjust, and transform images.
            Experience quick and efficient edits, leaving your photos exactly how you imagined them.
          </p>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import VideoControlButton from './VideoControlButton.vue';
  
  export default {
    name: 'Content2',
    components: { VideoControlButton },
    props: {
      isPlaying: Boolean,
    },
    emits: ['toggleVideo'],
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
    },
  };
  </script>

<style scoped>

.content2-layout {
    background-color: rgba(170, 170, 170, 0.534);
    display: flex;
    justify-content: center;
    align-items: center;
    grid-template-columns: 50% 50%;
    height: 80vh;
  }

  .content2-wrapper {
  display: grid;
  grid-template-columns: 40% 60%; 
  width: 70%; 
  height: 100%; 
 
}

.left2-column,
.right2-column {
  display: flex;
  align-items: center; 
  justify-content: center; 
  padding: 1rem; 
}


.left2-column {
    display: flex;
    align-items: center;
    justify-content: end;
    position: relative; 
    
}

.video-bg2 {
    top: 0;
    left: 0; 
}

.video2-container {
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    width: auto; 
    height: auto; 
}

.right2-column{
    display: flex;
    flex-direction: column;
    align-items: start;
    justify-content: start;
    height: 30%;
    margin: auto;
    text-align: start;
    width: 70%;
}

.p2{
    font-weight: 700;
    text-transform: uppercase;
    font-family: 'Adobe Clean', adobe-clean, 'Trebuchet MS', sans-serif;
    font-size: 12px;
}

.title2{
    font-size: 33px;
    font-family: 'Adobe Clean', adobe-clean, 'Trebuchet MS', sans-serif;
    line-height: 35px;
    margin-bottom: 1em;

}

.p21{
    word-wrap: break-word;
    text-align: justify;
    font-size: 16px;
    font-weight: 70;
}
    
</style>
  