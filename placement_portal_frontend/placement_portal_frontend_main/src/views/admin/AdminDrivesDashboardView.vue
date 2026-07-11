<template>
    <DashboardLayout :sidebarItems="adminSidebarItems">
        <PageHeader title="Manage Placement Drives">
            <template #actions>
                <AppInput v-model="search" placeholder="Search Placement Drives..." @input="searchDrives"
                    style="width:300px" />
            </template>
        </PageHeader>
        <div v-if="!loading">

            <DashboardSection title="Drives pending for approval">
                <DataTable :columns="driveColumns" :rows="dashboard.pendingDrives">


                    <template #cell-actions="{ row }">
                        <div class="d-flex gap-1">
                            <AppButton label="Approve" @click="updateDriveStatus(row.driveId, 'approve')" />
                            <AppButton label="Reject" @click="updateDriveStatus(row.driveId, 'reject')"
                                class="btn-danger" />
                        </div>
                    </template>
                </DataTable>
            </DashboardSection>

            <DashboardSection title="Approved Drives">
                <DataTable :columns="driveColumns" :rows="dashboard.approvedDrives">


                    <template #cell-actions="{ row }">
                        <div class="d-flex gap-1">
                            <AppButton label="Close" @click="updateDriveStatus(row.driveId, 'close')" class="btn-warning" />
                            <AppButton label="Reject" @click="updateDriveStatus(row.driveId, 'reject')"
                                class="btn-danger" />
                        </div>

                    </template>
                </DataTable>
            </DashboardSection>


            <DashboardSection title="Rejected Drives">
                <DataTable :columns="driveColumns" :rows="dashboard.rejectedDrives">

                    <template #cell-actions="{ row }">
                        <AppButton label="Approve" @click="updateDriveStatus(row.driveId, 'approve')" />

                    </template>
                </DataTable>
            </DashboardSection>

            <DashboardSection title="Closed Drives">
                <DataTable :columns="driveColumns" :rows="dashboard.closedDrives">

                    <template #cell-actions="{ row }">
                        <AppButton label="Reject" @click="updateDriveStatus(row.driveId, 'reject')" class="btn-danger" />

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
import { getAdminCompanyDashboard, getAdminDriveDashboard, getAdminStudentDashboard, updateCompanyStatusService, updateDriveStatusService, updateStudentStatusService } from '../../services/AdminService';
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
    approvedDrives: [],
    closedDrives: [],
    pendingDrives: [],
    rejectedDrives: []
});



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
        key: "actions",
        label: "Actions"
    }
];


async function updateDriveStatus(driveId, action) {
    try {
        await updateDriveStatusService(driveId, action)
        loadDashboard()
    } catch (err) {
        console.log(err);

    }
}

function searchDrives() {

    clearTimeout(searchTimeout);
    searchTimeout = setTimeout(() => {
        loadDashboard();
    }, 400);

}
async function loadDashboard() {
    loading.value = true;
    try {
        const response = await getAdminDriveDashboard(search.value);

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