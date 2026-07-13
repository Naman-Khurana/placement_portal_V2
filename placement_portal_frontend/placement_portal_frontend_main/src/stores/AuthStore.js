import { defineStore } from "pinia";
import { getCurrentUser, logout } from "../services/authService";

export const useAuthStore = defineStore("auth", {
    state: () => ({
        currentUser: null,
        isAuthenticated: false,
        isInitializing: false
    }),

    actions: {
        setAuthenticatedUser(user) {
            this.currentUser = user,
                this.isAuthenticated = true
        },

        clearAuthentication() {
            this.currentUser = null,
            this.isAuthenticated = false
        },
        async initAuth() {
            this.isInitializing = true;
            try {
                const response = await getCurrentUser();
                this.setAuthenticatedUser(response.data.data);

            } catch (error) {
                this.clearAuthentication()
            }
            finally {
                this.isInitializing = false;
            }
        },
        async logout(){
            try{
                await logout();
            }catch(error){
                console.log(error);
                
            }finally{
                this.clearAuthentication()
            }
        }

    },

    getters: {
        userRole: (state) => state.currentUser?.role ?? null
    }
});

