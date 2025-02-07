import React from "react";

export const Card = ({ children }) => {
  return (
    <div style={{ padding: "20px", border: "1px solid #ccc", borderRadius: "5px", marginBottom: "10px" }}>
      {children}
    </div>
  );
};