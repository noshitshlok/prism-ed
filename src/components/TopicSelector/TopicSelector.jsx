import { useEffect, useState } from "react";
import { fetchTopics } from "../../api/topics";
import "./TopicSelector.css";

export default function TopicSelector({ onSelectTopic }) {
    const [topics, setTopics] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        fetchTopics()
            .then(setTopics)
            .catch(() => setError("Could not load topics. Is the backend running?"))
            .finally(() => setLoading(false));
    }, []);

    if (loading) return <p className="status-text">Loading topics...</p>;
    if (error) return <p className="status-text error">{error}</p>;

    return (
        <div className="topic-selector">
            <h1>Choose a Topic</h1>
            <div className="topic-grid">
                {topics.map((topic) => (
                    <button
                        key={topic.id}
                        className="topic-card"
                        onClick={() => onSelectTopic(topic.id)}
                    >
                        <h2>{topic.name}</h2>
                        <p>{topic.description}</p>
                    </button>
                ))}
            </div>
        </div>
    );
}