-- Initialize database for RAG system
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_documents_filename ON documents(filename);
CREATE INDEX IF NOT EXISTS idx_documents_created_at ON documents(created_at);
CREATE INDEX IF NOT EXISTS idx_chat_sessions_created_at ON chat_sessions(created_at);
CREATE INDEX IF NOT EXISTS idx_chat_messages_session_id ON chat_messages(session_id);
CREATE INDEX IF NOT EXISTS idx_chat_messages_created_at ON chat_messages(created_at);

-- Insert sample data (optional)
-- INSERT INTO chat_sessions (session_name) VALUES ('Default Session');







-- -- Tạo extension uuid-ossp nếu chưa có
-- CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- -- Tạo bảng documents (ví dụ)
-- CREATE TABLE IF NOT EXISTS documents (
--     id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
--     filename TEXT NOT NULL,
--     created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW()
-- );

-- -- Tạo bảng chat_sessions (ví dụ)
-- CREATE TABLE IF NOT EXISTS chat_sessions (
--     id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
--     session_name TEXT NOT NULL,
--     created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW()
-- );

-- -- Tạo bảng chat_messages (ví dụ)
-- CREATE TABLE IF NOT EXISTS chat_messages (
--     id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
--     session_id UUID REFERENCES chat_sessions(id),
--     message TEXT NOT NULL,
--     created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW()
-- );

-- -- Tạo các index
-- CREATE INDEX IF NOT EXISTS idx_documents_filename ON documents(filename);
-- CREATE INDEX IF NOT EXISTS idx_documents_created_at ON documents(created_at);
-- CREATE INDEX IF NOT EXISTS idx_chat_sessions_created_at ON chat_sessions(created_at);
-- CREATE INDEX IF NOT EXISTS idx_chat_messages_session_id ON chat_messages(session_id);
-- CREATE INDEX IF NOT EXISTS idx_chat_messages_created_at ON chat_messages(created_at);

-- -- Chèn dữ liệu mẫu (tuỳ chọn)
-- -- INSERT INTO chat_sessions (session_name) VALUES ('Default Session');
