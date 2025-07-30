<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import { useUserStore } from '@/stores/user'


const name = ref("");
const email = ref("");
const oldPassword = ref("");
const newPassword = ref("");
const errorMessage = ref("");
const successMessage = ref("");
const userStore = useUserStore()
// Load current user info
onMounted(async () => {
    try {
        const userResponse = await axios.get('/api/dashboard')
        userStore.setUserDetails(userResponse.data)
    } catch (error) {
        toast.error("Session Expired. Login Again.")
        userStore.logout()
        router.push('/login')
        return
    }
    try {
        const res = await axios.get("/api/whoami");
        name.value = res.data.name;
        email.value = res.data.email;
    } catch (err) {
        errorMessage.value = "Failed to load profile.";
    }
});

const handleSubmit = async () => {
    errorMessage.value = "";
    successMessage.value = "";

    try {
        const payload = {
            name: name.value,
            email: email.value,
            old_password: oldPassword.value,
            new_password: newPassword.value || null,
        };

        const res = await axios.put("/api/whoami", payload);
        successMessage.value = "Profile updated successfully!";
    } catch (err) {
        errorMessage.value = err.response?.data?.message || "Update failed!";
    }
};
</script>
<template>
    <div class="edit-profile-container">
        <h2>Edit Profile</h2>

        <form @submit.prevent="handleSubmit" class="edit-form">
            <div class="form-group">
                <label for="oldPassword">Current Password</label>
                <input type="password" id="oldPassword" v-model="oldPassword" required />
            </div>

            <div class="form-group">
                <label for="name">Name</label>
                <input type="text" id="name" v-model="name" required />
            </div>

            <div class="form-group">
                <label for="email">Email</label>
                <input type="email" id="email" v-model="email" required />
            </div>

            <div class="form-group">
                <label for="password">New Password (optional)</label>
                <input type="password" id="password" v-model="newPassword" />
            </div>

            <div class="button-group">
                <button type="submit">Save Changes</button>
            </div>

            <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
            <p v-if="successMessage" class="success">{{ successMessage }}</p>
        </form>
    </div>
</template>


<style scoped>
.edit-profile-container {
    max-width: 500px;
    margin: 40px auto;
    padding: 20px;
    background: #f8f8f8;
    border-radius: 8px;
    box-shadow: 0px 2px 6px rgba(0, 0, 0, 0.1);
}

h2 {
    text-align: center;
    margin-bottom: 20px;
}

.edit-form {
    display: flex;
    flex-direction: column;
}

.form-group {
    display: flex;
    flex-direction: column;
    margin-bottom: 15px;
}

label {
    margin-bottom: 5px;
    font-weight: bold;
}

input {
    padding: 8px;
    border: 1px solid #ccc;
    border-radius: 4px;
}

.button-group {
    display: flex;
    justify-content: center;
}

button {
    background: #007bff;
    color: white;
    padding: 10px 18px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 15px;
}

button:hover {
    background: #0056b3;
}

.error {
    color: red;
    text-align: center;
    margin-top: 10px;
}

.success {
    color: green;
    text-align: center;
    margin-top: 10px;
}
</style>
