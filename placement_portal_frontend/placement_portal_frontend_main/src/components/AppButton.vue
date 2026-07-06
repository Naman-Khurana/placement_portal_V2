<template>
    <button :type="type" :disabled="loading" :class="['btn', `btn-${variant}`, 'w-100']">
        {{ loading ? loadingLabel : label }}

    </button>
</template>

<script setup>

const props = defineProps({
    label:{
        type : String, required: true
    },
    loadingLabel: {
        type: String,
        default: "Loading..."
    },
    loading: {
        type: Boolean,
        default: false
    },
    variant: {
        type : String,
        default: "primary"
    },
    type: {
        type : String,
        default: "submit"
    }
})

</script>