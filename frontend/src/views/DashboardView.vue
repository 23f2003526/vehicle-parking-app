<script setup>
import axios from 'axios';
import { onMounted, reactive } from 'vue';
import { useToast } from 'vue-toastification';
import router from '@/router';

import AdminDashboard from '@/components/AdminDashboard.vue';
import UserDashboard from '@/components/UserDashboard.vue';
import { useUserStore } from '@/stores/user';

const toast = useToast()
const userStore = useUserStore()

const state = reactive({
    // details: {},
    isLoading: true,
    // isAdmin: false,
})

onMounted(async () => {
    try {
        const response = await axios.get('/api/dashboard')
        userStore.setUserDetails(response.data)
    } catch (error) {
        // console.log('Error fetching user details', error);
        toast.error("Session Expired. Login Again.")
        userStore.logout()
        router.push('/login')
    } finally {
        state.isLoading = false;
    }
    // console.log(state.details)
})


</script>

<template>
    <AdminDashboard v-if="userStore.isAdmin" />
    <UserDashboard v-else />
</template>