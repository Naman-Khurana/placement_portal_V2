<template>
    <AuthLayout>
        <form @submit.prevent="handleCompanyRegistration">
            <h2 class="text-center mb-2">Placement Portal</h2>
            <p class="text-center text-muted mb-4">
                Register your organization!
            </p>
            <AppAlert :message="errors.register" />
            <AppInput id="companyName" label="Company Name" v-model="form.companyName" :error="errors.companyName"
                placeholder="Enter your Company Name" :disabled="isLoading" required />

            <AppInput id="email" label="HR Contact Email " v-model="form.email" :error="errors.email"
                placeholder="Enter your HR Email" :disabled="isLoading" required />
            <AppInput id="companyWebsite" label="Company Website" v-model="form.companyWebsite"
                :error="errors.companyWebsite" placeholder="Enter your Company Website" :disabled="isLoading"
                required />
            <AppInput id="password" label="Password" v-model="form.password" :error="errors.password"
                placeholder="Enter your password" type="password" :disabled="isLoading" required />
            <AppInput id="confirmPassword" label="Confirm Password" v-model="form.confirmPassword"
                :error="errors.confirmPassword" placeholder="Enter your password again" :disabled="isLoading"
                required />






            <button class="btn btn-primary  d-block mx-auto " :disabled="isLoading"> {{ isLoading ? "Registering Organization..." : "Register" }}
            </button>

            <div class="text-center mt-3">

                Already have an account?

                <RouterLink :to="LOGIN_ROUTE">

                    Login

                </RouterLink>


            </div>
            <div class="text-center mt-3">

                Register as Student?

                <RouterLink :to="STUDENT_REGISTER_ROUTE">

                    Register

                </RouterLink>


            </div>

        </form>

    </AuthLayout>



</template>


<script setup>

import { ref, reactive } from "vue"
import { login, registerCompany, registerStudent } from "../services/authService"
import AuthLayout from "../layout/AuthLayout.vue"
import api from "../api/axios.js"

import router from "../router/index.js"
import { getDashboardRoute } from "../utils/navigation.js"
import { LOGIN_ROUTE } from "../utils/routeConstants"
import AppInput from "../components/AppInput.vue"
import { REGISTER_STUDENT_API } from "../utils/urlConstants.js"
import { STUDENT_REGISTER_ROUTE } from "../utils/routeConstants"
import AppAlert from "../components/AppAlert.vue"

const form = reactive({
    companyName: "",
    email: "",
    companyWebsite: "",
    password: "",
    confirmPassword: ""
})

const errors = reactive({
    companyName: "",
    email: "",
    companyWebsite: "",
    password: "",
    confirmPassword: "",
    register: ""
})

const isLoading = ref(false)


function validateEmptyFormField(field) {
    if (form[field].trim() === "") {
        errors[field] = `${field} is required`;
        return false;
    }
    return true;
}

function validateForm() {

    errors.companyName = ""
    errors.email = ""
    errors.companyWebsite = ""
    errors.password = ""
    errors.confirmPassword = ""
    errors.register = ""


    let isValid = true


    if (!validateEmptyFormField("companyName")) isValid = false;
    if (!validateEmptyFormField("email")) isValid = false;
    if (!validateEmptyFormField("companyWebsite")) isValid = false;
    if (!validateEmptyFormField("password")) isValid = false;
    if (!validateEmptyFormField("confirmPassword")) isValid = false;

    if (form.password !== form.confirmPassword) {
        errors.confirmPassword = "Password doesn't match."
        isValid = false;
    }

    return isValid;
}


function getCompanyData() {

    return {
        company_name: form.companyName.trim(),
        hr_contact: form.email.trim(),
        company_website: form.companyWebsite.trim(),
        password: form.password.trim()
    }
}


async function handleCompanyRegistration() {


    if (!validateForm()) {
        return
    }


    isLoading.value = true

    try {
        const response = await registerCompany(getCompanyData())
        // console.log(response.data.data);

        alert("Registration Successfull")

        router.push(LOGIN_ROUTE);


    } catch (error) {
        console.log(error);
        errors.register = error.response?.data?.message || "Something went wrong. Please try again."

    } finally {
        isLoading.value = false
    }

}

</script>