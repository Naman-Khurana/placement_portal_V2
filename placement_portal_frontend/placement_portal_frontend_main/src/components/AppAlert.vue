<template>

<div v-if="message" :class="['alert',`alert-${variant}`]"> {{ message }} </div>


</template>

<script setup>

defineProps({
    message: {
        type : String,
        default: ""
    },
    variant: {
        type: String,
        default:"danger"
    }
})

</script>