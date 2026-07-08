<template>

<div class="card h-100 shadow-sm border-0 mb-4">

    <div class="card-body">

        <div class="d-flex justify-content-between align-items-center mb-3">

            <h6 class="text-muted mb-0">

                {{ title }}
                
            </h6>

            <div
                class="rounded-circle d-flex align-items-center justify-content-center"
                :class="`bg-${variant}-subtle`"
                style="width:48px;height:48px;"
            >

                <i
                    :class="[icon, `text-${variant}`]"
                ></i>

            </div>

        </div>

        <h2 class="fw-bold mb-1">

            {{ value }}

        </h2>

        <small class="text-muted">

            {{ subtitle }}

        </small>

    </div>

</div>

</template>

<script setup>

defineProps({
    title: {
        type: String,
        required: true
    },
    value: {
        type: [Number,String],
        required:  true
    },
    subtitle: {
        type: String, 
        default: ""
    },
    icon: {
        type: String,
        default: "bi bi-bar-chart"
    },
    variant: {
        type: String,
        default: "primary"
    }

})

</script>