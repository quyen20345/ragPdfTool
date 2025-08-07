// frontend/src/components/ChatInterface.jsx
import React, { useState, useEffect, useRef, useCallback } from 'react';
import { Send, MessageSquare, Plus, Trash2, FileText } from 'lucide-react';
import { chatAPI } from '../services/api';
import ReactMarkdown from 'react-markdown';

const ChatInterface = () => {
  const [sessions, setSessions] = useState([]);
  const [currentSession, setCurrentSession] = useState(null);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [sessionLoading, setSessionLoading] = useState(true);
  const messagesEndRef = useRef(null);

  // Load sessions from API
  const loadSessions = useCallback(async () => {
    try {
      setSessionLoading(true);
      const response = await chatAPI.listSessions();
      setSessions(response.data);
      if (response.data.length > 0 && !currentSession) {
        setCurrentSession(response.data[0]);
      }
    } catch (err) {
      console.error('Error loading sessions:', err);
    } finally {
      setSessionLoading(false);
    }
  }, [currentSession]);

  // Initial load
  useEffect(() => {
    loadSessions();
  }, [loadSessions]);

  // Load messages when session changes
  useEffect(() => {
    if (currentSession) {
      loadMessages(currentSession.id);
    }
  }, [currentSession]);

  // Scroll to bottom on new messages
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  // Fetch messages for a session
  const loadMessages = async (sessionId) => {
    try {
      const response = await chatAPI.getMessages(sessionId);
      setMessages(response.data);
    } catch (err) {
      console.error('Error loading messages:', err);
    }
  };

  // Create a new session
  const createNewSession = async () => {
    try {
      const sessionName = `Chat ${new Date().toLocaleString('vi-VN')}`;
      const response = await chatAPI.createSession({ session_name: sessionName });
      const newSession = response.data;
      setSessions(prev => [newSession, ...prev]);
      setCurrentSession(newSession);
      setMessages([]);
    } catch (err) {
      console.error('Error creating session:', err);
    }
  };

  // Delete a session
  const deleteSession = async (sessionId) => {
    if (!window.confirm('Bạn có chắc muốn xóa cuộc trò chuyện này?')) return;
    try {
      await chatAPI.deleteSession(sessionId);
      setSessions(prev => prev.filter(s => s.id !== sessionId));
      if (currentSession?.id === sessionId) {
        const remaining = sessions.filter(s => s.id !== sessionId);
        setCurrentSession(remaining[0] || null);
      }
    } catch (err) {
      console.error('Error deleting session:', err);
    }
  };

  // Send a message
  const sendMessage = async (e) => {
    e.preventDefault();
    if (!input.trim() || loading) return;

    const userMsg = input.trim();
    setInput('');
    setLoading(true);

    // Optimistic UI update
    const tempMsg = {
      id: Date.now(),
      message_type: 'user',
      content: userMsg,
      created_at: new Date().toISOString(),
    };
    setMessages(prev => [...prev, tempMsg]);

    try {
      const response = await chatAPI.query({
        query: userMsg,
        session_id: currentSession?.id,
        temperature: 0.7,
      });

      const assistantMsg = {
        id: Date.now() + 1,
        message_type: 'assistant',
        content: response.data.answer,
        created_at: new Date().toISOString(),
        source_documents: response.data.source_documents,
      };

      setMessages(prev => [...prev.slice(0, -1), tempMsg, assistantMsg]);
      if (currentSession) setTimeout(() => loadMessages(currentSession.id), 500);
    } catch (err) {
      console.error('Error sending message:', err);
      setMessages(prev => prev.slice(0, -1));
    } finally {
      setLoading(false);
    }
  };

  // Format timestamp
  const formatTime = (dateString) =>
    new Date(dateString).toLocaleTimeString('vi-VN', {
      hour: '2-digit',
      minute: '2-digit',
    });

  return (
    <div className="flex h-screen bg-gray-100">
      {/* Sidebar */}
      <div className="w-80 bg-white border-r border-gray-200 flex flex-col">
        <div className="p-4 border-b border-gray-200">
          <button
            onClick={createNewSession}
            className="w-full flex items-center justify-center px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors"
          >
            <Plus className="h-5 w-5 mr-2" />
            Cuộc trò chuyện mới
          </button>
        </div>
        <div className="flex-1 overflow-y-auto">
          {sessionLoading ? (
            <div className="p-4 text-center text-gray-500">Đang tải...</div>
          ) : sessions.length === 0 ? (
            <div className="p-4 text-center text-gray-500">
              <MessageSquare className="h-8 w-8 mx-auto mb-2" />
              Chưa có cuộc trò chuyện nào
            </div>
          ) : (
            sessions.map(session => (
              <div
                key={session.id}
                className={`p-4 border-b border-gray-100 cursor-pointer hover:bg-gray-50 ${
                  currentSession?.id === session.id ? 'bg-blue-50 border-l-4 border-l-blue-500' : ''
                }`}
                onClick={() => setCurrentSession(session)}
              >
                <div className="flex items-center justify-between">
                  <div className="flex-1">
                    <h3 className="font-medium text-gray-800 truncate">{session.session_name}</h3>
                    <p className="text-sm text-gray-500">
                      {new Date(session.created_at).toLocaleDateString('vi-VN')}
                    </p>
                  </div>
                  <button
                    onClick={e => {
                      e.stopPropagation();
                      deleteSession(session.id);
                    }}
                    className="p-1 text-gray-400 hover:text-red-500"
                  >
                    <Trash2 className="h-4 w-4" />
                  </button>
                </div>
              </div>
            )))
          }
        </div>
      </div>

      {/* Chat Area */}
      <div className="flex-1 flex flex-col">
        {currentSession ? (
          <>
            {/* Header */}
            <div className="p-4 bg-white border-b border-gray-200">
              <h2 className="text-lg font-semibold text-gray-800">{currentSession.session_name}</h2>
            </div>

            {/* Messages */}
            <div className="flex-1 overflow-y-auto p-4 space-y-4">
              {messages.length === 0 ? (
                <div className="text-center text-gray-500 mt-20">
                  <MessageSquare className="h-16 w-16 mx-auto mb-4" />
                  <p>Hãy bắt đầu cuộc trò chuyện bằng cách đặt câu hỏi về tài liệu!</p>
                </div>
              ) : (
                messages.map(message => (
                  <div
                    key={message.id}
                    className={`flex ${message.message_type === 'user' ? 'justify-end' : 'justify-start'}`}
                  >
                    <div
                      className={`max-w-3xl rounded-lg px-4 py-2 ${
                        message.message_type === 'user' ? 'bg-blue-500 text-white' : 'bg-white border border-gray-200'
                      }`}
                    >
                      <div className="prose prose-sm max-w-none">
                        {message.message_type === 'user' ? (
                          <p className="m-0">{message.content}</p>
                        ) : (
                          <ReactMarkdown>{message.content}</ReactMarkdown>
                        )}
                      </div>
                      {message.source_documents && message.source_documents.length > 0 && (
                        <div className="mt-3 pt-3 border-t border-gray-100">
                          <p className="text-xs text-gray-500 mb-2 flex items-center">
                            <FileText className="h-3 w-3 mr-1" /> Nguồn tham khảo:
                          </p>
                          <div className="space-y-2">
                            {message.source_documents.map((doc, idx) => (
                              <div key={idx} className="text-xs bg-gray-50 p-2 rounded">
                                <p className="font-medium text-gray-600">
                                  {doc.metadata.filename} (Chunk {doc.metadata.chunk_id + 1})
                                </p>
                                <p className="text-gray-500 truncate">{doc.content}</p>
                              </div>
                            ))}
                          </div>
                        </div>
                      )}
                      <div className="text-xs text-gray-400 mt-2">{formatTime(message.created_at)}</div>
                    </div>
                  </div>
                )))
              }
              {loading && (
                <div className="flex justify-start">
                  <div className="bg-white border border-gray-200 rounded-lg px-4 py-2">
                    <div className="flex items-center space-x-2">
                      <div className="animate-bounce h-2 w-2 bg-gray-400 rounded-full"></div>
                      <div className="animate-bounce h-2 w-2 bg-gray-400 rounded-full" style={{ animationDelay: '0.1s' }}></div>
                      <div className="animate-bounce h-2 w-2 bg-gray-400 rounded-full" style={{ animationDelay: '0.2s' }}></div>
                    </div>
                  </div>
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>

            {/* Input */}
            <div className="p-4 bg-white border-t border-gray-200">
              <form onSubmit={sendMessage} className="flex space-x-2">
                <input
                  type="text"
                  value={input}
                  onChange={e => setInput(e.target.value)}
                  placeholder="Đặt câu hỏi về tài liệu..."
                  disabled={loading}
                  className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
                <button
                  type="submit"
                  disabled={loading || !input.trim()}
                  className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <Send className="h-5 w-5" />
                </button>
              </form>
            </div>
          </>
        ) : (
          <div className="flex-1 flex items-center justify-center text-gray-500">
            <div className="text-center">
              <MessageSquare className="h-16 w-16 mx-auto mb-4" />
              <p>Chọn hoặc tạo một cuộc trò chuyện để bắt đầu</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ChatInterface;
