import apiClient from "./client";

export async function fetchQuizByTopic(topicId) {
    const res = await apiClient.get(`/api/v1/quiz/${topicId}`);
    return res.data;
}

export async function submitQuizAnswers(topicId, answers) {
    const res = await apiClient.post("/api/v1/quiz/submit", {
        topicId,
        answers,
    });
    return res.data;
}

export async function generateAiQuiz(topicId) {
    const res = await apiClient.post("/api/v1/quiz/generate", {
        topicId,
    });
    return res.data;
}