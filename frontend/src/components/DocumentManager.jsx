// frontend/src/components/DocumentManager.jsx
import React, { useState, useEffect } from 'react';
import { Upload, FileText, Trash2, AlertCircle, CheckCircle } from 'lucide-react';
import { documentAPI } from '../services/api';

const DocumentManager = () => {
  const [documents, setDocuments] = useState([]);
  const [uploading, setUploading] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    loadDocuments();
  }, []);

  const loadDocuments = async () => {
    try {
      setLoading(true);
      const response = await documentAPI.list();
      setDocuments(response.data);
      setError('');
    } catch (err) {
      setError('Lỗi khi tải danh sách tài liệu: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    if (!file.name.toLowerCase().endsWith('.pdf')) {
      setError('Chỉ hỗ trợ file PDF');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
      setUploading(true);
      setError('');
      await documentAPI.upload(formData);
      await loadDocuments();
    } catch (err) {
      setError('Lỗi khi upload tài liệu: ' + err.response?.data?.detail || err.message);
    } finally {
      setUploading(false);
      event.target.value = '';
    }
  };

  const handleDelete = async (documentId, filename) => {
    if (!window.confirm(`Bạn có chắc muốn xóa tài liệu "${filename}"?`)) {
      return;
    }

    try {
      await documentAPI.delete(documentId);
      await loadDocuments();
    } catch (err) {
      setError('Lỗi khi xóa tài liệu: ' + err.response?.data?.detail || err.message);
    }
  };

  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto p-6">
      <div className="bg-white rounded-lg shadow-lg p-6">
        <h2 className="text-2xl font-bold mb-6 text-gray-800">Quản lý tài liệu PDF</h2>
        
        {/* Upload Section */}
        <div className="mb-6 p-4 border-2 border-dashed border-gray-300 rounded-lg hover:border-blue-500 transition-colors">
          <div className="text-center">
            <Upload className="mx-auto h-12 w-12 text-gray-400 mb-4" />
            <label htmlFor="file-upload" className="cursor-pointer">
              <span className="text-lg text-gray-600">
                {uploading ? 'Đang upload...' : 'Chọn file PDF để upload'}
              </span>
              <input
                id="file-upload"
                type="file"
                accept=".pdf"
                onChange={handleFileUpload}
                disabled={uploading}
                className="hidden"
              />
            </label>
          </div>
        </div>

        {/* Error Display */}
        {error && (
          <div className="mb-4 p-4 bg-red-100 border border-red-400 text-red-700 rounded flex items-center">
            <AlertCircle className="h-5 w-5 mr-2" />
            {error}
          </div>
        )}

        {/* Documents List */}
        <div className="space-y-4">
          <h3 className="text-lg font-semibold text-gray-700">
            Danh sách tài liệu ({documents.length})
          </h3>
          
          {documents.length === 0 ? (
            <div className="text-center py-8 text-gray-500">
              <FileText className="mx-auto h-12 w-12 mb-4" />
              Chưa có tài liệu nào. Hãy upload file PDF đầu tiên!
            </div>
          ) : (
            documents.map((doc) => (
              <div key={doc.id} className="border rounded-lg p-4 hover:shadow-md transition-shadow">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-3">
                    <FileText className="h-8 w-8 text-red-500" />
                    <div>
                      <h4 className="font-medium text-gray-800">{doc.original_filename}</h4>
                      <div className="flex items-center space-x-4 text-sm text-gray-500">
                        <span>{formatFileSize(doc.file_size)}</span>
                        <span>{doc.total_chunks} chunks</span>
                        <span>
                          {doc.is_processed ? (
                            <div className="flex items-center text-green-600">
                              <CheckCircle className="h-4 w-4 mr-1" />
                              Đã xử lý
                            </div>
                          ) : (
                            <div className="flex items-center text-yellow-600">
                              <AlertCircle className="h-4 w-4 mr-1" />
                              Đang xử lý
                            </div>
                          )}
                        </span>
                      </div>
                      <p className="text-xs text-gray-400">
                        Upload: {new Date(doc.created_at).toLocaleString('vi-VN')}
                      </p>
                    </div>
                  </div>
                  
                  <button
                    onClick={() => handleDelete(doc.id, doc.original_filename)}
                    className="p-2 text-red-500 hover:bg-red-50 rounded-full transition-colors"
                    title="Xóa tài liệu"
                  >
                    <Trash2 className="h-5 w-5" />
                  </button>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
};

export default DocumentManager;
