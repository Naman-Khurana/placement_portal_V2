<template>
    <DashboardLayout :sidebarItems="adminSidebarItems">
        <PageHeader title="Manage Students">
            <template #actions>
                <AppInput v-model="search" placeholder="Search Student..." @input="searchStudents"
                    style="width:300px" />
            </template>
        </PageHeader>
        <div v-if="!loading">

            <DashboardSection title="Registered Students">
                <DataTable :columns="studentColumns" :rows="dashboard.students">
                    <template #cell-status="{ row }">
                        <StatusBadge :status="row.eligible ? 'ELIGIBLE' : 'BLACKLISTED'" />
                    </template>

                    <template #cell-actions="{ row }">
                        <AppButton v-if="row.eligible" label="Blacklist" class="btn-danger"
                            @click="updateStudentStatus(row.studentId, 'blacklist')" />

                        <AppButton v-else label="Whitelist" @click="updateStudentStatus(row.studentId, 'whitelist')" />

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
import { getAdminStudentDashboard, updateStudentStatusService } from '../../services/AdminService';
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
    students: []
});

const studentColumns = [
    {
        key: "studentId",
        label: "Student ID"
    },
    {
        key: "name",
        label: "Student Name"
    }, {
        key: "eligible",
        label: "Eligible for drives"
    }, {
        key: "actions",
        label: "Actions"
    }


];

async function updateStudentStatus(studentId, action) {
    try {
        await updateStudentStatusService(studentId, action)
        loadDashboard()
    } catch (err) {
        console.log(err);

    }
}

function searchStudents() {

    clearTimeout(searchTimeout);
    searchTimeout = setTimeout(() => {
        loadDashboard();
    }, 400);

}
async function loadDashboard() {
    loading.value = true;
    try {
        const response = await getAdminStudentDashboard(search.value);

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