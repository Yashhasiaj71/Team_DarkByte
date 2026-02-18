/**
 * AiDetectionPanel — displays per-document AI detection results.
 *
 * Shows a summary card for each document with an AI-likelihood gauge,
 * verdict badge, and expandable feature breakdown.
 */
import { useState } from 'react';

const VERDICT_CONFIG = {
    likely_human: { label: 'Likely Human', emoji: '✅', cls: 'verdict--human' },
    uncertain: { label: 'Uncertain', emoji: '⚠️', cls: 'verdict--uncertain' },
    likely_ai: { label: 'Likely AI', emoji: '🤖', cls: 'verdict--ai' },
};

const FEATURE_LABELS = {
    // Category 1 — AI Linguistic Markers
    transition_density: { label: 'Transition Words', desc: 'Overuse of "furthermore", "moreover", etc.' },
    formulaic_phrases: { label: 'Formulaic Phrases', desc: 'Canned expressions typical of AI' },
    hedging_density: { label: 'Hedging Language', desc: 'Excessive qualifying phrases' },
    connective_overuse: { label: 'Connective Overuse', desc: 'Discourse marker frequency' },
    repetitive_openers: { label: 'Repetitive Openers', desc: 'Sentences starting with same word' },
    // Category 2 — Statistical Patterns
    burstiness: { label: 'Sentence Burstiness', desc: 'Variation in sentence lengths' },
    vocabulary_richness: { label: 'Vocabulary Richness', desc: 'Diversity of word usage (MATTR)' },
    sentence_uniformity: { label: 'Sentence Uniformity', desc: 'How uniform sentence lengths are' },
    paragraph_regularity: { label: 'Paragraph Regularity', desc: 'Consistency of paragraph sizes' },
    sentence_complexity: { label: 'Sentence Complexity', desc: 'Comma usage patterns' },
    // Category 3 — Corpus Similarity
    corpus_similarity: { label: 'Corpus Match', desc: 'TF-IDF similarity to known AI texts' },
    ngram_overlap: { label: 'N-gram Overlap', desc: 'Shared phrases with AI reference texts' },
};

function GaugeBar({ score }) {
    const getColor = (s) => {
        if (s < 30) return 'var(--safe)';
        if (s < 50) return 'var(--caution)';
        if (s < 70) return 'var(--warning)';
        return 'var(--danger)';
    };

    return (
        <div className="gauge-bar">
            <div
                className="gauge-bar__fill"
                style={{
                    width: `${Math.min(score, 100)}%`,
                    background: getColor(score),
                }}
            />
            <span className="gauge-bar__label">{score.toFixed(1)}%</span>
        </div>
    );
}

function FeatureRow({ name, score }) {
    const config = FEATURE_LABELS[name] || { label: name, desc: '' };
    const pct = (score * 100).toFixed(0);

    return (
        <div className="ai-feature-row">
            <div className="ai-feature-row__info">
                <span className="ai-feature-row__name">{config.label}</span>
                <span className="ai-feature-row__desc">{config.desc}</span>
            </div>
            <div className="ai-feature-row__bar-wrap">
                <div className="ai-feature-row__bar">
                    <div
                        className="ai-feature-row__bar-fill"
                        style={{ width: `${pct}%` }}
                    />
                </div>
                <span className="ai-feature-row__pct">{pct}%</span>
            </div>
        </div>
    );
}

function DocAiCard({ doc }) {
    const [expanded, setExpanded] = useState(false);
    const ai = doc.ai_detection;

    if (!ai || !ai.verdict) {
        return null;
    }

    const cfg = VERDICT_CONFIG[ai.verdict] || VERDICT_CONFIG.uncertain;

    return (
        <div className="ai-doc-card">
            <div className="ai-doc-card__header" onClick={() => setExpanded(!expanded)}>
                <div className="ai-doc-card__left">
                    <span className="ai-doc-card__name">📄 {doc.original_name}</span>
                    <span className={`ai-verdict-badge ${cfg.cls}`}>
                        {cfg.emoji} {cfg.label}
                    </span>
                </div>
                <div className="ai-doc-card__right">
                    <GaugeBar score={ai.ai_score} />
                    <span className="ai-doc-card__toggle">{expanded ? '▲' : '▼'}</span>
                </div>
            </div>

            {expanded && ai.features && (
                <div className="ai-doc-card__details">
                    <div className="ai-features-title">Feature Breakdown</div>
                    {Object.entries(ai.features).map(([key, val]) => (
                        <FeatureRow key={key} name={key} score={val} />
                    ))}
                </div>
            )}
        </div>
    );
}

export default function AiDetectionPanel({ documents }) {
    const docsWithAi = documents?.filter((d) => d.ai_detection && d.ai_detection.verdict) || [];

    if (docsWithAi.length === 0) {
        return null;
    }

    const avgScore = docsWithAi.reduce((sum, d) => sum + d.ai_detection.ai_score, 0) / docsWithAi.length;
    const aiCount = docsWithAi.filter((d) => d.ai_detection.verdict === 'likely_ai').length;

    return (
        <div className="ai-panel">
            <h3 className="ai-panel__title">🤖 AI Content Detection</h3>
            <p className="ai-panel__subtitle">
                Statistical analysis of writing patterns across {docsWithAi.length} document{docsWithAi.length !== 1 ? 's' : ''}
            </p>

            {aiCount > 0 && (
                <div className="ai-panel__alert">
                    ⚠️ {aiCount} document{aiCount !== 1 ? 's' : ''} flagged as likely AI-generated
                </div>
            )}

            <div className="ai-panel__summary">
                <div className="ai-panel__stat">
                    <span className="ai-panel__stat-value">{avgScore.toFixed(1)}%</span>
                    <span className="ai-panel__stat-label">Avg AI Score</span>
                </div>
                <div className="ai-panel__stat">
                    <span className="ai-panel__stat-value">{aiCount}</span>
                    <span className="ai-panel__stat-label">Flagged</span>
                </div>
                <div className="ai-panel__stat">
                    <span className="ai-panel__stat-value">{docsWithAi.length - aiCount}</span>
                    <span className="ai-panel__stat-label">Clean</span>
                </div>
            </div>

            <div className="ai-doc-list">
                {docsWithAi.map((doc) => (
                    <DocAiCard key={doc.id} doc={doc} />
                ))}
            </div>
        </div>
    );
}
