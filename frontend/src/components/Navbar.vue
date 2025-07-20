<script setup>
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()

const goTo = (path) => {
    router.push(path)
}

const logout = () => {
    userStore.logout()
    router.push('/login')
}
</script>

<template>
    <nav class="navbar">
        <h1 @click="goTo('/dashboard')" class="nav-title">
            ParkEasy
        </h1>

        <div class="nav-links">
            <span class="welcome-message">
                Welcome {{ userStore.isAdmin ? 'Admin' : userStore.details.name }}
            </span>

            <button @click="goTo('/dashboard')">Home</button>

            <button v-if="userStore.isAdmin" @click="goTo('/users')">Users</button>
            <button v-if="userStore.isAdmin" @click="goTo('/search')">Search</button>

            <button @click="goTo('/summary')">Summary</button>

            <button @click="goTo('/edit-profile')">Edit Profile</button>

            <button @click="logout">Logout</button>
        </div>
    </nav>
</template>

<style scoped>
.navbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 10px 20px;
    background: #333;
    color: white;
}

.nav-title {
    cursor: pointer;
}

.nav-links {
    display: flex;
    gap: 10px;
    /* border: 2px solid red; */
}

button {
    background: transparent;
    border: none;
    color: white;
    cursor: pointer;
}

button:hover {
    text-decoration: underline;
}

.welcome-message {
    margin-right: 15px;
}
</style>
