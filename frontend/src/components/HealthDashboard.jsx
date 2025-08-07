// frontend/src/components/HealthDashboard.jsx
import React, { useState, useEffect, useCallback } from 'react';
import { Activity, Database, FileText, CheckCircle, XCircle, AlertCircle } from 'lucide-react';
import { healthAPI, documentAPI } from '../services/api';

const HealthDashboard = () => {
  const [healthStatus, setHealthStatus] = useState(null);
  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const loadHealthStatus = useCallback(async () => {
    try {
      const res = await healthAPI.check();
      setHealthStatus(res.data);
      setError('');
    } catch (err) {
      setError('Không thể kết nối đến backend: ' + err.message);
      setHealthStatus(null);
    } finally {
      setLoading(false);
    }
  }, []);

  const loadDocuments = useCallback(async () => {
    try {
      const res = await documentAPI.list();
      setDocuments(res.data);
    } catch (err) {
      console.error('Error loading documents:', err);
    }
  }, []);

  useEffect(() => {
    loadHealthStatus();
    loadDocuments();
    const interval = setInterval(loadHealthStatus, 30000);
    return () => clearInterval(interval);
  }, [loadHealthStatus, loadDocuments]);

  const getStatusIcon = (status) => {
    if (status === 'healthy' || status === 'connected' || status?.includes('connected')) {
      return <CheckCircle className="h-5 w-5 text-green-500" />;
    } else if (status?.includes('error')) {
      return <XCircle className="h-5 w-5 text-red-500" />;
    } else {
      return <AlertCircle className="h-5 w-5 text-yellow-500" />;
    }
  };

  const getStatusColor = (status) => {
    if (status === 'healthy' || status === 'connected' || status?.includes('connected')) {
      return 'text-green-600 bg-green-50';
    } else if (status?.includes('error')) {
      return 'text-red-600 bg-red-50';
    } else {
      return 'text-yellow-600 bg-yellow-50';
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto p-6">
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-gray-800">Trạng thái hệ thống</h2>
        <p className="text-gray-600">Giám sát tình trạng các dịch vụ và thống kê hệ thống</p>
      </div>

      {error && (
        <div className="mb-6 p-4 bg-red-100 border border-red-400 text-red-700 rounded-lg flex items-center">
          <XCircle className="h-5 w-5 mr-2" />
          {error}
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* System Health */}
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center mb-4">
            <Activity className="h-6 w-6 text-blue-500 mr-2" />
            <h3 className="text-lg font-semibold text-gray-800">Trạng thái dịch vụ</h3>
          </div>
          <div className="space-y-3">
            {/* Tổng thể, Qdrant, Ollama */}
            {['status', 'qdrant', 'ollama'].map((key) => (
              <div key={key} className="flex items-center justify-between p-3 border rounded-lg">
                <div className="flex items-center">
                  {getStatusIcon(healthStatus[key])}
                  <span className="ml-2 font-medium">
                    {key === 'status'
                      ? 'Hệ thống tổng thể'
                      : key === 'qdrant'
                      ? 'Qdrant Vector DB'
                      : 'Ollama LLM'}
                  </span>
                </div>
                <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(healthStatus[key])}`}>
                  {healthStatus[key] === 'healthy' ? 'Hoạt động tốt' : healthStatus[key]}
                </span>
              </div>
            ))}
            {healthStatus.ollama_response_sample && (
              <div className="mt-4 p-3 bg-gray-50 rounded-lg">
                <p className="text-sm text-gray-600 mb-1">Phản hồi mẫu từ Ollama:</p>
                <p className="text-sm font-mono text-gray-800">{healthStatus.ollama_response_sample}</p>
              </div>
            )}
          </div>
        </div>

        {/* Statistics */}
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center mb-4">
            <Database className="h-6 w-6 text-green-500 mr-2" />
            <h3 className="text-lg font-semibold text-gray-800">Thống kê dữ liệu</h3>
          </div>
          <div className="space-y-4">
            {[
              { label: 'Tài liệu PDF', count: documents.length },
              { label: 'Chunks', count: documents.reduce((sum, doc) => sum + doc.total_chunks, 0) },
              { label: 'Hoàn thành', count: documents.filter((doc) => doc.is_processed).length },
            ].map((item, idx) => (
              <div key={idx} className="flex items-center justify-between p-4 bg-blue-50 rounded-lg">
                <div className="flex items-center">
                  <FileText className="h-8 w-8 text-blue-500" />
                  <div className="ml-3">
                    <p className="text-sm text-gray-600">{item.label}</p>
                    <p className="text-2xl font-bold text-gray-800">{item.count}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default HealthDashboard;
