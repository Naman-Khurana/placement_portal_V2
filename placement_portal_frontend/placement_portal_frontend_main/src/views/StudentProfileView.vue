<template>
    <DashboardLayout :sidebarItems="sidebarItems" title="">

        <div class="container py-4">
            <div v-if="!loading">
                <PageHeader title="Edit Profile" :subtitle="`Welcome back, ${dashboard.student.name}`">
                    <template #actions>

                         <!-- <AppButton label="Edit Profile" @click="editProfile"/> -->

                    </template>
                </PageHeader>

                <StatsCard title="Applications" :value="dashboard.stats.applications" subtitle="Applications Submitted"
                    icon="bi bi-file-earmark-text" variant="primary" />

                <DashboardSection title="Approved Companies" subtitle="Companies Currently Hiring">
                    <DataTable :columns="companyColumns" :rows="dashboard.approvedCompanies">
                        <template #cell-actions="{ row }">
                            <AppButton label="View Drives" @click="viewCompanyDrives(row.id)">
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
            <DataTable v-if="companyDrives.length" :columns="companyColumns" :rows="companyDrives">

            
            
                
            </DataTable>
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
import { getStudentDashboard } from '../services/StudentService.js';
import { GET_COMPANY_ACTIVE_DRIVES } from '../utils/urlConstants.js';
import { getCompaniesActiveDrives } from '../services/CompanyService.js';
import AppModal from '../components/AppModal.vue';
import { STUDENT_DASHBOARD_ROUTE, STUDENT_APPLICATIONS_ROUTE, STUDENT_PROFILE_ROUTE } from '../utils/routeConstants';
import { RouterLink } from 'vue-router';
import { useRouter } from "vue-router"

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
        resumeUploaded: false
    },
    stats: {
        applications: 0,
        approvedCompanies: 0,
        upcomingDrives: 0
    },
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


const sidebarItems = [

    {
        label: "Dashboard",
        route: STUDENT_DASHBOARD_ROUTE
    },

    {
        label: "My Applications",
        route: STUDENT_APPLICATIONS_ROUTE
    },

    {
        label: "Profile",
        route: STUDENT_PROFILE_ROUTE
    }

];







function editProfile(){
    router.push(STUDENT_PROFILE_ROUTE);
}
async function viewCompanyDrives(companyId) {
    modalLoading.value = true;
    try {
        const response = await getCompaniesActiveDrives(companyId);
        const data = response.data.data;
        console.log(data)
        selectedCompany.value = data.company;
        companyDrives.value = data.activeDrives;
        showCompanyModal.value = true;


    } catch (err) {
        console.log(err);
    }
    finally {
        modalLoading.value = false;
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