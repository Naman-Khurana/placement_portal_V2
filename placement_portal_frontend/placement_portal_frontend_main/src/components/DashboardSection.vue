<template>

<div class="card"> 
    <div class="card-body">
        <div class="d-flex justify-content-between align-items-center mb-3" >
            <div>
                <h5>{{ title }}</h5>
                <small v-if="subtitle">{{ subtitle }}</small>
            </div>

            <div>
                <slot name="actions" />
            </div>

        </div>
        <slot />
    </div>
</div>



</template>


<script setup>

defineProps({
    title: {
        type : String,
        required : true
    },
    subtitle: {
        type : String,
        default: ""
    },
    loading: {
        type : Boolean,
        default: false
    }
})


</script>