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
                <h1>Edit Profile</h1>
                <form @submit.prevent="saveChanges">
                    <label for="fullName">Full Name:</label>
                    <input
                        type="text"
                        id="fullName"
                        v-model="editableProfile.name"
                        class="form-input"
                    />

                    <label for="email">Email:</label>
                    <input
                        type="email"
                        id="email"
                        v-model="editableProfile.email"
                        class="form-input"
                        readonly
                    />

                    <!-- <label for="registerdate">Registered at:</label>
                    <input
                        type="date"
                        id="registerdate"
                        :value="formattedRegisteredAt"
                        class="form-input"
                        readonly
                    /> -->

                    <!-- Overlay to change password -->
                    <div v-if="isPasswordEditOverlayVisible" class="overlay">
                        <div class="overlay-content">
                            <h2>Edit Password</h2>
                            <label for="newPassword">Current Password:</label>
                            <input
                                type="password"
                                id="newPassword"
                                v-model="editableProfile.currentPassword"
                                class="form-input"
                            />

                            <label for="newPassword">New Password:</label>
                            <input
                                type="password"
                                id="newPassword"
                                v-model="editableProfile.newPassword"
                                class="form-input"
                            />

                            <label for="confirmPassword">Confirm New Password:</label>
                            <input
                                type="password"
                                id="confirmPassword"
                                v-model="editableProfile.confirmPassword"
                                class="form-input"
                            />

                            <div class="profile-buttons">
                                <button type="button" @click="savePasswordChanges">
                                    Save Password
                                </button>
                                <button type="button" @click="togglePasswordEditOverlay">
                                    Cancel
                                </button>
                            </div>
                        </div>
                    </div>

                    <div class="profile-buttons">
                        <button type="button" @click="togglePasswordEditOverlay">
                            Edit Password
                        </button>
                        <button type="submit">
                            Save Changes
                        </button>
                        <RouterLink to="/profile">
                            <button type="button">
                                Cancel
                            </button>
                        </RouterLink>
                        <div class="deleteaccount-button">
                            <RouterLink to="/">
                                <button type="button" @click="deleteAccount">
                                        Delete Account
                                    </button>
                            </RouterLink>
                        </div>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useProfileStore } from '../stores/ProfileStore';
import { useRouter } from 'vue-router';
import axios from 'axios';

const profileStore = useProfileStore();
const router = useRouter();

const editableProfile = ref({
    email: '',
    name: '',
    password_hash: '',
    plan: '',
    registered_at: '',
    type: '',
    username: ''
});

const currentPassword = ref('');
const showPassword = ref(false);
const isPasswordEditOverlayVisible = ref(false);

onMounted(async () => {
    await profileStore.fetchProfile();
    // await profileStore.getCompleteProfile();
    editableProfile.value = { ...profileStore.profile }; // Sincroniza o estado local com o store
});

// Computed property para formatar a data corretamente para o campo 'date'
const formattedRegisteredAt = computed(() => {
    // Extrai a parte da data (YYYY-MM-DD) da string completa
    const date = new Date(editableProfile.value.registered_at);
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');  // Adiciona o zero à esquerda, se necessário
    const day = String(date.getDate()).padStart(2, '0');  // Adiciona o zero à esquerda, se necessário

    // Retorna no formato YYYY-MM-DD
    return `${year}-${month}-${day}`;
});

const togglePasswordVisibility = () => {
    showPassword.value = !showPassword.value;
};

const togglePasswordEditOverlay = () => {
    isPasswordEditOverlayVisible.value = !isPasswordEditOverlayVisible.value;
};

const savePasswordChanges = async () => {
    if (editableProfile.value.newPassword !== editableProfile.value.confirmPassword) {
        alert('Passwords do not match.');
        return;
    }

    // Atualizar a senha
    await profileStore.updatePassword(currentPassword.value, editableProfile.value.newPassword);
    alert('Password updated successfully!');
    togglePasswordEditOverlay(); // Fechar a overlay
};

const saveChanges = async () => {
    try {
        // Certifique-se de que o username é igual ao email
        console.log("Saving changes: ", editableProfile.value);

        const response = await profileStore.updateProfile(editableProfile.value);
        alert('Profile updated successfully!');
        router.push('/profile');
    } catch (error) {
        console.error('Failed to update profile:', error);
        alert('Failed to update profile.');
    }
};

const deleteAccount = async () => {
    try {
        const email = editableProfile.value.email; // Obtém o username do perfil
        if (!confirm('Are you sure you want to delete your account? This action is irreversible.')) {
            return;
        }
        const api = import.meta.env.VITE_API_GATEWAY;
        const response = await axios.delete(`${api}/api/users/${email}`);
        alert('Your account has been deleted successfully.');
        router.push('/'); // Redireciona para a página inicial após a exclusão
    } catch (error) {
        console.error('Failed to delete account:', error);
        alert('Failed to delete your account. Please try again.');
    }
};
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
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 40px;
    margin-top: 10vh;
    border-radius: 40px;
    box-shadow: rgba(0, 0, 0, 0.25) 0px 54px 55px, 
                 rgba(0, 0, 0, 0.12) 0px -12px 30px, 
                 rgba(0, 0, 0, 0.12) 0px 4px 6px, 
                 rgba(0, 0, 0, 0.17) 0px 12px 13px, 
                 rgba(0, 0, 0, 0.09) 0px -3px 5px;
}

.left-side {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    width: 100%;
}

.logo1 {
    width: 100px;
    height: 100px;
    margin-bottom: 16px;
}

.left-side h1 {
    font-size: 26px;
    margin-bottom: 20px;
}

.form-input {
    width: 100%;
    padding: 10px;
    margin-bottom: 20px;
    border: 1px solid #ccc;
    border-radius: 8px;
    font-size: 16px;
}

.profile-buttons {
    display: flex;
    justify-content: space-between;
    width: 100%;
}

.profile-buttons button {
    padding: 10px 30px;
    border-radius: 20px;
    background: #000000;
    color: #ffffff;
    border: none;
    cursor: pointer;
    transition: 0.25s;
}

.deleteaccount-button button {
    padding: 10px 30px;
    border-radius: 20px;
    background: #fa0202;
    color: #ffffff;
    border: none;
    cursor: pointer;
    transition: 0.25s;
}

.profile-buttons button:nth-child(2) {
    background: #000000;
    color: #ffffff;
}

.profile-buttons button:hover {
    background-color: #000000;
    box-shadow: 0 0 6px #000000;
}

.deleteaccount-button button:hover {
    background-color: #ff0000;
    box-shadow: 0 0 6px #ff0000;
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

/* Overlay */
.overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
}

.overlay-content {
    background-color: white;
    padding: 40px;
    border-radius: 10px;
    width: 400px;
    box-shadow: rgba(0, 0, 0, 0.25) 0px 4px 6px;
}

.overlay h2 {
    font-size: 20px;
    margin-bottom: 20px;
}
</style>
