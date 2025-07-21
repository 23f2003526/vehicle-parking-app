<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useToast } from 'vue-toastification'

const props = defineProps({
    lot: Object,      // Lot details object (required)
    spot: Object      // Spot details object (required)
})

const emit = defineEmits(['close', 'booked'])

const toast = useToast()

const vehicleList = ref([])
const selectedVehicle = ref('')
const isLoading = ref(false)
const error = ref(null)

onMounted(async () => {
    try {
        const res = await axios.get('/api/vehicles')
        vehicleList.value = res.data
    } catch (err) {
        console.error(err)
        error.value = 'Failed to load your vehicles.'
    }
})

const handleBook = async () => {
    if (!selectedVehicle.value) {
        error.value = 'Please select your vehicle.'
        return
    }

    isLoading.value = true
    try {
        await axios.post('/api/bookings', {
            vehicle_id: parseInt(selectedVehicle.value),
            spot_id: props.spot.spot_id,    // ✅ Should be spot.spot_id from lot summary
            start_time: new Date().toISOString(),
            end_time: null
        })
        toast.success('Booking started successfully.')
        emit('booked')
        emit('close')
    } catch (err) {
        console.error(err)
        error.value = err.response?.data?.message || 'Booking failed.'
    } finally {
        isLoading.value = false
    }
}

const showAddVehicle = ref(false)
const newVehiclePlate = ref('')
const newVehicleType = ref('')
const isAddingVehicle = ref(false)
const error2 = ref(null)

const handleAddVehicle = async () => {
    if (!newVehiclePlate.value || !newVehicleType.value) {
        toast.error('Please enter all details.')
        return
    }
    isAddingVehicle.value = true
    try {
        const res = await axios.post('/api/vehicles', {
            license_plate: newVehiclePlate.value,
            vehicle_type: newVehicleType.value
        })
        vehicleList.value.push(res.data)
        selectedVehicle.value = res.data.id
        showAddVehicle.value = false
        newVehiclePlate.value = ''
        newVehicleType.value = ''
        toast.success('Vehicle added successfully.')
    } catch (err) {
        console.error(err)
        error2.value = err.response?.data?.message || 'Vehicle Registration failed.'
        toast.error('Failed to add vehicle.')
    } finally {
        isAddingVehicle.value = false
    }
}

const handleSelectChange = () => {
    if (selectedVehicle.value === '__add_new__') {
        showAddVehicle.value = true
        selectedVehicle.value = ''  // Reset selection
    }
}
</script>

<template>
    <!-- Booking Modal -->
    <div v-if="!showAddVehicle" class="modal-overlay">
        <div class="modal-content">
            <div class="modal-header">
                <h3>Book Spot at {{ lot.prime_location_name }}</h3>
                <button class="close-btn" @click="emit('close')">×</button>
            </div>

            <div class="modal-body">
                <div v-if="error" class="error">{{ error }}</div>
                <p><strong>Spot Number:</strong> {{ spot.spot_number }} ({{ spot.spot_type || 'Standard' }})</p>

                <label for="vehicle">Select Your Vehicle:</label>
                <select id="vehicle" v-model="selectedVehicle" @change="handleSelectChange">
                    <option disabled value="">-- Select Vehicle --</option>
                    <option v-for="v in vehicleList" :key="v.id" :value="v.id">
                        {{ v.license_plate }} ({{ v.vehicle_type }})
                    </option>
                    <option value="__add_new__">+ Add New Vehicle</option>
                </select>
            </div>

            <div class="modal-footer">
                <button @click="emit('close')" class="btn btn-secondary">Cancel</button>
                <button @click="handleBook" class="btn btn-primary" :disabled="isLoading">
                    {{ isLoading ? 'Booking...' : 'Book Spot' }}
                </button>
            </div>
        </div>
    </div>

    <!-- Add Vehicle Modal -->
    <div v-else class="modal-overlay">
        <div class="modal-content">
            <div class="modal-header">
                <h3>Add a New Vehicle</h3>
                <button class="close-btn" @click="showAddVehicle = false">×</button>
            </div>

            <div class="modal-body">
                <input v-model="newVehiclePlate" placeholder="License Plate" />
                <input v-model="newVehicleType" placeholder="Vehicle Type" />
            </div>

            <div class="modal-footer">
                <button @click="handleAddVehicle" :disabled="isAddingVehicle">
                    {{ isAddingVehicle ? 'Adding...' : 'Add Vehicle' }}
                </button>
                <button @click="showAddVehicle = false" class="cancel-btn">Cancel</button>
            </div>
        </div>
    </div>
</template>


<style scoped>
.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
}

.modal-content {
    background: white;
    width: 350px;
    border-radius: 8px;
    overflow: hidden;
    animation: fadeIn 0.3s;
}

.modal-header {
    background: #333;
    color: white;
    padding: 10px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.modal-body {
    padding: 15px;
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.modal-footer {
    display: flex;
    justify-content: flex-end;
    gap: 10px;
    padding: 10px 15px;
    border-top: 1px solid #ddd;
}

.close-btn {
    background: none;
    border: none;
    color: white;
    font-size: 18px;
    cursor: pointer;
}

select,
button {
    padding: 6px 10px;
}

.error {
    color: red;
    font-size: 0.9rem;
}
</style>
