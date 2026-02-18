import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { createTextBatch } from '../api/client';

/**
 * TextComparePage — paste named text entries for cross-comparison.
 */
export default function TextComparePage() {
    const navigate = useNavigate();
    const [name, setName] = useState('');
    const [entries, setEntries] = useState([
        { author: '', text: '' },
        { author: '', text: '' },
    ]);
    const [submitting, setSubmitting] = useState(false);
    const [error, setError] = useState('');

    const updateEntry = (index, field, value) => {
        setEntries((prev) =>
            prev.map((e, i) => (i === index ? { ...e, [field]: value } : e))
        );
    };

    const addEntry = () => {
        setEntries((prev) => [...prev, { author: '', text: '' }]);
    };

    const removeEntry = (index) => {
        if (entries.length <= 2) return;
        setEntries((prev) => prev.filter((_, i) => i !== index));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');

        // Validate
        const valid = entries.filter((en) => en.author.trim() && en.text.trim());
        if (valid.length < 2) {
            setError('At least 2 entries with author name and text are required.');
            return;
        }

        setSubmitting(true);
        try {
            const batch = await createTextBatch(valid, name || 'Text Comparison', {});
            navigate(`/results/${batch.id}`);
        } catch (err) {
            setError(
                err.response?.data?.error || 'Submission failed. Please try again.'
            );
        } finally {
            setSubmitting(false);
        }
    };

    const filledCount = entries.filter((e) => e.author.trim() && e.text.trim()).length;

    return (
        <div className="page text-compare-page">
            <div className="page__header">
                <h1 className="page__title">
                    <span className="title-icon">📝</span> Text Comparison
                </h1>
                <p className="page__subtitle">
                    Paste documents with author names to check for similarities between them
                </p>
            </div>

            <form className="upload-form glass-card" onSubmit={handleSubmit}>
                <div className="form-group">
                    <label className="form-label" htmlFor="batch-name">
                        Batch Name
                    </label>
                    <input
                        id="batch-name"
                        type="text"
                        className="form-input"
                        placeholder="e.g. Assignment 3 — Section B"
                        value={name}
                        onChange={(e) => setName(e.target.value)}
                    />
                </div>

                <div className="entries-section">
                    <div className="entries-header">
                        <label className="form-label">Text Entries</label>
                        <span className="entries-count">
                            {filledCount} of {entries.length} filled
                        </span>
                    </div>

                    {entries.map((entry, i) => (
                        <div className="entry-card" key={i}>
                            <div className="entry-card__header">
                                <span className="entry-card__number">#{i + 1}</span>
                                <input
                                    type="text"
                                    className="form-input entry-card__author"
                                    placeholder="Author / Student name"
                                    value={entry.author}
                                    onChange={(e) =>
                                        updateEntry(i, 'author', e.target.value)
                                    }
                                />
                                {entries.length > 2 && (
                                    <button
                                        type="button"
                                        className="btn btn--danger btn--sm entry-card__remove"
                                        onClick={() => removeEntry(i)}
                                        title="Remove entry"
                                    >
                                        ✕
                                    </button>
                                )}
                            </div>
                            <textarea
                                className="form-input entry-card__text"
                                placeholder="Paste the document text here..."
                                rows={6}
                                value={entry.text}
                                onChange={(e) =>
                                    updateEntry(i, 'text', e.target.value)
                                }
                            />
                            {entry.text.trim() && (
                                <div className="entry-card__meta">
                                    {entry.text.trim().split(/\s+/).length} words •{' '}
                                    {entry.text.trim().length} characters
                                </div>
                            )}
                        </div>
                    ))}

                    <button
                        type="button"
                        className="btn btn--ghost add-entry-btn"
                        onClick={addEntry}
                    >
                        + Add Another Entry
                    </button>
                </div>

                {error && <div className="form-error">{error}</div>}

                <button
                    type="submit"
                    className="btn btn--primary btn--lg"
                    disabled={submitting || filledCount < 2}
                >
                    {submitting ? (
                        <span className="btn__loading">
                            <span className="spinner"></span> Analyzing...
                        </span>
                    ) : (
                        `🚀 Compare ${filledCount} Entries`
                    )}
                </button>
            </form>

            <div className="text-compare-nav">
                <Link to="/" className="btn btn--ghost">
                    📄 Or upload files instead →
                </Link>
            </div>
        </div>
    );
}
