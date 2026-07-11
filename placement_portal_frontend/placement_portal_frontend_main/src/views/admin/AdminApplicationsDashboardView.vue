<template>
    <DashboardLayout :sidebarItems="adminSidebarItems">
        <PageHeader title="Manage Application">
            <template #actions>
                <AppInput v-model="search" placeholder="Search by Drive, Company, Student ..." @input="searchApplications"
                    style="width:300px" />
            </template>
        </PageHeader>
        <div v-if="!loading">

            <DashboardSection title="Applications by Registered Students">
                <DataTable :columns="applicationColumns" :rows="dashboard.applications">
                    <template #cell-status="{ row }">
                        <AppDropDown :status="row.status"
                            @change="status => updateApplicationStatus(row.applicationId, status)" />
                    </template>

                    
                </DataTable>
            </DashboardSection>

        </div>
        <div v-else>
            Loading...
        </div>
    </DashboardLayout>



</template>

<script setup>
import PageHeader from '../../components/PageHeader.vue';
import DashboardLayout from '../../layout/DashboardLayout.vue';
import { getAdminApplicationDashboard,  updateApplicationStatusService} from '../../services/AdminService';
import { adminSidebarItems } from '../../utils/AdminUtils';
import { ref, onMounted } from 'vue';
import DashboardSection from '../../components/DashboardSection.vue';
import DataTable from '../../components/DataTable.vue';
import AppButton from '../../components/AppButton.vue';
import AppInput from '../../components/AppInput.vue';
import AppDropDown from '../../components/AppDropDown.vue';

const loading = ref(false)
const error = ref("")

const search = ref("")
let searchTimeout = null;

const dashboard = ref({
    applications: []
});

const applicationColumns = [
    {
        key:"applicationId",
        label: "Application ID"
    },
    {
        key: "driveName",
        label: "Drive Name"
    },
    {
        key: "studentName",
        label: "Student Name"
    },
    {
        key: "companyName",
        label: "Company Name"
    },
    {
        key: "applicationDate",
        label: "Application Date"
    },
    {
        key: "status",
        label: "Application Status"
    },


];

async function updateApplicationStatus(applicationId, action) {
    try {
        await updateApplicationStatusService(applicationId, action)
        loadDashboard()
    } catch (err) {
        console.log(err);

    }
}

function searchApplications() {

    clearTimeout(searchTimeout);
    searchTimeout = setTimeout(() => {
        loadDashboard();
    }, 400);

}
async function loadDashboard() {
    loading.value = true;
    try {
        const response = await getAdminApplicationDashboard(search.value);

        dashboard.value = response.data.data;
    } catch (err) {
        console.log(err)
        error.value = err.response?.data?.message || "Failed to load dashboard.";
    }
    finally {
        loading.value = false
    }
}

onMounted(loadDashboard)


</script>