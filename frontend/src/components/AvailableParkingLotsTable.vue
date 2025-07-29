<script setup>
import { ref, computed } from 'vue'
import { useToast } from 'vue-toastification'
import axios from 'axios'

const props = defineProps({
    lots: Array
})

const emit = defineEmits(['open-booking'])

const filterText = ref('')
const toast = useToast()

const filteredLots = computed(() => {
    if (!filterText.value.trim()) return props.lots
    return props.lots.filter(lot =>
        lot.prime_location_name.toLowerCase().includes(filterText.value.toLowerCase()) ||
        lot.pin_code.includes(filterText.value.trim())
    )
})

const fetchAvailableSpot = async (lot) => {
    try {
        const res = await axios.get(`/api/lots/${lot.id}/summary`)
        const availableSpots = res.data.spots.filter(s => !s.is_occupied && s.status === 'available')
        if (availableSpots.length === 0) {
            toast.error('No available spots in this lot.')
            return null
        }
        return availableSpots[0]
    } catch (err) {
        console.error('Failed to fetch lot summary:', err)
        toast.error('Could not fetch lot details.')
        return null
    }
}

const openBookingModal = async (lot, type) => {
    const spot = await fetchAvailableSpot(lot)
    if (!spot) return
    emit('open-booking', { lot, spot, type })
}


</script>

<template>
    <div>
        <h3>Available Parking Lots</h3>
        <input v-model="filterText" placeholder="Search by location or pincode"
            style="margin-bottom: 10px; padding: 5px; min-width: 25vh;" />
        <div class="table-wrapper" v-if="filteredLots.length">
            <table>
                <thead>
                    <tr>
                        <th>Lot ID</th>
                        <th>Location</th>
                        <th>Address</th>
                        <th>Availability</th>
                        <th>Hourly Price</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="lot in filteredLots" :key="lot.id">
                        <td>{{ lot.id }}</td>
                        <td>{{ lot.prime_location_name }}</td>
                        <td>{{ lot.address }}, {{ lot.pin_code }}</td>
                        <td>{{ lot.available_spots }} / {{ lot.number_of_spots }}</td>
                        <td>₹{{ lot.price }}</td>
                        <td>
                            <button @click="openBookingModal(lot, type = 'Book')" :disabled="lot.available_spots === 0">
                                {{ lot.available_spots > 0 ? 'Book' : 'Full' }}
                            </button>
                            <button @click="openBookingModal(lot, type = 'Reserve')"
                                :disabled="lot.available_spots === 0">
                                {{ lot.available_spots > 0 ? 'Reserve' : 'Full' }}
                            </button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
        <p v-else>No matching lots found.</p>
    </div>
</template>

<style scoped>
table {
    width: 100%;
    border-collapse: collapse;
}

th,
td {
    padding: 10px;
    border: 1px solid #ccc;
    text-align: left;
}

button {
    background: #333;
    color: white;
    border: none;
    padding: 5px 10px;
    cursor: pointer;
    margin: 3px;
}

button:disabled {
    background: #888;
    cursor: not-allowed;
}

.table-wrapper {
    max-height: 400px;
    /* approx 10 rows x 40px each */
    overflow-y: auto;
    border: 1px solid #ccc;
    margin-top: 15px;
}
</style>
