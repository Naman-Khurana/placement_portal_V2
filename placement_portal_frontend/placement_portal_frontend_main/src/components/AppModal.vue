<template>

    <div v-if="modelValue" class="app-modal-overlay">
        <div class="app-modal">
            <div class="app-modal-header">
                <h5> {{ title }}</h5>
                <button class="btn-close" @click="closeModal"></button>
            </div>

            <div class="app-modal-body">
                <slot />
            </div>


        </div>





    </div>



</template>

<script setup>

defineProps({
    modelValue: {
        type: Boolean ,
        required:true
    },
    title: {
        type: String,
        default : ""
    }
})

function closeModal(){
    emit("update:modelValue",false);
}

const emit = defineEmits(["update:modelValue"])

</script>
<style scoped>

.app-modal-overlay{

    position: fixed;

    inset: 0;

    background: rgba(0,0,0,0.45);

    display: flex;

    justify-content: center;

    align-items: center;

    z-index: 1050;

}

.app-modal{

    background: white;

    width: 700px;

    max-width: 90vw;

    border-radius: 12px;

    overflow: hidden;

}

.app-modal-header{

    display: flex;

    justify-content: space-between;

    align-items: center;

    padding: 1rem 1.25rem;

    border-bottom: 1px solid #dee2e6;

}

.app-modal-body{

    padding: 1.25rem;

}

</style>