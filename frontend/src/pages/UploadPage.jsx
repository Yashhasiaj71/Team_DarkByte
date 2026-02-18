import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import FileDropzone from '../components/FileDropzone';
import BatchList from '../components/BatchList';
import { createBatch } from '../api/client';

/**
 * UploadPage — file upload form with provider/options selection.
 */
export default function UploadPage() {
    const [files, setFiles] = useState([]);
    const [name, setName] = useState('');
    const [provider, setProvider] = useState('default');
    const [kgramSize, setKgramSize] = useState(5);
    const [windowSize, setWindowSize] = useState(4);
    const [uploading, setUploading] = useState(false);
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');

        if (files.length < 1) {
            setError('Please upload at least 1 file.');
            return;
        }

        setUploading(true);
        try {
            const options = {
                k_gram_size: kgramSize,
                window_size: windowSize,
            };
            const batch = await createBatch(files, name, provider, options);
            navigate(`/results/${batch.id}`);
        } catch (err) {
            setError(err.response?.data?.error || 'Upload failed. Please try again.');
        } finally {
            setUploading(false);
        }
    };

    return (
        <div className="page upload-page">
            <div className="page__header">
                <h1 className="page__title">
                    <span className="title-icon">🔍</span> Plagiarism Detector
                </h1>
                <p className="page__subtitle">
                    Upload documents to detect plagiarism using syntactic fingerprinting
                </p>
            </div>

            <form className="upload-form glass-card" onSubmit={handleSubmit}>
                <div className="form-section">
                    <label className="form-label">Upload Documents</label>
                    <FileDropzone onFilesSelected={setFiles} />
                </div>

                <div className="form-row">
                    <div className="form-group">
                        <label className="form-label" htmlFor="batch-name">Batch Name</label>
                        <input
                            id="batch-name"
                            type="text"
                            className="form-input"
                            placeholder="e.g. Assignment 3 submissions"
                            value={name}
                            onChange={(e) => setName(e.target.value)}
                        />
                    </div>

                    <div className="form-group">
                        <label className="form-label" htmlFor="provider">Detection Mode</label>
                        <select
                            id="provider"
                            className="form-select"
                            value={provider}
                            onChange={(e) => setProvider(e.target.value)}
                        >
                            <option value="default">Balanced (Structure + Vocabulary)</option>
                            <option value="fingerprint_only">Structure Only (Syntactic)</option>
                            <option value="tfidf_only">Vocabulary Only (Text)</option>
                        </select>
                    </div>
                </div>

                <div className="form-row">
                    <div className="form-group">
                        <label className="form-label" htmlFor="kgram">Match Sensitivity</label>
                        <input
                            id="kgram"
                            type="range"
                            className="form-range"
                            min={3}
                            max={10}
                            value={kgramSize}
                            onChange={(e) => setKgramSize(Number(e.target.value))}
                        />
                        <span className="form-hint">
                            {kgramSize <= 4 ? '🔬 High' : kgramSize <= 6 ? '⚖️ Balanced' : '🚀 Fast'} — catches {kgramSize <= 4 ? 'short matches (thorough)' : kgramSize <= 6 ? 'medium matches' : 'only long matches (faster)'}
                        </span>
                    </div>

                    <div className="form-group">
                        <label className="form-label" htmlFor="window">Analysis Depth</label>
                        <input
                            id="window"
                            type="range"
                            className="form-range"
                            min={2}
                            max={10}
                            value={windowSize}
                            onChange={(e) => setWindowSize(Number(e.target.value))}
                        />
                        <span className="form-hint">
                            {windowSize <= 3 ? '🔍 Deep' : windowSize <= 5 ? '⚖️ Balanced' : '⚡ Quick'} — {windowSize <= 3 ? 'more fingerprints, thorough' : windowSize <= 5 ? 'good coverage' : 'fewer fingerprints, faster'}
                        </span>
                    </div>
                </div>

                {error && <div className="form-error">{error}</div>}

                <button
                    type="submit"
                    className="btn btn--primary btn--lg"
                    disabled={uploading || files.length < 1}
                >
                    {uploading ? (
                        <span className="btn__loading">
                            <span className="spinner"></span> Uploading...
                        </span>
                    ) : (
                        '🚀 Analyze Documents'
                    )}
                </button>
            </form>

            <div className="text-compare-nav">
                <Link to="/compare" className="btn btn--ghost">
                    📝 Or paste text directly for comparison →
                </Link>
            </div>

            <BatchList />
        </div>
    );
}
