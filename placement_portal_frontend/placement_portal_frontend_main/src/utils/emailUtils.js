export function validateEmail(username) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (!emailRegex.test(username.trim())) {
        return false;
    }

    return true;
}