<script setup>
import { onMounted, ref } from 'vue'
import axios from 'axios'
import BookingHistoryTable from '@/components/BookingHistoryTable.vue'
import AvailableParkingLotsTable from '@/components/AvailableParkingLotsTable.vue'
import BookingModal from '@/components/BookingModal.vue'
import ReleaseBookingModal from './ReleaseBookingModal.vue'

const parkingLots = ref([])
const bookings = ref([])

const fetchDataAgain = async () => {
    try {
        const lotsRes = await axios.get('/api/lots')
        parkingLots.value = lotsRes.data

        const bookingsRes = await axios.get('/api/bookings')
        bookings.value = bookingsRes.data.sort((a, b) => new Date(b.start_time) - new Date(a.start_time))

    } catch (error) {
        console.error('Failed to fetch data', error)
    }
}

onMounted(fetchDataAgain)

const showModal = ref(false)
const selectedLot = ref(null)
const selectedSpot = ref(null)

const handleBook = ({ lot, spot }) => {
    selectedLot.value = lot
    selectedSpot.value = spot
    showModal.value = true
}

const closeModal = () => {
    showModal.value = false
    selectedLot.value = null
    selectedSpot.value = null
}

// ----------------- Release Modal Logic -----------------
const showReleaseModal = ref(false)
const selectedBooking = ref(null)
const selectedHourlyRate = ref(0)

const handleViewBooking = (booking) => {
    selectedBooking.value = booking
    const lot = parkingLots.value.find(l => l.id === booking.lot_id)
    selectedHourlyRate.value = lot ? lot.price : 0
    showReleaseModal.value = true
}

const closeReleaseModal = () => {
    showReleaseModal.value = false
    selectedBooking.value = null
    selectedHourlyRate.value = 0
    fetchDataAgain()
}

</script>


<template>
    <div class="main">
        <h2>User Dashboard</h2>

        <BookingHistoryTable :bookings="bookings" @view-booking="handleViewBooking" />

        <ReleaseBookingModal v-if="showReleaseModal" :booking="selectedBooking" :hourly-rate="selectedHourlyRate"
            @close="closeReleaseModal" @released="fetchDataAgain" />

        <AvailableParkingLotsTable :lots="parkingLots" @open-booking="handleBook" />

        <BookingModal v-if="showModal" :lot="selectedLot" :spot="selectedSpot" @close="closeModal"
            @booked="fetchDataAgain" />
    </div>
</template>

<style scoped>
.main {
    /* border: 2px solid red; */
    margin: 1% 2% 0 2%;
}
</style>
