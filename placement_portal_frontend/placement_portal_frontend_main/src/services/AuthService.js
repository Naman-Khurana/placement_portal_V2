import api from "../api/axios"

export async function login(credentials) {
    return await api.post("/api/auth/login",credentials);
}
