<template>

    <div class="mb-3">

        <small v-if="error" class="text-danger   mb-0">{{ error }}</small><br />
        <label class="form-label" :for="id"> {{ label }}
            <span v-if="required" class="text-danger">*</span>
        </label>
        <input :value="modelValue" @input="emit('update:modelValue', $event.target.value)" :id="id" :class="['form-control',
        {
            'is-invalid': error
        }
            ]" :placeholder="placeholder" :type="type" :disabled="disabled">
    </div>




</template>

<script setup>

const emit = defineEmits([
    "update:modelValue"
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
    },
    required: {
        type: Boolean,
        default: false
    },
    disabled: {
        type: Boolean,
        default: false
    }

});
</script>