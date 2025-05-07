<template>
    <div class="projects-list">
        <div class="projects-wrapper">
            <h2>All Projects</h2>
            <div class="top-projects">
                <div class="search-bar">
                    <input type="text" v-model="searchQuery" placeholder="Search in all projects..." />
                </div>
                <div class="plan-projects">
                    <p v-if="userInfo.plan === 'free'" class="free-plan">
                        You’re on the free plan!
                    </p>
                    <p v-else-if="userInfo.plan === 'premium'" class="premium-plan">
                        You’re on the premium plan!
                    </p>
                    <p v-else-if="userInfo.plan === 'basic'" class="basic-plan">
                        You’re on the basic plan!
                    </p>
                    <p v-else-if="userInfo.plan === 'enterprise'" class="enterprise-plan">
                        You’re on the enterprise plan!
                    </p>
                    <Button1 
                        style="margin-top: 0; margin-left: 1em;" 
                        label="Upgrade" 
                        @click="redirectToUpgrade" 
                        v-if="userInfo.plan === 'free'" 
                    />
                </div>
            </div>
            <table>
            <thead>
                <tr>
                    <th style="width: 5%;"><input type="checkbox" /></th>
                    <th style="width: 55%;">Title</th>
                    <th style="width: 30%;">Created at</th>
                    <th style="width: 10%;">Actions</th>
                </tr>
            </thead>
            <tbody>
                <!-- Projetos -->
                <template v-if="filteredProjects.length > 0">
                        <tr v-for="project in filteredProjects" :key="project.id">
                            <td><input type="checkbox" /></td>
                            <td 
                                class="editable-cell"
                                @mouseover="hoveringProjectId = project.id"
                                @mouseleave="hoveringProjectId = null"
                                >
                                <span v-if="editingProjectId !== project.id" class="project-name">
                                    {{ project.name }}
                                    <FontAwesomeIcon 
                                    v-if="hoveringProjectId === project.id"
                                    :icon="['fas', 'pen']"
                                    class="edit-icon" 
                                    @click.stop="startEditing(project.id)" 
                                    title="Edit project name"
                                    />
                                </span>
                                <div v-else class="edit-container">
                                    <input
                                    type="text"
                                    v-model="editName"
                                    @blur="saveEdit(project.id)"
                                    @keyup.enter="saveEdit(project.id)"
                                    class="edit-input"
                                    />
                                    <FontAwesomeIcon 
                                    :icon="['fas', 'check']" 
                                    class="save-icon"
                                    @click="saveEdit(project.id)"
                                    title="Save changes"
                                    />
                                </div>
                                </td>

                            <td>{{ formatDate(project.date) }}</td>
                            <td class="actions">
                                <FontAwesomeIcon :icon="['fas', 'edit']" title="Edit" class="action-icon" @click="goToProject(project.id)" />
                                <FontAwesomeIcon :icon="['fas', 'trash']" title="Delete" class="action-icon" @click="handleDeleteProject(project.id)" />
                            </td>
                        </tr>
                    </template>

                    <!-- Mensagem para quando não há projetos -->
                    <template v-else>
                        <tr>
                            <td colspan="4" style="text-align: center;">No projects found.</td>
                        </tr>
                    </template>
            </tbody>
        </table>
        <p class="footer">Showing {{ filteredProjects.length }} out of {{ projects.length }} projects.</p>
        </div>
    </div>
</template>


<script>
import Button1 from '../components/Button-style1.vue';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { faDownload, faEdit, faEye, faTrash, faPen,faCheck } from '@fortawesome/free-solid-svg-icons';
import { library } from '@fortawesome/fontawesome-svg-core';
import { useRouter } from 'vue-router';
import { useProjectStore } from '../stores/ProjectStore.js';

library.add(faDownload, faEdit, faEye, faTrash,faPen,faCheck);

