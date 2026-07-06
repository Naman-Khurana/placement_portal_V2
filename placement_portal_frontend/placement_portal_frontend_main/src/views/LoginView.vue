<template>
    <AuthLayout>
        <form @submit.prevent="handleLogin">
            <h2 class="text-center mb-2">Placement Portal</h2>
            <p class="text-center text-muted mb-4">
                Welcome back! Sign in to continue.
            </p>

                <AppInput id="username" label="Username" v-model="form.username" :error="errors.username"
                    placeholder="Enter your username" />

            <AppInput id="password" label="Password" v-model="form.password" :error="errors.password"
                placeholder="Enter your password" />





            <button class="btn btn-primary d-block mx-auto" :disabled="isLoading"> {{ isLoading ? "Logging in..." : "Login" }}
            </button>

            <div class="text-center mt-3">

                Don't have an account?

                <RouterLink :to =STUDENT_REGISTER_ROUTE>

                    Register

                </RouterLink>


            </div>

        </form>

    </AuthLayout>



</template>


<script setup>

import { ref, reactive } from "vue"
import { login, logout } from "../services/authService"
import AuthLayout from "../layout/AuthLayout.vue"
import api from "../api/axios.js"
import { useAuthStore } from "../stores/AuthStore.js"
import { getDashboardRoute } from "../utils/navigation.js"
import AppInput from "../components/AppInput.vue"
import { useRouter } from "vue-router"
import { STUDENT_REGISTER_ROUTE } from "../utils/routeConstants"
import { GET_CURRENT_USER_API, REGISTER_STUDENT_API } from "../utils/urlConstants.js"


const form = reactive({
    email: "",
    password: ""
})

const errors = reactive({
    email: "",
    password: "",
    login: ""
})

const router = useRouter()
const isLoading = ref(false)

const authStore = useAuthStore()

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
    // logout()
    // const response = await api.get(GET_CURRENT_USER_API)
    // console.log(response.data.data);
        
    if (!validateForm()) {
        return
    }


    isLoading.value = true

    try {
        const response = await login(buildCredentials())
        // console.log(response.data.data);

        authStore.setAuthenticatedUser(response.data.data);

        router.push(getDashboardRoute(authStore.userRole));


    } catch (error) {
        console.log(error);
        errors.login = error.response?.data?.message || "Something went wrong. Please try again."

    } finally {
        isLoading.value = false
    }

}

</script>














<!-- <div class="mb-3">
                <div v-if="errors.login" class="alert alert-danger">

                    {{ errors.login }}

                </div>

                <div class="text-danger mt-1">
                    {{ errors.email }}
                </div>
                <label class="form-label">Email</label>

                <input class="form-control" type="email" placeholder="Enter your email" v-model="form.email" />
            </div> -->