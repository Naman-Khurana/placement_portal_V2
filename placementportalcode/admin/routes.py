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
from placementportalcode.admin.admin_service import *
from placementportalcode.student.student_service import * 
from placementportalcode.company.company_service import *


admin_bp=Blueprint("admin",__name__,url_prefix="/api/admin")

@admin_bp.route("/dashboard",methods=[HTTPMethod.GET] )
def dashboard():
    if not checkAdmin():
        return error_response(message="Unauthorized",status_code=403)
   
    
   
    return success_response(
        message="admin dashboard fetched successfully",
        data=get_admin_dashboard_data(),
        status_code=200
        )
    

    
@admin_bp.route("/companies",methods= [HTTPMethod.GET])
def get_companies():
    
    if not checkAdmin():
        return error_response(message="Unauthorized",status_code=403)
   
    search = request.args.get("search")
    
    return success_response(
        message="all companies data fetched",
        data =get_admin_companies(search=search),
        status_code=200
    )


    
@admin_bp.route("/drives",methods= [HTTPMethod.GET])
def get_drives():
    
    if not checkAdmin():
        return error_response(message="Unauthorized",status_code=403)
   
    search=request.args.get("search")
        
    return success_response(
        message="all drives data fetched",
        data =get_admin_drives(search=search),
        status_code=200
    )

@admin_bp.route("/students",methods= [HTTPMethod.GET])
def get_students():
    
    if not checkAdmin():
        return error_response(message="Unauthorized",status_code=403)
   
    search=request.args.get("search")
        
    return success_response(
        message="all students data fetched",
        data =get_admin_students(search=search),
        status_code=200
    )



@admin_bp.route("/applications",methods= [HTTPMethod.GET])
def get_applications():
    
    if not checkAdmin():
        return error_response(message="Unauthorized",status_code=403)
   
    search = request.args.get("search")
        
    return success_response(
        message="all applications data fetched",
        data =get_admin_applications(search=search),
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
        cache.delete_memoized(get_admin_companies)
        cache.delete_memoized(get_admin_dashboard_data)
        invalidate_company_dashboard_and_drives_cache(company.user.id)
        cache.delete_memoized(get_company_profile, company.user.id)
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
        cache.delete_memoized(get_admin_drives)
        cache.delete_memoized(get_admin_dashboard_data)
        # cache.delete_memoized(get_student_dashboard_data)
        invalidate_company_dashboard_and_drives_cache(drive.company.user.id)
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
        cache.delete_memoized(get_admin_students)
        # cache.delete_memoized(get_student_dashboard_data,student.id)
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
    
    action=action.lower()
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
        cache.delete_memoized(get_admin_applications)
        # cache.delete_memoized(get_student_dashboard_data,application.student.id)
        invalidate_company_dashboard_and_drives_cache(application.drive.company.user.id)
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
    
    
