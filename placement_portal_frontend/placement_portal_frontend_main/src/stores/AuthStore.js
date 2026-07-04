import { defineStore } from "pinia";

export const useAuthStore = defineStore("auth", {
    state: () => ({
        currentUser: null,
        isAuthenticated: false
    }),

    actions: {
        login(user) {
            this.currentUser = user,
                this.isAuthenticated = true
        },

        logout() {
            this.currentUser = null,
                this.isAuthenticated = false
        }
    },

    getters: {
        userRole: (state) => state.currentUser?.role ?? null
    }
}); 