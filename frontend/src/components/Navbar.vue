<script setup>
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { useRoute } from 'vue-router'
import { computed } from 'vue'

const router = useRouter()
const userStore = useUserStore()
const route = useRoute()

const goTo = (path) => {
    router.push(path)
}

const logout = () => {
    userStore.logout()
    router.push('/login')
}

const hideNavLinks = computed(() =>
    route.name === 'login' || route.name === 'signup'
)

</script>

<template>
    <nav class="navbar">
        <h1 @click="goTo('/dashboard')" class="nav-title">
            ParkEasy
        </h1>

        <div v-if="!hideNavLinks">
            <div class="nav-content">
                <span class="welcome-message"> Welcome
                    {{ userStore.isAdmin ? 'Admin' : userStore.details.name }}
                </span>

                <div class="nav-links">
                    <button @click="goTo('/dashboard')" class="nav-button">Home</button>
                    <button v-if="userStore.isAdmin" @click="goTo('/admin/users')" class="nav-button">Users</button>
                    <button v-if="userStore.isAdmin" @click="goTo('/admin/bookings')"
                        class="nav-button">Bookings</button>
                    <button @click="goTo('/summary')" class="nav-button">Summary</button>
                    <button @click="goTo('/edit-profile')" class="nav-button">Edit Profile</button>
                    <button @click="logout" class="nav-button logout-button">Logout</button>
                </div>
            </div>
        </div>
    </nav>
</template>

<style scoped>
.navbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1.5rem 2rem;
    background: #ffffff;
    border-bottom: 1px solid #e5e5e5;
}

.nav-title {
    cursor: pointer;
    font-size: 1.5rem;
    font-weight: 600;
    margin: 0;
    color: #1a1a1a;
    transition: opacity 0.2s ease;
}

.nav-title:hover {
    opacity: 0.7;
}

.nav-content {
    display: flex;
    align-items: center;
    gap: 2rem;
}

.welcome-message {
    font-size: 1.1rem;
    color: #666;
    font-weight: 400;
}

.nav-links {
    display: flex;
    gap: 0.5rem;
    align-items: center;
}

.nav-button {
    background: none;
    border: none;
    color: #666;
    cursor: pointer;
    padding: 0.5rem 1rem;
    border-radius: 6px;
    font-size: 1rem;
    font-weight: 400;
    transition: all 0.2s ease;
}

.nav-button:hover {
    background: #f5f5f5;
    color: #1a1a1a;
}

.logout-button {
    color: #dc2626;
}

.logout-button:hover {
    background: #fef2f2;
    color: #dc2626;
}

/* Responsive Design */
@media (max-width: 768px) {
    .navbar {
        flex-direction: column;
        gap: 1rem;
        padding: 1rem;
    }

    .nav-content {
        width: 100%;
        flex-direction: column;
        gap: 1rem;
    }

    .nav-links {
        flex-wrap: wrap;
        justify-content: center;
        gap: 0.25rem;
    }

    .nav-button {
        font-size: 0.85rem;
    }
}
</style>