import axios from "axios";

// Generate or retrieve persistent anonymous session UUID
export function getOrCreateSessionId() {
    let sid = localStorage.getItem("prismed_session_id");
    if (!sid) {
        // Simple client-side UUID v4 generator
        sid = "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g, (c) => {
            const r = (Math.random() * 16) | 0;
            const v = c === "x" ? r : (r & 0x3) | 0x8;
            return v.toString(16);
        });
        localStorage.setItem("prismed_session_id", sid);
    }
    return sid;
}

const BASE_URL = import.meta.env.VITE_API_URL || "";

const apiClient = axios.create({
    baseURL: BASE_URL,
});

apiClient.interceptors.request.use((config) => {
    config.headers["X-Session-Id"] = getOrCreateSessionId();
    return config;
});

export default apiClient;
