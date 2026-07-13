from placementportalcode.models import *
from placementportalcode.extensions import cache

from flask import request
from sqlalchemy import or_

@cache.memoize(timeout=300)
def get_admin_dashboard_data():
    now=datetime.now()
    total_company_count=  Company.query.count()
    
    pending_approval_companies=Company.query.filter_by(approval_status=CompanyEnumStatus.PENDING.value).all()
    # registered_companies=Company.query.filter_by(approval_status=CompanyEnumStatus.APPROVED.value)    
    # blacklisted_companies=Company.query.filter_by(approval_status=CompanyEnumStatus.BLACKLISTED.value)
    
    total_student_count= User.query.filter_by( role=RoleEnum.STUDENT.value).count()
    # registered_students=User.query.filter_by(role=RoleEnum.STUDENT.value )

    total_drive_count=PlacementDrive.query.count()
    pending_approval_drives=PlacementDrive.query.filter(PlacementDrive.status==DriveApprovalStatusEnum.PENDING.value).all()
    # rejected_drives=PlacementDrive.query.filter(PlacementDrive.status==DriveApprovalStatusEnum.REJECT.value)
    # ongoing_drives=PlacementDrive.query.filter(PlacementDrive.status=='approved',PlacementDrive.status==DriveApprovalStatusEnum.APPROVED.value)
    
    total_application_count= Application.query.count()
    # student_applications=Application.query.all()
    
    pendingApprovalCompanies=[]
    
    for company in pending_approval_companies:
        pendingApprovalCompanies.append({
            "companyId":company.company_id, 
            "companyName":company.company_name,
            "website":company.company_website,
            "hrContact":company.hr_contact,
            "status":company.approval_status
        })
        
    pendingApprovalDrives=[]
    
    for drive in pending_approval_drives:
        pendingApprovalDrives.append({
            "driveId":drive.drive_id,
            "driveName":drive.drive_name,
            "jobTitle":drive.job_title, 
            "ctc":drive.ctc,
            # "job_desc":drive.company_name,
            # "eligibility_criteria":drive.company_website,
            "applicationDeadline":drive.application_deadline.strftime("%d %b %Y"),
            "status":drive.status
        })

    return{
            "stats":{
                "companies":total_company_count,
                "students":total_student_count,
                "drives":total_drive_count,
                "applications": total_application_count
            },
            "pendingDrives":pendingApprovalDrives,
            "pendingCompanies":pendingApprovalCompanies
        }
    
@cache.memoize(timeout=300)
def get_admin_companies(search=None):
    query = Company.query
    
    
    if(search):
        query=query.filter(
            Company.company_name.ilike(f"%{search}%")
        )
    companies=query.all()
    
    pendingCompanies = []
    approvedCompanies = []
    blacklistedCompanies = []
    
    for company in companies:
        companyData = {
            "companyId": company.company_id,
            "companyName": company.company_name,
            "companyWebsite": company.company_website,
            "hrContact": company.hr_contact,
            "approvalStatus": company.approval_status
        }
        
        if company.approval_status==CompanyEnumStatus.PENDING.value:
            pendingCompanies.append(companyData)
        elif company.approval_status==CompanyEnumStatus.APPROVED.value:
            approvedCompanies.append(companyData)
        elif company.approval_status==CompanyEnumStatus.BLACKLISTED.value:
            blacklistedCompanies.append(companyData)
        
        
        
    return {
            "pendingCompanies":pendingCompanies,
            "approvedCompanies":approvedCompanies,
            "blacklistedCompanies":blacklistedCompanies
        }
    
@cache.memoize(timeout=300)
def get_admin_drives(search=None):
    query = PlacementDrive.query
    
   
    
    if(search):
        query=query.filter(
            PlacementDrive.drive_name.ilike(f"%{search}%")
        )
    drives=query.all()
    
    pendingDrives = []
    approvedDrives = []
    closedDrives = []
    rejectedDrives = []
    
    now = datetime.now()
    
    for drive in drives:
        driveData = {
            "driveId": drive.drive_id,
            "driveName": drive.drive_name,
            "jobTitle": drive.job_title,
            "applicationDeadline": drive.application_deadline.strftime("%d %b %Y"),
            "company": drive.company.company_name,
            "status": drive.status,
            "ctc" : drive.ctc
        }
        
        if drive.status==DriveApprovalStatusEnum.PENDING.value:
            pendingDrives.append(driveData)
        elif drive.status==DriveApprovalStatusEnum.APPROVED.value and drive.application_deadline >= now:
            approvedDrives.append(driveData)
        elif drive.status==DriveApprovalStatusEnum.REJECT.value:
            rejectedDrives.append(driveData)
        else:
            closedDrives.append(driveData)
            
            
            
    return{
            "pendingDrives":pendingDrives,
            "approvedDrives":approvedDrives,
            "rejectedDrives":rejectedDrives,
            "closedDrives":closedDrives
        }
    
@cache.memoize(timeout=300)
def get_admin_students(search=None):
    
    query = User.query.filter(
        User.role== RoleEnum.STUDENT.value
    )
    
    
    if(search):
        query=query.filter(
            User.name.ilike(f"%{search}%")
        )
    students=query.all()
    studentsData=[];
    for student in students:
        studentData = {
            "studentId" : student.id,
            "name": student.name,
            "eligible": student.eligible
        }
        studentsData.append(studentData)
    
    return{
            "students":studentsData
        }
    
    
    
@cache.memoize(timeout=300)
def get_admin_applications(search=None):
    
    query=Application.query
    query = (
    Application.query
        .join(Application.student)
        .join(Application.drive)
        .join(PlacementDrive.company)
    )
    
    if search:
        query = query.filter(
            or_(
                User.name.ilike(f"%{search}%"),
                PlacementDrive.drive_name.ilike(f"%{search}%"),
                Company.company_name.ilike(f"%{search}%")
            )
        ).distinct()
    applications=query.all()
    applicationsData=[]
    for application in applications:
        applicationData = {
            "applicationId":application.application_id,
            "companyName" : application.drive.company.company_name,
            "studentName": application.student.name,
            "status": application.status,
            "applicationDate":application.application_date.strftime("%d %b %Y"),
            "driveName":application.drive.drive_name
        }
        applicationsData.append(applicationData)
        
    return {
            "applications":applicationsData
        }