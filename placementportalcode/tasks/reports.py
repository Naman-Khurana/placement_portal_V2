from flask import render_template
from placementportalcode.celery_utils import celery
from placementportalcode.models import *
from placementportalcode.utils.email import send_email
from datetime import datetime,timedelta
from placementportalcode.constants import ADMIN_EMAIL


@celery.task(name="monthly_report")
def monthly_report():
    
    one_month_before = datetime.now() - timedelta(days=30)
    
    total_companies= Company.query.count()
    
    total_students= User.query.filter_by(role= RoleEnum.STUDENT.value).count()
    
    total_drives=PlacementDrive.query.filter(
        PlacementDrive.application_deadline >=one_month_before
    ).count()
    
    total_applications= Application.query.filter(
        Application.application_date>=one_month_before.date()
    ).count()
    
    selected_students=Application.query.filter(
        Application.application_date>=one_month_before.date(),
        Application.status==ApplicationStatusEnum.SELECTED.value
    ).count()
    
    hired_students= Application.query.filter(
        Application.application_date>=one_month_before.date(),
        Application.status==ApplicationStatusEnum.HIRED.value
    ).count()
    
    html=render_template("emails/monthly_report.html",companies=total_companies,students=total_students,drives=total_drives,applications= total_applications,selected=selected_students,hired= hired_students)
    
    try:
        send_email(
            subject="Monthly Placement Activity Report",
            recipients=[ADMIN_EMAIL],
            body="""
            Dear Organization
            
            Please find your organization's monthly placement activity report below.
            Details Highlight the placement activity of your organization over the last 30 days.
            
            NOTE: AUTO GENERATED MONTHLY-REPORT 
            """,
            html=html
        )
        print("REPORT EMAIL SEND SUCCESSFULLY")
    except Exception as e:
        print(e)
    
    