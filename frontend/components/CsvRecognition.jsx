import { useState } from "react";

export default function CsvRecognition() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);

  const handleUpload = async () => {
    const formData = new FormData();
    formData.append("file", file);

    const res = await fetch("http://localhost:5000/api/csv", {
      method: "POST",
      body: formData,
    });

    const data = await res.json();
    setResult(data);
  };

  return (
    <div style={{ padding: 20 }}>
      <h2>CSV Recognition</h2>
      <input type="file" accept=".csv" onChange={(e) => setFile(e.target.files[0])} />
      <button onClick={handleUpload}>Upload</button>

      {result && (
        <div style={{ marginTop: 20 }}>
          <h3>Entities</h3>
          <p><b>Names:</b> {result.entities.names.join(", ")}</p>
          <p><b>Dates:</b> {result.entities.dates.join(", ")}</p>
          <p><b>Addresses:</b> {result.entities.addresses.join(", ")}</p>

          <h3>Columns</h3>
          <p>{result.columns.join(", ")}</p>

          <h3>Preview</h3>
          <pre>{JSON.stringify(result.preview, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}
