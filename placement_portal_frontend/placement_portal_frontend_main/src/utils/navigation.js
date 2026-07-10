import { ROLES } from "../enums/Roles";
import { ADMIN_ROUTE_PREFIX } from "./routeConstants";
import { STUDENT_DASHBOARD_ROUTE } from "./routeConstants";
import { LOGIN_ROUTE } from "./routeConstants";
import { COMPANY_DASHBOARD_ROUTE } from "./routeConstants";

export function getDashboardRoute(role){
    switch(role){
        case ROLES.ADMIN:
            return ADMIN_ROUTE_PREFIX;
        case ROLES.COMPANY:
            return COMPANY_DASHBOARD_ROUTE;
        case ROLES.STUDENT:
            return STUDENT_DASHBOARD_ROUTE
        default:
            return LOGIN_ROUTE
    }
}