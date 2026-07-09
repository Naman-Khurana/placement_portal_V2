<template>
    <div class="d-flex flex-column vh-100">

        <AppNavbar />
        <div class="flex-grow-1 d-flex  ">

            <AppSidebar :items="sidebarItems" :title="title"/>
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

defineProps({
    sidebarItems: {
        type: Array,
        default:()=> []
    },
    title:{
        type:String,
        default:""
    }
})
</script>