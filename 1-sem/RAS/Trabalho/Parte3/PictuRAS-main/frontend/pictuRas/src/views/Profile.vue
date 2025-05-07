<template>
    <div class="main-layout">
        <Navbar id="nav"></Navbar>
        <ProfileArea id="profileArea"></ProfileArea>
    </div>
</template>

<script>

import Navbar from '../components/Navbar.vue';
import ProfileArea from '../components/ProfileArea.vue';
import axios from 'axios';
import { useRouter } from 'vue-router';
import { useProfileStore } from '../stores/ProfileStore';
const api = import.meta.env.VITE_API_GATEWAY;

export default {
    name: 'Profile',
    components: {
        Navbar,
        ProfileArea
    },
    setup() {
    const profileStore = useProfileStore();
    const router = useRouter();

    // Check for selected project and user status
    const checkProfileAndUserStatus = async () => {

        const userStatus = await getUserStatus(); // Example: Replace with real API or authentication logic
        console.log(userStatus)
        if (userStatus === 'anonymous') {
          router.push('/projects'); // Redirect to projects page
        } else if (userStatus === 'loggedIn') {
        
          profileStore.fetchProfile()
        }
    };

    // Call the check function when the component mounts
    checkProfileAndUserStatus();
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
.main-layout {
    background-color: rgb(255, 255, 255);
}

</style>