<template>

<span class="badge rounded-pill px-3 py-2" :class="badgeClass">{{ status }}</span>

</template>

<script setup>
import { computed } from 'vue';

const badgeClass= computed(()=> {
    switch(props.status.toUpperCase()){
        case "APPLIED":
            return "bg-warning text-dark";
        
        case "SHORTLISTED":
            return "bg-primary";
        
        case "REJECTED":
            return "bg-danger";
        case "HIRED":
            return "bg-success";
        default:
            return "bg-secondary";
    }
});

const props =defineProps({
    status: {
        type:String,
        required: true
    }
})

</script>