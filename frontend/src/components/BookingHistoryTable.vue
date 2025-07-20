<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const bookings = ref([])
const isLoading = ref(true)
const error = ref(null)

const fetchBookings = async () => {
    try {
        const res = await axios.get('/api/bookings')
        bookings.value = res.data
    } catch (err) {
        error.value = 'Failed to load bookings'
        console.error(err)
    } finally {
        isLoading.value = false
    }
}

onMounted(fetchBookings)
</script>

<template>
    <div>
        <h3>Recent Parking History</h3>

        <p v-if="isLoading">Loading...</p>
        <p v-if="error">{{ error }}</p>

        <table v-if="!isLoading && bookings.length">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Location</th>
                    <th>Spot Number</th>
                    <th>Vehicle ID</th>
                    <th>Start Time</th>
                    <th>End Time</th>
                    <th>Action</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="b in bookings" :key="b.id">
                    <td>{{ b.id }}</td>
                    <td>{{ b.location_name }} ({{ b.address }})</td>
                    <td>{{ b.spot_number }}</td>
                    <td>{{ b.vehicle_id }}</td>
                    <td>{{ new Date(b.start_time).toLocaleString() }}</td>
                    <td>{{ new Date(b.end_time).toLocaleString() }}</td>
                    <td><button @click="$emit('view-booking', b)">View</button></td>
                </tr>
            </tbody>
        </table>

        <p v-else-if="!isLoading">No bookings found.</p>
    </div>
</template>
