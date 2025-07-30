<!-- UserSummaryView.vue -->
<script setup>
import { useUserStore } from '@/stores/user'
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import {
    Chart as ChartJS,
    Title,
    Tooltip,
    Legend,
    LineElement,
    BarElement,
    CategoryScale,
    LinearScale,
    PointElement,
    Filler
} from 'chart.js'
import { Line as LineChart, Bar as BarChart } from 'vue-chartjs'

ChartJS.register(
    Title,
    Tooltip,
    Legend,
    LineElement,
    BarElement,
    CategoryScale,
    LinearScale,
    PointElement,
    Filler
)

const bookings = ref([])
const isLoading = ref(false)
const errorMsg = ref('')
const userStore = useUserStore()

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
    isLoading.value = true
    try {
        // Fetch the current user's bookings
        const res = await axios.get('/api/bookings')
        bookings.value = Array.isArray(res.data) ? res.data : []
    } catch (err) {
        console.error('Failed to fetch user bookings:', err)
        errorMsg.value = err.response?.data?.message || 'Failed to load bookings.'
    } finally {
        isLoading.value = false
    }
})

/** Bookings Over Time — Line Chart */
const lineChartData = computed(() => {
    const counts = {}

    bookings.value.forEach(b => {
        if (!b?.start_time) return
        const date = b.start_time.slice(0, 10) // YYYY-MM-DD
        counts[date] = (counts[date] || 0) + 1
    })

    const labels = Object.keys(counts).sort()
    const data = labels.map(d => counts[d])

    return {
        labels,
        datasets: [
            {
                label: 'Bookings',
                data,
                fill: true,
                borderColor: '#36A2EB',
                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                tension: 0.3,
                pointRadius: 4,
                pointBackgroundColor: '#36A2EB'
            }
        ]
    }
})

/** Popular Parking Lots — Bar Chart */
const barChartData = computed(() => {
    const counts = {}
    bookings.value.forEach(b => {
        const lot = b?.location_name || 'Unknown'
        counts[lot] = (counts[lot] || 0) + 1
    })

    const labels = Object.keys(counts)
    const data = labels.map(lot => counts[lot])

    return {
        labels,
        datasets: [
            {
                label: 'Total Bookings',
                data,
                backgroundColor: '#FF6384'
            }
        ]
    }
})

const chartOptions = {
    responsive: true,
    plugins: {
        legend: { display: true, position: 'bottom' },
        tooltip: { intersect: false, mode: 'index' }
    },
    scales: {
        y: { beginAtZero: true, ticks: { precision: 0 } }
    }
}
</script>

<template>
    <div class="summary-page">
        <h2 class="page-title">Your Parking Summary</h2>

        <div v-if="isLoading" class="loading">Loading charts…</div>
        <div v-else-if="errorMsg" class="error">{{ errorMsg }}</div>
        <div v-else>
            <div class="chart-card">
                <h3 class="chart-title">Bookings Over Time</h3>
                <div v-if="!lineChartData.labels.length" class="placeholder">
                    No booking data available yet.
                </div>
                <div v-else>
                    <LineChart :data="lineChartData" :options="chartOptions" />
                </div>
            </div>

            <div class="chart-card">
                <h3 class="chart-title">Most Popular Parking Lots</h3>
                <div v-if="!barChartData.labels.length" class="placeholder">
                    No lot usage data available yet.
                </div>
                <div v-else>
                    <BarChart :data="barChartData" :options="chartOptions" />
                </div>
            </div>
        </div>
    </div>
</template>

<style>
.summary-page {
    max-width: 980px;
    margin: 0 auto;
    padding: 24px 16px;
}

.page-title {
    font-size: 22px;
    font-weight: 700;
    margin-bottom: 16px;
}

.chart-card {
    background: #fff;
    border: 1px solid #e7e7e7;
    border-radius: 6px;
    padding: 16px;
    margin-bottom: 24px;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.06);
}

.chart-title {
    margin: 0 0 12px 0;
    font-size: 16px;
    font-weight: 600;
}

.loading,
.error,
.placeholder {
    padding: 16px;
    text-align: center;
    font-size: 14px;
}

.error {
    color: #b00020;
    background: #fff2f2;
    border: 1px solid #ffd7d7;
    border-radius: 4px;
}
</style>
