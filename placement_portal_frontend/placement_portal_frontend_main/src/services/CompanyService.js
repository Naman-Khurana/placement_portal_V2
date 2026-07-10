import api from "../api/axios";
import { COMPANY_DASHBOARD_API, GET_COMPANY_ACTIVE_DRIVES } from "../utils/urlConstants";

export async function getCompaniesActiveDrives(companyId){
    return await api.get(GET_COMPANY_ACTIVE_DRIVES(companyId));
}
export async function getCompanyDashboard() {
    return await api.get(COMPANY_DASHBOARD_API)
}