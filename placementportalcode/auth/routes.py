from flask import Blueprint,request,session, render_template, request, redirect, url_for, session, flash
from placementportalcode.models import User,Company
from http import HTTPMethod
from placementportalcode.enums.approval_status import CompanyEnumStatus
from placementportalcode.enums.modelsenum import UserEnum ,CompanyEnum
from placementportalcode.enums.role import RoleEnum
from placementportalcode.extensions import db
from placementportalcode.utils.responses import success_response,error_response
from placementportalcode.utils.db import save,commit_session
from flask import jsonify


auth_bp=Blueprint("auth",__name__,url_prefix="/api/auth")

@auth_bp.route("/login", methods=['GET','POST'])
def login():
    # if(request.method=='GET'):
    #     return render_template("auth/login.html")
    
    # POST LOGIC
    data=request.get_json()    

    username=data.get(UserEnum.USERNAME.value)
    password=data.get(UserEnum.PASSWORD.value)

    

    if not username or not password:
        return error_response("Missing Credentials",None,400)
    
        
    user=User.query.filter_by(username=username).first()

    if not user or not user.check_password(password):
        # flash("Invalid password")
        return error_response("Invalid Username or  Password",None,401)
    

    session["user_id"]=user.id
    print(user.role)
   
    return success_response("Login Successfull",
        {
            "id": user.id,
            "username": username,
            "role": user.role
        }
    ,200)

@auth_bp.route("/logout" , methods=[HTTPMethod.GET,HTTPMethod.POST])
def logout():
    session.pop("user_id",None)
    return success_response("Logged out successfully",None,200);

@auth_bp.route("/register-company" ,methods=['GET','POST'])
def register_company():
   
    data=request.get_json()
    hr_contact=data.get(CompanyEnum.HR_CONTACT.value)
    company_name = data.get(CompanyEnum.COMPANY_NAME.value)
    password = data.get(UserEnum.PASSWORD.value)
    website = data.get(CompanyEnum.COMPANY_WEBSITE.value)
    existing_user = User.query.filter_by(username=hr_contact).first()

    if existing_user: 
        return error_response("Email already registered",None,409)
    

    try:
        print("check 1")
        user=User(
            username=hr_contact,
            name=company_name,
            role=RoleEnum.COMPANY.value        
        )
        user.set_password(password)
        
        print(user.username , user.name)
        
        db.session.add(user)
        db.session.flush() 

        
        print("check 2")
        company = Company(
                    company_name=company_name,
                    hr_contact=hr_contact,
                    company_website=website,
                    approval_status=CompanyEnumStatus.PENDING.value,
                    user_id=user.id

                )

        db.session.add(company)
        db.session.commit()
        print("check 3")
        return success_response("Organization Registerd Successfully",
                                  {
                                        "id": user.id,
                                        "email":hr_contact ,
                                        "company_name": company_name,
                                        "company_website": website, 
                                        "role": user.role,
                                        "approval_status":CompanyEnumStatus.PENDING.value
                                    }
                                ,201);
    except Exception as e:
        db.session.rollback()
        print(e)
        return error_response("Something Went wrong.",None,400)
        

@auth_bp.route("/register", methods=[HTTPMethod.GET,HTTPMethod.POST])
def signup():
    data=request.get_json()


    username=data.get(UserEnum.USERNAME.value)
    password=data.get(UserEnum.PASSWORD.value)
    name=data.get(UserEnum.NAME.value)

    
    #missing fields check
    if not username or not password or not name:
        return error_response("Missing Credentials",None,400)
        
    #duplicate username check
    if User.query.filter_by(username=username).first():
        return error_response("Username already exists",None,409)
       
    user=User(
        username=username,
        name=name,
        role=RoleEnum.STUDENT.value
    )

    user.set_password(password)
    #save and commit the user to db
    save(user)
    commit_session()

    return success_response("Student Registerd Successfully", 
        {
            "id": user.id,
            "username": username,
            "role": user.role
        } ,201);
    
    
@auth_bp.get("/test")
def test():

    if "user_id" not in session:
        return error_response("Not Authenticated",None, 401); 
    

    return success_response("Authenticated",
        {
            "user_id": session["user_id"]
        }
        ,200) 
