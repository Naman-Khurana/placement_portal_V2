import { ROLES } from "../enums/Roles";

export function getDashboardRoute(role){
    switch(role){
        case ROLES.ADMIN:
            return "/admin";
        case ROLES.COMPANY:
            return "/company";
        case ROLES.STUDENT:
            return "/student"
        default:
            return "/login"
    }
}