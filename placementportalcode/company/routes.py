from flask import Flask ,Blueprint,session,render_template,redirect,url_for,request
from placementportalcode.models import Company,User,PlacementDrive,Application
from placementportalcode.enums.role import RoleEnum
from placementportalcode.enums.modelsenum import PlacementDriveEnum,UserEnum,CompanyEnum
from http import HTTPMethod
from placementportalcode.extensions import db
from datetime import datetime,date
from placementportalcode.enums.approval_status import DriveApprovalStatusEnum,CompanyEnumStatus
from sqlalchemy import or_
from placementportalcode.utils.responses import success_response,error_response
from placementportalcode.enums.application_status import ApplicationStatusEnum 
from placementportalcode.company.company_service import *

company_bp=Blueprint("company",__name__,url_prefix="/api/company")

@company_bp.route("/dashboard",methods=[HTTPMethod.GET] )
def dashboard():
    user_id=session.get("user_id")
    
    return success_response(
        message="Dashboard fetched successfully",
        data=get_company_dashboard_data(user_id=user_id),
        status_code=200
    )
    
    
@company_bp.route("/drives",methods=[HTTPMethod.GET,HTTPMethod.POST])
def drives():
    user_id=session.get("user_id")
    if not user_id:
        return error_response( message ="user not found", status_code=404) 
    
    if(request.method==HTTPMethod.GET):
    
        return success_response(
            message="Company drives fetched successfully",
            data=get_company_drives(user_id=user_id)
        )
    
    user=User.query.get(user_id)
    if not user or user.role!=RoleEnum.COMPANY  .value:
        return error_response(message="user not found", status_code=404)
    

    current_company=user.company
    if not current_company:
        return error_response(message='company not found' , status_code=404)
    
    if current_company.approval_status!= CompanyEnumStatus.APPROVED.value:
        return error_response(message="Forbidden", status_code=403)
    
    data=request.get_json()
    drive_name=data.get(PlacementDriveEnum.DRIVE_NAME.value)
    job_title=data.get(PlacementDriveEnum.JOB_TITLE.value)
    job_desc=data.get(PlacementDriveEnum.JOB_DESC.value)
    eligibility_criteria=data.get(PlacementDriveEnum.ELIGIBILITY_CRITERIA.value)
    deadline_raw = data.get(PlacementDriveEnum.APPLICATION_DEADLINE.value)
    ctc=data.get(PlacementDriveEnum.CTC.value)
    application_deadline = datetime.strptime(
        deadline_raw, "%Y-%m-%dT%H:%M"
    )
  
    try:
        new_drive=PlacementDrive(
            drive_name=drive_name,
            company_id=current_company.company_id,
            job_title=job_title,
            job_desc=job_desc,
            status=DriveApprovalStatusEnum.PENDING.value,
            eligibility_criteria=eligibility_criteria,
            application_deadline=application_deadline,
            ctc=ctc

        )

        db.session.add(new_drive)
        db.session.commit()

        invalidate_company_dashboard_and_drives_cache()
        return success_response(
            message="Drive created successfully.",
            data={
                "driveName":new_drive.drive_name,
                "companyId":new_drive.company_id,
                "jobTitle":new_drive.job_title,
                "jobDescription":new_drive.job_desc,
                "status":new_drive.status,
                "eligibilityCriteria":new_drive.eligibility_criteria,
                "applicationDeadline":new_drive.application_deadline,
                "ctc":new_drive.ctc
            },status_code=201
        )
        
    except Exception as e:
        db.session.rollback()
        return error_response(message=str(e), status_code=500)
    

@company_bp.route("drive/<int:dri>/update-applicant-status", methods=[HTTPMethod.POST])
def update_applicant_status():
    user_id=session.get("user_id")
    if not user_id:
        return error_response( message ="user not found", status_code=404) 
    
    
    user=User.query.get(user_id)
    if not user or user.role!=RoleEnum.COMPANY  .value:
        return error_response(message="user not found", status_code=404)
    

    current_company=user.company
    if not current_company:
        return error_response(message='company not found' , status_code=404)

    application_id = request.form.get("application_id")
    status = request.form.get("status")

    application = Application.query.get_or_404(application_id)

    application.status = status

    db.session.commit()

    return redirect(request.referrer)

