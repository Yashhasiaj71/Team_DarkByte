import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { uploadAssignment } from '../api/api';
import Button from '../components/Button';

const UploadPage = () => {
    const navigate = useNavigate();
    const [studentId, setStudentId] = useState('');
    const [assignmentId, setAssignmentId] = useState('');
    const [file, setFile] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!file || !studentId || !assignmentId) {
            setError('Please fill all fields');
            return;
        }

        setLoading(true);
        setError('');

        try {
            const result = await uploadAssignment(studentId, assignmentId, file);
            // Navigate to report page with result ID
            navigate(`/report/${result.submission_id}`);
        } catch (err) {
            console.error(err);
            setError('Failed to analyze submission. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div>
            <div className="page-header">
                <h1>Upload Assignment</h1>
            </div>
            <div className="card" style={{ maxWidth: '600px' }}>
                <form onSubmit={handleSubmit}>
                    <div className="form-group">
                        <label>Student ID</label>
                        <input
                            type="text"
                            value={studentId}
                            onChange={(e) => setStudentId(e.target.value)}
                            placeholder="Enter Student ID"
                        />
                    </div>
                    <div className="form-group">
                        <label>Assignment ID</label>
                        <input
                            type="text"
                            value={assignmentId}
                            onChange={(e) => setAssignmentId(e.target.value)}
                            placeholder="Enter Assignment ID"
                        />
                    </div>
                    <div className="form-group">
                        <label>Assignment File (Text, PDF, Image)</label>
                        <input
                            type="file"
                            onChange={handleFileChange}
                        />
                    </div>

                    {error && <p style={{ color: 'red' }}>{error}</p>}

                    <Button type="submit" disabled={loading}>
                        {loading ? 'Analyzing...' : 'Upload & Analyze'}
                    </Button>
                </form>
            </div>
        </div>
    );
};

export default UploadPage;
