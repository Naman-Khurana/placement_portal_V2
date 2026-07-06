<template>
    <AuthLayout>
        <form @submit.prevent="handleLogin">
            <h2 class="text-center mb-2">Placement Portal</h2>
            <p class="text-center text-muted mb-4">
                Welcome back! Sign in to continue.
            </p>
            <AppAlert :message="errors.login" />

            <AppInput id="username" label="Username" v-model="form.username" :error="errors.username"
                placeholder="Enter your username" :disabled="isLoading" required  />

            <AppInput id="password" label="Password" v-model="form.password" :error="errors.password"
                placeholder="Enter your password" type="password" :disabled="isLoading" required />





            <AppButton label="Login" loading-label="Logging In..." :loading="isLoading" />

            <div class="text-center mt-3">

                Don't have an account?

                <RouterLink :to="STUDENT_REGISTER_ROUTE">

                    Register

                </RouterLink>


            </div>

            <div class="text-center mt-3">

                Register your organization for drives?

                <RouterLink :to="COMPANY_REGISTER_ROUTE">

                    Register

                </RouterLink>


            </div>

        </form>

    </AuthLayout>



</template>


<script setup>

import { ref, reactive } from "vue"
import { login} from "../services/authService"
import AuthLayout from "../layout/AuthLayout.vue"
import { useAuthStore } from "../stores/AuthStore.js"
import { getDashboardRoute } from "../utils/navigation.js"
import AppInput from "../components/AppInput.vue"
import { useRouter } from "vue-router"
import { STUDENT_REGISTER_ROUTE } from "../utils/routeConstants"
import AppButton from "../components/AppButton.vue"
import AppAlert from "../components/AppAlert.vue"
import { COMPANY_REGISTER_ROUTE } from "../utils/routeConstants"


const form = reactive({
    username: "",
    password: ""
})

const errors = reactive({
    username: "",
    password: "",
    login: ""
})

const router = useRouter()
const isLoading = ref(false)

const authStore = useAuthStore()

function validateForm() {

    errors.username = ""
    errors.password = ""
    errors.login = ""


    let isValid = true


    if (form.username.trim() === "") {
        errors.username = "Username is required"
        isValid = false
    }

    if (form.password.trim() === "") {
        errors.password = "Password is required"
        isValid = false
    }

    return isValid;
}


function getCredentials() {

    return {
        username: form.username.trim(),
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
        const response = await login(getCredentials())
        // console.log(response.data.data);

        authStore.setAuthenticatedUser(response.data.data);

        router.push(getDashboardRoute(authStore.userRole));


    } catch (error) {
        console.log(error);
        errors.login = error.response?.data?.message || "Something went wrong. Please try again."
        form.password=""

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