<template>
    <AuthLayout>
        <form @submit.prevent="handleStudentRegistration">
            <h2 class="text-center mb-2">Placement Portal</h2>
            <p class="text-center text-muted mb-4">
                Register as Student
            </p>
            <AppAlert :message="errors.register" />

            <AppInput id="name" label="Name" v-model="form.name" :error="errors.name" placeholder="Enter your name" :disabled="isLoading" required />

            <AppInput id="username" label="Username" v-model="form.username" :error="errors.username"
                placeholder="Enter your username" :disabled="isLoading" required />
            <AppInput id="password" label="Password" v-model="form.password" :error="errors.password"
                placeholder="Enter your password" type="password" :disabled="isLoading" required/>
            <AppInput id="confirmPassword" label="Confirm Password" v-model="form.confirmPassword"
                :error="errors.confirmPassword" placeholder="Enter your password again" :disabled="isLoading" required />






            <button class="btn btn-primary  d-block mx-auto " :disabled="isLoading"> {{ isLoading ? "Registering Student..." : "Register" }}
            </button>

            <div class="text-center mt-3">

                Already have an account?

                <RouterLink :to="LOGIN_ROUTE">

                    Login

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
import { login, registerStudent } from "../services/authService"
import AuthLayout from "../layout/AuthLayout.vue"
import api from "../api/axios.js"

import router from "../router/index.js"
import { getDashboardRoute } from "../utils/navigation.js"
import { LOGIN_ROUTE } from "../utils/routeConstants"
import AppInput from "../components/AppInput.vue"
import { COMPANY_REGISTER_ROUTE } from "../utils/routeConstants"
import AppAlert from "../components/AppAlert.vue"
import { validateEmail } from "../utils/emailUtils.js"

const form = reactive({
    name: "",
    username: "",
    password: "",
    confirmPassword: ""
})

const errors = reactive({
    name: "",
    username: "",
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

    errors.name = ""
    errors.username = ""
    errors.password = ""
    errors.confirmPassword = ""
    errors.register = ""


    let isValid = true


    if (!validateEmptyFormField("name")) isValid = false;
    if (!validateEmptyFormField("username")) isValid = false;
    if (!validateEmptyFormField("password")) isValid = false;
    if (!validateEmptyFormField("confirmPassword")) isValid = false;

    if (form.password !== form.confirmPassword) {
        errors.confirmPassword = "Password doesn't match."
        isValid = false;
    }
    if(!validateEmail(form.username)){
        errors.username = "Please enter a valid email address.";
        isValid=false
    }
    return isValid;
}


function getStudentData() {

    return {
        name: form.name.trim(),
        username: form.username.trim(),
        password: form.password.trim()
    }
}


async function handleStudentRegistration() {


    if (!validateForm()) {
        return
    }


    isLoading.value = true

    try {
        const response = await registerStudent(getStudentData())
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