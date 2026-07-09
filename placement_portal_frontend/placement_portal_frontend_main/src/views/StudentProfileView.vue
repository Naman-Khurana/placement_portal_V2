<template>
    <DashboardLayout :sidebarItems="studentSidebarItems" title="">

        <div class="container py-4">
            <div v-if="!loading">
                <PageHeader title="Edit Profile" subtitle="Keep your profile updated">
                    <!-- <template #actions> -->

                    <!-- <AppButton label="Edit Profile" @click="editProfile"/> -->

                    <!-- </template> -->
                </PageHeader>



                <DashboardSection title="Personal Information">
                    <AppInput label="Name" v-model="profile.name" />

                    <AppInput label="Username" v-model="profile.username" disabled />

                    <AppInput label="Department" v-model="profile.department" />

                    <AppInput type="date" label="Date of Birth" v-model="profile.dob" />


                    <AppButton label="Save Changes" loadingLabel="Saving Changes..." :loading="saving"
                        @click="updateProfile" />

                </DashboardSection>

                <DashboardSection title="Resume">
                    <div class="mb-3">
                        <div v-if="profile.resumePath">
                            <div class="d-flex justify-content-between align-items-center">
                                <div>
                                    <div class="fw-semibold">
                                        Current Resume
                                    </div>

                                    <small class="text-muted">
                                        {{ resumeFileName }}
                                    </small>

                                </div>
                                <a :href="resumeUrl" target="_blank" class="btn btn-outline-primary btn-sm">
                                    View Resume
                                </a>
                            </div>
                        </div>

                        <div v-else>
                            <p class="text-muted mb-0">
                                No resume uploaded yet.
                            </p>
                        </div>

                    </div>

                    <div v-if="resumeUploading" class="text-primary">
                        Uploading resume...
                    </div>
                    <div v-else>
                        <AppFileINput label="Replace Resume" accept=".pdf" @selected="uploadResume" />
                    </div>

                </DashboardSection>


            </div>
            <div v-else>
                Loading...
            </div>

        </div>

    </DashboardLayout>



</template>


<script setup>
import DashboardLayout from '../layout/DashboardLayout.vue';
import PageHeader from '../components/PageHeader.vue';
import { ref, onMounted, reactive } from 'vue';
import DashboardSection from '../components/DashboardSection.vue';
import { getStudentProfile, updateStudentProfile, uploadStudentResume } from '../services/StudentService.js';
import { studentSidebarItems } from '../utils/StudentsUtils.js';
import AppInput from '../components/AppInput.vue';
import AppButton from '../components/AppButton.vue';
import { computed } from "vue";
import AppFileINput from '../components/AppFileINput.vue';

const loading = ref(false);
const saving = ref(false);
const resumeUploading = ref(false);
const error = ref("");




const profile = reactive({
    name: "",
    username: "",
    department: "",
    dob: "",
    resumePath: ""
});



const resumeUrl = computed(() => {
    if (!profile.resumePath) return "";
    return `http://localhost:5000/${profile.resumePath}`;
});



const resumeFileName = computed(() => {

    if (!profile.resumePath) {
        return "";
    }

    return profile.resumePath.split("/").pop();

});




async function uploadResume(file) {
    if (!file) {
        return;
    }
    resumeUploading.value = true;

    const formData = new FormData()
    formData.append("resume", file)


    try {
        const response = await uploadStudentResume(formData)
        profile.resumePath = response.data.data.resumePath
        console.log(profile.resumePath)
    } catch (err) {
        console.log(err)
    } finally {
        resumeUploading.value = false;
    }
}


async function updateProfile() {
    saving.value = true;
    try {
        const response = await updateStudentProfile(profile)
        Object.assign(profile,response.data.data)
    } catch (err) {
        error.value = err.response?.data?.message || "Something went wrong"
        console.log(err)
    } finally {
        saving.value = false
    }
}


async function loadProfile() {
    loading.value = true;
    try {
        const response = await getStudentProfile();
        console.log(response.data.data)
        Object.assign(profile, response.data.data)

    } catch (err) {
        console.log(err)
        error.value = err.response?.data?.message || "Failed to load dashboard.";
    }
    finally {
        loading.value = false
    }
}


onMounted(() => loadProfile())

</script>