import { useEffect, useState } from "react";
import { fetchQuizByTopic } from "../../api/quiz";
import "./Quiz.css";

export default function Quiz({ topicId, onExit }) {
    const [quiz, setQuiz] = useState(null);
    const [currentIndex, setCurrentIndex] = useState(0);
    const [answers, setAnswers] = useState([]);
    const [submitted, setSubmitted] = useState(false);

    useEffect(() => {
        fetchQuizByTopic(topicId).then(setQuiz);
    }, [topicId]);

    if (!quiz) return <p className="status-text">Loading quiz...</p>;

    const questions = quiz.questions;
    const currentQuestion = questions[currentIndex];
    const isLastQuestion = currentIndex === questions.length - 1;

    function selectAnswer(optionIndex) {
        const updated = [...answers];
        updated[currentIndex] = optionIndex;
        setAnswers(updated);
    }

    function goNext() {
        if (isLastQuestion) {
            setSubmitted(true);
        } else {
            setCurrentIndex(currentIndex + 1);
        }
    }

    if (submitted) {
        const score = answers.filter(
            (ans, i) => ans === questions[i].correctAnswerIndex
        ).length;

        return (
            <div className="quiz-container">
                <h2>Quiz Complete</h2>
                <p className="score">
                    You scored {score} / {questions.length}
                </p>
                <button className="primary-btn" onClick={onExit}>
                    Back to Topics
                </button>
            </div>
        );
    }

    return (
        <div className="quiz-container">
            <p className="quiz-progress">
                Question {currentIndex + 1} of {questions.length}
            </p>
            <h2>{currentQuestion.question}</h2>

            <div className="quiz-options">
                {currentQuestion.options.map((option, i) => (
                    <button
                        key={i}
                        className={`quiz-option ${answers[currentIndex] === i ? "selected" : ""}`}
                        onClick={() => selectAnswer(i)}
                    >
                        {option}
                    </button>
                ))}
            </div>

            <button
                className="primary-btn"
                disabled={answers[currentIndex] === undefined}
                onClick={goNext}
            >
                {isLastQuestion ? "Submit" : "Next"}
            </button>
        </div>
    );
}