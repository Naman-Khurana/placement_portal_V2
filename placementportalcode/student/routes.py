from flask import Blueprint,Flask,session,url_for,redirect,render_template,request
from http import HTTPMethod
from placementportalcode.models import User,Company,PlacementDrive,Application
from placementportalcode.enums.modelsenum import ApplicationEnum 
from placementportalcode.enums.role import RoleEnum
from placementportalcode.enums.approval_status import CompanyEnumStatus,DriveApprovalStatusEnum
from placementportalcode.enums.application_status import ApplicationStatusEnum
from datetime import datetime ,date
from placementportalcode.extensions import db
import os
from flask import current_app
from werkzeug.utils import secure_filename
from placementportalcode.utils.responses import success_response,error_response
from placementportalcode.tasks.export import export_student_applications
from placementportalcode.student.student_service import *
from placementportalcode.admin.admin_service import *
from placementportalcode.company.company_service import *


student_bp=Blueprint("student",__name__,url_prefix="/api/student")

@student_bp.route("/dashboard",methods=[HTTPMethod.GET])
def dashboard():
    
    user_id=session.get("user_id")
    # if not user or user.role!=RoleEnum.STUDENT.value:
    #     return redirect(url_for("auth.login"))
    
    # dashboard_data=get_student_dashboard_data(user_id=)
    
    return success_response(
        message="Student Dashboard fetched successfully",
        data=get_student_dashboard_data(user_id=user_id),
        status_code=200)
    
    

# @student_bp.route('/<int:student_id>/<int:company_id>/drives',methods=[HTTPMethod.GET])
# def company_drives(student_id,company_id):
#     company = Company.query.get(company_id)

#     if not company:
#         return redirect(url_for('student.dashboard'))
#     now= datetime.now()
#     current_drives=PlacementDrive.query.filter(PlacementDrive.company_id==company_id,PlacementDrive.status==DriveApprovalStatusEnum.APPROVED.value, PlacementDrive.application_deadline>=now)
#     rejected_applications=Application.query.filter(Application.student_id==student_id,Application.status=='rejected')
#     shortlistedOrHired_applications=Application.query.filter(Application.student_id==student_id,Application.status.in_(["shortlisted", "hired"]))
#     applications = Application.query.filter(Application.student_id==student_id,Application.status=='applied')
#     student=User.query.get(student_id)
#     rejected_application_ids={app.drive_id for app in rejected_applications}
#     applied_drive_ids= {app.drive_id for app in applications}
#     shortlistedOrHired_application_ids={app.drive_id for app in shortlistedOrHired_applications}
#     return render_template('student/company-details.html',company=company,current_drives=current_drives,student=student,applied_drive_ids=applied_drive_ids,rejected_application_ids=rejected_application_ids,shortlistedOrHired_application_ids=shortlistedOrHired_application_ids)

@student_bp.route('/drives/<int:drive_id>/applications', methods=[HTTPMethod.POST])
def apply_drive(drive_id):
    
    user_id=session.get("user_id")
    
    
    
    if not user_id:
        return error_response( message="Unauthorized",status_code=401)
   
   
    student = User.query.get(user_id)
    
    if not student or student.role != RoleEnum.STUDENT.value:
        return error_response(message="Unauthorized",status_code=401)
    
    if not student.eligible:
        return error_response(message="not eligible to participate in drive",status_code=403)
    
    drive= PlacementDrive.query.get(drive_id)
    if not drive:
        return error_response(message="Placement Drive Not Found ",status_code=404)
  
    if drive.status != DriveApprovalStatusEnum.APPROVED.value:
        return error_response(
            message="This drive is not accepting applications.",
            status_code=400
        )
        
    if drive.application_deadline < datetime.now():
        return error_response(
            message="Application deadline has passed.",
            status_code=400
        )
    
    drive = PlacementDrive.query.get(drive_id)
    if not drive:
        return error_response(message="Placement Drive not found",status_code=404)
    
    
    existingApplication=Application.query.filter(Application.student_id==user_id , Application.drive_id==drive_id).first()
    if existingApplication:
        return error_response(message="Already Applied" ,status_code=409)
    try:
        application=Application(
            application_date=date.today(),
            status=ApplicationStatusEnum.APPLIED.value,
            student_id=user_id,
            drive_id=drive_id
        )

        db.session.add(application)
        db.session.commit()
        cache.delete_memoized(get_admin_applications)
        cache.delete_memoized(get_admin_dashboard_data)
        invalidate_company_dashboard_and_drives_cache(user_id=drive.company.user.id)
        return success_response(message="Applied Successfully", status_code=201)

    
    except Exception as e:
        db.session.rollback()
        return error_response(message=str(e) , status_code=500) 
