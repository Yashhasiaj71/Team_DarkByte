import { BrowserRouter, Routes, Route } from 'react-router-dom';
import UploadPage from './pages/UploadPage';
import ResultsPage from './pages/ResultsPage';
import TextComparePage from './pages/TextComparePage';
import './index.css';

export default function App() {
  return (
    <BrowserRouter>
      <div className="app">
        <Routes>
          <Route path="/" element={<UploadPage />} />
          <Route path="/compare" element={<TextComparePage />} />
          <Route path="/results/:batchId" element={<ResultsPage />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}
