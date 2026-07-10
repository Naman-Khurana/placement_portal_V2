<template>
    <DashboardLayout :sidebarItems="companySidebarItems">
        <div v-if="!loading">

            <PageHeader title="Company Dashboard" :subtitle="`Welcome back,  ${dashboard.company.companyName}`">
            </PageHeader>

            <div class="row g-4 mb-4">
                <div class="col-md-3">
                    <StatsCard title="Upcoming Drives" :value="dashboard.stats.upcomingDrives" subtitle="Drives" />
                </div>

                <div class="col-md-3">
                    <StatsCard title="Closed Drives" :value="dashboard.stats.closedDrives" subtitle="Drives"
                        variant="primary" />
                </div>

                <div class="col-md-3">
                    <StatsCard title="Total Applications" :value="dashboard.stats.totalApplications"
                        subtitle="Applications" variant="primary" />

                </div>
                <div class="col-md-3">
                    <StatsCard title="Hired Students" :value="dashboard.stats.hiredStudents" subtitle="Students"
                        variant="success" />

                </div>




            </div>

            <DashboardSection title="Upcoming Drives">
                <DataTable :columns="driveColumns" :rows="dashboard.upcomingDrives">
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

</template>

<script setup>
import PageHeader from '../../components/PageHeader.vue';
import DashboardLayout from '../../layout/DashboardLayout.vue';
import { companySidebarItems } from '../../utils/CompanyUtils.js';
import { ref, onMounted } from 'vue';
import StatsCard from '../../components/StatsCard.vue';
import { getCompanyDashboard } from '../../services/CompanyService.js';
import DashboardSection from '../../components/DashboardSection.vue';
import DataTable from '../../components/DataTable.vue';
const loading = ref(false)
const error = ref("")

const dashboard = ref({
    company: {
        approval_status: "",
        companyName: ""
    },
    stats: {
        closedDrives: 0,
        hiredStudents: 0,
        totalApplications: 0,
        upcomingDrives: 0
    },
    upcomingDrives: []
});

const driveColumns = [
    {
        key: "title",
        label: "Drive"
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
        key: "status",
        label: "Status"
    },
    {
        key: "actions",
        label: "Action"
    }
];


async function loadDashboard() {
    loading.value = true;
    try {
        const response = await getCompanyDashboard();

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