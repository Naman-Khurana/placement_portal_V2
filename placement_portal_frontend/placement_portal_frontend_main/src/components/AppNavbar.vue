<template>
    <nav class="navbar-expand-lg bg-white border-bottom  d-flex justify-content-between align-items-center py-3 px-3">
        <div class="navbar-brand fw-bold">Placement Portal</div>
        <div class="d-flex gap-5 align-items-center">
            <div class="ms-auto">
               
            </div>
            <AppButton label="Logout" loading-label="Logging out..." type="danger" @click="logoutUser()">Logout</AppButton>
        </div>
    </nav>
</template>


<script setup>
import AppButton from './AppButton.vue';
import { useAuthStore } from '../stores/AuthStore.js';
import { useRouter } from "vue-router"
import { LOGIN_ROUTE } from '../utils/routeConstants';
const authStore= useAuthStore()
const router = useRouter()

async function logoutUser() {
    await authStore.logout()

    router.push(LOGIN_ROUTE)
}
</script>