@company_bp.route("/drives/<int:drive_id>/applications",methods=[HTTPMethod.GET])
def get_drive_applicants(drive_id):
    
    user_id=session.get("user_id")
    if not user_id:
        return error_response( message ="Unauthorized", status_code=401) 
    
    user=User.query.get(user_id)
    if not user or user.role!=RoleEnum.COMPANY.value:
        return error_response(message="Unauthorized", status_code=401)

    drive = PlacementDrive.query.get(drive_id)
    
    if request.method == HTTPMethod.GET:
        
    
        applications = (
            Application.query
            .filter_by(drive_id=drive_id)
            .all()
        )

        applicants = []

        for application in applications:
            student = application.student

            applicants.append({
                "applicationId": application.application_id,
                "studentId": student.id,
                "studentName": student.name,
                "email": student.username,
                "department": student.department,
                "status": application.status,
                "applicationDate": application.application_date.strftime("%d %b %Y"),
                "resume":student.resume_path
            })

        return success_response(data={
            "drive":{
                "driveId":drive.drive_id,
                "driveName":drive.drive_name,
                "jobTitle":drive.job_title,    
            },
            "applications":applicants
        })
        
    
    
    


@company_bp.route("/close-drive", methods=[HTTPMethod.POST])
def close_drive():
    drive_id=request.form.get('drive_id')
    drive=PlacementDrive.query.get_or_404(drive_id)

    drive.status=DriveApprovalStatusEnum.CLOSED.value

    db.session.commit()

    return redirect(request.referrer)

    

@company_bp.route("/drives/<int:id>", methods=[HTTPMethod.PUT,HTTPMethod.PATCH])
def update_drive(id):
    if(request.method==HTTPMethod.PATCH):
            
        user_id=session.get("user_id")
        if not user_id:
            
            return error_response( message ="user not found", status_code=404) 
        user=User.query.get(user_id)
        if not user or user.role!=RoleEnum.COMPANY  .value:
            return error_response(message="user not found", status_code=404)
        

        current_company=user.company
        if not current_company:
            return error_response(message='company not found' , status_code=404)
        drive = PlacementDrive.query.get(id)
        data =request.get_json()
        new_status= data.get("status")
        if not drive:
            return error_response(message="Drive not found",status_code=404)
        
        if drive.company_id != current_company.company_id:
            return error_response(
                message="Unauthorized",
                status_code=403
            )
        
        if (drive.status!= DriveApprovalStatusEnum.APPROVED.value and drive.status!= DriveApprovalStatusEnum.CLOSED.value) or (new_status!= DriveApprovalStatusEnum.APPROVED.value and new_status!= DriveApprovalStatusEnum.CLOSED.value ):
            return error_response(message="Unauthorized",status_code=403)
        try:
            
            drive.status= new_status
            db.session.commit()
            invalidate_company_dashboard_and_drives_cache()
            return success_response(message="drive status updated",status_code=200)
        except Exception as e:
            db.session.rollback()
            return error_response(message=str(e),status_code=500)
    
    
    if(request.method==HTTPMethod.PUT):
        drive = PlacementDrive.query.get(id)
        if not drive:
            return error_response(message="Drive not found",status_code=404)
        data = request.get_json()
        deadline = data.get("application_deadline")
        ctc = data.get("ctc")


        if deadline:
            drive.application_deadline = datetime.strptime(deadline,"%Y-%m-%dT%H:%M").date()

        if ctc:
            drive.ctc = ctc

    
        try:
            db.session.commit()
            invalidate_company_dashboard_and_drives_cache()
            return success_response(message="drive updated successfully", status_code=200)
        except Exception as e:
            db.session.rollback()
            return error_response(message=str(e),status_code=500)

    
