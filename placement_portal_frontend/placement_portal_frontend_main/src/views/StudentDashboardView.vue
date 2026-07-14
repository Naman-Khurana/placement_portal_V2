<template>
    <DashboardLayout :sidebarItems="studentSidebarItems" title="">

        <div class="container py-4">
            <div v-if="!loading">
                <PageHeader title="Student Dashboard" :subtitle="`Welcome back, ${dashboard.student.name}`">
                    <template #actions>

                        <AppButton label="Edit Profile" @click="editProfile" />

                        <div
                        v-if="!dashboard.student.eligible"
                        class="alert alert-warning mt-2 mb-0"
                        >
                        <span >
                            You are not eligible to participate in Upcoming Placement Drives. Please contact the administrator for more information.
                        </span>

                    
                    </div>
                    </template>
                </PageHeader>

                <StatsCard title="Applications" :value="dashboard.stats.applications" subtitle="Applications Submitted"
                    icon="bi bi-file-earmark-text" variant="primary" />

                <DashboardSection title="Approved Companies" subtitle="Companies Currently Hiring">
                    <DataTable :columns="companyColumns" :rows="dashboard.approvedCompanies">
                        <template #cell-actions="{ row }">
                            <AppButton  label="View Drives" @click="viewCompanyDrives(row.id)" :disabled="!dashboard.student.eligible">
                            </AppButton>

                        </template>
                    </DataTable>
                </DashboardSection>

            </div>
            <div v-else>
                Loading...
            </div>

        </div>

    </DashboardLayout>


    <AppModal v-model="showCompanyModal" :title="selectedCompany?.companyName">

        <div v-if="modalLoading">Loading...</div>
        <div v-else>
            <DashboardSection v-if="companyDrives.length"  title="Upcoming Drives">
                <DataTable   :columns="driveColumns" :rows="companyDrives">
                    <template #cell-actions="{ row }">
                       
                        <AppButton label="Apply" @click="applyToDrive(row.driveId)" class="btn-success">
                
                        </AppButton>

                    </template>
                </DataTable>
            </DashboardSection>
            <div v-else>
                No Active Placement Drives
            </div>
        </div>

    </AppModal>

</template>


<script setup >
import DashboardLayout from '../layout/DashboardLayout.vue';
import PageHeader from '../components/PageHeader.vue';
import AppButton from '../components/AppButton.vue';
import StatsCard from '../components/StatsCard.vue';
import { ref, onMounted } from 'vue';
import DashboardSection from '../components/DashboardSection.vue';
import DataTable from '../components/DataTable.vue';
import { applyDrive, getCompaniesActiveDrivesForStudent, getStudentDashboard } from '../services/StudentService.js';
import { GET_COMPANY_ACTIVE_DRIVES } from '../utils/urlConstants.js';
import { getCompaniesActiveDrives } from '../services/CompanyService.js';
import AppModal from '../components/AppModal.vue';
import { STUDENT_DASHBOARD_ROUTE, STUDENT_APPLICATIONS_ROUTE, STUDENT_PROFILE_ROUTE } from '../utils/routeConstants';
import { RouterLink } from 'vue-router';
import { useRouter } from "vue-router"
import { studentSidebarItems } from '../utils/StudentsUtils.js';

const router = useRouter()

const loading = ref(false);
const error = ref("");

const selectedCompany = ref(null);
const companyDrives = ref([]);
const showCompanyModal = ref(false);
const modalLoading = ref(false);



const dashboard = ref({
    student: {
        department: null,
        id: null,
        name: "",
        resumeUploaded: false,
        eligible: true
    },
    stats: {
        applications: 0,
        approvedCompanies: 0,
        upcomingDrives: 0
    }
    ,
    approvedCompanies: [],
    recentApplications: []
});

const companyColumns = [
    {
        key: "companyName",
        label: "Company"
    },
    {
        key: "website",
        label: "Website"
    },
    {
        key: "actions",
        label: "Action"
    }
];




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
        key: "eligibilityCriteria",
        label: "Eligibility"
    },
    {
        key: "ctc",
        label: "CTC"
    },
    {
        key: "actions",
        label: "Actions"
    }
];







function editProfile(){
    router.push(STUDENT_PROFILE_ROUTE);
}
async function viewCompanyDrives(companyId) {
    modalLoading.value = true;
    try {
        const response = await getCompaniesActiveDrivesForStudent(companyId);
        const data = response.data.data;
        console.log(data)
        selectedCompany.value = data.company;
        companyDrives.value = data.drives;
        showCompanyModal.value = true;


    } catch (err) {
        console.log(err);
    }
    finally {
        modalLoading.value = false;
    }
}

async function applyToDrive(driveId) {
    try {
        await applyDrive(driveId);
        await viewCompanyDrives(selectedCompany.value.company_id)
        await loadDashboard()
        // showCompanyModal.value=false
        

    }catch(err){
        console.log(err)
    }
    
}



async function loadDashboard() {
    loading.value = true;
    try {
        const response = await getStudentDashboard();

        dashboard.value = response.data.data;
    } catch (err) {
        console.log(err)
        error.value = err.response?.data?.message || "Failed to load dashboard.";
    }
    finally {
        loading.value = false
    }
}


onMounted(() => loadDashboard())

</script>