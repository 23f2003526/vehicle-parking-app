<script setup>
import axios from 'axios';
import { onMounted, reactive } from 'vue';
import { useToast } from 'vue-toastification';
import AdminDashboard from '@/components/AdminDashboard.vue';
import UserDashboard from '@/components/UserDashboard.vue';
import router from '@/router';

const toast = useToast()

const state = reactive({
    details: {},
    isLoading: true,
    isAdmin: false,
})

onMounted(async () => {
    try {
        const response = await axios.get('/api/dashboard')
        state.details = response.data
        if (state.details.role === 'admin') {
            state.isAdmin = true
        }
    } catch (error) {
        console.log('Error fetching user details', error);
        toast.error("Session Expired. Login Again.")
        router.push('/login')
    } finally {
        state.isLoading = false;
    }
    // console.log(state.details)
})


</script>

<template>
    <AdminDashboard v-if="state.isAdmin" />
    <UserDashboard v-else />
</template>