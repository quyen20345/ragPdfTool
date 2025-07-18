import React from "react";
import MessageList from "./MessageList";
import InputBox from "./InputBox";
import TypingIndicator from "./TypingIndicator";

const ChatWindow = ({ messages, onSend, isTyping }) => {
  return (
    <div style={styles.window}>
      <h2>💬 AI Chatbot</h2>
      <MessageList messages={messages} />
      {isTyping && <TypingIndicator />}
      <InputBox onSend={onSend} />
    </div>
  );
};

const styles = {
  window: {
    width: 400,
    margin: "auto",
    border: "1px solid #ccc",
    padding: 20,
    borderRadius: 10,
    height: "80vh",
    display: "flex",
    flexDirection: "column",
    justifyContent: "space-between",
  },
};

export default ChatWindow;
