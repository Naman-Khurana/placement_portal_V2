<template>
    <DashboardLayout :sidebarItems="studentSidebarItems">



        <PageHeader title="My Applications" subtitle="Track all your placement applications." >
            <template #actions>

                <AppButton
                    label="Export CSV"
                    class="btn-success"
                    loadingLabel="Exporting..."
                    :loading="csvLoading"
                    @click="exportApplications"
                />

            </template>
        
        </PageHeader>


        <div class="row g-4 mb-4">
            <div class="col-md-3">
                <StatsCard title="Applied" :value="dashboard.stats.applied" subtitle="Applications" />
            </div>

            <div class="col-md-3">
                <StatsCard title="Shortlisted" :value="dashboard.stats.shortlisted" subtitle="Interviews"
                    variant="primary" />
            </div>

            <div class="col-md-3">
                <StatsCard title="Rejected" :value="dashboard.stats.rejected" subtitle="Applications"
                    variant="primary" />

            </div>
            <div class="col-md-3">
                <StatsCard title="Hired" :value="dashboard.stats.hired" subtitle="Offers" variant="success" />

            </div>


        </div>

        <DashboardSection title="Applications" subtitle="Track the progress of your applications">

            <DataTable :columns="applicationColumns" :rows="dashboard.applications">

                <template #cell-status="{ row }">

                    <StatusBadge :status="row.status" />

                </template>

                <template #cell-actions="{ row }">

                    <AppButton v-if="row.status.toUpperCase()!== 'REJECTED'"  label="Withdraw" loadingLabel="Withdrawing..."
                        @click="withdrawApplication(row.driveId)" />


                </template>
            </DataTable>

        </DashboardSection>

        <!-- <DashboardSection >
        
            
        
        </DashboardSection> -->



    </DashboardLayout>
</template>


<script setup>
import DashboardLayout from '../layout/DashboardLayout.vue';
import { studentSidebarItems } from '../utils/StudentsUtils';
import StatsCard from '../components/StatsCard.vue';
import PageHeader from '../components/PageHeader.vue';
import { ref } from 'vue';
import { onMounted } from 'vue';
import { getApplication, StudentsApplicationExportCSVService, withdrawStudentApplication } from '../services/StudentService.js';
import DataTable from '../components/DataTable.vue';
import StatusBadge from '../components/StatusBadge.vue';
import AppButton from '../components/AppButton.vue';


const loading = ref(false)
const error = ref("")

const csvLoading = ref(false)

onMounted(loadApplication)

const dashboard = ref({
    stats: {
        applied: 0,
        shortlisted: 0,
        rejected: 0,
        hired: 0
    },
    applications: []
});


const applicationColumns = [
    {
        key: "companyName",
        label: "Company"
    },
    {
        key: "driveName",
        label: "Drive"
    },
    {
        key: "applicationDate",
        label: "Applied On"
    },
    {
        key:"ctc",
        label:"CTC"
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

async function exportApplications(){
    csvLoading.value=true
    try{
        await StudentsApplicationExportCSVService();
        alert("Export has started.The CSV will be emailed to you shortly.")
    }catch(err){
        console.log(err)
    }
    finally{
        csvLoading.value=false
    }
}

async function withdrawApplication(driveId){
    try{
        const response = await withdrawStudentApplication(driveId)
        loadApplication()
    }
    catch(err){
        console.log(err)  
    }
}

async function loadApplication() {
    loading.value = true;
    try {
        const response = await getApplication();
        dashboard.value = response.data.data;
        console.log(response.data.data)
    }
    catch (err) {
        console.log(err);
    }
    finally {
        loading.value = false;
    }
}

</script>
