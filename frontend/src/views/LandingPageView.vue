<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const goToLogin = () => {
    router.push('/login')
}
const goToSignup = () => {
    router.push('/signup')
}
</script>

<template>
    <div class="landing-container">
        <section class="hero">
            <h2>Find and Reserve Parking in Seconds</h2>
            <p>Manage parking spots with ease and avoid last-minute hassles.</p>
            <button @click="goToSignup" class="cta-btn">Get Started</button>
        </section>
    </div>
</template>

<style scoped>
.landing-container {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
    background: #f8f9fa;
    color: #333;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* Navbar */
.navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 15px 30px;
    background: white;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
}

.logo {
    font-size: 1.5rem;
    font-weight: 600;
}

.nav-actions {
    display: flex;
    gap: 10px;
}

.nav-btn {
    background: transparent;
    border: 1px solid #007bff;
    padding: 6px 14px;
    border-radius: 4px;
    cursor: pointer;
    color: #007bff;
    font-size: 14px;
}

.nav-btn.primary {
    background: #007bff;
    color: white;
}

.nav-btn:hover {
    opacity: 0.85;
}

/* Hero section */
.hero {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 30px;
}

.hero h2 {
    font-size: 2rem;
    margin-bottom: 10px;
}

.hero p {
    font-size: 1rem;
    color: #666;
    max-width: 500px;
}

.cta-btn {
    margin-top: 20px;
    background: #007bff;
    border: none;
    padding: 10px 22px;
    color: white;
    font-size: 15px;
    border-radius: 4px;
    cursor: pointer;
}

.cta-btn:hover {
    background: #0056b3;
}
</style>
