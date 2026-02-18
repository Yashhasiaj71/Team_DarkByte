import { useState, useEffect, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getBatch } from '../api/client';
import SimilarityMatrix from '../components/SimilarityMatrix';
import SegmentViewer from '../components/SegmentViewer';
import AiDetectionPanel from '../components/AiDetectionPanel';

const POLL_INTERVAL = 3000; // 3 seconds

/**
 * ResultsPage — polls batch status and displays results.
 */
export default function ResultsPage() {
    const { batchId } = useParams();
    const navigate = useNavigate();
    const [batch, setBatch] = useState(null);
    const [error, setError] = useState('');
    const pollRef = useRef(null);

    useEffect(() => {
        fetchBatch();
        return () => clearInterval(pollRef.current);
    }, [batchId]);

    const fetchBatch = async () => {
        try {
            const data = await getBatch(batchId);
            setBatch(data);

            // Start polling if not yet completed
            if (data.status === 'queued' || data.status === 'processing') {
                startPolling();
            }
        } catch (err) {
            setError('Failed to load batch. It may have been deleted.');
        }
    };

    const startPolling = () => {
        if (pollRef.current) return;
        pollRef.current = setInterval(async () => {
            try {
                const data = await getBatch(batchId);
                setBatch(data);
                if (data.status === 'completed' || data.status === 'failed') {
                    clearInterval(pollRef.current);
                    pollRef.current = null;
                }
            } catch {
                clearInterval(pollRef.current);
                pollRef.current = null;
            }
        }, POLL_INTERVAL);
    };

    if (error) {
        return (
            <div className="page results-page">
                <div className="glass-card error-card">
                    <h2>Error</h2>
                    <p>{error}</p>
                    <button className="btn btn--primary" onClick={() => navigate('/')}>
                        ← Back to Upload
                    </button>
                </div>
            </div>
        );
    }

    if (!batch) {
        return (
            <div className="page results-page">
                <div className="loading-state">
                    <div className="spinner spinner--lg"></div>
                    <p>Loading batch...</p>
                </div>
            </div>
        );
    }

    return (
        <div className="page results-page">
            <div className="page__header">
                <button className="btn btn--ghost" onClick={() => navigate('/')}>
                    ← Back
                </button>
                <div>
                    <h1 className="page__title">{batch.name || 'Batch Results'}</h1>
                    <p className="page__subtitle">
                        {batch.documents?.length || 0} documents • Created{' '}
                        {new Date(batch.created_at).toLocaleString()}
                    </p>
                </div>
                <span className={`badge badge--${batch.status} badge--lg`}>
                    {batch.status}
                </span>
            </div>

            {/* Processing State */}
            {(batch.status === 'queued' || batch.status === 'processing') && (
                <div className="glass-card processing-card">
                    <div className="processing-animation">
                        <div className="spinner spinner--lg"></div>
                    </div>
                    <h2>
                        {batch.status === 'queued' ? 'Queued for Analysis' : 'Analyzing Documents...'}
                    </h2>
                    <p>
                        {batch.status === 'queued'
                            ? 'Your batch is in the queue. Processing will begin shortly.'
                            : 'Running TF-IDF comparison and syntactic fingerprinting. This may take a moment.'}
                    </p>
                    <div className="progress-bar">
                        <div
                            className={`progress-bar__fill ${batch.status === 'processing' ? 'progress-bar__fill--animated' : ''}`}
                        ></div>
                    </div>
                </div>
            )}

            {/* Failed State */}
            {batch.status === 'failed' && (
                <div className="glass-card error-card">
                    <h2>Analysis Failed</h2>
                    <p>
                        Something went wrong while processing your documents. Please try uploading again.
                    </p>
                </div>
            )}

            {/* Completed State — Results */}
            {batch.status === 'completed' && (() => {
                const isCorpusMode = batch.results?.some((r) => r.details?.is_corpus_comparison);
                const userDocs = isCorpusMode
                    ? (batch.documents || []).filter((d) => !d.minio_key?.startsWith('__corpus__/'))
                    : (batch.documents || []);
                const displayResults = batch.results || [];

                return (
                    <>
                        {/* Summary Stats */}
                        <div className="stats-row">
                            <div className="stat-card glass-card">
                                <div className="stat-value">{userDocs.length}</div>
                                <div className="stat-label">{isCorpusMode ? 'Uploaded' : 'Documents'}</div>
                            </div>
                            <div className="stat-card glass-card">
                                <div className="stat-value">{displayResults.length}</div>
                                <div className="stat-label">{isCorpusMode ? 'AI Corpus Matches' : 'Comparisons'}</div>
                            </div>
                            <div className="stat-card glass-card">
                                <div className="stat-value">
                                    {displayResults.length > 0
                                        ? Math.max(...displayResults.map((r) => r.similarity_pct)).toFixed(1) + '%'
                                        : '0%'}
                                </div>
                                <div className="stat-label">{isCorpusMode ? 'Highest AI Match' : 'Highest Similarity'}</div>
                            </div>
                            <div className="stat-card glass-card">
                                <div className="stat-value">
                                    {displayResults.length > 0
                                        ? (
                                            displayResults.reduce((sum, r) => sum + r.similarity_pct, 0) /
                                            displayResults.length
                                        ).toFixed(1) + '%'
                                        : '0%'}
                                </div>
                                <div className="stat-label">{isCorpusMode ? 'Avg AI Match' : 'Average Similarity'}</div>
                            </div>
                        </div>

                        {/* AI Content Detection */}
                        <div className="glass-card">
                            <AiDetectionPanel documents={userDocs} />
                        </div>

                        {/* Similarity Matrix */}
                        <div className="glass-card">
                            <SimilarityMatrix
                                documents={batch.documents || []}
                                results={displayResults}
                            />
                        </div>

                        {/* Flagged Segments */}
                        <div className="glass-card">
                            <SegmentViewer
                                results={displayResults}
                                documents={batch.documents || []}
                            />
                        </div>
                    </>
                );
            })()}
        </div>
    );
}
