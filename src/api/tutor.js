import apiClient, { getOrCreateSessionId } from "./client";

export async function askTutor(topicId, partId, question, history = []) {
    const res = await apiClient.post("/api/v1/tutor/ask", {
        topicId,
        partId,
        question,
        history,
    });
    return res.data.answer;
}

export async function streamTutor(topicId, partId, question, history = [], onChunk, onDone, onError) {
    const baseUrl = import.meta.env.VITE_API_URL || "";
    try {
        const response = await fetch(`${baseUrl}/api/v1/tutor/stream`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-Session-Id": getOrCreateSessionId(),
            },
            body: JSON.stringify({
                topicId,
                partId,
                question,
                history,
            }),
        });

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }

        const reader = response.body.getReader();
        const decoder = new TextDecoder("utf-8");
        let buffer = "";

        while (true) {
            const { done, value } = await reader.read();
            if (done) break;

            buffer += decoder.decode(value, { stream: true });
            const lines = buffer.split("\n\n");
            buffer = lines.pop(); // retain incomplete block

            for (const line of lines) {
                if (line.includes("data: ")) {
                    const dataStr = line.replace(/.*data: /, "").trim();
                    if (!dataStr) continue;
                    try {
                        const parsed = JSON.parse(dataStr);
                        if (parsed.token) onChunk(parsed.token);
                        if (parsed.done && onDone) onDone();
                        if (parsed.error && onError) onError(parsed.error);
                    } catch {
                        // ignore malformed chunks
                    }
                }
            }
        }
        if (onDone) onDone();
    } catch (err) {
        if (onError) onError(err.message);
    }
}