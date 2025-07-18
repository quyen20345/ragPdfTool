import React from "react";
import MessageItem from "./MessageItem";

const MessageList = ({ messages }) => {
  return (
    <div style={{ flex: 1, overflowY: "auto", marginBottom: 10 }}>
      {messages.map((msg, index) => (
        <MessageItem key={index} sender={msg.sender} text={msg.text} />
      ))}
    </div>
  );
};

export default MessageList;
