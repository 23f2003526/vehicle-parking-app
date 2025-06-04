<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const id = route.params.id

const lot = ref(null)
const loading = ref(true)

onMounted(async () => {
    try {
        const response = await axios.get(`/api/admin/lots/${id}/summary`)
        lot.value = response.data
    } catch (error) {
        console.error('Error fetching lot summary:', error)
    } finally {
        loading.value = false
    }
})
</script>

<template>
    <div v-if="loading">Loading...</div>

    <div v-else-if="lot" class="lot-summary">
        <h2>{{ lot.prime_location_name }}</h2>
        <p>{{ lot.address }}, {{ lot.pin_code }}</p>
        <p>₹{{ lot.price }} per hour</p>
        <p>Total Spots: {{ lot.number_of_spots }}</p>
        <p>Available: {{ lot.available_spots }}</p>
        <p>Occupied: {{ lot.occupied_spots }}</p>

        <h3>Spots:</h3>
        <div class="spots-grid">
            <div v-for="spot in lot.spots" :key="spot.spot_id" class="spot-card"
                :class="spot.is_occupied ? 'occupied' : 'available'">
                <p><strong>Spot #:</strong> {{ spot.spot_number }}</p>
                <p><strong>Type:</strong> {{ spot.spot_type }}</p>
                <p><strong>Status:</strong> {{ spot.is_occupied ? 'Occupied' : 'Available' }}</p>
            </div>
        </div>
    </div>

    <div v-else>
        <p>Error loading lot data.</p>
    </div>
</template>

<style scoped>
.lot-summary {
    padding: 20px;
    border: 1px solid #ccc;
    margin: 20px;
}

.spots-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
    gap: 16px;
    margin-top: 20px;
}

.spot-card {
    padding: 12px;
    border: 1px solid #999;
    border-radius: 8px;
    background-color: #f3f3f3;
}

.spot-card.available {
    background-color: #d4f8d4;
    color: black;
}

.spot-card.occupied {
    background-color: #f8d4d4;
    color: black;
}
</style>
