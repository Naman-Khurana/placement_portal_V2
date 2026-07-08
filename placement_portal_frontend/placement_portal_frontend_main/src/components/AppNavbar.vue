<script setup lang="ts">
import AppButton from './AppButton.vue';

</script>

<template>
    <nav class="navbar-expand-lg bg-white border-bottom  d-flex justify-content-between align-items-center py-3 px-3">
        <div class="navbar-brand fw-bold">Placement Portal</div>
        <div class="d-flex gap-5 align-items-center">
            <div class="ms-auto">
                User
            </div>
            <AppButton label="Logout" loading-label="Logging out..." type="danger">Logout</AppButton>
        </div>
    </nav>
</template>