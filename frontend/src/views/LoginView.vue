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
    toast.error('Both fields are required');
    return;
  }

  try {
    await axios.post('/api/login', form);
    toast.success('Login successful!');
    router.push('/dashboard');
  } catch (error) {
    toast.error('Login failed. Please check your credentials.');
  }
};
</script>

<template>
  <div class="container">
    <form @submit.prevent="handleSubmit" class="form">
      <h2>Login</h2>

      <label for="email">Email</label>
      <input v-model="form.email" type="email" placeholder="Email" required />

      <label for="password">Password</label>
      <input v-model="form.password" type="password" placeholder="Password" required />

      <button type="submit">Log In</button>
      <router-link to="/signup" class="signup-link">
        Go to Signup instead
      </router-link>
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

.signup-link {
  display: block;
  margin-top: 10px;
  text-align: center;
  color: rgb(253, 100, 62);
  text-decoration: underline;
}
</style>