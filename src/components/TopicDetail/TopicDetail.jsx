import { useEffect, useState } from "react";
import { fetchTopicById } from "../../api/topics";
import ModelViewer from "../ModelViewer/ModelViewer";
import ConceptPanel from "../ConceptPanel/ConceptPanel.jsx";
import "./TopicDetail.css";

export default function TopicDetail({ topicId, onStartQuiz }) {
    const [topic, setTopic] = useState(null);
    const [selectedPartId, setSelectedPartId] = useState(null);

    useEffect(() => {
        fetchTopicById(topicId).then(setTopic);
    }, [topicId]);

    if (!topic) return <p className="status-text">Loading model...</p>;

    const selectedPart = topic.parts.find((p) => p.id === selectedPartId) || null;

    return (
        <div className="topic-detail">
            <h1>{topic.name}</h1>
            <div className="topic-detail-layout">
                <ModelViewer
                    modelUrl={topic.modelUrl}
                    parts={topic.parts}
                    selectedPartId={selectedPartId}
                    onPartSelect={setSelectedPartId}
                />
                <ConceptPanel part={selectedPart} topicId={topicId} />
            </div>
            <button className="primary-btn" onClick={() => onStartQuiz(topicId)}>
                Take Quiz
            </button>
        </div>
    );
}