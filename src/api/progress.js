import apiClient from "./client";

export async function recordQuizAttempt(topicId, score, total) {
    const res = await apiClient.post("/api/v1/progress/attempts", {
        topicId,
        score,
        total,
    });
    return res.data;
}

export async function fetchProgressSummary() {
    const res = await apiClient.get("/api/v1/progress/summary");
    return res.data;
}
