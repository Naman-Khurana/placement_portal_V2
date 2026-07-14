import csv
import os
from placementportalcode.celery_utils import celery
from placementportalcode.models import User,Application
from datetime import datetime
from flask_mail import Message
from placementportalcode.extensions import mail
from placementportalcode.utils.email import send_email
@celery.task(name="export_student_applications")
def export_student_applications(student_id):
    
    student=User.query.get(student_id)
    if not student:
        return
    
    applications=Application.query.filter_by(student_id=student_id).all()    
    
    export_folder = os.path.join(
        os.getcwd(),
        "placementportalcode",
        "static",
        "exports"
    )
    
    os.makedirs(export_folder, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    file_path = os.path.join(
        export_folder,
        f"student_{student_id}_{timestamp}.csv"
    )

    
    with open(file_path, "w", newline="", encoding="utf-8") as csv_file:

        writer = csv.writer(csv_file)

        writer.writerow([
            "Student ID",
            "Company",
            "Drive",
            "Job Title",
            "Application Status",
            "Application Date"
        ])
        
        
        for application in applications:

            writer.writerow([
                student.id,
                application.drive.company.company_name,
                application.drive.drive_name,
                application.drive.job_title,
                application.status,
                application.application_date.strftime("%d-%m-%Y")
            ])
            
    body = """
    Dear Student,

    Your placement application history has been exported successfully.

    The CSV file is attached.

    Regards,
    Placement Portal
        """        
            
    

    try:
        send_email(subject="Placement Application Export",recipients=[student.username],body=body,attachment_path=file_path)
        print("Email sent successfully.")
        
        os.remove(file_path)
        print("CSV deleted.")
    except Exception as e:
        print(e)

    
