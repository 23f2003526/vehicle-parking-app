<script setup>
import { computed, ref, onMounted } from 'vue'
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

const userStore = useUserStore()
const isAdmin = computed(() => userStore.isAdmin)

onMounted(async () => {

    try {
        const userResponse = await axios.get('/api/dashboard')
        userStore.setUserDetails(userResponse.data)
    } catch (error) {
        toast.error("Session Expired. Login Again.")
        userStore.logout()
        router.push('/login')
        return
    }

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

const showSpotModal = ref(false)
const selectedSpot = ref(null)

const showOccupiedModal = ref(false)
const occupiedDetails = ref(null)
const loadingOccupied = ref(false)

const openSpotModal = (spot) => {
    selectedSpot.value = spot
    showSpotModal.value = true
}

const closeSpotModal = () => {
    showSpotModal.value = false
    selectedSpot.value = null
}

const deleteSpot = async () => {
    try {
        await axios.delete(`/api/admin/lots/${id}/spots/${selectedSpot.value.spot_number}`)
        toast.success('Spot deleted successfully')
        closeSpotModal()
        location.reload()  // Or re-fetch lot data
    } catch (err) {
        toast.error(err.response?.data?.message || 'Failed to delete spot')
    }
}

const openOccupiedDetails = async () => {
    loadingOccupied.value = true
    try {
        const res = await axios.get(`/api/admin/lots/${id}/spots/${selectedSpot.value.spot_number}/active-booking`)
        occupiedDetails.value = res.data
        // console.log(occupiedDetails.value)
        showOccupiedModal.value = true
    } catch (err) {
        toast.error(err.response?.data?.message || 'Failed to fetch occupied details')
    } finally {
        loadingOccupied.value = false
    }
}

const openReservedDetails = async () => {
    loadingOccupied.value = true
    try {
        const res = await axios.get(
            `/api/admin/lots/${id}/spots/${selectedSpot.value.spot_number}/active-reservation`
        )
        occupiedDetails.value = res.data
        showOccupiedModal.value = true
    } catch (err) {
        toast.error(
            err.response?.data?.message || 'Failed to fetch reserved details'
        )
    } finally {
        loadingOccupied.value = false
    }
}


const closeOccupiedModal = () => {
    showOccupiedModal.value = false
    occupiedDetails.value = null
}

</script>

<template>
    <div class="container">
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
                    <button @click="goBack" class="btn btn-secondary">← Back</button>
                    <button v-if="isAdmin" @click="handleEdit" class="btn btn-primary">Edit</button>
                    <!-- disappears when I reload -->
                    <button v-if="isAdmin" @click="confirmDelete" class="btn btn-danger" :disabled="deleteLoading">
                        Delete
                    </button>
                    <!-- disappears when I reload -->
                </div>
            </div>

            <!-- Lot details -->
            <div class="details-section">
                <div class="detail-card">
                    <h3>Pricing</h3>
                    <p class="price">₹{{ lot.price }}/hr</p>
                </div>
                <div class="detail-card">
                    <h3>Capacity</h3>
                    <div class="capacity-stats">
                        <div class="stat">
                            <span class="stat-value">{{ lot.number_of_spots }}</span>
                            <span class="stat-label">Total</span>
                        </div>
                        <div class="stat">
                            <span class="stat-value available">{{ lot.available_spots }}</span>
                            <span class="stat-label">Available</span>
                        </div>
                        <div class="stat">
                            <span class="stat-value occupied">{{ lot.occupied_spots }}</span>
                            <span class="stat-label">Occupied</span>
                        </div>
                        <div class="stat">
                            <span class="stat-value reserved">{{ lot.reserved_spots }}</span>
                            <span class="stat-label">Reserved</span>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Spots grid -->
            <div class="spots-section">
                <h3>Parking Spots</h3>
                <div class="spots-grid">
                    <div v-for="spot in lot.spots" :key="spot.spot_id" class="spot-card" :class="{
                        occupied: spot.status === 'occupied',
                        available: spot.status === 'available',
                        reserved: spot.status === 'reserved'
                    }" @click="openSpotModal(spot)">

                        <div class="spot-number">{{ spot.spot_number }}</div>
                        <div class="spot-type">{{ spot.spot_type }}</div>
                        <div class="spot-status" :class="{
                            'status-occupied': spot.status === 'occupied',
                            'status-available': spot.status === 'available',
                            'status-reserved': spot.status === 'reserved'
                        }">
                            {{ spot.status }}
                        </div>
                    </div>
                </div>
            </div>

        </div>

        <div v-else class="error-container">
            <h2>Unable to load parking lot</h2>
            <p>Please try again later</p>
            <button @click="goBack" class="btn btn-secondary">Go Back</button>
        </div>

        <!-- Delete Confirmation Modal -->
        <div v-if="showDeleteModal" class="modal-overlay" @click="cancelDelete">
            <div class="modal-content" @click.stop>
                <div class="modal-header">
                    <h3>Delete Parking Lot</h3>
                    <button @click="cancelDelete" class="close-btn">×</button>
                </div>
                <div class="modal-body">
                    <p>Are you sure you want to delete <strong>"{{ lot?.prime_location_name }}"</strong>?</p>
                    <p class="warning-text">This action cannot be undone.</p>
                </div>
                <div class="modal-footer">
                    <button @click="cancelDelete" class="btn btn-secondary">Cancel</button>
                    <button @click="handleDelete" class="btn btn-danger" :disabled="deleteLoading">
                        {{ deleteLoading ? 'Deleting...' : 'Delete' }}
                    </button>
                </div>
            </div>
        </div>
    </div>

    <!-- Spot Details Modal -->
    <div v-if="showSpotModal" class="modal-overlay" @click="closeSpotModal">
        <div class="modal-content" @click.stop>
            <div class="modal-header">
                <h3>Spot Details</h3>
                <button @click="closeSpotModal" class="close-btn">×</button>
            </div>
            <div class="modal-body">
                <p><strong>Spot ID:</strong> {{ selectedSpot.spot_id }}</p>
                <p>
                    <strong>Status:</strong>
                    <template v-if="selectedSpot.status === 'occupied'">
                        <span @click="openOccupiedDetails" class="">
                            Occupied <span class="link">(Click for Details)</span>
                        </span>
                    </template>
                    <template v-else-if="selectedSpot.status === 'reserved'">
                        <span @click="openReservedDetails" class="">
                            Reserved <span class="link">(Click for Details)</span>
                        </span>
                    </template>
                    <template v-else>
                        Available
                    </template>
                </p>
            </div>
            <div class="modal-footer">
                <button @click="deleteSpot" class="btn btn-danger">Delete Spot</button>
                <button @click="closeSpotModal" class="btn btn-secondary">Close</button>
            </div>
        </div>
    </div>


    <!-- Occupied Details Modal -->
    <div v-if="showOccupiedModal" class="modal-overlay" @click="closeOccupiedModal">
        <div class="modal-content" @click.stop>
            <div class="modal-header">
                <h3>Occupied Spot Details</h3>
                <button @click="closeOccupiedModal" class="close-btn">×</button>
            </div>
            <div class="modal-body" v-if="!loadingOccupied">
                <p><span>Spot ID:</span> {{ occupiedDetails.spot_id }}</p>
                <p><span>Customer ID:</span> {{ occupiedDetails.customer_id }}</p>
                <p><span>Vehicle No.:</span> {{ occupiedDetails.vehicle_number }}</p>
                <p><span>Parking Since:</span> {{ new Date(occupiedDetails.start_time).toLocaleString() }}</p>
                <p><span>Cost:</span> ₹{{ occupiedDetails.estimated_cost }}</p>
            </div>
            <div v-else>
                Loading occupied details...
            </div>
            <div class="modal-footer">
                <button @click="closeOccupiedModal" class="btn btn-secondary">Close</button>
            </div>
        </div>
    </div>


