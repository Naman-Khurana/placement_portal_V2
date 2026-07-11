from flask import Blueprint,render_template,session,redirect,url_for,abort
from http import HTTPMethod 
from flask import request
from placementportalcode.models import User,Company,PlacementDrive,Application
from placementportalcode.enums.role import RoleEnum
from placementportalcode.enums.modelsenum import UserEnum
from placementportalcode.enums.approval_status import CompanyEnumStatus,DriveApprovalStatusEnum
from placementportalcode.enums.application_status import ApplicationStatusEnum
from placementportalcode.extensions import db
from datetime import datetime
from sqlalchemy import or_
from placementportalcode.utils.responses import success_response,error_response


admin_bp=Blueprint("admin",__name__,url_prefix="/api/admin")

@admin_bp.route("/dashboard",methods=[HTTPMethod.GET] )
def dashboard():
    if not checkAdmin():
        return error_response(message="Unauthorized",status_code=403)
   
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

   
    return success_response(
        message="admin dashboard fetched successfully",
        data= {
            "stats":{
                "companies":total_company_count,
                "students":total_student_count,
                "drives":total_drive_count,
                "applications": total_application_count
            },
            "pendingDrives":pendingApprovalDrives,
            "pendingCompanies":pendingApprovalCompanies
        },
        status_code=200
        )
    

    
@admin_bp.route("/companies",methods= [HTTPMethod.GET])
def get_companies():
    
    if not checkAdmin():
        return error_response(message="Unauthorized",status_code=403)
   
    
    query = Company.query
    
    search=request.args.get("search")
    
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
        
    return success_response(
        message="all companies data fetched",
        data ={
            "pendingCompanies":pendingCompanies,
            "approvedCompanies":approvedCompanies,
            "blacklistedCompanies":blacklistedCompanies
        },status_code=200
    )


    
@admin_bp.route("/drives",methods= [HTTPMethod.GET])
def get_drives():
    
    if not checkAdmin():
        return error_response(message="Unauthorized",status_code=403)
   
    
    query = PlacementDrive.query
    
    search=request.args.get("search")
    
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
            "status": drive.status
        }
        
        if drive.status==DriveApprovalStatusEnum.PENDING.value:
            pendingDrives.append(driveData)
        elif drive.status==DriveApprovalStatusEnum.APPROVED.value and drive.application_deadline >= now:
            approvedDrives.append(driveData)
        elif drive.status==DriveApprovalStatusEnum.REJECT.value:
            rejectedDrives.append(driveData)
        else:
            closedDrives.append(driveData)
        
    return success_response(
        message="all drives data fetched",
        data ={
            "pendingDrives":pendingDrives,
            "approvedDrives":approvedDrives,
            "rejectedDrives":rejectedDrives,
            "closedDrives":closedDrives
        },
        status_code=200
    )

@admin_bp.route("/students",methods= [HTTPMethod.GET])
def get_students():
    
    if not checkAdmin():
        return error_response(message="Unauthorized",status_code=403)
   
    
    query = User.query.filter(
        User.role== RoleEnum.STUDENT.value
    )
    search=request.args.get("search")
    
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
        
        
        
    return success_response(
        message="all students data fetched",
        data ={
            "students":studentsData
        },
        status_code=200
    )



@admin_bp.route("/applications",methods= [HTTPMethod.GET])
def get_applications():
    
    if not checkAdmin():
        return error_response(message="Unauthorized",status_code=403)
   
    query=Application.query
    query = (
    Application.query
        .join(Application.student)
        .join(Application.drive)
        .join(PlacementDrive.company)
    )
    search = request.args.get("search")
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
            "companyName" : application.drive.company.company_name,
            "studentName": application.student.name,
            "status": application.status,
            "applicationDate":application.application_date.strftime("%d %b %Y"),
            "driveName":application.drive.drive_name
        }
        applicationsData.append(applicationData)
        
        
        
    return success_response(
        message="all applications data fetched",
        data ={
            "applications":applicationsData
        },
        status_code=200
    )

    
@admin_bp.route("/companies/<int:company_id>/status",methods=[HTTPMethod.PATCH])
def update_company_status(company_id):
    
    company=Company.query.get(company_id)
    if not company:
        return error_response( message="company not found",status_code=404)
    data =request.get_json()
    action=data.get('action')
    
    if(action=='approve'):
        company.approval_status=CompanyEnumStatus.APPROVED.value
    
    elif action=='blacklist':
        company.approval_status=CompanyEnumStatus.BLACKLISTED.value
    else:
        return error_response(message="Bad Request", status_code=400)
    try:
        db.session.commit()
        return success_response(message="company status updated successfully",status_code=200)
    except Exception as e:
        db.session.rollback()
        return error_response(message=str(e),status_code=500)

@admin_bp.route("/drives/<int:drive_id>/status",methods=[HTTPMethod.PATCH])
def update_drive_status(drive_id):
    drive=PlacementDrive.query.get(drive_id)
    if not drive:
        return error_response(message="drive not found", status_code=404)
    data =request.get_json()
    action=data.get('action')
    
    if(action=='approve'):
        drive.status=DriveApprovalStatusEnum.APPROVED.value
    
    elif action=='reject':
        drive.status=DriveApprovalStatusEnum.REJECT.value
    elif action=='close':
        drive.status=DriveApprovalStatusEnum.CLOSED.value
    else:
        return error_response(message="Bad Request", status_code=400)

    try:
        db.session.commit()
        return success_response(message="drive status updated successfully",status_code=200)
    except Exception as e:
        db.session.rollback()
        return error_response(message=str(e),status_code=500)

@admin_bp.route("/students/<int:student_id>/status",methods=[HTTPMethod.PATCH])
def update_student_status(student_id):
    student=User.query.get(student_id)
    if not student:
        return error_response(message="student not found", status_code=404)
    data =request.get_json()
    action=data.get('action')
    
    if(action=='whitelist'):
        student.eligible=True
    
    elif action=='blacklist':
        student.eligible=False
    else:
        return error_response(message="Bad Request", status_code=400)

    try:
        db.session.commit()
        return success_response(message="student status updated successfully",status_code=200)
    except Exception as e:
        db.session.rollback()
        return error_response(message=str(e),status_code=500)


@admin_bp.route("/applications/<int:application_id>/status",methods=[HTTPMethod.PATCH])
def update_application_status(application_id):
    application=Application.query.get(application_id)
    if not application:
        return error_response(message="application not found", status_code=404)
    data = request.get_json()
    action=data.get('action')
    
    
    if(action=='shortlisted'):
        application.status=ApplicationStatusEnum.SHORTLISTED.value
    elif action=='rejected':
        application.status=ApplicationStatusEnum.REJECTED.value
    elif action=='selected':
        application.status=ApplicationStatusEnum.SELECTED.value
    elif action=='hired':
        application.status=ApplicationStatusEnum.HIRED.value
    elif action=='waitlisted':
        application.status=ApplicationStatusEnum.WAITLISTED.value
    else:
        return error_response(message="Bad Request", status_code=400)

    try:
        db.session.commit()
        return success_response(message="application status updated successfully",status_code=200)
    except Exception as e:
        db.session.rollback()
        return error_response(message=str(e),status_code=500)


    

def checkAdmin():
    user_id=session.get("user_id")
    if not user_id:
        return False
    user=User.query.get(user_id)
    if not user or user.role!=RoleEnum.ADMIN.value:
        return False
    return True
    
    
