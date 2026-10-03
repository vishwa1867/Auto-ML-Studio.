import axios from "axios";
import { useState } from "react";

export default function DatasetInsights() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);

  const uploadFile = async () => {
    const formData = new FormData();
    formData.append("file", file); // 'file' key must match multer.single('file')

    try {
      const res = await axios.post("http://localhost:5000/api/dataset/insights", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setResult(res.data.result);
    } catch (error) {
      console.error("Upload failed", error);
    }
  };

  return (
    <div>
      <input type="file" onChange={(e) => setFile(e.target.files[0])} />
      <button onClick={uploadFile}>Upload</button>
      <div>{result}</div>
    </div>
  );
}
