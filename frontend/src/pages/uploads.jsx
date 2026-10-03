import React, { useState } from "react";
import axios from "axios";

function UploadCSV() {
  const [file, setFile] = useState(null);
  const [processedData, setProcessedData] = useState(null);
  const [columns, setColumns] = useState([]);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) {
      alert("Please select a CSV file first!");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await axios.post("http://localhost:8000/process-csv/", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      setProcessedData(response.data.processed_data);
      setColumns(response.data.columns);
    } catch (err) {
      console.error("Upload failed:", err);
      alert("Error processing CSV. Check backend logs.");
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h2>Upload CSV for Preprocessing</h2>

      <input type="file" accept=".csv" onChange={handleFileChange} />
      <button onClick={handleUpload} style={{ marginLeft: "10px" }}>
        Process
      </button>

      {processedData && (
        <div style={{ marginTop: "20px" }}>
          <h3>Processed Data (Step 3)</h3>
          <table border="1" cellPadding="5" style={{ borderCollapse: "collapse" }}>
            <thead>
              <tr>
                {columns.map((col, idx) => (
                  <th key={idx}>{col}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {processedData.slice(0, 5).map((row, i) => (
                <tr key={i}>
                  {columns.map((col, j) => (
                    <td key={j}>{row[col]}</td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
          <p>Showing first 5 rows ✅</p>
        </div>
      )}
    </div>
  );
}

export default UploadCSV;