@student_bp.route("/drives/<drive_id>/applications", methods=[HTTPMethod.DELETE])
def withdraw_application(drive_id):

    user_id=session.get("user_id")
    
    if not user_id:
        return error_response( message="Unauthorized",status_code=401)
   
    student = User.query.get(user_id)
    
    if not student:
        return error_response(message="Student not found",status_code=404)

    # drive = PlacementDrive.query.get(drive_id)
    
    # if not drive:
    #     return error_response(message="Placement Drive not found",status_code=404)
    
    
    application = Application.query.filter(
        Application.student_id == user_id,
        Application.drive_id == drive_id
    ).first()
    if not application:
        return error_response(message="Application not found", status_code=404 )
    
    try:
        db.session.delete(application)
        db.session.commit()
        
        return success_response(message="Application withdrawn successfully",status_code=200)
    except Exception as e:
        db.session.rollback()
        return error_response(message=str(e),status_code=500 )

@student_bp.route("/applications", methods=[HTTPMethod.GET] )
def my_applications():
    user_id=session.get("user_id")
    
    if not user_id:
        return error_response( message="Unauthorized",status_code=401)
   
    student = User.query.get(user_id)
    
    if not student:
        return error_response(message="Student not found",status_code=404)
    
    applications = Application.query.filter_by(
        student_id= user_id
    ).all()
    
    stats={
        ApplicationStatusEnum.APPLIED.value: 0,
        ApplicationStatusEnum.SHORTLISTED.value: 0,
        ApplicationStatusEnum.SELECTED.value: 0,
        ApplicationStatusEnum.REJECTED.value: 0,
        ApplicationStatusEnum.WAITLISTED.value: 0,
        ApplicationStatusEnum.HIRED.value: 0,
    }
    application_list=[]
    
    for application in applications:
        if application.status:
            stats[application.status]+=1


        application_list.append({
            "applicationId": application.application_id,
            "status": application.status,
            "applicationDate": application.application_date.isoformat(),
            "driveId": application.drive.drive_id,
            "driveName": application.drive.drive_name,
            "companyId": application.drive.company.company_id,
            "companyName": application.drive.company.company_name,
            "deadline": application.drive.application_deadline.isoformat(),
        })
        
    return success_response(
        message="Applications fetched successfully",
        data= {
            "stats" : stats,
            "applications":application_list
        },
        status_code=200
    )       


