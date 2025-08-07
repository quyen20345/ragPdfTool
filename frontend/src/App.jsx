// frontend/src/App.jsx
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom';
import { FileText, MessageSquare, Activity } from 'lucide-react';
import DocumentManager from './components/DocumentManager';
import ChatInterface from './components/ChatInterface';
import HealthDashboard from './components/HealthDashboard';
import './index.css';

const Navigation = () => {
  const location = useLocation();
  
  const navItems = [
    { path: '/', icon: MessageSquare, label: 'Trò chuyện', exact: true },
    { path: '/documents', icon: FileText, label: 'Quản lý tài liệu' },
    { path: '/health', icon: Activity, label: 'Trạng thái hệ thống' }
  ];

  return (
    <nav className="bg-white shadow-lg">
      <div className="max-w-7xl mx-auto px-4">
        <div className="flex justify-between items-center h-16">
          <div className="flex items-center space-x-4">
            <h1 className="text-xl font-bold text-gray-800">RAG PDF System</h1>
          </div>
          <div className="flex space-x-4">
            {navItems.map(({ path, icon: Icon, label, exact }) => {
              const isActive = exact 
                ? location.pathname === path 
                : location.pathname.startsWith(path);
              
              return (
                <Link
                  key={path}
                  to={path}
                  className={`flex items-center px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                    isActive
                      ? 'bg-blue-100 text-blue-700'
                      : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
                  }`}
                >
                  <Icon className="h-4 w-4 mr-2" />
                  {label}
                </Link>
              );
            })}
          </div>
        </div>
      </div>
    </nav>
  );
};

const App = () => {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        <Navigation />
        <Routes>
          <Route path="/" element={<ChatInterface />} />
          <Route path="/documents" element={<DocumentManager />} />
          <Route path="/health" element={<HealthDashboard />} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;
