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
    CategoryScale,
    BarElement,
    LinearScale,
    PointElement,
    Filler
} from 'chart.js'
import { Line, Bar } from 'vue-chartjs'

ChartJS.register(Title, Tooltip, Legend, LineElement, CategoryScale, BarElement, LinearScale, PointElement, Filler)

const bookings = ref([])
const isLoading = ref(false)
const userStore = useUserStore()

onMounted(async () => {
    isLoading.value = true
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
        const res = await axios.get('/api/admin/bookings')
        bookings.value = res.data
    } catch (err) {
        console.error('Failed to fetch bookings', err)
    } finally {
        isLoading.value = false
    }
})



/** Bookings Over Time - Line Chart */
const lineChartData = computed(() => {
    const counts = {}
    bookings.value.forEach(b => {
        const date = b.start_time.split('T')[0]
        counts[date] = (counts[date] || 0) + 1
    })

    const labels = Object.keys(counts).sort()
    const data = labels.map(date => counts[date])

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


/** Popular Parking Lots - Bar Chart */
const barChartData = computed(() => {
    const counts = {}
    bookings.value.forEach(b => {
        const lot = b.location_name || 'Unknown'
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
        legend: { display: true, position: 'bottom' }
    },
    scales: {
        y: { beginAtZero: true }
    }
}
</script>

<template>
    <div>
        <div class="chart-container">
            <h3>Bookings Over Time</h3>
            <div v-if="isLoading" class="loading">Loading...</div>
            <div v-else>
                <Line :data="lineChartData" :options="chartOptions" />
            </div>
        </div>

        <div class="chart-container">
            <h3>Most Popular Parking Lots</h3>
            <div v-if="isLoading" class="loading">Loading...</div>
            <div v-else>
                <Bar :data="barChartData" :options="chartOptions" />
            </div>
        </div>
    </div>
</template>

<style scoped>
.chart-container {
    background: #fff;
    padding: 20px;
    border-radius: 6px;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
}

.chart-container h3 {
    margin-bottom: 12px;
    font-size: 18px;
    font-weight: bold;
}

.loading {
    text-align: center;
    padding: 20px;
    font-size: 14px;
}
</style>