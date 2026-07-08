<template>

    <div class="d-flex justify-content-between align-items-start mb-4">
        <div>
            <h2 class="fw-bold mb-1">{{ title }}</h2>
            <p v-if="subtitle" class="text-muted mb-0">{{ subtitle }}</p>
        </div>
        <div>
            <slot name="actions"/>
        </div>

    </div>

</template>

<script setup>
defineProps({
    title:{
        type : String,
        required:true
    },
    subtitle:{
        type: String,
        default: ""
    }
})
</script>