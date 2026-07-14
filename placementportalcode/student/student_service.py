from placementportalcode.models import Company,Application,PlacementDrive,User
from placementportalcode.enums.approval_status import CompanyEnumStatus,DriveApprovalStatusEnum
from datetime import datetime
from flask import session
from placementportalcode.extensions import cache
from placementportalcode.utils.responses import success_response,error_response

# @cache.memoize(timeout=300)
def get_student_dashboard_data(user_id):
    
    print("FETCHING FROM DATABASE")
    if not user_id:
        return error_response(message="Unauthorized",status_code=401)
    user=User.query.get(user_id)
    
    registered_companies = (Company.query.join(PlacementDrive)
        .filter(
            Company.approval_status == CompanyEnumStatus.APPROVED.value,
            PlacementDrive.status == DriveApprovalStatusEnum.APPROVED.value,
            PlacementDrive.application_deadline >= datetime.now()
        ).distinct()
    )
    student_applications=Application.query.filter(Application.student_id==user_id).all()
    upcoming_drives= PlacementDrive.query.filter(
            PlacementDrive.status== DriveApprovalStatusEnum.APPROVED.value,
            PlacementDrive.application_deadline >=datetime.now()
        ).count() 
    
    stats= {
        "applications" : len(student_applications),
        "approvedCompanies": registered_companies.count(),
        "upcomingDrives": upcoming_drives
    }
    
    approved_companies =[]
    
    for company in registered_companies:
        approved_companies.append({
            "id":company.company_id,
            "companyName":company.company_name,
            "website": company.company_website
        })
        
    applications = []
    
    for application in student_applications:
        applications.append({
            "applicationId": application.application_id,
            "status": application.status,
            "applicationDate" : application.application_date.isoformat(),
            "driveTitle" : application.drive.drive_name,
            "companyName" : application.drive.company.company_name
        })

    
    return{
            "student": {
                "id":user.id,
                "name":user.name,
                "department":user.department,
                "resumeUploaded": bool(user.resume_path),
                "eligible": user.eligible
            },
            "stats" : stats,
            "approvedCompanies" : approved_companies,
            "recentApplications": applications
        }

@cache.memoize(timeout=300)    
def get_student_profile(user_id):
    student = User.query.get(user_id)

    if not student:
        return error_response("Student not found" , status_code=404)
    
    return{
                "name": student.name,
                "username": student.username,
                "department": student.department,
                "dob": student.dob.isoformat() if student.dob else None,
                "resumePath": student.resume_path
            }