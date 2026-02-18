/**
 * API client for communicating with the Django backend.
 */
import axios from 'axios';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const client = axios.create({
    baseURL: API_BASE,
    timeout: 30000,
});

/**
 * Upload files and create a new batch.
 * @param {FileList|File[]} files
 * @param {string} name
 * @param {string} provider
 * @param {object} options
 * @returns {Promise} batch data
 */
export async function createBatch(files, name = '', provider = 'default', options = {}) {
    const formData = new FormData();
    for (const file of files) {
        formData.append('files', file);
    }
    formData.append('name', name);
    formData.append('provider', provider);
    formData.append('options', JSON.stringify(options));

    const response = await client.post('/batches/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
    });
    return response.data;
}

/**
 * Get batch details (status + results) — used for polling.
 * @param {string} batchId
 * @returns {Promise} batch data with documents and results
 */
export async function getBatch(batchId) {
    const response = await client.get(`/batches/${batchId}/`);
    return response.data;
}

/**
 * List all batches.
 * @returns {Promise} paginated batch list
 */
export async function listBatches() {
    const response = await client.get('/batches/');
    return response.data;
}

/**
 * Delete a batch.
 * @param {string} batchId
 */
export async function deleteBatch(batchId) {
    await client.delete(`/batches/${batchId}/`);
}

/**
 * Create a batch from named text entries (text comparison mode).
 * @param {Array<{author: string, text: string}>} entries
 * @param {string} name
 * @param {object} options
 * @returns {Promise} batch data
 */
export async function createTextBatch(entries, name = '', options = {}) {
    const response = await client.post('/batches/text/', {
        name,
        entries,
        options,
    });
    return response.data;
}

export default client;
