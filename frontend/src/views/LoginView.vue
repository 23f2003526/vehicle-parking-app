<script setup>
import { reactive } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';
import { useToast } from 'vue-toastification';

const router = useRouter();
const toast = useToast();

const form = reactive({
  email: '',
  password: '',
});

const handleSubmit = async () => {
  if (!form.email || !form.password) {
    // console.error("Both field are required")
    toast.error('Both fields are required');
    return;
  }

  try {
    await axios.post('/api/login', form); // Replace with your real endpoint
    toast.success('Login successful!');
    router.push('/dashboard'); // Redirect after login
  } catch (error) {
    // console.error(error);
    toast.error('Login failed. Please check your credentials.');
  }
};
</script>

<template>
  <div class="login-container">
    <h2>Login</h2>
    <form @submit.prevent="handleSubmit" class="login-form">
      <div class="form-group">
        <label for="email">Email</label>
        <input id="email" v-model="form.email" type="email" placeholder="you@example.com" />
      </div>

      <div class="form-group">
        <label for="password">Password</label>
        <input id="password" v-model="form.password" type="password" placeholder="********" />
      </div>

      <button type="submit" class="submit-btn">Log In</button>
    </form>
  </div>
</template>

<style scoped></style>
