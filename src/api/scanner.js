import apiClient from "./client";

export async function fetchSupportedMarkers() {
    const res = await apiClient.get("/api/v1/scanner/markers");
    return res.data;
}

export async function matchTextbookPhoto(file) {
    const formData = new FormData();
    formData.append("file", file);
    const res = await apiClient.post("/api/v1/scanner/match", formData, {
        headers: {
            "Content-Type": "multipart/form-data",
        },
    });
    return res.data;
}
