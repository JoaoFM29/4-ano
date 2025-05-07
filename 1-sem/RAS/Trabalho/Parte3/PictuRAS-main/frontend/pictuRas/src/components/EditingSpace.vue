<template>
  <div class="editing-space">
    <!-- Non-blocking Loading Spinner -->
    <div v-if="imageStore.previewMode" class="non-blocking-spinner">
      <div class="spinner"></div>
    </div>

    <div class="relative" id="first-relative">
      <div v-if="imageStore.selectedImage" class="image-preview" id="prev">
        <img :src="imageStore.selectedImage" alt="Selected Image" />
      </div>
      <div v-else class="placeholder" id="prev">
        <p>No image selected</p>
      </div>
      <ToolsList id="tools"></ToolsList>
    </div>
    <div class="relative" id="second-relative">
      <ParamsSelector v-if="imageStore.selectedImage" id="params"></ParamsSelector>
      <ProcessButtons id="submit-area" />
    </div>
  </div>
</template>


<script setup>
import { useImageStore } from '../stores/ImageStore';
import ParamsSelector from './ParamsSelector.vue';
import ProcessButtons from './ProcessButtons.vue'
import ToolsList from './ToolsList.vue';

const imageStore = useImageStore();
</script>

<style scoped>
/*
  .editing-space {
    background-color: #fff;
    display: grid;
    grid-template-areas:
      "prev tools"
      "params submit-area";
    grid-template-columns: 75% 25%;
    width: 100%;
    margin-top: 10%;
  }
 */

.editing-space {
  display: flex;
  flex-direction: column;
}

.relative {
  position: relative;
  width: 100%;
  display: flex;
}

#first-relative{
  justify-content: space-around;
  max-height: 60%;
  min-height: 60%;
  margin-top: 50px;
}

.image-preview,
.placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 76%;
  height: auto;
}

.image-preview img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}

.image-preview img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}

.placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 3rem;
  color: #999;
}

#tools {
  width: 15%;
  align-self: center;
}

#second-relative {
  flex-grow: 1;
  display: flex;
  overflow: hidden;
}

#params {
  width: 85%;
  position: relative;
  margin-top: 20px;
}

#submit-area {
  width: 15%;
  position: absolute;
  right: 3%;
}

.non-blocking-spinner {
  position: fixed;
  bottom: 20px; /* Position at the bottom-right corner */
  right: 20px;
  z-index: 9999; /* Keep it above other content */
  pointer-events: none; /* Allow clicks to pass through */
}

/* Spinner */
.spinner {
  border: 4px solid rgba(0, 0, 0, 0.1);
  border-top: 4px solid #3498db;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
}

/* Animation */
@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

</style>