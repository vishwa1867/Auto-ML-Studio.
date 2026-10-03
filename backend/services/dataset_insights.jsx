import axios from "axios";
import { useState } from "react";

export default function DatasetInsights() {
    const [file, setFile] = useState(null);
    const [message, setMessage] = useState("");

    const uploadFile = async () => {
        if (!file) {
            alert("Please select a file first.");
            return;
        }
        const formData = new FormData();
        formData.append("file", file);

        try {
            const response = await axios.post("http://localhost:5173/api/dataset/insights", formData, {
                headers: {
                    "Content-Type": "multipart/form-data"
                }
            });
            setMessage(response.data.message);
        } catch (error) {
            console.error("Upload failed", error);
            setMessage("Upload failed: " + error.message);
        }
    };

    return (
        <div>
            <h2>Dataset Insights</h2>
            <input type="file" onChange={e => setFile(e.target.files[0])} />
            <button onClick={uploadFile}>Upload</button>
            <p>{message}</p>
        </div>
    );
}
