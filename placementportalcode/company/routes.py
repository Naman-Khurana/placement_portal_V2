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

company_bp=Blueprint("company",__name__,url_prefix="/api/company")

@company_bp.route("/dashboard",methods=[HTTPMethod.GET] )
def dashboard():
    user_id=session.get("user_id")
    if not user_id:
        
        return error_response( message ="user not found", status_code=404) 
    user=User.query.get(user_id)
    if not user or user.role!=RoleEnum.COMPANY  .value:
        return error_response(message="user not found", status_code=404)
    

    current_company=user.company
    if not current_company:
        return error_response(message='company not found' , status_code=404)

    now=datetime.now()


    upcoming_drives=PlacementDrive.query.filter(
        PlacementDrive.company_id==current_company.company_id,
        PlacementDrive.application_deadline >=now,
        PlacementDrive.status == DriveApprovalStatusEnum.APPROVED.value
    ).order_by(PlacementDrive.application_deadline.asc()).all()
        
    drivesList=[]
    for drive in upcoming_drives:
        
        
        application_count = Application.query.filter_by(drive_id=drive.drive_id).count()

        drivesList.append({
            "driveId": drive.drive_id,
            "title": drive.drive_name,
            "applicationDeadline": drive.application_deadline.strftime("%d %b %Y"),
            "applicationCount": application_count,

            "status": drive.status
        })
    
    closed_drives=PlacementDrive.query.filter(
        PlacementDrive.company_id==current_company.company_id,
        or_(
            PlacementDrive.application_deadline < now,
            PlacementDrive.status==DriveApprovalStatusEnum.CLOSED.value
        )).count()
        
    total_applications=Application.query.join(
        PlacementDrive, Application.drive_id == PlacementDrive.drive_id
    ).filter(
        PlacementDrive.company_id == current_company.company_id
    ).count()
    
    hired_students = Application.query.join(
        PlacementDrive,
        Application.drive_id == PlacementDrive.drive_id
    ).filter(
        PlacementDrive.company_id == current_company.company_id,
        Application.status == ApplicationStatusEnum.HIRED.value
    ).count()
        
      

    return success_response(
        message="Dashboard fetched successfully",
        data={
            "company": {
                "companyName": current_company.company_name,
                "approval_status": current_company.approval_status     
            },
            "stats":{
                "upcomingDrives" : len(upcoming_drives),
                "closedDrives": closed_drives,
                "totalApplications": total_applications,
                "hiredStudents" : hired_students
            },
            "upcomingDrives": drivesList
        }
    )
    
    
@company_bp.route("/drives",methods=[HTTPMethod.GET,HTTPMethod.POST])
def drives():
    user_id=session.get("user_id")
    if not user_id:
        
        return error_response( message ="user not found", status_code=404) 
    user=User.query.get(user_id)
    if not user or user.role!=RoleEnum.COMPANY  .value:
        return error_response(message="user not found", status_code=404)
    

    current_company=user.company
    if not current_company:
        return error_response(message='company not found' , status_code=404)
    
    if(request.method==HTTPMethod.GET):
    
        now=datetime.now()


        all_drives=PlacementDrive.query.filter(
            PlacementDrive.company_id==current_company.company_id,
        ).all()
        
        upcoming_drives=[]
        closed_drives=[]
        pending_approval_drives=[]
        rejected_drives=[]
        now =datetime.now()
            
        # drivesList=[]
        for drive in all_drives:
            drivesList=None
            
            if(drive.status== DriveApprovalStatusEnum.PENDING.value):
                drivesList=pending_approval_drives
            elif(drive.status== DriveApprovalStatusEnum.REJECT.value):
                drivesList=rejected_drives
            elif(drive.status== DriveApprovalStatusEnum.APPROVED.value and drive.application_deadline>=now):
                drivesList=upcoming_drives
            else:
                drivesList=closed_drives
            application_count = Application.query.filter_by(drive_id=drive.drive_id).count()

            drivesList.append({
                "driveId": drive.drive_id,
                "driveName": drive.drive_name,
                "applicationDeadline": drive.application_deadline.strftime("%d %b %Y"),
                "applicationCount":application_count,
                "jobTitle":drive.job_title,
                "eligibilityCriteria":drive.eligibility_criteria,
                "ctc":drive.ctc,
                "status": drive.status
            })

        

        return success_response(
            message="Company drives fetched successfully",
            data={
                "upcomingDrives":upcoming_drives,
                "pendingApprovalDrives":pending_approval_drives,
                "rejectedDrives":rejected_drives,
                "closedDrives":closed_drives
            }
        )
    
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
    

@company_bp.route("/update-applicant-status", methods=[HTTPMethod.POST])
def update_applicant_status():

    application_id = request.form.get("application_id")
    status = request.form.get("status")

    application = Application.query.get_or_404(application_id)

    application.status = status

    db.session.commit()

    return redirect(request.referrer)


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
            return success_response(message="drive updated successfully", status_code=200)
        except Exception as e:
            db.session.rollback()
            return error_response(message=str(e),status_code=500)

    
@company_bp.route("/profile", methods=[HTTPMethod.GET,HTTPMethod.PUT])
def edit_profile():

    user_id=session.get("user_id")
    if not user_id:
        
        return error_response( message ="user not found", status_code=404) 
    user=User.query.get(user_id)
    if not user or user.role!=RoleEnum.COMPANY  .value:
        return error_response(message="user not found", status_code=404)
    

    company=user.company
    if not company:
        return error_response(message='company not found' , status_code=404)
    
    if request.method==HTTPMethod.GET:
        return success_response(
            message="company profile fetched successfully",
            data={
                "companyId":company.company_id,
                "companyName" : company.company_name,
                "companyWebsite":company.company_website,
                "hrContact":company.hr_contact,
                "approvalStatus":company.approval_status   
            },status_code=200
        )
    
    
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