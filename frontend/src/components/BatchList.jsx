import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { listBatches, deleteBatch } from '../api/client';

/**
 * BatchList — shows past batches with status badges.
 */
export default function BatchList() {
    const [batches, setBatches] = useState([]);
    const [loading, setLoading] = useState(true);
    const navigate = useNavigate();

    useEffect(() => {
        fetchBatches();
    }, []);

    const fetchBatches = async () => {
        try {
            const data = await listBatches();
            setBatches(data.results || data);
        } catch (err) {
            console.error('Failed to load batches:', err);
        } finally {
            setLoading(false);
        }
    };

    const handleDelete = async (e, batchId) => {
        e.stopPropagation();
        if (!confirm('Delete this batch and all its results?')) return;
        try {
            await deleteBatch(batchId);
            setBatches((prev) => prev.filter((b) => b.id !== batchId));
        } catch (err) {
            console.error('Delete failed:', err);
        }
    };

    const statusBadge = (status) => {
        const classes = {
            queued: 'badge badge--queued',
            processing: 'badge badge--processing',
            completed: 'badge badge--completed',
            failed: 'badge badge--failed',
        };
        return <span className={classes[status] || 'badge'}>{status}</span>;
    };

    if (loading) {
        return <div className="batch-list__loading">Loading batches...</div>;
    }

    if (batches.length === 0) {
        return (
            <div className="batch-list__empty">
                <p>No batches yet. Upload some files to get started!</p>
            </div>
        );
    }

    return (
        <div className="batch-list">
            <h3 className="batch-list__title">Recent Batches</h3>
            <div className="batch-list__grid">
                {batches.map((batch) => (
                    <div
                        key={batch.id}
                        className="batch-card"
                        onClick={() => navigate(`/results/${batch.id}`)}
                    >
                        <div className="batch-card__header">
                            <span className="batch-card__name">{batch.name || 'Unnamed Batch'}</span>
                            {statusBadge(batch.status)}
                        </div>
                        <div className="batch-card__meta">
                            <span>{batch.document_count} files</span>
                            <span>{new Date(batch.created_at).toLocaleDateString()}</span>
                        </div>
                        <div className="batch-card__actions">
                            <button
                                className="btn btn--sm btn--danger"
                                onClick={(e) => handleDelete(e, batch.id)}
                            >
                                Delete
                            </button>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}
