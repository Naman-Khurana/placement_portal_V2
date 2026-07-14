import api from "../api/axios";
import { COMPANY_DASHBOARD_API, COMPANY_DRIVE_APPLICANTS_API, COMPANY_DRIVES_API, COMPANY_DRIVES_EDIT_API, COMPANY_PROFILE_API, COMPANY_UPDATE_APPLICATION_STATUS, GET_COMPANY_ACTIVE_DRIVES } from "../utils/urlConstants";

export async function getCompaniesActiveDrives(companyId){
    return await api.get(GET_COMPANY_ACTIVE_DRIVES(companyId));
}
export async function getCompanyDashboard() {
    return await api.get(COMPANY_DASHBOARD_API);
}

export async function getCompanyDrives(){
    return await api.get(COMPANY_DRIVES_API);
}

export async function createCompanyDrive(newDrive) {
    return await api.post(COMPANY_DRIVES_API,newDrive);
}

export async function editCompanyDrive(driveId,updateDrive) {
    return await api.put(COMPANY_DRIVES_EDIT_API(driveId),updateDrive);
}

export async function updateCompanyDriveStatus(driveId,status) {
    return await api.patch(COMPANY_DRIVES_EDIT_API(driveId),{action:status});
}

export async function getCompanyProfile() {
    return await api.get(COMPANY_PROFILE_API);
}

export async function updateCompanyProfile(data) {
    return await api.put(COMPANY_PROFILE_API,data);
}

export async function getCompanyDriveApplications(driveId){
    return await api.get(COMPANY_DRIVE_APPLICANTS_API(driveId))
}
export async function updateCompanyApplicationStatus(applicationId,status){
    return await api.patch(COMPANY_UPDATE_APPLICATION_STATUS(applicationId),{ status : status })
}


