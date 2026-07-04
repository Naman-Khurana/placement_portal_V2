<template>
    <AuthLayout>
        <form @submit.prevent="handleLogin">
            <h2 class="text-center mb-2">Placement Portal</h2>
            <p class="text-center text-muted mb-4">
                Welcome back! Sign in to continue.
            </p>
            <div class="mb-3">
                <div v-if="errors.login" class="alert alert-danger">

                    {{ errors.login }}

                </div>

                <div class="text-danger mt-1">
                    {{ errors.email }}
                </div>
                <label class="form-label">Email</label>

                <input class="form-control" type="email" placeholder="Enter your email" v-model="form.email" />
            </div>

            <div class="mb-3">
                <div class="text-danger mt-1">
                    {{ errors.password }}
                </div>

                <label class="form-label">Password</label>

                <input class="form-control" type="password" placeholder="Enter your password" v-model="form.password" />
            </div>




            <button class="btn btn-primary" :disabled="isLoading"> {{ isLoading ? "Logging in..." : "Login" }}
            </button>

            <div class="text-center mt-3">

                Don't have an account?

                <RouterLink to="/register">

                    Register

                </RouterLink>


            </div>

        </form>

    </AuthLayout>



</template>


<script setup>

import { ref, reactive } from "vue"
import { login } from "../services/authService"
import AuthLayout from "../layout/AuthLayout.vue"
import api from "../api/axios.js"
import { useAuthStore } from "../stores/AuthStore.js"


const form = reactive({
    email: "",
    password: ""
})

const errors = reactive({
    email: "",
    password: "",
    login: ""
})

const isLoading = ref(false)

const authStore =useAuthStore()

function validateForm() {

    errors.email = ""
    errors.password = ""
    errors.login = ""


    let isValid = true


    if (form.email.trim() === "") {
        errors.email = "Email is required"
        isValid = false
    }

    if (form.password.trim() === "") {
        errors.password = "Password is required"
        isValid = false
    }

    return isValid;
}


function buildCredentials() {

    return {
        username: form.email.trim(),
        password: form.password.trim()
    }
}


async function handleLogin() {


    if (!validateForm()) {
        return
    }


    isLoading.value = true

    try {
        const response = await login(buildCredentials())
        // console.log(response.data.data);

        authStore.login(response.data.data);
        console.log(authStore.currentUser)
        console.log(authStore.userRole);

        
        // const response2= await api.get("/api/auth/test");
        // console.log(response2.data);

        

    } catch (error) {
        console.log(error);
        errors.login = error.response?.data?.message || "Something went wrong. Please try again."

    } finally {
        isLoading.value = false
    }

}

</script>