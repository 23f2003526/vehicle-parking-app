<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import BookingModal from '@/components/BookingModal.vue'
import { useToast } from 'vue-toastification'

const lots = ref([])
const filterText = ref('')
const isLoading = ref(true)
const error = ref(null)

const showBookingModal = ref(false)
const selectedLot = ref(null)
const selectedSpot = ref(null)

const toast = useToast()

const fetchLots = async () => {
    try {
        const res = await axios.get('/api/lots')
        lots.value = res.data
    } catch (err) {
        error.value = 'Failed to load parking lots'
    } finally {
        isLoading.value = false
    }
}

const filteredLots = computed(() => {
    if (!filterText.value.trim()) return lots.value

    return lots.value.filter(lot =>
        lot.prime_location_name.toLowerCase().includes(filterText.value.toLowerCase()) ||
        lot.pin_code.includes(filterText.value.trim())
    )
})

const openBookingModal = (lot) => {
    console.log('User clicked book on:', lot);

    selectedLot.value = lot
    // Here spot_id will be assigned dynamically, adjust if needed
    selectedSpot.value = { id: lot.id, spot_number: 'Auto Assigned', spot_type: 'Standard' }
    showBookingModal.value = true
}

const handleBookingSuccess = () => {
    toast.success('Booking successful.')
    showBookingModal.value = false
    fetchLots()
}

onMounted(fetchLots)
</script>

<template>
    <div>
        <h3>Available Parking Lots</h3>

        <input v-model="filterText" placeholder="Search by location or pincode"
            style="margin-bottom: 10px; padding: 5px;" />

        <p v-if="isLoading">Loading...</p>
        <p v-if="error">{{ error }}</p>

        <table v-if="!isLoading && filteredLots.length">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Location</th>
                    <th>Address</th>
                    <th>Availability</th>
                    <th>Action</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="lot in filteredLots" :key="lot.id">
                    <td>{{ lot.id }}</td>
                    <td>{{ lot.prime_location_name }}</td>
                    <td>{{ lot.address }}, {{ lot.pin_code }}</td>
                    <td>{{ lot.available_spots }} / {{ lot.number_of_spots }}</td>
                    <td>
                        <button @click="openBookingModal(lot)" :disabled="lot.available_spots === 0">
                            {{ lot.available_spots > 0 ? 'Book' : 'Full' }}
                        </button>
                    </td>
                </tr>
            </tbody>
        </table>

        <p v-else-if="!isLoading">No matching lots found.</p>

        <BookingModal v-if="showBookingModal" :lot="selectedLot" :spot="selectedSpot" @close="showBookingModal = false"
            @booked="handleBookingSuccess" />
    </div>
</template>


<style scoped>
table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 15px;
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
}

button:disabled {
    background: #888;
    cursor: not-allowed;
}
</style>
