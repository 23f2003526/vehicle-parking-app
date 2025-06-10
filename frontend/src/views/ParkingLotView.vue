<!-- <script setup>
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
</style> -->


<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useToast } from 'vue-toastification'
import axios from 'axios'

const route = useRoute()
const router = useRouter()
const toast = useToast()
const id = route.params.id

const lot = ref(null)
const loading = ref(true)
const deleteLoading = ref(false)
const showDeleteModal = ref(false)

onMounted(async () => {
    try {
        const response = await axios.get(`/api/admin/lots/${id}/summary`)
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
                <button @click="handleEdit" class="btn btn-primary">
                    ✎ Edit
                </button>
                <button @click="confirmDelete" class="btn btn-danger" :disabled="deleteLoading">
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
                    :class="spot.is_occupied ? 'occupied' : 'available'">
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
</template>

<style scoped>
.loading-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 60px 20px;
    color: #666;
}

.spinner {
    width: 40px;
    height: 40px;
    border: 4px solid #f3f3f3;
    border-top: 4px solid #3498db;
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin-bottom: 20px;
}

.spinner-small {
    width: 16px;
    height: 16px;
    border: 2px solid #ffffff;
    border-top: 2px solid transparent;
    border-radius: 50%;
    animation: spin 1s linear infinite;
    display: inline-block;
    margin-right: 8px;
}

@keyframes spin {
    0% {
        transform: rotate(0deg);
    }

    100% {
        transform: rotate(360deg);
    }
}

.lot-summary {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}

.header-section {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 30px;
    padding-bottom: 20px;
    border-bottom: 2px solid #eee;
}

.header-info h2 {
    margin: 0 0 8px 0;
    font-size: 2.2em;
    color: white;
}

.address {
    color: white;
    font-size: 1.1em;
    margin: 0;
}

.action-buttons {
    display: flex;
    gap: 12px;
    flex-wrap: wrap;
}

.btn {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 10px 16px;
    border: none;
    border-radius: 8px;
    font-size: 14px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
    text-decoration: none;
}

.btn:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}

.btn-primary {
    background-color: #3498db;
    color: white;
}

.btn-primary:hover:not(:disabled) {
    background-color: #2980b9;
}

.btn-secondary {
    background-color: #95a5a6;
    color: white;
}

.btn-secondary:hover:not(:disabled) {
    background-color: #7f8c8d;
}

.btn-danger {
    background-color: #e74c3c;
    color: white;
}

.btn-danger:hover:not(:disabled) {
    background-color: #c0392b;
}

.icon {
    width: 16px;
    height: 16px;
}

.details-section {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 20px;
    margin-bottom: 30px;
}

.detail-card {
    background: #f8f9fa;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #e9ecef;
    color: black;
}

.detail-card h3 {
    margin: 0 0 12px 0;
    color: #495057;
    font-size: 1.1em;
}

.price {
    font-size: 1.8em;
    font-weight: bold;
    color: #28a745;
    margin: 0;
}

.highlight {
    font-weight: bold;
    color: #333;
}

.available {
    color: #28a745;
    font-weight: bold;
}

.occupied {
    color: #dc3545;
    font-weight: bold;
}

.spots-section h3 {
    margin-bottom: 20px;
    color: white;
}

.spots-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 16px;
}

.spot-card {
    padding: 16px;
    border-radius: 12px;
    border: 2px solid #dee2e6;
    background-color: #ffffff;
    transition: all 0.2s ease;
    position: relative;
}

.spot-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.spot-card.available {
    border-color: #28a745;
    background-color: #f8fff8;
}

.spot-card.occupied {
    border-color: #dc3545;
    background-color: #fff8f8;
}

.spot-number {
    font-size: 1.5em;
    font-weight: bold;
    margin-bottom: 8px;
    color: #333;
}

.status {
    margin: 8px 0 0 0;
}

.status-available {
    color: #28a745;
    font-weight: bold;
}

.status-occupied {
    color: #dc3545;
    font-weight: bold;
}

.error-container {
    text-align: center;
    padding: 60px 20px;
    color: #666;
}

.error-container h2 {
    color: #dc3545;
    margin-bottom: 16px;
}

/* Modal Styles */
.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
}

.modal-content {
    background: white;
    border-radius: 12px;
    width: 90%;
    max-width: 500px;
    max-height: 90vh;
    overflow-y: auto;
}

.modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20px;
    border-bottom: 1px solid #eee;
}

.modal-header h3 {
    margin: 0;
    color: #333;
}

.close-btn {
    background: none;
    border: none;
    cursor: pointer;
    padding: 4px;
    color: #666;
    border-radius: 4px;
}

.close-btn:hover {
    background-color: #f1f1f1;
}

.modal-body {
    padding: 20px;
    text-align: center;
}

.warning-icon {
    width: 64px;
    height: 64px;
    margin: 0 auto 16px;
    color: #f39c12;
}

.warning-icon svg {
    width: 100%;
    height: 100%;
}

.warning-text {
    color: #666;
    font-size: 0.9em;
    margin-top: 12px;
}

.modal-footer {
    display: flex;
    justify-content: flex-end;
    gap: 12px;
    padding: 20px;
    border-top: 1px solid #eee;
}

/* Responsive Design */
@media (max-width: 768px) {
    .header-section {
        flex-direction: column;
        gap: 16px;
    }

    .action-buttons {
        justify-content: flex-start;
    }

    .details-section {
        grid-template-columns: 1fr;
    }

    .spots-grid {
        grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
    }
}
</style>