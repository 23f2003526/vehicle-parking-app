<script setup>
import { onMounted } from 'vue';
import axios from 'axios';


onMounted(async () => {
    try {
        const response = await axios.get('/api/admin/lots')
        console.log(response.data)
    } catch (error) {
        console.log('Something went wrong while fetching parking lots data', error);
    }
    // console.log(state.details)
})
</script>

<template>
    AdminDashboard
</template>