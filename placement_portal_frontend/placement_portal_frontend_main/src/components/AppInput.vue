<template>

    <div class="mb-3">

        <p v-if="error" class="text-danger mt-1 mb-0">{{ error }}</p>
        <label class="form-label" :for="id"> {{ label }}</label>
        <input :value="modelValue" @input="emit('update:modelValue', $event.target.value)" :id="id" class="form-control"
            :placeholder="placeholder" :type="type">
    </div>




</template>

<script setup>

const emit = ([
    "update:modalValue"
])

defineProps({
    modelValue: String,
    label: String,
    id: String,
    type: {
        type: String,
        default: "text"
    },
    placeholder: {
        type: String,
        default: ""
    },
    error: {
        type: String,
        default: ""
    }

});
</script>