<template>
  <div class="main-layout">
    <Navbar id="nav"></Navbar>
    <div class="main-part">
      <ImageList id="image-list"></ImageList>
      <EditingSpace id="editing-space"></EditingSpace>
    </div>
  </div>
</template>

<script>
import { useProjectStore } from '../stores/ProjectStore.js';
import { useEditingToolStore } from '../stores/EditingTool';
import { useImageStore } from '../stores/ImageStore';
import { useProfileStore } from '../stores/ProfileStore.js';
import { useRouter } from 'vue-router';
import Navbar from '../components/Navbar.vue';
import ImageList from '../components/ImageList.vue';
import EditingSpace from '../components/EditingSpace.vue';
import { storeToRefs } from 'pinia'
import axios from 'axios';


const api = import.meta.env.VITE_API_GATEWAY;

export default {
  name: 'Project',
  components: {
    Navbar,
    ImageList,
    EditingSpace
  },
  props: {
    projectUrlId: String,
  },
  setup(props) {
    const projectStore = useProjectStore();
    const editingToolsStore = useEditingToolStore();
    const imageStore = useImageStore();
    const profileStore = useProfileStore();
    const router = useRouter();
    // Check for selected project and user status
    const receivedProjectId = props.projectUrlId || router.params.projectUrlId; // Check prop or route param
    const checkProjectAndUserStatus = async () => {
      projectStore.clear();
      imageStore.clear();
      editingToolsStore.clear();
      const userStatus = await getUserStatus(); // Example: Replace with real API or authentication logic
      if (!projectStore.selectedProject) {

        
        console.log(userStatus)
        if (userStatus === 'loggedIn') {

          if (receivedProjectId) {
            console.log("here:",receivedProjectId)
            await projectStore.fetchProject(receivedProjectId)
          } else {
            router.push('/projects'); // Redirect to projects page
          }

        } else if (userStatus === 'anonymous') {
          
          // generate session project
          alert('You are currently Anonymous. Reduced features ');
          await projectStore.generateSessionProject();
        }
      }else{
        if (receivedProjectId) {
            console.log("here:",receivedProjectId)
            await projectStore.fetchProject(receivedProjectId)
          }
      }
      await setState();
    };

    const setState = async() =>{
      console.log("setingState!")
      const projectId = projectStore.getId()
      await editingToolsStore.fetchTools();
      await imageStore.fetchImages(projectId);
      await profileStore.fetchProfile();
      const tools = projectStore.getTools()
      editingToolsStore.mergeTools(tools)
      if (!profileStore.userPlanName){
        profileStore.userPlanName="free";
      }
      // update toolsStore tendo em conta o que recebemos do projeto.
      console.log(profileStore.userPlanName);
    }
    // Call the check function when the component mounts
     checkProjectAndUserStatus();
     
  }
};


const getUserStatus = async () => {
  try {
    const response = await axios.get(api+'/api/user/status', { withCredentials: true });
    return response.data.status;
  } catch (error) {
    console.error('Error fetching user status:', error);
  }
};


</script>

<style scoped>
/*
  .main-part {
    display: grid;
      height: 100%;
      width: 100%;
      grid-template-columns: 25% 75%;
      grid-template-areas:
        "image-list editing-space";
      overflow: auto;
      gap:0px;
  }
*/


#nav {
    flex-shrink: 0;
}

.main-layout {
    background-color: rgb(255, 255, 255);
    display: flex;
    flex-direction: column;
    height: 100vh;
    max-height: 100vh;
}

.main-part {
    flex-grow: 1;
    overflow-y: auto;
    display: flex;
}

#nav {
    position: sticky;
    top: 0;
}

#image-list {
  grid-area: image-list;
  width: 25%;
}

#editing-space {
  grid-area: editing-space;
  width: 75%;
}
</style>