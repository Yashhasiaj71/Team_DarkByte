import axios from 'axios';

const api = axios.create({
    baseURL: 'http://localhost:8000',
});

export const uploadAssignment = async (studentId, assignmentId, file) => {
    const formData = new FormData();
    formData.append('student_id', studentId);
    formData.append('assignment_id', assignmentId);
    formData.append('file', file);

    // Note: The backend endpoint is /submissions/analyze for direct analysis
    // or /upload-assignment if just storing.
    // Based on requirements, "Upload Assignment" and "Assign to Student" might be separate steps,
    // but looking at backend implementation, we have /submissions/analyze which takes student_id, assignment_id and file.
    // The prompt asked for:
    // 1. Upload assignments (soft copy)
    // 2. Assign submission to Student ID
    // 3. View scores

    // We will use the analyze endpoint to upload AND analyze immediately for the prototype.
    const response = await api.post('/submissions/analyze', formData, {
        headers: {
            'Content-Type': 'multipart/form-data',
        },
    });
    return response.data; // Returns DetectionResult
};

export const getStudent = async (id) => {
    const response = await api.get(`/students/${id}`);
    return response.data;
};

export const getReport = async (submissionId) => {
    const response = await api.get(`/submissions/${submissionId}/report`);
    return response.data;
};

export default api;
