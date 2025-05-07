<template>
  <div class="wrapper">
    <div class="image-list">
      <div
        v-for="(image, index) in imageStore.images"
        :key="index"
        :class="['image-thumbnail', deleteMode && selectedForDeletion.includes(index) ? 'selected' : '']"
        @click="deleteMode ? toggleImageSelection(index) : selectImage(image)"
      >
        <img :src="image" alt="Thumbnail" />
      </div>

      <!-- Gray effect and loading spinner -->
      <div v-show="imageStore.onProcess" class="overlay">
        <div class="spinner"></div>
      </div>
    </div>

    <div class="btn-flex">
      <button @click="triggerFileUpload">Upload</button>
      <input
        type="file"
        ref="fileInput"
        @change="handleFileUpload"
        accept="image/*,application/zip"
        multiple
        style="display: none"
      />
      <button @click="downloadAllImagesAsZip()">Download</button>
      <button @click="toggleDeleteMode()" :class="{ active: deleteMode }">
        {{ deleteMode ? "Confirm Delete" : "Delete" }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'; // Import ref
import { useImageStore } from '../stores/ImageStore';
import { useProjectStore } from '../stores/ProjectStore';
import axios from 'axios';
import JSZip from 'jszip';

const api = import.meta.env.VITE_API_GATEWAY;

// Access the store
const imageStore = useImageStore();
const projectStore = useProjectStore();

// File input reference
const fileInput = ref(null);

// Delete mode state and selected indexes for deletion
const deleteMode = ref(false);
const selectedForDeletion = ref([]);

// Select an image using the store's action
function selectImage(image) {
  imageStore.selectImage(image);
}

// Trigger file input click
function triggerFileUpload() {
  fileInput.value.click();
}

// Handle file upload
async function handleFileUpload(event) {
  const files = Array.from(event.target.files);

  // Separate valid image files and ZIP files
  const validImageFiles = files.filter((file) => file.type.startsWith("image/"));
  const zipFiles = files.filter((file) => file.type === "application/zip");

  // Check if there are any invalid files
  if (validImageFiles.length + zipFiles.length !== files.length) {
    alert("Some files are not valid formats. Only images and ZIP files are allowed.");
  }

  // Limit the upload to 20 files (images + images inside ZIPs)
  if (validImageFiles.length + zipFiles.length > 20) {
    alert("You can only upload up to 20 files at once.");
    return;
  }

  const projectStore = useProjectStore();
  const projectId = projectStore.selectedProject?.id;
  if (!projectId) {
    console.error("No project selected. Cannot upload files.");
    return;
  }

  let tempArray = [];

  // Helper function to process ZIP files
  async function extractImagesFromZip(file) {
    const images = [];
    const jszip = new JSZip();

    try {
      const zipContent = await jszip.loadAsync(file);
      const fileNames = Object.keys(zipContent.files);

      for (const fileName of fileNames) {
        const zipFile = zipContent.files[fileName];

        // Check if the file is an image and not a folder
        if (!zipFile.dir && /\.(png|jpe?g|gif|webp)$/i.test(fileName)) {
          const fileData = await zipFile.async("blob");
          const imageFile = new File([fileData], fileName, { type: "image/*" });
          images.push(imageFile);
        }
      }
    } catch (error) {
      console.error(`Failed to extract images from ZIP: ${file.name}`, error);
      alert(`Error processing ZIP file ${file.name}. Please try again.`);
    }

    return images;
  }

  // Extract images from all ZIP files
  for (const zipFile of zipFiles) {
    const extractedImages = await extractImagesFromZip(zipFile);
    validImageFiles.push(...extractedImages);
  }

  // Check the total image count again after extracting ZIPs
  if (validImageFiles.length > 20) {
    alert("You can only upload up to 20 images at once, including extracted images from ZIPs.");
    return;
  }

  // Iterate over each image file and send it in a separate request
  for (const file of validImageFiles) {
    const formData = new FormData();
    formData.append("image", file); // Append the file as 'image'
    formData.append("projectId", projectId); // Include the project ID

    try {
      const response = await axios.post(`${api}/api/projects/images`, formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
        withCredentials: true, // Include credentials for authentication
      });
      tempArray.push(response.data);
    } catch (error) {
      console.error(`Failed to upload ${file.name}:`, error);
      alert(`Error uploading ${file.name}. Please try again.`);
    }
  }

  // Fetch additional data for uploaded images
  for (const element of tempArray) {
    await axios.get(`${api}/api/projects/images/${element.id}`, {
      responseType: "arraybuffer",
    });
  }

  // Refresh the image store to reflect new uploads
  await imageStore.fetchImages(projectId);

  alert("All images have been uploaded.");
  event.target.value = "";
}

