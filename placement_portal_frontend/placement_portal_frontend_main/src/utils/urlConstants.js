
// auth apis
export const AUTH_PREFIX ="/api/auth";
export const LOGOUT_API = AUTH_PREFIX + "/logout"
export const LOGIN_API = AUTH_PREFIX + "/login"
export const GET_CURRENT_USER_API = AUTH_PREFIX + "/test"
export const REGISTER_STUDENT_API = AUTH_PREFIX + "/register"
export const REGISTER_COMPANY_API= AUTH_PREFIX + "/register-company"


// student apis
export const STUDENT_PREFIX="/api/student"
export const STUDENT_DASHBOARD_API= STUDENT_PREFIX + "/dashboard"
export const STUDENT_PROFILE_API=STUDENT_PREFIX + "/profile"
export const STUDENT_RESUME_UPLOAD_API= STUDENT_PREFIX + "/profile/resume"
export const STUDENT_APPLICATION_API=STUDENT_PREFIX + "/applications"
export const STUDENT_APPLICATION_WITHDRAW_API=(driveId)=> STUDENT_PREFIX + `/drives/${driveId}/applications`

//company api"
export const COMPANY_PREFIX= "/api/company"
export const GET_COMPANY_ACTIVE_DRIVES= (companyId) =>COMPANY_PREFIX +`/${companyId}/drives`
export const COMPANY_DASHBOARD_API= COMPANY_PREFIX + "/dashboard"
export const COMPANY_DRIVES_API= COMPANY_PREFIX + "/drives"
export const COMPANY_DRIVES_EDIT_API=(driveId)=> COMPANY_PREFIX + `/drives/${driveId}`
export const COMPANY_PROFILE_API= COMPANY_PREFIX + "/profile"

//admin apis

export const ADMIN_PREFIX= "/api/admin"
export const ADMIN_DASHBOARD_API= ADMIN_PREFIX + "/dashboard"
export const ADMIN_COMPANIES_STATUS_UPDATE_API=(id)=>ADMIN_PREFIX + `/companies/${id}/status`
export const ADMIN_STUDENTS_STATUS_UPDATE_API=(id)=>ADMIN_PREFIX + `/students/${id}/status`
export const ADMIN_DRIVES_STATUS_UPDATE_API=(id)=>ADMIN_PREFIX + `/drives/${id}/status`
export const ADMIN_APPLICATIONS_STATUS_UPDATE_API=(id)=>ADMIN_PREFIX + `/applications/${id}/status`
export const ADMIN_COMPANIES_API=ADMIN_PREFIX + "/companies"
export const ADMIN_STUDENTS_API=ADMIN_PREFIX + "/students"
export const ADMIN_DRIVES_API=ADMIN_PREFIX + "/drives"
export const ADMIN_APPLICATIONS_API=ADMIN_PREFIX + "/applications"