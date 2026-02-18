import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { getReport } from '../api/api';
import { PieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const ReportPage = () => {
    const { id } = useParams();
    const [report, setReport] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    useEffect(() => {
        const fetchReport = async () => {
            try {
                const data = await getReport(id);
                setReport(data);
            } catch (err) {
                console.error(err);
                setError('Failed to load report.');
            } finally {
                setLoading(false);
            }
        };

        if (id) {
            fetchReport();
        }
    }, [id]);

    if (loading) return <div>Loading report...</div>;
    if (error) return <div style={{ color: 'red' }}>{error}</div>;
    if (!report) return <div>No report found.</div>;

    const data = [
        { name: 'Stylometric Deviation', value: report.stylometric_deviation_score * 100 },
        { name: 'AI Probability', value: report.ai_probability_score * 100 },
        { name: 'Semantic Similarity', value: report.semantic_similarity_score * 100 },
    ];

    // Normalize simplistic values for pie chart visualization if they are too small
    const chartData = data.map(d => ({ ...d, value: Math.max(d.value, 1) }));

    const COLORS = ['#0088FE', '#00C49F', '#FFBB28'];

    return (
        <div>
            <div className="page-header">
                <h1>Analysis Report</h1>
            </div>

            <div className="card">
                <h2>Risk Level: <span style={{
                    color: report.final_risk_level === 'High' ? 'red' :
                        report.final_risk_level === 'Medium' ? 'orange' : 'green'
                }}>{report.final_risk_level}</span></h2>
                <p>Submission ID: {report.submission_id}</p>
                <p>Analyzed at: {new Date(report.created_at).toLocaleString()}</p>
            </div>

            <div style={{ display: 'flex', gap: '20px', flexWrap: 'wrap' }}>
                <div className="card" style={{ flex: 1, minWidth: '300px' }}>
                    <h3>Detailed Metrics</h3>
                    <ul>
                        <li><strong>Stylometric Deviation:</strong> {(report.stylometric_deviation_score * 100).toFixed(1)}%</li>
                        <li><strong>AI Probability Score:</strong> {(report.ai_probability_score * 100).toFixed(1)}%</li>
                        <li><strong>Semantic Similarity:</strong> {(report.semantic_similarity_score * 100).toFixed(1)}%</li>
                    </ul>
                </div>

                <div className="card" style={{ flex: 1, minWidth: '300px', height: '300px' }}>
                    <h3>Visual Breakdown</h3>
                    <ResponsiveContainer width="100%" height="100%">
                        <PieChart>
                            <Pie
                                data={chartData}
                                cx="50%"
                                cy="50%"
                                innerRadius={60}
                                outerRadius={80}
                                fill="#8884d8"
                                paddingAngle={5}
                                dataKey="value"
                            >
                                {chartData.map((entry, index) => (
                                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                                ))}
                            </Pie>
                            <Tooltip />
                            <Legend />
                        </PieChart>
                    </ResponsiveContainer>
                </div>
            </div>
        </div>
    );
};

export default ReportPage;