</template>

<style scoped>
.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem;
}

/* Loading State */
.loading-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 4rem;
    color: #666;
}

.spinner {
    width: 24px;
    height: 24px;
    border: 2px solid #e5e5e5;
    border-top: 2px solid #666;
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin-bottom: 1rem;
}

@keyframes spin {
    0% {
        transform: rotate(0deg);
    }

    100% {
        transform: rotate(360deg);
    }
}

/* Header Section */
.header-section {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 2rem;
    padding-bottom: 1.5rem;
    border-bottom: 1px solid #e5e5e5;
}

.header-info h2 {
    margin: 0 0 0.5rem 0;
    font-size: 1.75rem;
    font-weight: 600;
    color: #1a1a1a;
}

.address {
    margin: 0;
    color: #666;
    font-size: 1rem;
}

.action-buttons {
    display: flex;
    gap: 0.75rem;
}

/* Buttons */
.btn {
    padding: 0.75rem 1.25rem;
    border: none;
    border-radius: 6px;
    font-size: 0.9rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
}

.btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.btn-primary {
    background: #1a1a1a;
    color: white;
}

.btn-primary:hover:not(:disabled) {
    background: #333;
}

.btn-secondary {
    background: #f5f5f5;
    color: #666;
}

.btn-secondary:hover:not(:disabled) {
    background: #e5e5e5;
    color: #333;
}

.btn-danger {
    background: #dc2626;
    color: white;
}

