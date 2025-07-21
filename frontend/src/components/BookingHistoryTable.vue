<script setup>
defineProps({
    bookings: Array
})

const emit = defineEmits(['view-booking'])

// Duration in hours and minutes
function getDuration(start, end) {
    const startTime = new Date(start)
    const endTime = end ? new Date(end) : new Date()
    const diffMs = endTime - startTime
    const hours = Math.floor(diffMs / (1000 * 60 * 60))
    const minutes = Math.floor((diffMs % (1000 * 60 * 60)) / (1000 * 60))
    return `${hours}h ${minutes}m`
}

// Assuming price is per hour (pass it from backend with each booking)
function getCost(start, end, pricePerHour) {
    const startTime = new Date(start)
    const endTime = end ? new Date(end) : new Date()
    const diffHours = Math.ceil((endTime - startTime) / (1000 * 60 * 60))
    // console.log(diffHours)
    // console.log(pricePerHour);

    return diffHours * pricePerHour
}
</script>


<template>
    <div class="history-container">
        <h3>Recent Parking History</h3>
        <div class="table-wrapper" v-if="bookings.length">
            <table class="history-table">
                <thead>
                    <tr>
                        <th>Booking ID</th>
                        <th>Location</th>
                        <th>Spot Number</th>
                        <th>Vehicle No.</th>
                        <th>Start Time</th>
                        <th>End Time</th>
                        <th>Duration</th>
                        <th>Cost</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="b in bookings" :key="b.id">
                        <td>{{ b.id }}</td>
                        <td>{{ b.location_name }} ({{ b.address }})</td>
                        <td>{{ b.spot_number }}</td>
                        <td>{{ b.vehicle_number }}</td>
                        <td>{{ new Date(b.start_time).toLocaleString('en-GB', { hour12: false }) }}</td>
                        <td>
                            {{ b.end_time
                                ? new Date(b.end_time).toLocaleString('en-GB', { hour12: false })
                                : 'Active' }}
                        </td>
                        <td>
                            {{ getDuration(b.start_time, b.end_time) }}
                        </td>
                        <td>
                            ₹{{ getCost(b.start_time, b.end_time, b.price) }}
                        </td>
                        <td>
                            <button v-if="!b.end_time" @click="emit('view-booking', b)" class="release-btn">
                                Release
                            </button>
                            <span v-else class="parked-out">Parked Out</span>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
        <p v-else>No bookings found.</p>
    </div>
</template>

<style scoped>
.history-container {
    margin: 20px 0;
}

.history-table {
    width: 100%;
    border-collapse: collapse;
    background: #fff;
    border: 1px solid #ddd;
}

.history-table th,
.history-table td {
    padding: 10px;
    text-align: left;
    border-bottom: 1px solid #ddd;
}

.history-table th {
    background: #f5f5f5;
}

.release-btn {
    background: #007bff;
    color: white;
    border: none;
    padding: 6px 12px;
    cursor: pointer;
    border-radius: 4px;
}

.release-btn:hover {
    background: #0056b3;
}

.parked-out {
    color: #888;
    font-style: italic;
}

.table-wrapper {
    max-height: 400px;
    /* Around 10 rows */
    overflow-y: auto;
    border: 1px solid #ccc;
    margin-top: 15px;
}
</style>
