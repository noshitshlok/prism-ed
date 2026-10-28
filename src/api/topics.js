import apiClient from "./client";

export async function fetchTopics(filters = {}) {
    const params = new URLSearchParams();
    if (filters.discipline) params.append("discipline", filters.discipline);
    if (filters.tag) params.append("tag", filters.tag);
    if (filters.level) params.append("level", filters.level);
    if (filters.status) params.append("status", filters.status);
    if (filters.include_all) params.append("include_all", "true");

    const query = params.toString() ? `?${params.toString()}` : "";
    const res = await apiClient.get(`/api/v1/topics${query}`);
    return res.data;
}

export async function fetchTopicById(topicId) {
    const res = await apiClient.get(`/api/v1/topics/${topicId}`);
    return res.data;
}