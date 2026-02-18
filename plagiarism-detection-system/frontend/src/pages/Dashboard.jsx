import React from 'react';
import { Link } from 'react-router-dom';

const Dashboard = () => {
    return (
        <div>
            <div className="page-header">
                <h1>Dashboard</h1>
            </div>
            <div className="card">
                <h3>Welcome to the Plagiarism Detection System</h3>
                <p>Use the sidebar to navigate to "Upload Assignment" to start checking documents.</p>
                <div style={{ marginTop: '20px' }}>
                    <Link to="/upload" className="btn btn-primary" style={{ textDecoration: 'none', display: 'inline-block' }}>
                        Start New Analysis
                    </Link>
                </div>
            </div>

            {/* Future: List of recent submissions table */}
            <div className="card">
                <h3>Recent Activity</h3>
                <p>No recent submissions.</p>
            </div>
        </div>
    );
};

export default Dashboard;
