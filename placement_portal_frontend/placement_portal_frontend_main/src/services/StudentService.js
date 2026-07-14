import api from "../api/axios";
import { STUDENT_APPLICATION_API, STUDENT_APPLICATION_WITHDRAW_API, STUDENT_APPLICATIONS_HISTORY_EXPORT_CSV, STUDENT_DASHBOARD_API, STUDENT_DRIVE_APPLY_API, STUDENT_GET_ACTIVE_COMPANY_DRIVES, STUDENT_PROFILE_API, STUDENT_RESUME_UPLOAD_API } from "../utils/urlConstants";

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

export async function getApplication() {
    return await api.get(STUDENT_APPLICATION_API)
}

export async function withdrawStudentApplication(driveId){
    return await api.delete(STUDENT_APPLICATION_WITHDRAW_API(driveId));
}

export async function applyDrive(driveId){
    return await api.post(STUDENT_DRIVE_APPLY_API(driveId))
}

export async function getCompaniesActiveDrivesForStudent(companyId){
    return await api.get(STUDENT_GET_ACTIVE_COMPANY_DRIVES(companyId))
}

export async function StudentsApplicationExportCSVService(){
    return await api.post(STUDENT_APPLICATIONS_HISTORY_EXPORT_CSV)
}