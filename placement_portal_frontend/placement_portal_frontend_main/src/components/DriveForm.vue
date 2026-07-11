<template>
    <form @submit.prevent="emit('submit')">

        <AppInput label="Drive Name" v-model="form.driveName" :error="errors.driveName" />
        <AppInput label="Job Title" v-model="form.jobTitle" :error="errors.jobTitle" />
        <AppInput label="CTC" v-model="form.ctc" :error="errors.ctc" />
        <AppInput type="datetime-local" label="Application Deadline" v-model="form.applicationDeadline"
            :error="errors.applicationDeadline" />
        <AppInput label="Eligibility Criteria" v-model="form.eligibilityCriteria" :error="errors.eligibilityCriteria" />
        
        <div class="mb-3">
            <label class="form-label">Job Description</label>
            <textarea class="form-control" rows="5" v-model="form.jobDescription"></textarea>
        </div>

        <div class="d-flex justify-content-end mt-4">
            <AppButton label="Save" />
        </div>

    </form>


</template>

<script setup>
import AppButton from './AppButton.vue'
import AppInput from './AppInput.vue';


defineProps({
    form:{
        type:Object,
        required:true
    },
    errors:{
        type:Object,
        required:true
    }
});


const emit = defineEmits(["submit"])

</script>