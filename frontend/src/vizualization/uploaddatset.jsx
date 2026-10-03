import React, { useState } from "react";

function UploadDataset() {
  const [columns, setColumns] = useState([]);
  const [data, setData] = useState([]);

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch("http://127.0.0.1:8000/upload-dataset/", {
      method: "POST",
      body: formData,
    });

    const result = await response.json();
    setColumns(result.columns);
    setData(result.data);
  };

  return (
    <div>
      <h2>Upload Dataset</h2>
      <input type="file" accept=".csv" onChange={handleFileUpload} />

      {data.length > 0 && (
        <div style={{ marginTop: "20px" }}>
          <h3>Preview</h3>
          <table border="1" cellPadding="5">
            <thead>
              <tr>
                {columns.map((col, index) => (
                  <th key={index}>{col}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {data.map((row, rowIndex) => (
                <tr key={rowIndex}>
                  {columns.map((col, colIndex) => (
                    <td key={colIndex}>{row[col]}</td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default UploadDataset;
