<template>
    <div class="main-layout">
        <Navbar id="nav"></Navbar>
        <EditProfileArea id="editProfileArea"></EditProfileArea>
    </div>
</template>

<script>

import Navbar from '../components/Navbar.vue';
import EditProfileArea from '../components/EditProfileArea.vue';

export default {
    name: 'EditProfile',
    components: {
        Navbar,
        EditProfileArea
    },
};

</script>

<style scoped>
.main-layout {
    background-color: rgb(255, 255, 255);
}

</style>