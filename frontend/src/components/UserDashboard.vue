<script setup>
import { onMounted, ref } from 'vue'
import axios from 'axios'
import BookingHistoryTable from '@/components/BookingHistoryTable.vue'
import AvailableParkingLotsTable from '@/components/AvailableParkingLotsTable.vue'

const parkingLots = ref([])

onMounted(async () => {
    try {
        const response = await axios.get('/api/lots')
        parkingLots.value = response.data
    } catch (error) {
        console.error('Failed to fetch parking lots', error)
    }
})

const handleViewBooking = (booking) => {
    console.log('User clicked view on:', booking)
}

const showModal = ref(false)
const selectedLot = ref(null)

const handleBook = (lot) => {
    selectedLot.value = lot
    showModal.value = true
}

</script>

<template>
    <h2>User Dashboard</h2>

    <AvailableParkingLotsTable :lots="parkingLots" @book="handleBook" />

    <BookingHistoryTable @view-booking="handleViewBooking" />

</template>