@student_bp.route('/profile',methods=[HTTPMethod.PUT,HTTPMethod.GET])
def edit_profile():
    
    
    
    user_id = session.get("user_id")
    if not user_id:
        return error_response(message="Unauthorized" , status_code=401)
    
    if(request.method==HTTPMethod.GET):
        return success_response(
            data=get_student_profile(user_id=user_id),status_code=200
        )

    
    student = User.query.get(user_id)

    if not student:
        return error_response("Student not found" , status_code=404)

    
    

    data = request.get_json()
    
    if not data:
        return error_response(
            message="Invalid request body",
            status_code=400
        )

    name = data.get("name")
    if not name or not name.strip():
        return error_response("Name cannot be emppty", status_code=400)
    student.name =name.strip()
    
    
    try: 
    
        department = data.get("department")

        if department :
            student.department= department.strip()
        
        dob = data.get("dob")
        if dob:
            student.dob = datetime.strptime(dob, "%Y-%m-%d").date()

        db.session.commit()
        cache.delete_memoized(get_student_profile,user_id)
        return success_response(
            message="Profile Updated Successfully",
            data={
                "name": student.name,
                "username": student.username,
                "department": student.department,
                "dob": student.dob.isoformat() if student.dob else None
            },
            status_code=200
        )
    except Exception as e:
        db.session.rollback()
        return error_response(
            message="Something went wrong.",
            status_code=500
        )

@student_bp.route('/profile/resume',methods=[HTTPMethod.POST])
def update_resume():
    
    user_id = session.get("user_id")
    if not user_id:
        return error_response(message="Unauthorized" , status_code=401)
    student = User.query.get(user_id)

    if not student:
        return error_response("Student not found" , status_code=404)
    
    
    file = request.files.get("resume")
    if not file or file.filename == "":
        return error_response(
            message="Resume file is required",
            status_code=400
        )

    try:
        
        
        filename = secure_filename(file.filename)

        filepath = os.path.join(
            current_app.root_path,
            "static",
            "uploads",
            "resumes",
            filename
        )

        file.save(filepath)

        if student.resume_path:
            old_path = os.path.join(current_app.root_path, student.resume_path)
            if os.path.exists(old_path):
                os.remove(old_path)

        student.resume_path = f"static/uploads/resumes/{filename}"

        db.session.commit()
        return success_response(
            message="Resume uploaded successfully",
            data={
                "resumePath": student.resume_path
            },
            status_code=201
        )
    except Exception:
        db.session.rollback()
        return error_response(
            message="Failed to upload resume",
            status_code=500
        )

@student_bp.route("/export",methods=[HTTPMethod.POST])
def export():
    user_id=session.get("user_id")
    if not user_id:
        return error_response(message="Unauthorized", status_code=403)
    
    export_student_applications.delay(user_id)
    
    return success_response(
        message="Your Export has started. You will receive it by email shortly.",
        status_code=202
    )
    
    
    
    
@student_bp.route("/companies/<int:company_id>/drives",methods=[HTTPMethod.GET])
def get_company_active_drives(company_id):
    user_id=session.get("user_id")
    if not user_id:
        return error_response( message ="Unauthorized", status_code=401) 
    
    user=User.query.get(user_id)
    if not user or user.role!=RoleEnum.STUDENT.value:
        return error_response(message="Unauthorized", status_code=401)
    
    current_company=Company.query.get(company_id)
    if not current_company:
        return error_response(message='Company Not Found' , status_code=404)
        
    
    now=datetime.now()
    
    applied_drive_ids = {
        application.drive_id
        for application in Application.query.filter_by(student_id=user_id).all()
    }
    
    drives=PlacementDrive.query.filter(
            PlacementDrive.company_id==current_company.company_id,
            PlacementDrive.status == DriveApprovalStatusEnum.APPROVED.value,
            PlacementDrive.application_deadline >= now
            
        ).all()
        
    now =datetime.now()
        
    drivesList=[]
    for drive in drives:
        
        if drive.drive_id in applied_drive_ids:
            continue
        
        drivesList.append({
            "driveId": drive.drive_id,
            "driveName": drive.drive_name,
            "applicationDeadline": drive.application_deadline.strftime("%d %b %Y"),
            "jobTitle":drive.job_title,
            "eligibilityCriteria":drive.eligibility_criteria,
            "ctc":drive.ctc,
            
        })
    
    return success_response(
        message="Company drives fetched successfully",
        data={
        "drives":drivesList,
        "company":{
            "companyName":current_company.company_name,
            "company_id":current_company.company_id
        }
        },status_code=200
    )


