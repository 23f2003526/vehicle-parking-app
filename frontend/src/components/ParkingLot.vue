<script setup>
defineProps({
    lot: {
        type: Object,
        required: true
    }
})
</script>

<template>
    <div class="lot-content">
        <h3 class="lot-name">{{ lot.prime_location_name }}</h3>
        <p class="lot-address">{{ lot.address }}, {{ lot.pin_code }}</p>
        <div class="lot-details">
            <p class="lot-price">₹{{ lot.price }}/hr</p>
            <p class="lot-occupancy">{{ lot.occupied_spots + lot.reserved_spots }}/{{ lot.number_of_spots }} spots</p>
        </div>
    </div>
</template>

<style scoped>
.lot-content {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
}

.lot-name {
    margin: 0;
    font-size: 1.2rem;
    font-weight: 600;
    color: #1a1a1a;
    line-height: 1.3;
}

.lot-address {
    margin: 0;
    font-size: 0.9rem;
    color: #666;
    line-height: 1.4;
}

.lot-details {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 0.25rem;
}

.lot-price {
    margin: 0;
    font-size: 1rem;
    font-weight: 500;
    color: #1a1a1a;
}

.lot-occupancy {
    margin: 0;
    font-size: 0.9rem;
    color: #666;
    font-variant-numeric: tabular-nums;
}

/* Responsive adjustments */
@media (max-width: 480px) {
    .lot-details {
        flex-direction: column;
        align-items: flex-start;
        gap: 0.25rem;
    }

    .lot-name {
        font-size: 1rem;
    }

    .lot-address,
    .lot-price,
    .lot-occupancy {
        font-size: 0.8rem;
    }
}
</style>