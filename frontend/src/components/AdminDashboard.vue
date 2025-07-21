<script setup>
import { onMounted, reactive } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import ParkingLot from './ParkingLot.vue'

const state = reactive({
    parkingLots: []
})

const router = useRouter()

onMounted(async () => {
    try {
        const response = await axios.get('/api/admin/lots')
        state.parkingLots = response.data
    } catch (error) {
        console.error('Failed to fetch parking lots', error)
    }
})

function goToLot(id) {
    router.push(`/lots/${id}`)
}
</script>

<template>
    <h2>Parking Lots</h2>
    <div class="lots-grid">
        <div v-for="lot in state.parkingLots" :key="lot.id" class="lot-card" @click="goToLot(lot.id)">
            <ParkingLot :lot="lot" />
        </div>

        <div class="lot-card add-lot">
            <button @click="router.push('/admin/lots/create')">+</button>
        </div>
    </div>
</template>

<style scoped>
h2 {
    /* margin-bottom: 1rem; */
    font-size: 1.5rem;
    font-weight: bold;
    text-align: left;
    margin: 1% 2% 0 2%;
}

.lots-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
    gap: 20px;
    padding: 0 1rem;
    margin: 1% 2% 0 2%;
}

.lot-card {
    border: 1px solid #ccc;
    border-radius: 10px;
    padding: 1rem;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    cursor: pointer;
}

.lot-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 4px 12px rgba(255, 255, 255, 0.527);
}

.add-lot {
    display: flex;
    align-items: center;
    justify-content: center;
    border: 2px dashed #aaa;
}

.add-lot:hover {
    background-color: #d0d0d0;
}

button {
    width: 3.5rem;
    height: 3.5rem;
    font-size: 1.8rem;
    border-radius: 50%;
    border: none;
    background-color: #4caf50;
    color: white;
    cursor: pointer;
    transition: background-color 0.2s ease;
}

button:hover {
    background-color: #43a047;
}
</style>