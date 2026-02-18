/**
 * Similarity Matrix — displays pairwise similarity as a heatmap table.
 */
export default function SimilarityMatrix({ documents, results }) {
    if (!documents || !results || results.length === 0) {
        return null;
    }

    // Build a lookup: "docA_id-docB_id" → result
    const resultMap = {};
    for (const r of results) {
        resultMap[`${r.doc_a}-${r.doc_b}`] = r;
        resultMap[`${r.doc_b}-${r.doc_a}`] = r;
    }

    const getColor = (pct) => {
        if (pct >= 80) return 'var(--danger)';
        if (pct >= 50) return 'var(--warning)';
        if (pct >= 25) return 'var(--caution)';
        return 'var(--safe)';
    };

    const getLabel = (pct) => {
        if (pct >= 80) return 'High';
        if (pct >= 50) return 'Medium';
        if (pct >= 25) return 'Low';
        return 'Minimal';
    };

    return (
        <div className="matrix-container">
            <h3 className="matrix-title">Similarity Matrix</h3>
            <div className="matrix-scroll">
                <table className="matrix-table">
                    <thead>
                        <tr>
                            <th className="matrix-corner"></th>
                            {documents.map((doc) => (
                                <th key={doc.id} className="matrix-header" title={doc.original_name}>
                                    {doc.original_name.length > 15
                                        ? doc.original_name.slice(0, 12) + '...'
                                        : doc.original_name}
                                </th>
                            ))}
                        </tr>
                    </thead>
                    <tbody>
                        {documents.map((docRow) => (
                            <tr key={docRow.id}>
                                <td className="matrix-row-header" title={docRow.original_name}>
                                    {docRow.original_name.length > 15
                                        ? docRow.original_name.slice(0, 12) + '...'
                                        : docRow.original_name}
                                </td>
                                {documents.map((docCol) => {
                                    if (docRow.id === docCol.id) {
                                        return (
                                            <td key={docCol.id} className="matrix-cell matrix-cell--self">
                                                —
                                            </td>
                                        );
                                    }
                                    const result = resultMap[`${docRow.id}-${docCol.id}`];
                                    const pct = result ? result.similarity_pct : 0;
                                    return (
                                        <td
                                            key={docCol.id}
                                            className="matrix-cell"
                                            style={{ backgroundColor: getColor(pct), color: '#fff' }}
                                            title={`${pct}% — ${getLabel(pct)}`}
                                        >
                                            {pct.toFixed(1)}%
                                        </td>
                                    );
                                })}
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>

            <div className="matrix-legend">
                <span className="legend-item"><span className="legend-dot" style={{ background: 'var(--safe)' }}></span> Minimal (&lt;25%)</span>
                <span className="legend-item"><span className="legend-dot" style={{ background: 'var(--caution)' }}></span> Low (25-50%)</span>
                <span className="legend-item"><span className="legend-dot" style={{ background: 'var(--warning)' }}></span> Medium (50-80%)</span>
                <span className="legend-item"><span className="legend-dot" style={{ background: 'var(--danger)' }}></span> High (&gt;80%)</span>
            </div>
        </div>
    );
}
