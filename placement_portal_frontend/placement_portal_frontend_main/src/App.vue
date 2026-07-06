<script setup>
import Login from './views/LoginView.vue';
import { onMounted } from 'vue';
import { useAuthStore } from './stores/AuthStore.js';

const authStore = useAuthStore();

onMounted(() => {
  authStore.initAuth();
});

</script>

<template>
  <div v-if="authStore.isInitializing" class="vh-100 d-flex justify-content-center align-items-center">
    Loading...
  </div>
  <RouterView v-else/>
</template>
