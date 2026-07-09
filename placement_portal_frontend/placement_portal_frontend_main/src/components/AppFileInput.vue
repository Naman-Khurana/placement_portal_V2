<template>
    <div class="mb-3">
        <label v-if="label" class="form-label">{{ label }}</label>
        <input type="file" class="form-control" :accept="accept" @change="handleFileChange">
    </div>

</template>

<script setup>

defineProps({
    label:{
        type: String,
        default:""
    },
    accept:{
        type: String,
        default:""
    }
});

const emit = defineEmits(["selected"])

function handleFileChange(){
    const file= event.target.files[0];
    emit("selected",file)
}
    
</script>