<script setup>
defineProps({
    lot: {
        type: Object,
        required: true
    }
})
</script>

<template>
    <h3 class="">{{ lot.prime_location_name }}</h3>
    <p>{{ lot.address }}, {{ lot.pin_code }}</p>
    <p>💲 ₹{{ lot.price }} per hour</p>
    <p> Occupied: {{ lot.occupied_spots }} / {{ lot.number_of_spots }} spots</p>

</template>

<style scoped></style>