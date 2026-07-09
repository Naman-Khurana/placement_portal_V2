import api from "../api/axios";
import { STUDENT_DASHBOARD_API, STUDENT_PROFILE_API, STUDENT_RESUME_UPLOAD_API } from "../utils/urlConstants";

export async function getStudentDashboard(){
    return await api.get(STUDENT_DASHBOARD_API)
} 

export async function getStudentProfile(){
    return await api.get(STUDENT_PROFILE_API)
}
export async function updateStudentProfile(profile){
    return await api.put(STUDENT_PROFILE_API,profile)
}

export async function uploadStudentResume(formData){
    return await api.post(STUDENT_RESUME_UPLOAD_API,formData,{
        headers:{
            "Content-Type":"multipart/form-data"
        }
    })
}