import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import IndexPage from "./pages/IndexPage";
import TopicPage from "./pages/TopicPage";
import QuizPage from "./pages/QuizPage";
import ScanPage from "./pages/ScanPage";
import ProgressPage from "./pages/ProgressPage";
import ShowcasePage from "./pages/ShowcasePage";
import NotFoundPage from "./pages/NotFoundPage";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<IndexPage />} />
        <Route path="/showcase" element={<ShowcasePage />} />
        <Route path="/topics/:id" element={<TopicPage />} />
        <Route path="/topics/:id/quiz" element={<QuizPage />} />
        <Route path="/scan" element={<ScanPage />} />
        <Route path="/progress" element={<ProgressPage />} />
        <Route path="*" element={<NotFoundPage />} />
      </Routes>
    </BrowserRouter>
  );
}