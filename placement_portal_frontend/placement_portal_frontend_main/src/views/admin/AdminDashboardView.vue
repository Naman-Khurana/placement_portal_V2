<template>
    <DashboardLayout :sidebarItems="adminSidebarItems">
        <div v-if="!loading">

            <PageHeader title="Admin Dashboard" :subtitle="`Welcome back, Admin`">
            </PageHeader>

            <div class="row g-4 mb-4">
                <div class="col-md-3">
                    <StatsCard title="Companies" :value="dashboard.stats.companies" subtitle="Companies"
                        variant="success" />
                </div>

                <div class="col-md-3">
                    <StatsCard title="Students" :value="dashboard.stats.students" subtitle="students"
                        variant="primary" />
                </div>

                <div class="col-md-3">
                    <StatsCard title="Drives" :value="dashboard.stats.drives" subtitle="Drives" variant="success" />

                </div>
                <div class="col-md-3">
                    <StatsCard title="Applications" :value="dashboard.stats.applications" subtitle="Applications"
                        variant="primary" />

                </div>




            </div>

            <DashboardSection title="Companies pending for approvals">
                <DataTable :columns="companyColumns" :rows="dashboard.pendingCompanies">
                    <template #cell-status="{ row }">
                        <StatusBadge :status="row.status" />
                    </template>

                    <template #cell-actions="{ row }">
                        <div class="d-flex gap-1">
                            <AppButton label="Approve" @click="updateCompanyStatus(row.companyId, 'approve')"  />
                            <AppButton label="Blacklist" @click="updateCompanyStatus(row.companyId, 'blacklist')" class="btn-danger" />
                        </div>
                    </template>
                </DataTable>
            </DashboardSection>

            <DashboardSection title="Drives pending for approval">
                <DataTable :columns="driveColumns" :rows="dashboard.pendingDrives">
                    <template #cell-status="{ row }">
                        <StatusBadge :status="row.status" />
                    </template>

                    <template #cell-actions="{ row }">
                        <div class="d-flex gap-1">
                            <AppButton label="Approve" @click="updateDriveStatus(row.driveId,'approve')"  />
                            <AppButton label="Reject" @click="updateDriveStatus(row.driveId,'reject')" class="btn-danger" />
                        </div>
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
import DashboardLayout from '../../layout/DashboardLayout.vue';
import DashboardSection from '../../components/DashboardSection.vue';
import StatsCard from '../../components/StatsCard.vue';
import StatusBadge from '../../components/StatusBadge.vue';
import DataTable from '../../components/DataTable.vue';
import { adminSidebarItems } from '../../utils/AdminUtils';
import { ref, onMounted } from 'vue';
import PageHeader from '../../components/PageHeader.vue';
import AppButton from '../../components/AppButton.vue';
import { getAdminDashboard, updateCompanyStatusService, updateDriveStatusService } from '../../services/AdminService.js';

const loading = ref(false)
const error=ref("")

const dashboard = ref({
    stats: {
        companies: 0,
        students: 0,
        drives: 0,
        applications: 0
    },
    pendingCompanies: [],
    pendingDrives: []
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
        key: "website",
        label: "Website"
    },
    {
        key: "hrContact",
        label: "HR Contact"
    },
    {
        key: "status",
        label: "Status"
    },
    {
        key: "actions",
        label: "Action"
    }
];


const driveColumns = [
    {
        key: "driveId",
        label: "ID"
    },
    {
        key: "driveName",
        label: "Drive Name"
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

async function updateCompanyStatus(companyId, action) {
    try {
        await updateCompanyStatusService(companyId, action);
        await loadDashboard();
    } catch (err) {
        console.log(err);
    }
}

async function updateDriveStatus(companyId, action) {
    try {
        await updateDriveStatusService(companyId, action);
        await loadDashboard();
    } catch (err) {
        console.log(err);
    }
}

async function loadDashboard() {
    loading.value = true;
    try {
        const response = await getAdminDashboard();

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