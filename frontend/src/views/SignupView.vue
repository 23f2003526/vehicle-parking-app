<script setup>
import { reactive } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';
import { useToast } from 'vue-toastification';

const router = useRouter();
const toast = useToast();

const form = reactive({
    name: '',
    email: '',
    password: '',
});

const handleSubmit = async () => {
    if (!form.name || !form.email || !form.password) {
        toast.error('All fields are required');
        return;
    }

    try {
        await axios.post('/api/signup', form); // Replace with your backend route
        toast.success('Signup successful!');
        router.push('/login');
    } catch (error) {
        console.error(error);
        toast.error('Signup failed. Try again.');
    }
};
</script>

<template>
    <div class="container">
        <form @submit.prevent="handleSubmit" class="form">
            <div class="form-group">
                <h2>Sign Up</h2>
                <label for="name">Name</label>
                <input id="name" v-model="form.name" type="text" placeholder="Your Name" />
            </div>

            <div class="form-group">
                <label for="email">Email</label>
                <input id="email" v-model="form.email" type="email" placeholder="you@example.com" />
            </div>

            <div class="form-group">
                <label for="password">Password</label>
                <input id="password" v-model="form.password" type="password" placeholder="********" />
            </div>

            <button type="submit" class="submit-btn">Sign Up</button>
        </form>
    </div>
</template>

<style scoped>
.container {
    min-height: calc(100vh - 76px);
    display: flex;
    align-items: center;
    justify-content: center;
    background: #f8f9fa;
}

.form {
    background: white;
    padding: 2rem;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    width: 100%;
    max-width: 320px;
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

button:hover {
    background: #0056b3;
}

button:active {
    transform: translateY(1px);
}
</style>
