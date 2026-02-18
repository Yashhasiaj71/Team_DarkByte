import { useState, useRef } from 'react';

/**
 * Drag-and-drop file upload component with file list preview.
 */
export default function FileDropzone({ onFilesSelected, acceptedTypes = '.txt,.pdf,.jpg,.jpeg,.png,.bmp,.webp' }) {
    const [dragActive, setDragActive] = useState(false);
    const [selectedFiles, setSelectedFiles] = useState([]);
    const inputRef = useRef(null);

    const handleDrag = (e) => {
        e.preventDefault();
        e.stopPropagation();
        if (e.type === 'dragenter' || e.type === 'dragover') {
            setDragActive(true);
        } else if (e.type === 'dragleave') {
            setDragActive(false);
        }
    };

    const handleDrop = (e) => {
        e.preventDefault();
        e.stopPropagation();
        setDragActive(false);
        const files = Array.from(e.dataTransfer.files);
        addFiles(files);
    };

    const handleChange = (e) => {
        const files = Array.from(e.target.files);
        addFiles(files);
    };

    const addFiles = (files) => {
        const updated = [...selectedFiles, ...files];
        setSelectedFiles(updated);
        onFilesSelected(updated);
    };

    const removeFile = (index) => {
        const updated = selectedFiles.filter((_, i) => i !== index);
        setSelectedFiles(updated);
        onFilesSelected(updated);
    };

    const formatSize = (bytes) => {
        if (bytes < 1024) return `${bytes} B`;
        if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
        return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
    };

    return (
        <div className="dropzone-wrapper">
            <div
                className={`dropzone ${dragActive ? 'dropzone--active' : ''}`}
                onDragEnter={handleDrag}
                onDragLeave={handleDrag}
                onDragOver={handleDrag}
                onDrop={handleDrop}
                onClick={() => inputRef.current?.click()}
            >
                <input
                    ref={inputRef}
                    type="file"
                    multiple
                    accept={acceptedTypes}
                    onChange={handleChange}
                    className="dropzone__input"
                />
                <div className="dropzone__content">
                    <div className="dropzone__icon">📄</div>
                    <p className="dropzone__text">
                        Drag & drop files here, or <span className="dropzone__link">browse</span>
                    </p>
                    <p className="dropzone__hint">
                        1 file → AI check • 2+ files → plagiarism check • 📸 Images supported (OCR)
                    </p>
                </div>
            </div>

            {selectedFiles.length > 0 && (
                <ul className="file-list">
                    {selectedFiles.map((file, i) => (
                        <li key={i} className="file-list__item">
                            <span className="file-list__name">{file.name}</span>
                            <span className="file-list__size">{formatSize(file.size)}</span>
                            <button
                                className="file-list__remove"
                                onClick={() => removeFile(i)}
                                title="Remove file"
                            >
                                ✕
                            </button>
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
}
