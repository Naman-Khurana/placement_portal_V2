from placementportalcode.celery_utils import celery
from datetime import datetime, timedelta
from placementportalcode.models import User,Application,PlacementDrive
from placementportalcode.utils.email import send_email
from placementportalcode.enums.approval_status import DriveApprovalStatusEnum
from placementportalcode.enums.role import RoleEnum

@celery.task(name="daily_reminder")
def daily_reminder():
    
    print("=" * 50)
    print("RUNNING DAILY REMINDER")
    print("=" * 50)

    now = datetime.now()
    tomorrow=now + timedelta(days=1)
    
    last_day_left_drives=PlacementDrive.query.filter(
        PlacementDrive.status== DriveApprovalStatusEnum.APPROVED.value,
        PlacementDrive.application_deadline >=now,
        PlacementDrive.application_deadline <=tomorrow
    ).all()
    
    print(f"{len(last_day_left_drives)} drives found.")

    
    
    eligible_students=User.query.filter_by(
        role=RoleEnum.STUDENT.value, eligible=True
    ).all()


    for drive in last_day_left_drives:
        
        
        
        
        applied_student_ids={
            application.student_id
            for application in Application.query.filter_by(
                drive_id=drive.drive_id
            ).all()
        }
        
        for student in eligible_students:
            if student.id in applied_student_ids:
                continue
            
            body = f"""
                Hello {student.name},

                This is a reminder that the placement drive below closes within 24 hours.

                Company :
                {drive.company.company_name}

                Drive :
                {drive.drive_name}

                Role :
                {drive.job_title}

                Deadline :
                {drive.application_deadline.strftime("%d %b %Y %I:%M %p")}

                Please apply before the deadline.

                Regards,
                Placement Portal
            """
            
            try:
                send_email(
                    subject="Placement Drive Reminder",
                    recipients=[student.username],
                    body=body
                )
                print("email sent successfully ")
            except Exception as e:
                print(e)