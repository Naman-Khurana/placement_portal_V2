import api from "../api/axios";
import { COMPANY_DASHBOARD_API, COMPANY_DRIVES_API, COMPANY_DRIVES_EDIT_API, GET_COMPANY_ACTIVE_DRIVES } from "../utils/urlConstants";

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
    return await api.patch(COMPANY_DRIVES_EDIT_API(driveId),status);
}