<template>

    <div class="dropdown">

        <div class="dropdown-toggle" role="button" data-bs-toggle="dropdown">
            <StatusBadge :status="status" />
        </div>

        <ul class="dropdown-menu">

            <li v-for="option in options" :key="option">
                <button type="button" class="dropdown-item" @click="changeStatus(option)">
                    <StatusBadge :status="option.toUpperCase()" />
                </button>
            </li>

        </ul>

    </div>

</template>

<script setup>
import StatusBadge from './StatusBadge.vue';

const props = defineProps({

    status: {
        type: String,
        required: true
    },

    options: {
        type: Array,
        default: () => [
            "APPLIED",
            "SHORTLISTED",
            "WAITLISTED",
            "SELECTED",
            "HIRED",
            "REJECTED"
        ]
    }

});

const emit = defineEmits([
    "change"
]);

function changeStatus(status) {

    if (status === props.status) return;

    emit("change", status);

}

</script>

<style scoped>
.dropdown-toggle {

    cursor: pointer;

    display: inline-block;

}

.dropdown-item {

    background: none;
    border: none;
    width: 100%;
    text-align: left;

}

.dropdown-item:hover {

    background: #f8f9fa;

}
</style>