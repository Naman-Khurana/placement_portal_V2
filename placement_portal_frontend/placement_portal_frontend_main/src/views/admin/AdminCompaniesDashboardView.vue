<template>
    <DashboardLayout :sidebarItems="adminSidebarItems">
        <PageHeader title="Manage Companies">
            <template #actions>
                <AppInput v-model="search" placeholder="Search Companies..." @input="searchCompanies"
                    style="width:300px" />
            </template>
        </PageHeader>
        <div v-if="!loading">

            <DashboardSection title="Companies pending for approvals">
                <DataTable :columns="companyColumns" :rows="dashboard.pendingCompanies">
                 

                    <template #cell-actions="{ row }">
                        <div class="d-flex gap-1">
                            <AppButton label="Approve" @click="updateCompanyStatus(row.companyId, 'approve')"  />
                            <AppButton label="Blacklist" @click="updateCompanyStatus(row.companyId, 'blacklist')" class="btn-danger" />
                        </div>
                    </template>
                </DataTable>
            </DashboardSection>

            <DashboardSection title="Approved Companies">
                <DataTable :columns="companyColumns" :rows="dashboard.approvedCompanies">
                 

                    <template #cell-actions="{ row }">
                        <AppButton label="Blacklist" @click="updateDriveStatus(row.companyId,'blacklist')" class="btn-danger" />
                        
                    
                    </template>
                </DataTable>
            </DashboardSection>
            

            <DashboardSection title="Blacklisted Companies">
                <DataTable :columns="companyColumns" :rows="dashboard.blacklistedCompanies">

                    <template #cell-actions="{ row }">
                        <AppButton label="Approve" @click="updateCompanyStatus(row.companyId,'approve')"  />
                        
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
import { getAdminCompanyDashboard, getAdminStudentDashboard, updateCompanyStatusService, updateStudentStatusService } from '../../services/AdminService';
import { adminSidebarItems } from '../../utils/AdminUtils';
import { ref, onMounted } from 'vue';
import DashboardSection from '../../components/DashboardSection.vue';
import DataTable from '../../components/DataTable.vue';
import AppButton from '../../components/AppButton.vue';
import AppInput from '../../components/AppInput.vue';
import StatusBadge from '../../components/StatusBadge.vue';


const loading = ref(false)
const error = ref("")

const search = ref("")
let searchTimeout = null;

const dashboard = ref({
    approvedCompanies: [],
    blacklistedCompanies: [],
    pendingCompanies: []
});

const companyColumns = [
    {
        key: "companyId",
        label: "ID"
    },
    {
        key: "companyName",
        label: "Company"
    },
    {
        key: "companyWebsite",
        label: "Website"
    },
    {
        key: "hrContact",
        label: "HR Contact"
    },

    {
        key: "actions",
        label: "Action"
    }
];


async function updateCompanyStatus(companyId, action) {
    try {
        await updateCompanyStatusService(companyId, action)
        loadDashboard()
    } catch (err) {
        console.log(err);

    }
}

function searchCompanies() {

    clearTimeout(searchTimeout);
    searchTimeout = setTimeout(() => {
        loadDashboard();
    }, 400);

}
async function loadDashboard() {
    loading.value = true;
    try {
        const response = await getAdminCompanyDashboard(search.value);

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