export default {
    name: "ProjectsList",
    components:{
        Button1,
        FontAwesomeIcon,
    },
    props: {
        projects: {
            type: Array,
            required: true,
            default: () => [], 
        },
        userInfo: {
        type: Object,
        },
    },
    data() {
        return {
            searchQuery: "",
            editingProjectId: null,
            hoveringProjectId: null, 
            editName: "",
        };
    },
    computed: {
        filteredProjects() {
            if (!this.projects || this.projects.length === 0) {
                return [];
            }
            return this.projects.filter((project) =>
                project.name.toLowerCase().includes(this.searchQuery.toLowerCase())
            );
        },
    },
    methods: {
        

        formatDate(date) {
        if (!date) return 'N/A'; // Caso não tenha data
        const options = { year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit', second: '2-digit' };
        return new Intl.DateTimeFormat('en-GB', options).format(new Date(date));
        },

        editProject(projectId) {
            const router = useRouter();
            router.push(`/project/`);
        },
        goToProject(projectId) {
            this.$router.push(`/project/${projectId}`);
        },

        startEditing(projectId) {
            this.editingProjectId = projectId;
            this.editName = this.projects.find((project) => project.id === projectId).name;
        },

        redirectToUpgrade() {
            this.$router.push('/plan'); 
        },

        async saveEdit(projectId) {
            const projectStore = useProjectStore();

            if (!this.editName.trim()) {
                console.error('Project name cannot be empty.');
                return;
            }

            try {
                await projectStore.updateProjectName(projectId, this.editName);
                const project = this.projects.find((project) => project.id === projectId);
                if (project) {
                    project.name = this.editName; 
                }
                console.log(`Project ${projectId} updated successfully.`);
            } catch (error) {
                console.error(`Failed to update project ${projectId}:`, error);
            } finally {
                this.editingProjectId = null;
            }
        },
    

    },

    setup(){
        const handleDeleteProject = async (projectId) => {
            const projectStore = useProjectStore();
            try {
                await projectStore.deleteProject(projectId);
                console.log('Project deleted successfully.');
            } catch (error) {
                console.error('Failed to delete project:', error);
            }
        }

        
        return {
            handleDeleteProject,
        }
    },

    mounted() {
        console.log("User Info received from props:", this.userInfo);
    },


    

}


</script>

<style scoped>
    .projects-list {
    width: 83%;
    align-self: flex-end;
    padding: 20px;
    background-color: #ffffff;
    border-radius: 5px;
    border: 1px solid #ddd;
    flex: 1;
    overflow-y: auto; 
    
}

.projects-wrapper{
    display: flex;
    flex-direction: column;
    align-self: center;
    padding: 20px;
    width: 95%;
    height: 100%;
}

.top-projects{
    display: flex;
    justify-content: space-between;
    flex-direction: row;
    align-items: center;
    width: 90%;
    align-self: center;
    margin-bottom: 4em;
}

.plan-projects{
    display: flex;
    flex-direction: row;
    align-items: center;
}

h2 {
    font-size: 1.5em;
    margin-bottom: 10px;
    color: #333;
    margin-left: 5%
}

.search-bar {
    width: 60%;
}

.search-bar input {
    width: 50%;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 5px;
}

table {
    width: 70%;
    align-self: center;
    border-collapse: collapse;
    margin-bottom: 20px;
}

thead {
    background-color: #f9f9f9;
}

th, td {
    text-align: left;
    padding: 10px;
    border: 1px solid #ddd;
}

th {
    font-weight: bold;
    color: #555;
}

td.actions {
    display: flex;
    gap: 10px;
}

.action-icon {
    font-size: 1.2em; 
    cursor: pointer; 
    color: #555; 
    transition: color 0.3s ease-in-out; 
}

.action-icon:hover {
    color: #ff6600c2; 
    cursor: pointer; 
}


.actions{
    display: flex;
    justify-content: space-around;
}

.footer {
    font-size: 0.9em;
    color: #555;
    align-self: center;
}

.editable-cell {
  position: relative; 
}

.edit-icon {
  visibility: hidden; 
  opacity: 0;
  margin-left: 8px;
  color: #6c757d; 
  font-size: 1rem; 
  transition: visibility 0.2s, opacity 0.2s, color 0.2s ease-in-out;
  cursor: pointer;
}

.editable-cell:hover .edit-icon {
  visibility: visible; 
  opacity: 1;
}

.edit-icon:hover {
  color: #ffa602; 
}

.edit-input {
  width: 90%;
  padding: 5px;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-shadow: 0 0 2px rgba(0, 0, 0, 0.1);
}

.save-icon {
  color: #000000;
  margin-left: 10px;
  font-size: 1.2rem;
  cursor: pointer;
  transition: color 0.2s;
}

.save-icon:hover {
  color: #218838;
}

.premium-plan {
    font-weight: bold;
    animation: premiumEffect 2s infinite alternate;
}

@keyframes premiumEffect {
    0% {
        color: black;
    }
    100% {
        color: gold;
    }
}

.basic-plan {
    font-weight: bold;
    animation: basicEffect 2s infinite alternate;
}

@keyframes basicEffect {
    0% {
        color: black;
    }
    100% {
        color: rgb(255, 0, 200);
    }
}

.enterprise-plan {
    font-weight: bold;
    animation: enterpriseEffect 2s infinite alternate;
}

@keyframes enterpriseEffect {
    0% {
        color: black;
    }
    100% {
        color: rgb(87, 72, 72);
    }
}

</style>