.btn-danger:hover:not(:disabled) {
    background: #b91c1c;
}

/* Details Section */
.details-section {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1.5rem;
    margin-bottom: 2rem;
}

.detail-card {
    border: 1px solid #e5e5e5;
    border-radius: 8px;
    padding: 1.5rem;
}

.detail-card h3 {
    margin: 0 0 1rem 0;
    font-size: 1.125rem;
    font-weight: 500;
    color: #1a1a1a;
}

.price {
    margin: 0;
    font-size: 1.5rem;
    font-weight: 600;
    color: #1a1a1a;
}

.capacity-stats {
    display: flex;
    gap: 1.5rem;
}

.stat {
    display: flex;
    flex-direction: column;
    align-items: center;
}

.stat-value {
    font-size: 1.25rem;
    font-weight: 600;
    color: #1a1a1a;
}

.stat-value.available {
    color: #059669;
}

.stat-value.occupied {
    color: #dc2626;
}

.stat-value.reserved {
    color: #FFD700;
}

.stat-label {
    font-size: 0.9rem;
    color: #666;
    margin-top: 0.25rem;
}

/* Spots Section */
.spots-section h3 {
    margin: 0 0 1.5rem 0;
    font-size: 1.4rem;
    font-weight: 500;
    color: #1a1a1a;
}

.spots-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
    gap: 1rem;
}

.spot-card {
    border: 1px solid #e5e5e5;
    border-radius: 8px;
    padding: 1.5rem;
    text-align: center;
    transition: all 0.2s ease;
}

.spot-card.available {
    cursor: pointer;
}

.spot-card.available:hover {
    border-color: #d0d0d0;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.spot-card.occupied {
    background: #fafafa;
    opacity: 0.7;
}

.spot-card.reserved {
    cursor: pointer;
}

.spot-number {
    font-size: 1.2rem;
    font-weight: 600;
    color: #1a1a1a;
    margin-bottom: 0.5rem;
}

.spot-type {
    font-size: 0.9rem;
    color: #666;
    margin-bottom: 0.5rem;
}

.spot-status {
    font-size: 0.9rem;
    font-weight: 500;
    padding: 0.25rem 0.5rem;
    border-radius: 12px;
}

.status-available {
    background: #d1fae5;
    color: #065f46;
}

.status-occupied {
    background: #fee2e2;
    color: #991b1b;
}

.status-reserved {
    background: #f8efb9;
    color: #ff9100;
}

/* Error State */
.error-container {
    text-align: center;
    padding: 4rem 2rem;
    color: #666;
}

.error-container h2 {
    margin: 0 0 0.5rem 0;
    font-size: 1.5rem;
    font-weight: 500;
    color: #1a1a1a;
}

/* Modal */
.modal-overlay {
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.4);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
}

.modal-content {
    background: white;
    border-radius: 8px;
    width: 90%;
    max-width: 500px;
    max-height: 90vh;
    overflow-y: auto;
}

.modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1.5rem;
    border-bottom: 1px solid #e5e5e5;
}

.modal-header h3 {
    margin: 0;
    font-size: 1.25rem;
    font-weight: 600;
    color: #1a1a1a;
}

.close-btn {
    background: none;
    border: none;
    font-size: 1.5rem;
    color: #666;
    cursor: pointer;
    padding: 0;
    width: 24px;
    height: 24px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.close-btn:hover {
    color: #333;
}

.modal-body {
    padding: 1.5rem;
}

.modal-body p {
    margin: 8px 0;
    font-size: 1rem;
    line-height: 1.4;
}

.modal-body span:first-child {
    /* color: #666; */
    margin-right: 8px;
}

.link {
    color: #0066cc;
    cursor: pointer;
    text-decoration: underline;
}

.warning-text {
    color: #666;
    font-size: 0.9rem;
    margin: 0.5rem 0 0 0;
}

.modal-footer {
    display: flex;
    justify-content: flex-end;
    gap: 0.75rem;
    padding: 1.5rem;
    border-top: 1px solid #e5e5e5;
}

/* Responsive Design */
@media (max-width: 768px) {
    .container {
        padding: 1rem;
    }

    .header-section {
        flex-direction: column;
        gap: 1rem;
    }

    .action-buttons {
        align-self: flex-start;
    }

    .details-section {
        grid-template-columns: 1fr;
    }

    .capacity-stats {
        justify-content: space-around;
    }

    .spots-grid {
        grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
    }
}

@media (max-width: 480px) {
    .action-buttons {
        flex-direction: column;
        width: 100%;
    }

    .btn {
        width: 100%;
        justify-content: center;
    }

    .spots-grid {
        grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
    }
}
</style>