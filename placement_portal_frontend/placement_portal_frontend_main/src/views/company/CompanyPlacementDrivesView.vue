<template>

    <DashboardLayout :sidebarItems="companySidebarItems">
        <div v-if="!loading">
            <PageHeader title="Placement Drives" subtitle="Manage all your placement drives">
                <template #actions>
                    <AppButton label="Create Drive +" @click="showCreateDriveModal = true" />
                </template>

                <template #cell-status="{ row }">
                    <StatusBadge :status="row.status" />
                </template>
            </PageHeader>

            <DashboardSection title="Upcoming Drives">
                <DataTable :columns="driveColumns" :rows="drives.upcomingDrives">
                    <template #cell-actions="{ row }">
                        <AppButton label="Edit" @click="editDrive(row)" />
                        <AppButton v-if="row.status.toUpperCase() === 'APPROVED'" label="Close"
                            @click="changeDriveStatus(row.driveId, 'CLOSED')" />

                        <AppButton v-if="row.status.toUpperCase() === 'CLOSED'" label="Reopen"
                            @click="changeDriveStatus(row.driveId, 'APPROVED')" />
                    </template>

                    <template #cell-status="{ row }">
                        <StatusBadge :status="row.status" />
                    </template>

                </DataTable>

            </DashboardSection>

            <DashboardSection title="Pending Drives" subtitle="*subject to approval from admin">
                <DataTable :columns="driveColumns" :rows="drives.pendingApprovalDrives">
                    <template #cell-actions="{ row }">
                        <AppButton label="Edit" @click="editDrive(row)" />
                    </template>

                    <template #cell-status="{ row }">
                        <StatusBadge :status="row.status" />
                    </template>
                </DataTable>
            </DashboardSection>

            <DashboardSection title="Closed Drives">
                <DataTable :columns="driveColumns" :rows="drives.closedDrives">
                    <template #cell-actions="{ row }">
                        <AppButton label="Edit" @click="editDrive(row)" />
                        <AppButton v-if="row.status.toUpperCase() === 'APPROVED'" label="Close"
                            @click="changeDriveStatus(row.driveId, 'CLOSED')" />

                        <AppButton v-if="row.status.toUpperCase() === 'CLOSED'" label="Reopen"
                            @click="changeDriveStatus(row.driveId, 'APPROVED')" />
                    </template>

                    <template #cell-status="{ row }">
                        <StatusBadge :status="row.status" />
                    </template>
                </DataTable>
            </DashboardSection>

            <DashboardSection title="Rejected Drives">
                <DataTable :columns="driveColumns" :rows="drives.rejectedDrives">
                    <template #cell-actions="{ row }">
                        <AppButton label="Edit" @click="editDrive(row)" />
                    </template>

                    <template #cell-status="{ row }">
                        <StatusBadge :status="row.status" />
                    </template>
                </DataTable>
            </DashboardSection>


        </div>
        <div v-else>
            Loading...
        </div>


    </DashboardLayout>
    <AppModal v-model="showCreateDriveModal" :title="isEditing ? 'Edit Placement Drive' : 'Create Placement Drive'">
        <DriveForm :form="driveForm" :errors="errors" @submit="createDrive"></DriveForm>

    </AppModal>


</template>


<script setup>
import { create } from 'axios';
import PageHeader from '../../components/PageHeader.vue';
import DashboardLayout from '../../layout/DashboardLayout.vue';
import { createCompanyDrive, editCompanyDrive, getCompanyDrives, updateCompanyDriveStatus } from '../../services/CompanyService.js';
import { companySidebarItems } from '../../utils/CompanyUtils';
import { ref, onMounted, reactive } from 'vue';
import AppButton from '../../components/AppButton.vue';
import DashboardSection from '../../components/DashboardSection.vue';
import DataTable from '../../components/DataTable.vue';
import AppModal from '../../components/AppModal.vue';
import DriveForm from '../../components/DriveForm.vue';
import StatusBadge from '../../components/StatusBadge.vue';

const loading = ref(false)
const error = ref("")
const showCreateDriveModal = ref(false);

const isEditing = ref(false);
const editingDriveId = ref(null);


