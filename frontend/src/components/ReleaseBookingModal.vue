<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useToast } from 'vue-toastification'
import { computed } from 'vue'

const props = defineProps({
    booking: Object,
    hourlyRate: Number  // Pass from lot.price if you want
})

const emit = defineEmits(['close', 'released'])

const toast = useToast()

const releaseTime = ref(new Date())
const isLoading = ref(false)
const error = ref(null)

const totalCost = computed(() => {
    const start = new Date(props.booking.start_time)
    const end = releaseTime.value
    const hours = Math.ceil((end - start) / (1000 * 60 * 60))
    // console.log(props.price)
    return hours * props.hourlyRate
})

const costBreakdown = computed(() => {
    const start = new Date(props.booking.start_time)
    const end = releaseTime.value
    const hours = Math.ceil((end - start) / (1000 * 60 * 60))
    return `${hours} hour(s) × ₹${props.hourlyRate} = ₹${hours * props.hourlyRate}`
})

const handleRelease = async () => {
    isLoading.value = true
    try {
        await axios.patch(`/api/bookings/${props.booking.id}/release`)
        toast.success('Booking released successfully.')
        emit('released')
        emit('close')
    } catch (err) {
        console.error(err)
        error.value = err.response?.data?.message || 'Release failed.'
    } finally {
        isLoading.value = false
    }
}
</script>

<template>
    <div class="modal-overlay">
        <div class="modal-content">
            <div class="modal-header">
                <h3>Release Booking</h3>
                <button class="close-btn" @click="emit('close')">×</button>
            </div>

            <div class="modal-body">
                <div v-if="error" class="error">{{ error }}</div>

                <p><strong>Spot Number:</strong> {{ booking.spot_number }}</p>
                <p><strong>Vehicle Number:</strong> {{ booking.vehicle_number }}</p>
                <p><strong>Parking Start Time:</strong> {{ new Date(booking.start_time).toLocaleString() }}</p>
                <p><strong>Release Time:</strong> {{ releaseTime.toLocaleString() }}</p>
                <p><strong>Total Cost:</strong> ₹{{ totalCost }}</p>
                <p><em>{{ costBreakdown }}</em></p>
            </div>

            <div class="modal-footer">
                <button class="btn-secondary" @click="emit('close')">Cancel</button>
                <button class="btn-primary" @click="handleRelease" :disabled="isLoading">
                    {{ isLoading ? 'Releasing...' : 'Release' }}
                </button>
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
    background: #fff;
    width: 400px;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
    animation: fadeIn 0.3s ease;
}

.modal-header {
    background: #f5f5f5;
    padding: 15px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid #ddd;
}

.modal-header h3 {
    margin: 0;
    font-size: 18px;
}

.close-btn {
    background: none;
    border: none;
    font-size: 20px;
    cursor: pointer;
}

.modal-body {
    padding: 15px;
}

.modal-body p {
    margin: 8px 0;
}

.error {
    color: red;
    margin-bottom: 10px;
}

.modal-footer {
    display: flex;
    justify-content: flex-end;
    padding: 15px;
    gap: 10px;
    border-top: 1px solid #ddd;
}

.btn-secondary,
.btn-primary {
    padding: 6px 12px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

.btn-secondary {
    background: #ccc;
}

.btn-secondary:hover {
    background: #bbb;
}

.btn-primary {
    background: #007bff;
    color: white;
}

.btn-primary:hover {
    background: #0056b3;
}

@keyframes fadeIn {
    from {
        opacity: 0;
        transform: scale(0.95);
    }

    to {
        opacity: 1;
        transform: scale(1);
    }
}
</style>
