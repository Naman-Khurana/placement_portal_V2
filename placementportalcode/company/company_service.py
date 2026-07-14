from placementportalcode.models import *
from sqlalchemy import or_
from placementportalcode.utils.responses import success_response,error_response
from placementportalcode.extensions import cache

@cache.memoize(timeout=300)
def get_company_dashboard_data(user_id):
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
    
    return {
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
        
   
@cache.memoize(timeout=300)   
def get_company_drives(user_id):
    user=User.query.get(user_id)
    if not user or user.role!=RoleEnum.COMPANY  .value:
        return error_response(message="user not found", status_code=404)
    

    current_company=user.company
    if not current_company:
        return error_response(message='company not found' , status_code=404)
    
    
    
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
            "applicationDeadlineRaw":drive.application_deadline.strftime("%Y-%m-%dT%H:%M"),
            "applicationCount":application_count,
            "jobTitle":drive.job_title,
            "eligibilityCriteria":drive.eligibility_criteria,
            "ctc":drive.ctc,
            "status": drive.status,
            "jobDescription" : drive.job_desc
        })

    

    return {
            "upcomingDrives":upcoming_drives,
            "pendingApprovalDrives":pending_approval_drives,
            "rejectedDrives":rejected_drives,
            "closedDrives":closed_drives,
            "company":{
                "approvalStatus":current_company.approval_status
            }
        }
    
@cache.memoize(timeout=300)
def get_company_profile(user_id):
    user=User.query.get(user_id)
    if not user or user.role!=RoleEnum.COMPANY  .value:
        return error_response(message="user not found", status_code=404)
    

    company=user.company
    if not company:
        return error_response(message='company not found' , status_code=404)

    return {
                "companyId":company.company_id,
                "companyName" : company.company_name,
                "companyWebsite":company.company_website,
                "hrContact":company.hr_contact,
                "approvalStatus":company.approval_status   
            }
    
    

def invalidate_company_dashboard_and_drives_cache(user_id):
    cache.delete_memoized(get_company_dashboard_data,user_id)
    cache.delete_memoized(get_company_drives,user_id)