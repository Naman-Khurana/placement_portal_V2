<template>

    <DashboardLayout :sidebarItems="companySidebarItems">
        <div v-if="!loading">
            <PageHeader title="Placement Drives" subtitle="Manage all your placement drives">
                <template #actions>
                    <AppButton
                        label="Create Drive +"
                        @click="openCreateDriveModal"
                        :disabled="drives.company.approvalStatus !== 'approved' " class="btn-success"
                    />

                    <div
                        v-if="drives.company.approvalStatus !== 'approved'"
                        class="alert alert-warning mt-2 mb-0"
                    >
                        <span v-if="drives.company.approvalStatus === 'pending'">
                            Your company is pending approval. Please contact the administrator for more information.
                        </span>

                        <span v-else-if="drives.company.approvalStatus === 'blacklisted'">
                            Your company has been blacklisted. Please contact the administrator for more information.
                        </span>
                    </div>
                </template>

                <template #cell-status="{ row }">
                    <StatusBadge :status="row.status" />
                </template>
            </PageHeader>

            <DashboardSection title="Upcoming Drives">
                <DataTable :columns="driveColumns" :rows="drives.upcomingDrives">
                    <template #cell-actions="{ row }">
                        <div class="d-flex flex-row gap-1">
                            <AppButton label="Edit" @click="editDrive(row)" />
                            <AppButton  label="View Applications"
                                @click="viewDriveApplicants(row.driveId)" class='btn-secondary' />
                            <AppButton v-if="row.status.toUpperCase() === 'APPROVED'" label="Close"
                                                            @click="changeDriveStatus(row.driveId, 'close')" class='btn-danger' />
                            <AppButton v-if="row.status.toUpperCase() === 'close'" label="Reopen"
                                @click="changeDriveStatus(row.driveId, 'reopen')" />
                            
                        </div>
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
                        <div class='d-flex flex-column gap-1'>
                            <AppButton label="Edit" @click="editDrive(row)" />
                            <AppButton  label="View Applications"
                                @click="viewDriveApplicants(row.driveId)" class='btn-secondary' />

                            <AppButton v-if="row.status.toUpperCase() === 'APPROVED'" label="Close"
                                @click="changeDriveStatus(row.driveId, 'close')" class='btn-danger' />
                            <AppButton v-if="row.status.toUpperCase() === 'CLOSED'" label="Reopen"
                                @click="changeDriveStatus(row.driveId, 'reopen')" class='btn-success' />
                        </div>
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

    <AppModal v-model="showApplicationsModal" title="Drive Applications">

        <div v-if="applicantsLoading">Loading...</div>

        <DashboardSection v-else title="Applications" >
            <DataTable :columns="applicationColumns" :rows="driveApplicants" >
                <template #cell-status="{ row }">
                    <AppDropDown
                        :status="row.status"
                        @change="status => updateApplicationStatus(row.applicationId, status)" />
                 
                </template>

                <template #cell-resume="{ row }">

                    <AppButton label="View Resume" @click="viewResume(row.resume)" class="btn-secondary" />

                </template>

            </DataTable>

        </DashboardSection>

    </AppModal>


    </template>


<script setup>
import { create } from 'axios';
import PageHeader from '../../components/PageHeader.vue';
import DashboardLayout from '../../layout/DashboardLayout.vue';
import { createCompanyDrive, editCompanyDrive, getCompanyDriveApplications, getCompanyDrives, updateCompanyApplicationStatus, updateCompanyDriveStatus } from '../../services/CompanyService.js';
import { companySidebarItems } from '../../utils/CompanyUtils';
import { ref, onMounted, reactive } from 'vue';
import AppButton from '../../components/AppButton.vue';
import DashboardSection from '../../components/DashboardSection.vue';
import DataTable from '../../components/DataTable.vue';
import AppModal from '../../components/AppModal.vue';
import DriveForm from '../../components/DriveForm.vue';
import StatusBadge from '../../components/StatusBadge.vue';
import AppDropDown from '../../components/AppDropDown.vue';

const loading = ref(false)
const error = ref("")
const showCreateDriveModal = ref(false);

const isEditing = ref(false);
const editingDriveId = ref(null);

const showApplicationsModal = ref(false);
const applicantsLoading = ref(false);

const driveApplicants = ref([]);

const selectedDriveId = ref(null);

const drives = ref({
    upcomingDrives: [],
    pendingApprovalDrives: [],
    rejectedDrives: [],
    closedDrives: [],
    company :{
        approvalStatus:""
    }
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


const applicationColumns = [
    {
        key: "studentName",
        label: "Student"
    },{
        key:"email",
        label:"Email"
    },
    {
        key: "department",
        label: "Department"
    },
    {
        key: "applicationDate",
        label: "Applied On"
    },
    {
        key: "status",
        label: "Status"
    },
    {
        key: "resume",
        label: "Resume"
    },
    // {
    //     key: "actions",
    //     label: "Actions"
    // }
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

async function viewDriveApplicants(driveId) {
    applicantsLoading.value = true;
    selectedDriveId.value = driveId;
    try {
        const response = await getCompanyDriveApplications(driveId);
        driveApplicants.value = response.data.data.applications;
        console.log(driveApplicants.value)
        showApplicationsModal.value = true;
    } catch (err) {
        console.log(err);
    } finally {
        applicantsLoading.value = false;
    }
}

async function updateApplicationStatus(applicationId, status) {

    try {

        await updateCompanyApplicationStatus(applicationId, status);
        await viewDriveApplicants(selectedDriveId.value);

        await loadDrives();

    } catch (err) {
        console.log(err);
    }

}

function openCreateDriveModal() {
    isEditing.value = false;
    editingDriveId.value = null;
    resetForm();
    showCreateDriveModal.value = true;
}

function viewResume(path) {
    window.open(`http://localhost:5000/${path}`, "_blank");
}

async function editDrive(row) {

    isEditing.value = true;

    editingDriveId.value = row.driveId;

    driveForm.driveName = row.driveName;
    driveForm.jobTitle = row.jobTitle;
    driveForm.ctc = row.ctc;
    driveForm.applicationDeadline = row.applicationDeadlineRaw;
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
            await editCompanyDrive(editingDriveId.value,driveResponse)
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