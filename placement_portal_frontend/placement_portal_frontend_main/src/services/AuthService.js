import api from "../api/axios"
import {GET_CURRENT_USER_API, LOGIN_API, LOGOUT_API, REGISTER_COMPANY_API, REGISTER_STUDENT_API } from "../utils/urlConstants";

export async function login(credentials) {
    return await api.post(LOGIN_API,credentials);
}

export async function getCurrentUser() {
    return await api.get(GET_CURRENT_USER_API);
}

export async function logout(userid) {
    return await api.post(LOGOUT_API,userid);
}

export async function registerStudent(studentData) {
    return await api.post(REGISTER_STUDENT_API,studentData);
}

export async function registerCompany(companyData){
    return await api.post(REGISTER_COMPANY_API,companyData)
}