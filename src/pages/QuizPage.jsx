import React, { useState, useEffect, useCallback } from "react";
import { useParams, Link } from "react-router-dom";
import HeaderBar from "../shared/HeaderBar";
import QuizRunner from "../features/quiz/QuizRunner";
import StateView from "../shared/StateView";
import { fetchQuizByTopic } from "../api/quiz";
import { fetchTopicById } from "../api/topics";

export default function QuizPage() {
  const { id } = useParams();
  const [topic, setTopic] = useState(null);
  const [quizData, setQuizData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const loadData = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const [tData, qData] = await Promise.all([
        fetchTopicById(id),
        fetchQuizByTopic(id),
      ]);
      setTopic(tData);
      setQuizData(qData);
    } catch (err) {
      setError(err);
    } finally {
      setLoading(false);
    }
  }, [id]);

  useEffect(() => {
    loadData();
  }, [loadData]);

  return (
    <div style={{ minHeight: "100vh", display: "flex", flexDirection: "column" }}>
      <HeaderBar
        backTo={`/topics/${id}`}
        backLabel="Back to Specimen"
        title={topic ? `${topic.name} Quiz` : "Assessment"}
      />

      <main style={{ maxWidth: "1360px", margin: "0 auto", padding: "var(--space-6)", width: "100%", flex: 1 }}>
        <StateView
          loading={loading}
          error={error}
          onRetry={loadData}
          emptyMessage="No quiz found for this specimen."
          emptyAction={<Link to={`/topics/${id}`} style={{ color: "var(--amber)" }}>Return to Topic</Link>}
        >
          {quizData && (
            <QuizRunner
              topicId={id}
              topicName={topic?.name || id}
              initialQuestions={quizData.questions}
            />
          )}
        </StateView>
      </main>
    </div>
  );
}