@company_bp.route("/profile", methods=[HTTPMethod.GET,HTTPMethod.PUT])
def edit_profile():

    user_id=session.get("user_id")
    if not user_id:
        
        return error_response( message ="user not found", status_code=404) 
    
    if request.method==HTTPMethod.GET:
        return success_response(
            message="company profile fetched successfully",
            data=get_company_profile(user_id=user_id)
            ,status_code=200
        )
    
    
    user=User.query.get(user_id)
    if not user or user.role!=RoleEnum.COMPANY  .value:
        return error_response(message="user not found", status_code=404)
    

    company=user.company
    if not company:
        return error_response(message='company not found' , status_code=404)
    
    data = request.get_json()

    # hr_contact = data.get("hr_contact")
    company_website = data.get("company_website")
    company_name = data.get("company_name")

    # if hr_contact:
    #     company.hr_contact=hr_contact
    if company_website:
        company.company_website=company_website
    if company_name:
        company.company_name=company_name
   
    try:
        db.session.commit()
        
        cache.delete_memoized(get_company_profile,user_id)
        
        return success_response(
            message="company profile updated successfully",
            data={
                "companyId":company.company_id,
                "companyName" : company.company_name,
                "companyWebsite":company.company_website,
                "hrContact":company.hr_contact,
                "approvalStatus":company.approval_status  
            },
            status_code=200)
    except Exception as e:
        db.session.rollback();
        return error_response(message=str(e),status_code=500)
    

    

@company_bp.route("/<int:company_id>/drives",methods=[HTTPMethod.GET])
def on_click_company_drives(company_id):
    company = Company.query.get_or_404(company_id)

    now = datetime.now()

    current_drives = PlacementDrive.query.filter(
        PlacementDrive.company_id == company_id,
        PlacementDrive.status == DriveApprovalStatusEnum.APPROVED.value,
        PlacementDrive.application_deadline >= now
    ).order_by(
        PlacementDrive.application_deadline.asc()
    ).all()
    data={
        "company": {
            "companyId": company.company_id,
            "companyName": company.company_name,
            "website": company.company_website
        },
        "activeDrives": [
        {
            "driveId": drive.drive_id,
            "title": drive.title,
            "package": drive.package,
            "location": drive.location,
            "deadline": drive.application_deadline.strftime("%d %b %Y")
        }
        for drive in current_drives]
    }
        
    return success_response(data=data,message="Company drives fetched successfully", status_code=200)



@company_bp.route("/applications/<int:application_id>/status", methods=[HTTPMethod.PATCH])
def update_application_status(application_id):

    user_id = session.get("user_id")

    if not user_id:
        return error_response(
            message="Unauthorized",
            status_code=401
        )

    user = User.query.get(user_id)

    if not user or user.role != RoleEnum.COMPANY.value:
        return error_response(
            message="Unauthorized",
            status_code=403
        )

    application = Application.query.get(application_id)

    if not application:
        return error_response(
            message="Application not found",
            status_code=404
        )

    if application.drive.company.user.id != user_id:
        return error_response(
            message="Forbidden",
            status_code=403
        )

    data = request.get_json()

    status = data.get("status")

    if not status:
        return error_response(
            message="Status is required",
            status_code=400
        )

    status = status.lower()

    allowed_statuses = {
        ApplicationStatusEnum.APPLIED.value,
        ApplicationStatusEnum.SHORTLISTED.value,
        ApplicationStatusEnum.WAITLISTED.value,
        ApplicationStatusEnum.SELECTED.value,
        ApplicationStatusEnum.HIRED.value,
        ApplicationStatusEnum.REJECTED.value
    }

    if status not in allowed_statuses:
        return error_response(
            message="Invalid status",
            status_code=400
        )

    application.status = status
    
    try:

        db.session.commit()
        return success_response(message="Status updated successfully", status_code=200)
    except Exception as e:
        db.session.rollback()
        return error_response(message=str(e),status_code=500)