// Toggle delete mode
function toggleDeleteMode() {
  if (deleteMode.value) {
    // If delete mode is active, confirm deletion
    confirmDeletion();
  }
  deleteMode.value = !deleteMode.value;
  if (!deleteMode.value) {
    selectedForDeletion.value = []; // Clear selection when exiting delete mode
  }
}

// Toggle selection of an image for deletion
function toggleImageSelection(index) {
  const selectedIndex = selectedForDeletion.value.indexOf(index);
  if (selectedIndex > -1) {
    // If already selected, remove it from the list
    selectedForDeletion.value.splice(selectedIndex, 1);
  } else {
    // Add to the selected list
    selectedForDeletion.value.push(index);
  }
}

// Confirm deletion
async function confirmDeletion() {
  if (selectedForDeletion.value.length === 0) {
    alert("No images selected for deletion.");
    return;
  }
 // Prevent deletion if the currently selected image is in the deletion list
 if (selectedForDeletion.value.includes(imageStore.images.indexOf(imageStore.selectedImage))) {
    alert("The selected image cannot be deleted.");
    return;
  }
  
  const confirmed = confirm("Are you sure you want to delete the selected images?");
  if (!confirmed) return;

  try {
    const projectStore = useProjectStore();
    const projectId = projectStore.selectedProject?.id;

    // Create an array of image IDs to delete (based on selected indexes)
    const imageIdsToDelete = selectedForDeletion.value.map(index => imageStore.ids[index]);
    // Remove the deleted images from the image store
    await imageStore.deleteImages(projectId,imageIdsToDelete);
    selectedForDeletion.value = [];
    alert("Selected images have been deleted.");
  } catch (error) {
    console.error("Error deleting images:", error);
    alert("Failed to delete images. Please try again.");
  }
}

// Download all images as a ZIP
async function downloadAllImagesAsZip() {
  const projectStore = useProjectStore();
  const projectId = projectStore.selectedProject?.id;
  await imageStore.downloadAllImagesAsZip(projectId);
  alert("Download has finished!");
}
</script>

<style scoped>
.wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  background-color: #f0f0f0;
  height: 100%;
  overflow-y: hidden;
}

.image-list {
  position: relative; /* Needed for overlay positioning */
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  padding-top: 10px;
  overflow-y: scroll;
  height: 90%;
  width: 100%;
  justify-content: center;
}

.image-list > div {
  width: 45%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.image-thumbnail {
  cursor: pointer;
  border: 2px solid transparent;
  border-radius: 8px;
  transition: border-color 0.3s;
  align-self: center;
}

.image-thumbnail img {
  width: 150px;
  height: 150px;
  border-radius: 6px;
  display: block;
}

.image-thumbnail:hover {
  border-color: #000000;
}

.overlay {
  position: absolute;
  top: 0;
  left: 25%;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 10; /* Ensure the overlay is on top of images */
}

.spinner {
  width: 50px;
  height: 50px;
  border: 5px solid #f3f3f3;
  border-top: 5px solid #000000;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.btn-flex {
  display: flex;
  flex-direction: row;
  width: 100%;
  position: relative;
  padding-top: 5%;
  justify-content: space-around;
  border-top: 1px solid #000000;
}

.btn-flex button {
  padding: 10px 30px;
  border-radius: 20px;
  background: #000000;
  color: #ffffff;
  border: none;
  cursor: pointer;
  overflow: hidden;
  border: 1px solid #000000;
  transition: 0.25s;
}

.btn-flex:nth-child(2) {
  right: 0;
}

.btn-flex button:hover {
  background-color: #ffffff;
  box-shadow: 0 0 6px #000000;
  color: #000000;
}

.image-thumbnail.selected {
  border-color: red;
  opacity: 0.7;
}

.btn-flex button.active {
  background-color: red;
  color: white;
}

</style>
