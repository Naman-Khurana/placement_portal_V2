import api from "../api/axios";
import { STUDENT_DASHBOARD_API } from "../utils/urlConstants";

export async function getStudentDashboard(){
    return await api.get(STUDENT_DASHBOARD_API)
} 

