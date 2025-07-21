<script setup>
import { onMounted, reactive, ref } from 'vue';
import axios from 'axios';
import { useRoute, useRouter } from 'vue-router';
import { useToast } from 'vue-toastification';

const router = useRouter();
const toast = useToast();
const loading = ref(true);
const route = useRoute();

const id = route.params.id;

const form = reactive({
    prime_location_name: '',
    address: '',
    pin_code: '',
    price: '',
    number_of_spots: ''
});

onMounted(async () => {
    try {
        const response = await axios.get(`/api/admin/lots/${id}`);
        form.prime_location_name = response.data.prime_location_name;
        form.address = response.data.address;
        form.pin_code = response.data.pin_code;
        form.price = response.data.price;
        form.number_of_spots = response.data.number_of_spots;
    } catch (error) {
        console.error('Error fetching lot details:', error);
        toast.error('Failed to load parking lot data');
        router.push(`/admin/lots/${id}`);
    } finally {
        loading.value = false;
    }
});

const validateForm = () => {
    if (!form.prime_location_name.trim()) {
        toast.error('Prime location name is required');
        return false;
    }
    if (!form.address.trim()) {
        toast.error('Address is required');
        return false;
    }
    if (!form.pin_code || !/^\d{6}$/.test(form.pin_code)) {
        toast.error('PIN code must be exactly 6 digits');
        return false;
    }
    if (!form.price || parseFloat(form.price) <= 0) {
        toast.error('Price must be greater than 0');
        return false;
    }
    if (!form.number_of_spots || parseInt(form.number_of_spots) <= 0) {
        toast.error('Number of spots must be greater than 0');
        return false;
    }
    return true;
};

const handleSubmit = async () => {
    if (!validateForm()) return;
    if (loading.value) return;

    loading.value = true;

    try {
        const payload = {
            ...form,
            price: parseFloat(form.price),
            number_of_spots: parseInt(form.number_of_spots)
        };

        await axios.put(`/api/admin/lots/${id}`, payload);
        toast.success(`Parking Lot updated successfully! ID: ${id}`);
        router.push(`/lots/${id}`);
    } catch (error) {
        console.error(error);
        const errorMessage = error.response?.data?.message || 'Error while updating parking lot';
        toast.error(errorMessage);
    } finally {
        loading.value = false;
    }
};
</script>

<template>
    <div class="container">
        <div v-if="loading" class="loading">
            <div class="spinner"></div>
            <p>Loading...</p>
        </div>

        <form v-else @submit.prevent="handleSubmit" class="form">
            <h2>Edit Parking Lot</h2>

            <label for="prime_location_name">Prime Location Name</label>
            <input v-model="form.prime_location_name" type="text" placeholder="Prime Location Name" required />

            <label for="address">Address</label>
            <textarea v-model="form.address" placeholder="Address" rows="3" required></textarea>

            <div class="row">
                <label for="pincode">PIN Code</label>
                <input v-model="form.pin_code" type="text" maxlength="6" placeholder="PIN Code" required />

                <label for="price">Price per Hour (₹)</label>
                <input v-model="form.price" type="number" step="1" min="0" placeholder="Price (₹)" required />
            </div>

            <label for="number_of_spots">Number of Parking Spots</label>
            <input v-model="form.number_of_spots" type="number" min="1" placeholder="Number of Spots" required />

            <div class="actions">
                <button type="button" @click="router.go(-1)" class="cancel">
                    Cancel
                </button>
                <button type="submit" :disabled="loading">
                    {{ loading ? 'Updating...' : 'Update' }}
                </button>
            </div>
        </form>
    </div>
</template>

<style scoped>
.container {
    min-height: calc(100vh - 83px);
    display: flex;
    align-items: center;
    justify-content: center;
    background: #f8f9fa;
    padding: 1rem;
}

.loading {
    background: white;
    padding: 2rem;
    border-radius: 8px;
    text-align: center;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.spinner {
    width: 24px;
    height: 24px;
    border: 2px solid #ddd;
    border-top: 2px solid #007bff;
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin: 0 auto 1rem;
}

@keyframes spin {
    to {
        transform: rotate(360deg);
    }
}

.form {
    background: white;
    padding: 2rem;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    width: 100%;
    max-width: 480px;
}

h2 {
    margin: 0 0 1.5rem;
    font-size: 1.5rem;
    font-weight: 500;
    color: #333;
}

input,
textarea {
    width: 100%;
    padding: 0.75rem;
    margin-bottom: 1rem;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 1rem;
    transition: border-color 0.2s;
    box-sizing: border-box;
    font-family: inherit;
}

input:focus,
textarea:focus {
    outline: none;
    border-color: #007bff;
}

textarea {
    resize: vertical;
    min-height: 80px;
}

.row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
    margin-bottom: 1rem;
}

.row input {
    margin-bottom: 0;
}

.actions {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
    margin-top: 1rem;
}

button {
    padding: 0.75rem;
    border: none;
    border-radius: 4px;
    font-size: 1rem;
    cursor: pointer;
    transition: all 0.2s;
    background: #007bff;
    color: white;
}

button:hover:not(:disabled) {
    background: #0056b3;
}

button:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}

.cancel {
    background: #6c757d;
    color: white;
}

.cancel:hover {
    background: #545b62;
}

@media (max-width: 480px) {
    .row {
        grid-template-columns: 1fr;
        gap: 0;
    }

    .row input {
        margin-bottom: 1rem;
    }

    .actions {
        grid-template-columns: 1fr;
    }
}
</style>