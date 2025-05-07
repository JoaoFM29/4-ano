<template>
    <div class="main-layout">
        <SidebarProjects />
        <div class="content-layout">
            <Navbar id="nav"></Navbar>
            <ProjectList 
                v-if="isUserInfoLoaded" 
                :projects="projects" 
                :userInfo="userInfo" 
            />

        </div>
    </div>
</template>

<script>
import Navbar from '../components/Navbar.vue';
import SidebarProjects from '../components/Sidebar-Projects.vue';
import ProjectList from '../components/ProjectList.vue';
import axios from 'axios';
import { useRouter } from 'vue-router';
import { useProjectStore } from '../stores/ProjectStore.js';
import { ref, onMounted, computed } from 'vue';
import { useProfileStore } from '../stores/ProfileStore.js';

const api = import.meta.env.VITE_API_GATEWAY;

export default {
    name: 'Projects',
    components: {
        Navbar,
        SidebarProjects,
        ProjectList,
    },
    setup() {
        const router = useRouter();
        const projectStore = useProjectStore();
        const ProfileStore =useProfileStore();
        const userInfo = ref({ name: '', email: '', status: 'None' }); // Torna userInfo reativo
        const isUserInfoLoaded = ref(false);

        const getUserStatus = async () => {
            try {
                const response = await axios.get(`${api}/api/user/status`, { withCredentials: true });
                return response.data.status;
            } catch (error) {
                console.error('Error fetching user status:', error);
            }
        };

        const getUserInfo = async () => {
            try {
                await ProfileStore.fetchProfile();
                userInfo.value = ProfileStore.profile;
                console.log("Updated userInfo:", userInfo.value);
                isUserInfoLoaded.value = true;
            } catch (error) {
                console.error('Error fetching user info:', error);
            }
        };

        const quickCheck = async () => {
            const userStatus = await getUserStatus();
            if (userStatus === 'anonymous') {
                router.push('/project/undefined');
            }
        };

        onMounted(async () => {
            try {
                await quickCheck();
                await projectStore.fetchProjects();
                await getUserInfo();
            } catch (error) {
                console.error('Error during initialization:', error);
            }
        });

        const projects = computed(() => projectStore.projects);

        return {
            projects,
            userInfo,
            isUserInfoLoaded,
        };
    },
};
</script>



<style scoped>
.main-layout {
    display: flex;
    flex-direction: column;
    overflow: auto;
    gap: 0px;
    overflow-x: hidden;
}

.content-layout {
    width: 100%;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    overflow-y: auto;
    overflow-x: hidden;
}
</style>
