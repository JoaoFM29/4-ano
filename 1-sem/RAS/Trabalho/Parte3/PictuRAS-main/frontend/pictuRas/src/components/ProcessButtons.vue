<template>
  <div class="btn-wrapper">
    <button @click="preview">Preview</button>
    <button @click="process">Process</button>
    <button @click="saveProject">Save</button>
    <button v-if="previewMode || onProcess" @click="cancel">Cancel</button>
  </div>
</template>

<script>
import { useProjectStore } from '../stores/ProjectStore';
import { useEditingToolStore } from '../stores/EditingTool';
import { storeToRefs } from 'pinia';
import { computed } from "vue";
import { useImageStore } from '../stores/ImageStore';

const ws = import.meta.env.VITE_WS_GATEWAY;

export default {
  name: "ProcessButtons",
  setup() {
    const projectStore = useProjectStore();
    const toolsStore = useEditingToolStore();
    const imageStore = useImageStore();
    const { tools } = storeToRefs(toolsStore);


    const ws = import.meta.env.VITE_WS_GATEWAY;
    let websocket = null; // WebSocket instance

    const previewMode = computed(() => imageStore.previewMode);
    const onProcess = computed(() => imageStore.onProcess);

    const saveProject = async () => {
  // Parse tools to remove the " copy x" suffix from each tool name
  const parsedTools = tools.value.map(tool => {
    const baseName = tool.name.split(" copy")[0].trim(); // Extract the base name
    return {
      ...tool,
      name: baseName, // Set the name to the base name only
    };
  });

  // Save the parsed tools
  await projectStore.saveProject(parsedTools);
  alert("Project Saved!");
};

    const process = () => {
      // Establish WebSocket connection
      // trocar com o ws
      if(projectStore.selectedProject.tools.length ===0){
        alert("Select at least one tool before processing!");
        return;
      }
      if(imageStore.images.length ===0){
        alert("Upload at least one image before processing!");
        return;
      }
      websocket = new WebSocket(ws); // Replace with your WebSocket server URL

      websocket.onopen = () => {
        console.log("WebSocket connection established");
        
        // Send a JSON message to the server
        const payload = {
          type: "process",
          project: projectStore.getId()
        };
        websocket.send(JSON.stringify(payload));
        console.log("Message sent:", payload);
        imageStore.enterProcessMode();
      };

      websocket.onmessage = (event) => {
        // Parse the JSON message received from the server
        const message = JSON.parse(event.data);
        console.log("Message from server:", message);

        // Handle the message based on the `action` or content
        if (message.type === "progress" && message.progress < 1.0) {
          imageStore.updateList(message.images)
          console.log(`Update: ${message.progress}`);
        } else if (message.type === "progress" && message.progress === 1.0) {
          alert(`Processing complete!`);
          imageStore.fetchImages(message.project)
          websocket.close(); // Close the WebSocket connection
        }else if (message.type === "error") {
          alert(`Processing error: ${message.progress}`);
          websocket.error(); // Close the WebSocket connection
        }
      };

      websocket.onerror = (error) => {
        console.error("WebSocket error:", error);
        imageStore.leaveProcessMode(true)
      };

      websocket.onclose = () => {
        console.log("WebSocket connection closed");
        imageStore.leaveProcessMode(false)
      };
    };

    const preview = () => {
      // Establish WebSocket connection
      // trocar com o ws
      if (!imageStore.canPreview()){
        alert("Cant select a Preview Image for another Preview!")
        return;
      }
      websocket = new WebSocket(ws); // Replace with your WebSocket server URL

      websocket.onopen = () => {
        console.log("WebSocket connection established");
        
        // Send a JSON message to the server
        const payload = {
          type: "preview",
          project: projectStore.getId(),
          image: imageStore.getSelectedImageId()
        };
        websocket.send(JSON.stringify(payload));
        console.log("Message sent:", payload);
        imageStore.enterPreviewMode();
      };

      websocket.onmessage = (event) => {
        // Parse the JSON message received from the server
        const message = JSON.parse(event.data);
        console.log("Message from server:", message);

        // Handle the message based on the `action` or content
        if (message.type === "progress" && message.progress < 1.0) {
         //  imageStore.updateList(message.images)
          console.log(`Update: ${message.progress}`);
        } else if (message.type === "progress" && message.progress === 1.0) {
          imageStore.updateSelectedImage(message.images);
          alert(`Preview complete!`);
          websocket.close(); // Close the WebSocket connection
        }else if (message.error) {
          alert(`Preview error: ${message.error}`);
          imageStore.leavePreviewMode(true)
          websocket.error(); // Close the WebSocket connection
        }
      };

      websocket.onerror = (error) => {
        console.error("WebSocket error:", error);
        imageStore.leavePreviewMode(true)
      };

      websocket.onclose = () => {
        console.log("WebSocket connection closed");
        imageStore.leavePreviewMode(false)
      };
    };
    const cancel = () => {
  if (websocket && websocket.readyState === WebSocket.OPEN) {
    // If the WebSocket connection is already open
    const payload = {
      type: "cancel",
      project: projectStore.getId(),
    };
    websocket.send(JSON.stringify(payload));
    console.log("Cancel message sent:", payload);

    websocket.close(); // Close the WebSocket connection after sending cancel
  } else {
    console.warn("WebSocket is not open or doesn't exist.");
  }

  // Ensure we leave any active modes in the store
  imageStore.leavePreviewMode(false);
  imageStore.leaveProcessMode(true);
  imageStore.fetchImages(projectStore.getId());
};
    return {
      saveProject,
      process,
      preview,
      cancel,
      previewMode,
      onProcess
    };
  },
};
</script>
<style scoped>
.btn-wrapper {
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;
  gap: 30px;
  padding-top: 20px;
}

.btn-wrapper button {
  padding: 10px 40px;
  border-radius: 20px;
  background: #000000;
  color: #ffffff;
  border: none;
  cursor: pointer;
  overflow: hidden;
  border: 1px solid #000000;
  transition: 0.25s;
  width: fit-content;
  align-self: center;
}

.btn-wrapper button:hover {
  background-color: #ffffff;
  box-shadow: 0 0 6px #000000;
  color: #000000;
}
</style>