const drives = ref({
    upcomingDrives: [],
    pendingApprovalDrives: [],
    rejectedDrives: [],
    closedDrives: []
});

const driveColumns = [
    {
        key: "driveName",
        label: "Drive Title"
    },
    {
        key: "jobTitle",
        label: "Job Title"
    },
    {
        key: "applicationDeadline",
        label: "Application Deadline"
    },
    {
        key: "applicationCount",
        label: "Applications"
    },
    {
        key: "eligibilityCriteria",
        label: "Eligibility"
    },
    {
        key: "ctc",
        label: "CTC"
    },
    {
        key: "status",
        label: "Status"
    },
    {
        key: "actions",
        label: "Actions"
    }
];



const driveForm = reactive({
    driveName: "",
    jobTitle: "",
    ctc: "",
    applicationDeadline: "",
    eligibilityCriteria: "",
    jobDescription: ""
});

const errors = reactive({
    driveName: "",
    jobTitle: "",
    ctc: "",
    applicationDeadline: "",
    eligibilityCriteria: "",
    jobDescription: ""
});


function validateEmptyFormField(field) {
    if (!driveForm[field] || driveForm[field].trim() === "") {
        errors[field] = `${field} is required`;
        return false;
    }
    return true;
}

function validateForm() {



    errors.driveName = "",
        errors.jobTitle = "",
        errors.ctc = "",
        errors.applicationDeadline = "",
        errors.eligibilityCriteria = "",
        errors.jobDescription = ""

    let isValid = true


    if (!validateEmptyFormField("driveName")) isValid = false;
    if (!validateEmptyFormField("jobTitle")) isValid = false;
    if (!validateEmptyFormField("ctc")) isValid = false;
    if (!validateEmptyFormField("applicationDeadline")) isValid = false;
    if (!validateEmptyFormField("eligibilityCriteria")) isValid = false;
    if (!validateEmptyFormField("jobDescription")) isValid = false;

    return isValid;
}

function resetForm() {

    Object.assign(driveForm, {
        driveName: "",
        jobTitle: "",
        ctc: "",
        applicationDeadline: "",
        eligibilityCriteria: "",
        jobDescription: ""
    });

}

async function changeDriveStatus(driveId,status){
    try{
        await updateCompanyDriveStatus(driveId,status)
        loadDrives()
    }catch(err){
        console.log(err);
    }
}


async function editDrive(row) {

    isEditing.value = true;

    editingDriveId.value = row.driveId;

    driveForm.driveName = row.title;
    driveForm.jobTitle = row.jobTitle;
    driveForm.ctc = row.ctc;
    driveForm.applicationDeadline = row.applicationDeadline;
    driveForm.eligibilityCriteria = row.eligibilityCriteria;
    driveForm.jobDescription = row.jobDescription;

    showCreateDriveModal.value = true;

}



async function createDrive() {


    if (!validateForm()) {
        return
    }


    // isLoading.value = true
    // creatingNewDrive.value=true;

    try {

        const driveResponse = {
            "drive_name": driveForm.driveName,
            "job_title": driveForm.jobTitle,
            "ctc": driveForm.ctc,
            "application_deadline": driveForm.applicationDeadline,
            "eligibility_criteria": driveForm.eligibilityCriteria,
            "job_desc": driveForm.jobDescription
        }
        // const response = null
        if (isEditing.value) {
            await editCompanyDrive(editingDriveId,driveResponse)
        }
        else {
             await createCompanyDrive(driveResponse)
        }
    
        showCreateDriveModal.value = false;


        // console.log(response.data.data);

        loadDrives();
        resetForm();


    } catch (error) {
        console.log(error);
        // errors.reg/ister = error.response?.data?.message || "Something went wrong. Please try again."

    }
    finally{
        isEditing.value=false;
        editingDriveId.value=null;
    }

}





async function loadDrives() {
    loading.value = true;
    try {
        const response = await getCompanyDrives();

        drives.value = response.data.data;
    } catch (err) {
        console.log(err)
        error.value = err.response?.data?.message || "Failed to load dashboard.";
    }
    finally {
        loading.value = false
    }
}


onMounted(() => loadDrives())

</script>