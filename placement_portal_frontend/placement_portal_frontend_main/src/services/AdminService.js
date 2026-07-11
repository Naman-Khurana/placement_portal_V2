import api from "../api/axios";
import { ADMIN_APPLICATIONS_API, ADMIN_APPLICATIONS_STATUS_UPDATE_API, ADMIN_COMPANIES_API, ADMIN_COMPANIES_STATUS_UPDATE_API, ADMIN_DASHBOARD_API, ADMIN_DRIVES_API, ADMIN_DRIVES_STATUS_UPDATE_API, ADMIN_STUDENTS_API, ADMIN_STUDENTS_STATUS_UPDATE_API } from "../utils/urlConstants";


export async function getAdminDashboard() {
    return await api.get(ADMIN_DASHBOARD_API);
}

export async function getAdminStudentDashboard() {
    return await api.get(ADMIN_STUDENTS_API);
}
export async function getAdminCompanyDashboard() {
    return await api.get(ADMIN_COMPANIES_API);
}
export async function getAdminDriveDashboard() {
    return await api.get(ADMIN_DRIVES_API);
}
export async function getAdminApplicationDashboard() {
    return await api.get(ADMIN_APPLICATIONS_API);
}

export async function updateStudentStatusService(id,data){
    return await api.patch(ADMIN_STUDENTS_STATUS_UPDATE_API(id),{action:data})
}
export async function updateCompanyStatusService(id,data){
    return await api.patch(ADMIN_COMPANIES_STATUS_UPDATE_API(id),{action:data})
}
export async function updateDriveStatusService(id,data){
    return await api.patch(ADMIN_DRIVES_STATUS_UPDATE_API(id),{action:data})
}
export async function updateApplicationStatusService(id,data){
    return await api.patch(ADMIN_APPLICATIONS_STATUS_UPDATE_API(id),{action:data})
}