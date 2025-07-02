<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useToast } from 'vue-toastification'
import axios from 'axios'
import { useUserStore } from '@/stores/user'

const route = useRoute()
const router = useRouter()
const toast = useToast()
const id = route.params.id

const lot = ref(null)
const loading = ref(true)
const deleteLoading = ref(false)
const showDeleteModal = ref(false)
const showBookSpotModal = ref(false)

const userStore = useUserStore()

onMounted(async () => {
    try {
        const response = await axios.get(`/api/lots/${id}/summary`)
        lot.value = response.data
    } catch (error) {
        console.error('Error fetching lot summary:', error)
        toast.error('Failed to load parking lot data')
    } finally {
        loading.value = false
    }
})

const handleEdit = () => {
    router.push(`/admin/lots/${id}/edit`)
}

const confirmDelete = () => {
    showDeleteModal.value = true
}

const cancelDelete = () => {
    showDeleteModal.value = false
}

const confirmBooking = () => {
    showBookSpotModal.value = true
}

const cancelBooking = () => {
    showBookSpotModal.value = false
}

const handleBooking = async () => {
    console.log("hello there");

}

const handleDelete = async () => {
    if (deleteLoading.value) return

    deleteLoading.value = true

    try {
        await axios.delete(`/api/admin/lots/${id}`)
        toast.success('Parking lot deleted successfully')
        router.push('/dashboard') // Redirect to lots list
    } catch (error) {
        console.error('Error deleting lot:', error)
        const errorMessage = error.response?.data?.message || 'Failed to delete parking lot'
        toast.error(errorMessage)
    } finally {
        deleteLoading.value = false
        showDeleteModal.value = false
    }
}

const goBack = () => {
    router.push('/dashboard')
}
</script>

<template>
    <div v-if="loading" class="loading-container">
        <div class="spinner"></div>
        <p>Loading...</p>
    </div>

    <div v-else-if="lot" class="lot-summary">
        <!-- Header with actions -->
        <div class="header-section">
            <div class="header-info">
                <h2>{{ lot.prime_location_name }}</h2>
                <p class="address">{{ lot.address }}, {{ lot.pin_code }}</p>
            </div>
            <div class="action-buttons">
                <button @click="goBack" class="btn btn-secondary">
                    &larr; Back
                </button>
                <button v-if="userStore.isAdmin" @click="handleEdit" class="btn btn-primary">
                    ✎ Edit
                </button>
                <button v-if="userStore.isAdmin" @click="confirmDelete" class="btn btn-danger"
                    :disabled="deleteLoading">
                    🗑 Delete
                </button>
            </div>
        </div>

        <!-- Lot details -->
        <div class="details-section">
            <div class="detail-card">
                <h3>Pricing</h3>
                <p class="price">₹{{ lot.price }} per hour</p>
            </div>
            <div class="detail-card">
                <h3>Capacity</h3>
                <p>Total Spots: <span class="highlight">{{ lot.number_of_spots }}</span></p>
                <p>Available: <span class="available">{{ lot.available_spots }}</span></p>
                <p>Occupied: <span class="occupied">{{ lot.occupied_spots }}</span></p>
            </div>
        </div>

        <!-- Spots grid -->
        <div class="spots-section">
            <h3>Parking Spots</h3>
            <div class="spots-grid">
                <div v-for="spot in lot.spots" :key="spot.spot_id" class="spot-card"
                    :class="spot.is_occupied ? 'occupied' : 'available'" @click="confirmBooking">
                    <div class="spot-number">{{ spot.spot_number }}</div>
                    <p><strong>Type:</strong> {{ spot.spot_type }}</p>
                    <p class="status">
                        <span :class="spot.is_occupied ? 'status-occupied' : 'status-available'">
                            {{ spot.is_occupied ? 'Occupied' : 'Available' }}
                        </span>
                    </p>
                </div>
            </div>
        </div>
    </div>

    <div v-else class="error-container">
        <h2>Oops! Something went wrong</h2>
        <p>We couldn't load the parking lot data.</p>
        <button @click="goBack" class="btn btn-secondary">Go Back</button>
    </div>

    <!-- Delete Confirmation Modal -->
    <div v-if="showDeleteModal" class="modal-overlay" @click="cancelDelete">
        <div class="modal-content" @click.stop>
            <div class="modal-header">
                <h3>Confirm Delete</h3>
                <button @click="cancelDelete" class="close-btn">
                    <svg class="icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12">
                        </path>
                    </svg>
                </button>
            </div>
            <div class="modal-body">
                <div class="warning-icon">
                    <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.732-.833-2.5 0L3.34 16.5c-.77.833.192 2.5 1.732 2.5zs">
                        </path>
                    </svg>
                </div>
                <p>Are you sure you want to delete <strong>"{{ lot?.prime_location_name }}"</strong>?</p>
                <p class="warning-text">This action cannot be undone. All parking spots and associated data will be
                    permanently deleted.</p>
            </div>
            <div class="modal-footer">
                <button @click="cancelDelete" class="btn btn-secondary">Cancel</button>
                <button @click="handleDelete" class="btn btn-danger" :disabled="deleteLoading">
                    <span v-if="deleteLoading" class="spinner-small"></span>
                    {{ deleteLoading ? 'Deleting...' : 'Delete' }}
                </button>
            </div>
        </div>
    </div>

    <!-- Book Spot Modal -->
    <div v-if="showBookSpotModal && !userStore.isAdmin" class="modal-overlay" @click="cancelBooking">
        <div class="modal-content" @click.stop>
            <div class="modal-header">
                <h3>Book your Spot</h3>
                <button @click="cancelBooking" class="close-btn">
                    <svg class="icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12">
                        </path>
                    </svg>
                </button>
            </div>
            <div class="modal-body">
                spot_id
                lot_id
                user_id
                vehicle_number
                booking_start_time
                booking_end_time
                anything else?
            </div>
            <div class="modal-footer">
                <button @click="cancelBooking" class="btn btn-secondary">Cancel</button>
                <button @click="handleBooking" class="btn btn-danger" :disabled="deleteLoading">
                    <span v-if="deleteLoading" class="spinner-small"></span>
                    {{ deleteLoading ? 'Deleting...' : 'Delete' }}
                </button>
            </div>
        </div>
    </div>

</template>

<style scoped></style>