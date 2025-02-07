import React from "react";

export const Button = ({ children, onClick }) => {
  return (
    <button onClick={onClick} style={{ padding: "10px", backgroundColor: "blue", color: "white", border: "none" }}>
      {children}
    </button>
  );
};