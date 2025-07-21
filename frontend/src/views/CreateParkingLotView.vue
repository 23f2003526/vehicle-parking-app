<script setup>
import { reactive, ref } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';
import { useToast } from 'vue-toastification';

const router = useRouter();
const toast = useToast();
const loading = ref(false);

const form = reactive({
    prime_location_name: '',
    address: '',
    pin_code: '',
    price: '',
    number_of_spots: ''
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

        const response = await axios.post('/api/admin/lots', payload);
        toast.success(`Parking Lot created successfully! ID: ${response.data.lot_id}`);

        Object.keys(form).forEach(key => form[key] = '');
        router.push('/dashboard');
    } catch (error) {
        console.error(error);
        const errorMessage = error.response?.data?.message || 'Error while creating Parking Lot';
        toast.error(errorMessage);
    } finally {
        loading.value = false;
    }
};
</script>

<template>
    <div class="container">
        <form @submit.prevent="handleSubmit" class="form">
            <h2>Create Parking Lot</h2>

            <input v-model="form.prime_location_name" type="text" placeholder="Prime Location Name" :disabled="loading"
                required />

            <input v-model="form.address" type="text" placeholder="Address" :disabled="loading" required />

            <input v-model="form.pin_code" type="text" maxlength="6" placeholder="PIN Code" :disabled="loading"
                required />

            <input v-model="form.price" type="number" step="1" min="0" placeholder="Price per hour" :disabled="loading"
                required />

            <input v-model="form.number_of_spots" type="number" min="1" placeholder="Number of spots"
                :disabled="loading" required />

            <button type="submit" :disabled="loading">
                {{ loading ? 'Creating...' : 'Create Parking Lot' }}
            </button>
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

.form {
    background: white;
    padding: 2rem;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    width: 100%;
    max-width: 400px;
}

h2 {
    margin: 0 0 1.5rem;
    font-size: 1.5rem;
    font-weight: 500;
    text-align: center;
    color: #333;
}

input {
    width: 100%;
    padding: 0.75rem;
    margin-bottom: 1rem;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 1rem;
    transition: border-color 0.2s;
    box-sizing: border-box;
}

input:focus {
    outline: none;
    border-color: #007bff;
}

input:disabled {
    background: #f8f9fa;
    color: #6c757d;
    cursor: not-allowed;
}

button {
    width: 100%;
    padding: 0.75rem;
    background: #007bff;
    color: white;
    border: none;
    border-radius: 4px;
    font-size: 1rem;
    cursor: pointer;
    transition: background-color 0.2s;
}

button:hover:not(:disabled) {
    background: #0056b3;
}

button:disabled {
    background: #6c757d;
    cursor: not-allowed;
}
</style>