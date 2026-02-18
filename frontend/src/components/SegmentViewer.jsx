/**
 * SegmentViewer — shows flagged plagiarized segments from comparison details.
 */
export default function SegmentViewer({ results, documents }) {
    if (!results || results.length === 0) return null;

    // Build doc name lookup
    const docNames = {};
    for (const doc of documents) {
        docNames[doc.id] = doc.original_name;
    }

    // Filter results with flagged segments
    const flaggedResults = results.filter(
        (r) => r.details?.flagged_segments?.length > 0
    );

    if (flaggedResults.length === 0) {
        return (
            <div className="segment-viewer">
                <h3 className="segment-title">Flagged Segments</h3>
                <p className="segment-empty">No suspicious segments detected.</p>
            </div>
        );
    }

    return (
        <div className="segment-viewer">
            <h3 className="segment-title">Flagged Segments</h3>
            {flaggedResults.map((result) => (
                <div key={result.id} className="segment-pair">
                    <div className="segment-pair__header">
                        <span className="segment-pair__docs">
                            {docNames[result.doc_a]} ↔ {docNames[result.doc_b]}
                        </span>
                        <span className="segment-pair__score">
                            {result.similarity_pct.toFixed(1)}% similar
                        </span>
                    </div>

                    <div className="segment-pair__details">
                        <div className="detail-chip">
                            <span className="detail-label">Text</span>
                            <span className="detail-value">{result.details.text_similarity}%</span>
                        </div>
                        <div className="detail-chip">
                            <span className="detail-label">Fingerprint</span>
                            <span className="detail-value">{result.details.fingerprint_similarity}%</span>
                        </div>
                        <div className="detail-chip">
                            <span className="detail-label">Matches</span>
                            <span className="detail-value">
                                {result.details.matched_fingerprints} / {Math.max(result.details.total_fingerprints_a, result.details.total_fingerprints_b)}
                            </span>
                        </div>
                    </div>

                    <div className="segment-list">
                        {result.details.flagged_segments.map((seg, i) => (
                            <div key={i} className="segment-item">
                                <div className="segment-item__badge">Segment {i + 1}</div>
                                <div className="segment-item__positions">
                                    <span>Doc A: pos {seg.doc_a_start}–{seg.doc_a_end}</span>
                                    <span>Doc B: pos {seg.doc_b_start}–{seg.doc_b_end}</span>
                                    <span>{seg.match_count} matching fingerprints</span>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            ))}
        </div>
    );
}
