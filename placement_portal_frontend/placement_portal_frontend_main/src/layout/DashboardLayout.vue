<template>
    <div class="d-flex vh-100">
        <AppSidebar />
        <div class="flex-grow-1 d-flex flex-column">
            <AppNavbar />

            <main class="flex-grow-1 p-4 bg-light overflow-auto">

                <slot />

            </main>

        </div>

        <Slot />

    </div>
</template>

<script setup>
import AppNavbar from '../components/AppNavbar.vue';
import AppSidebar from '../components/AppSidebar.vue';
</script>