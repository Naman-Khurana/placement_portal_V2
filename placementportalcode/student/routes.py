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


student_bp=Blueprint("student",__name__,url_prefix="/api/student")

@student_bp.route("/dashboard",methods=[HTTPMethod.GET])
def dashboard():
    user_id=session.get("user_id")
    if not user_id:
        return error_response(message="Unauthorized",status_code=401)
    user=User.query.get(user_id)
    
    # if not user or user.role!=RoleEnum.STUDENT.value:
    #     return redirect(url_for("auth.login"))
    
    registered_companies=Company.query.filter_by(approval_status=CompanyEnumStatus.APPROVED.value)
    student_applications=Application.query.filter(Application.student_id==user.id).all()
    
    stats= {
        "applications" : len(student_applications),
        "approvedCompanies": registered_companies.count(),
        "upcomingDrives": PlacementDrive.query.filter(
            PlacementDrive.status== DriveApprovalStatusEnum.APPROVED.value,
            PlacementDrive.application_deadline >=datetime.now()
        ).count() 
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

    
    return success_response(
        message="Student Dashboard fetched successfully",
        data= {
            "student": {
                "id":user.id,
                "name":user.name,
                "department":user.department,
                "resumeUploaded": bool(user.resume_path)
            },
            "stats" : stats,
            "approvedCompanies" : approved_companies,
            "recentApplications": applications
        },status_code=200)
    

@student_bp.route('/<int:student_id>/<int:company_id>/drives',methods=[HTTPMethod.GET])
def company_drives(student_id,company_id):
    company = Company.query.get(company_id)

    if not company:
        return redirect(url_for('student.dashboard'))
    now= datetime.now()
    current_drives=PlacementDrive.query.filter(PlacementDrive.company_id==company_id,PlacementDrive.status==DriveApprovalStatusEnum.APPROVED.value, PlacementDrive.application_deadline>=now)
    rejected_applications=Application.query.filter(Application.student_id==student_id,Application.status=='rejected')
    shortlistedOrHired_applications=Application.query.filter(Application.student_id==student_id,Application.status.in_(["shortlisted", "hired"]))
    applications = Application.query.filter(Application.student_id==student_id,Application.status=='applied')
    student=User.query.get(student_id)
    rejected_application_ids={app.drive_id for app in rejected_applications}
    applied_drive_ids= {app.drive_id for app in applications}
    shortlistedOrHired_application_ids={app.drive_id for app in shortlistedOrHired_applications}
    return render_template('student/company-details.html',company=company,current_drives=current_drives,student=student,applied_drive_ids=applied_drive_ids,rejected_application_ids=rejected_application_ids,shortlistedOrHired_application_ids=shortlistedOrHired_application_ids)

@student_bp.route('/<int:student_id>/<int:drive_id>/application', methods=[HTTPMethod.POST])
def apply_drive(student_id,drive_id):
   
    student_id = request.form.get("student_id")
    drive_id = request.form.get("drive_id")
    company_id=request.form.get('company_id')

    drive = PlacementDrive.query.get_or_404(drive_id)
    student = User.query.get_or_404(student_id)
    company=Company.query.get_or_404(company_id)
    
    checkApplication=Application.query.filter(Application.student_id==student_id , Application.drive_id==drive_id).first()
    if checkApplication:
        return redirect(url_for('student.dashboard'))
    
    application=Application(
        application_date=date.today(),
        status=ApplicationStatusEnum.APPLIED.value,
        student_id=student_id,
        drive_id=drive_id
    )

    db.session.add(application)
    db.session.commit()

    if not company :
        return redirect(url_for('student.dashboard'))
    return redirect(url_for('student.company_drives', company_id=company.company_id,student_id=student_id))

@student_bp.route("/withdraw_application", methods=[HTTPMethod.POST])
def withdraw_application():

    student_id = session.get("user_id")
    drive_id = request.form.get("drive_id")

    if not student_id or not drive_id:
        return redirect(url_for("student.dashboard"))

    application = Application.query.filter(
        Application.student_id == student_id,
        Application.drive_id == drive_id
    ).first()

    if application:
        db.session.delete(application)
        db.session.commit()

    return redirect(request.referrer)    


@student_bp.route('/profile',methods=[HTTPMethod.PUT,HTTPMethod.GET])
def edit_profile():
    
    
    
    user_id = session.get("user_id")
    if not user_id:
        return error_response(message="Unauthorized" , status_code=401)
    student = User.query.get(user_id)

    if not student:
        return error_response("Student not found" , status_code=404)

    if(request.method==HTTPMethod.GET):
        return success_response(
        
        
            data={
                "name": student.name,
                "username": student.username,
                "department": student.department,
                "dob": student.dob.isoformat() if student.dob else None,
                "resumePath": student.resume_path
            },status_code=200
        )

    

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

        filepath = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)

        if student.resume_path:
            old_path = os.path.join(current_app.root_path, student.resume_path)
            if os.path.exists(old_path):
                os.remove(old_path)

        student.resume_path = f"uploads/resumes/{filename}"
        
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

