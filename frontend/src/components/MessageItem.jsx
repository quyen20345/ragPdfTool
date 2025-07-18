import React from "react";

const MessageItem = ({ sender, text }) => {
  const isUser = sender === "user";
  return (
    <div
      style={{
        textAlign: isUser ? "right" : "left",
        margin: "4px 0",
        color: isUser ? "blue" : "green",
      }}
    >
      <b>{isUser ? "You" : "AI"}:</b> {text}
    </div>
  );
};

export default MessageItem;
