<template>
    <DashboardLayout :sidebarItems="companySidebarItems">

        <div class="container py-4">
            <div v-if="!loading">
                <PageHeader title="Company Profile" subtitle="Keep your company information updated">
                    <!-- <template #actions> -->

                    <!-- <AppButton label="Edit Profile" @click="editProfile"/> -->

                    <!-- </template> -->
                </PageHeader>



                <DashboardSection title="Company Information">
                    <AppInput label="Company Name" v-model="profile.companyName" />

                    <AppInput label="HR Contact" v-model="profile.hrContact" disabled />

                    <AppInput label="Company Website" v-model="profile.companyWebsite" />

                    <AppInput label="Approval Status" v-model="profile.approvalStatus" disabled />


                    <AppButton label="Save Changes" loadingLabel="Saving Changes..." :loading="saving"
                        @click="updateProfile" />

                </DashboardSection>

                


            </div>
            <div v-else>
                Loading...
            </div>

        </div>
    </DashboardLayout>

</template>

<script setup>

import DashboardLayout from '../../layout/DashboardLayout.vue';
import PageHeader from '../../components/PageHeader.vue';
import DashboardSection from '../../components/DashboardSection.vue';
import AppInput from '../../components/AppInput.vue';
import AppButton from '../../components/AppButton.vue';
import { companySidebarItems } from '../../utils/CompanyUtils';
import { ref,reactive,onMounted } from 'vue';
import { getCompanyProfile, updateCompanyProfile } from '../../services/CompanyService.js';

const loading = ref(false)
const error = ref("")
const saving= ref(false)

const profile = reactive({
    companyName: "",
    companyWebsite: "",
    hrContact: "",
    approvalStatus: ""
    
});


const errors = reactive({
    companyName: "",
    companyWebsite: ""
});


function validateEmptyFormField(field) {
    if (!profile[field] || profile[field].trim() === "") {
        errors[field] = `${field} is required`;
        return false;
    }
    return true;
}

function validateForm() {



    errors.companyName = "";
    errors.companyWebsite = "";

    

    let isValid = true


    if (!validateEmptyFormField("companyName")) isValid = false;
    if (!validateEmptyFormField("companyWebsite")) isValid = false;

    return isValid;
}

async function updateProfile(){
    if(!validateForm()){
        return
    }

    saving.value= true;
    try{
        const profileResponse = {
            "company_name":profile.companyName,
            "company_website":profile.companyWebsite
        }
        const response = await updateCompanyProfile(profileResponse)

    }catch(err){
        console.log(err)
    }finally{
        saving.value=false
    }
}





async function loadProfile(params) {
    loading.value= true;
    try {
        const response = await getCompanyProfile()
        Object.assign(profile,response.data.data)
    } catch (err) {
        console.log(err);
               
    }finally{
        loading.value=false
    }
}

onMounted(loadProfile)

</script>