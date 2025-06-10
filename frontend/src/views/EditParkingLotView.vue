<script setup>
import { onMounted, reactive, ref } from 'vue';
import axios from 'axios';
import { useRoute, useRouter } from 'vue-router';
import { useToast } from 'vue-toastification';

const router = useRouter();
const toast = useToast();
const loading = ref(true);
const route = useRoute()


const id = route.params.id

const form = reactive({
    prime_location_name: '',
    address: '',
    pin_code: '',
    price: '',
    number_of_spots: ''
});

onMounted(async () => {
    try {
        const response = await axios.get(`/api/admin/lots/${id}`)
        form.prime_location_name = response.data.prime_location_name
        form.address = response.data.address
        form.pin_code = response.data.pin_code
        form.price = response.data.price
        form.number_of_spots = response.data.number_of_spots

    } catch (error) {
        console.error('Error fetching lot details:', error)
        toast.error('Failed to load parking lot data')
        router.push(`/admin/lots/${id}`)
    }
    finally {
        loading.value = false
    }
})
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

        await axios.put(`/api/admin/lots/${id}`, payload);
        toast.success(`Parking Lot updated successfully! ID: ${id}`);

        router.push(`/admin/lots/${id}`);
    } catch (error) {
        console.error(error);
        const errorMessage = error.response?.data?.message || 'Error while updating parking lot';
        toast.error(errorMessage);
    } finally {
        loading.value = false;
    }
};
</script>

<!-- <template>

    <div class="signup-container">
        <h2>Edit Parking Lot</h2>
        <form @submit.prevent="handleSubmit" class="signup-form">
            <div class="form-group">
                <label for="prime_location_name">Prime Location Name</label>
                <input id="prime_location_name" v-model="form.prime_location_name" type="text"
                    placeholder="Enter Prime Location Name" :disabled="loading" />
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
                {{ loading ? 'Editing...' : 'Edit Parking Lot' }}
            </button>
        </form>
    </div>
</template>

<style scoped></style> -->

<template>
    <div class="edit-container">
        <!-- Loading spinner for initial data fetch -->
        <div v-if="initialLoading" class="loading-spinner">
            <div class="spinner"></div>
            <p>Loading parking lot data...</p>
        </div>

        <!-- Main form -->
        <div v-else class="form-wrapper">
            <div class="header">
                <h2>Edit Parking Lot</h2>
                <p class="subtitle">Update parking lot information</p>
            </div>

            <form @submit.prevent="handleSubmit" class="edit-form">
                <div class="form-group">
                    <label for="prime_location_name">Prime Location Name</label>
                    <input id="prime_location_name" v-model="form.prime_location_name" type="text"
                        placeholder="Enter Prime Location Name" :disabled="loading" class="form-input" />
                </div>

                <div class="form-group">
                    <label for="address">Address</label>
                    <textarea id="address" v-model="form.address" placeholder="Enter full address" :disabled="loading"
                        class="form-input form-textarea" rows="3"></textarea>
                </div>

                <div class="form-row">
                    <div class="form-group">
                        <label for="pincode">PIN Code</label>
                        <input id="pincode" v-model="form.pin_code" type="text" maxlength="6" placeholder="6-digit PIN"
                            :disabled="loading" class="form-input" />
                    </div>

                    <div class="form-group">
                        <label for="price">Price per Hour (₹)</label>
                        <input id="price" v-model="form.price" type="number" step="1" min="0" placeholder="Enter price"
                            :disabled="loading" class="form-input" />
                    </div>
                </div>

                <div class="form-group">
                    <label for="number_of_spots">Number of Parking Spots</label>
                    <input id="number_of_spots" v-model="form.number_of_spots" type="number" min="1"
                        placeholder="Total parking spots available" :disabled="loading" class="form-input" />
                </div>

                <div class="form-actions">
                    <button type="button" @click="router.go(-1)" class="btn btn-secondary" :disabled="loading">
                        Cancel
                    </button>
                    <button type="submit" class="btn btn-primary" :disabled="loading">
                        <span v-if="loading" class="btn-spinner"></span>
                        {{ loading ? 'Updating...' : 'Update Parking Lot' }}
                    </button>
                </div>
            </form>
        </div>
    </div>
</template>

<style scoped>
.edit-container {
    min-height: 100vh;
    padding: 2rem;
    display: flex;
    align-items: center;
    justify-content: center;
}

.loading-spinner {
    background: white;
    padding: 3rem;
    border-radius: 12px;
    text-align: center;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

.spinner {
    width: 40px;
    height: 40px;
    border: 4px solid #f3f3f3;
    border-top: 4px solid #667eea;
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin: 0 auto 1rem;
}

@keyframes spin {
    0% {
        transform: rotate(0deg);
    }

    100% {
        transform: rotate(360deg);
    }
}

.form-wrapper {
    background: white;
    padding: 2.5rem;
    border-radius: 16px;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
    width: 100%;
    max-width: 600px;
}

.header {
    text-align: center;
    margin-bottom: 2rem;
}

.header h2 {
    color: #333;
    font-size: 2rem;
    margin-bottom: 0.5rem;
    font-weight: 700;
}

.subtitle {
    color: #666;
    font-size: 1rem;
    margin: 0;
}

.edit-form {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
}

.form-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
}

.form-group {
    display: flex;
    flex-direction: column;
}

.form-group label {
    color: #333;
    font-weight: 600;
    margin-bottom: 0.5rem;
    font-size: 0.9rem;
}

.form-input {
    padding: 0.875rem;
    border: 2px solid #e1e5e9;
    border-radius: 8px;
    font-size: 1rem;
    transition: all 0.3s ease;
    background: #fafafa;
}

.form-input:focus {
    outline: none;
    border-color: #667eea;
    background: white;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.form-input:disabled {
    background: #f5f5f5;
    color: #999;
    cursor: not-allowed;
}

.form-textarea {
    resize: vertical;
    min-height: 80px;
    font-family: inherit;
}

.form-actions {
    display: flex;
    gap: 1rem;
    margin-top: 1rem;
}

.btn {
    padding: 0.875rem 1.5rem;
    border: none;
    border-radius: 8px;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    flex: 1;
}

.btn:disabled {
    cursor: not-allowed;
    opacity: 0.6;
}

.btn-primary {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
}

.btn-primary:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
}

.btn-secondary {
    background: #f8f9fa;
    color: #666;
    border: 2px solid #e1e5e9;
}

.btn-secondary:hover:not(:disabled) {
    background: #e9ecef;
    border-color: #dee2e6;
}

.btn-spinner {
    width: 16px;
    height: 16px;
    border: 2px solid transparent;
    border-top: 2px solid currentColor;
    border-radius: 50%;
    animation: spin 1s linear infinite;
}

/* Responsive design */
@media (max-width: 768px) {
    .edit-container {
        padding: 1rem;
    }

    .form-wrapper {
        padding: 1.5rem;
    }

    .form-row {
        grid-template-columns: 1fr;
    }

    .form-actions {
        flex-direction: column;
    }

    .header h2 {
        font-size: 1.5rem;
    }
}

/* Input validation states */
.form-input:invalid {
    border-color: #dc3545;
}

.form-input:valid {
    border-color: #28a745;
}
</style>