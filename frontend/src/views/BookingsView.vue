<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { useToast } from 'vue-toastification'
import BookingHistoryTable from '@/components/BookingHistoryTable.vue'

const bookings = ref([])
const loading = ref(true)
const searchQuery = ref('')

const router = useRouter()
const userStore = useUserStore()
const toast = useToast()

onMounted(async () => {
    if (!userStore.isAdmin) {
        router.push('/unauthorized')
        return
    }
    try {
        const res = await axios.get('/api/admin/bookings')
        bookings.value = res.data
    } catch (err) {
        console.error(err)
        toast.error('Failed to fetch bookings.')
    } finally {
        loading.value = false
    }
})

// Filter and sort computed property
const filteredBookings = computed(() => {
    return bookings.value
        .filter(b => {
            const query = searchQuery.value.toLowerCase()
            return (
                b.id.toString().includes(query) ||
                b.location_name.toLowerCase().includes(query) ||
                b.address.toLowerCase().includes(query) ||
                b.vehicle_number.toLowerCase().includes(query)
            )
        })
        .sort((a, b) => new Date(b.start_time) - new Date(a.start_time))
})
</script>

<template>
    <div class="container">
        <h2>All Bookings</h2>

        <div class="filter-box">
            <input v-model="searchQuery" placeholder="Filter by ID, Location, Address, Vehicle No." />
        </div>

        <div v-if="loading">Loading...</div>
        <BookingHistoryTable v-else :bookings="filteredBookings" />
    </div>
</template>

<style scoped>
.container {
    margin: 1% 2% 0 2%;
}

.filter-box {
    margin-bottom: 1rem;
}

.filter-box input {
    width: 300px;
    padding: 6px 10px;
    border: 1px solid #ccc;
    border-radius: 4px;
}
</style>
