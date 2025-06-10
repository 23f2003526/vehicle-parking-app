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

    if (loading.value) return; // Prevent double submission

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
        <h2>Create New Parking Lot</h2>
        <form @submit.prevent="handleSubmit" class="signup-form">
            <div class="form-group">
                <label for="prime_location_name">Prime Location Name</label>
                <input id="prime_location_name" v-model="form.prime_location_name" type="text"
                    placeholder="Prime Location Name" :disabled="loading" />
            </div>

            <div class="form-group">
                <label for="address">Address</label>
                <input id="address" v-model="form.address" type="text" placeholder="Enter Address"
                    :disabled="loading" />
            </div>

            <div class="form-group">
                <label for="pincode">PIN Code</label>
                <input id="pincode" v-model="form.pin_code" type="text" maxlength="6"
                    placeholder="Enter 6-digit PIN code" :disabled="loading" />
            </div>

            <div class="form-group">
                <label for="price">Price per hour</label>
                <input id="price" v-model="form.price" type="number" step="1" min="0" placeholder="Enter price"
                    :disabled="loading" />
            </div>

            <div class="form-group">
                <label for="number_of_spots">Number of spots</label>
                <input id="number_of_spots" v-model="form.number_of_spots" type="number" min="1"
                    placeholder="Enter number of spots" :disabled="loading" />
            </div>

            <button type="submit" class="submit-btn" :disabled="loading">
                {{ loading ? 'Creating...' : 'Create Parking Lot' }}
            </button>
        </form>
    </div>
</template>

<style scoped></style>