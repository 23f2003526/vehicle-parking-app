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
    <div class="signup-container">
        <h2>Sign Up</h2>
        <form @submit.prevent="handleSubmit" class="signup-form">
            <div class="form-group">
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

<style scoped></style>
