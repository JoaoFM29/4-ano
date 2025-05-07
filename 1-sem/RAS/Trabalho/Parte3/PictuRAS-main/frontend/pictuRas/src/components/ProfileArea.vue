<template>
    <div class="profile-area">
        <div v-if="profileStore.loading" class="text-center">
            Loading...
        </div>

        <div v-else-if="profileStore.error" class="text-red-500">
            {{ profileStore.error }}
        </div>
        
        <div v-else class="profile-Container">
            <div class="left-side">
                <img src="/logo-no-text.png" alt="Logo" class="logo1" />
                <h1>Name: {{ profileStore.profile.name }}</h1>
                <p>Email: {{ profileStore.profile.email }}</p>
                <p>Status: <b>{{ profileStore.profile.plan }}</b></p>
                <div class="profile-buttons">
                    <button>
                        <RouterLink to="/editprofile">Edit profile</RouterLink>
                    </button>
                    <button>
                        <RouterLink to="/plan">Change plan</RouterLink>
                    </button>
                    <button>
                        <RouterLink to="/projects">My projects</RouterLink>
                    </button>
                </div>
            </div>
        </div>
        
    </div>
</template>

<script setup>
import { onMounted } from 'vue';
import { useProfileStore } from '../stores/ProfileStore';
import { RouterLink } from 'vue-router';


const profileStore = useProfileStore();


onMounted(async () => {
    await profileStore.fetchProfile();
});


</script>

<style scoped>
.profile-area {
    width: 100%;
    display: flex;
    justify-content: center;
}

.profile-Container {
    background-color: #f7f7f7;
    width: 60%;
    height: auto;
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: 10vh;
    padding: 70px;
    border-radius: 40px;
    cursor: default;
    box-shadow: rgba(0, 0, 0, 0.25) 0px 54px 55px, 
                 rgba(0, 0, 0, 0.12) 0px -12px 30px, 
                 rgba(0, 0, 0, 0.12) 0px 4px 6px, 
                 rgba(0, 0, 0, 0.17) 0px 12px 13px, 
                 rgba(0, 0, 0, 0.09) 0px -3px 5px;

}

.left-side {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 50%;
}

.logo1 {
    width: 100px;
    height: 100px;
    margin-bottom: 16px;
}

.left-side p {
    font-size: 20px;
}

.profile-buttons {
    width: 100%;
    margin-top: 10%;
    display: flex;
    flex-direction: row;
    justify-content: space-around;
}

.profile-buttons button {
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



.profile-buttons button:hover {
    background-color: #ffffff;
    box-shadow: 0 0 6px #000000;
}

.profile-buttons button>a {
    position: relative;
    z-index: 1;
    text-decoration: none;
    color: #ffffff;
    font-size: 15px;
}

.profile-buttons button:hover>a {
    color: #000000;
}

.right-side button {
    position: absolute;
    padding: 10px 30px;
    border-radius: 20px;
    background: #000000;
    color: #ffffff;
    border: none;
    cursor: pointer;
    overflow: hidden;
    position: absolute;
    border: 1px solid #000000;
    transition: 0.25s;
}

.right-side button:hover {
    background-color: #ffffff;
    box-shadow: 0 0 6px #000000;
}

.right-side button a {
    position: relative;
    z-index: 1;
    text-decoration: none;
    color: #ffffff;
    font-size: 14px;
}

.right-side button:hover a {
    color: #000000;
}

</style>