import api from "../api/axios";
import { GET_COMPANY_ACTIVE_DRIVES } from "../utils/urlConstants";

export async function getCompaniesActiveDrives(companyId){
    return await api.get(GET_COMPANY_ACTIVE_DRIVES(companyId));
}