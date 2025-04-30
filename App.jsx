import React, { useState } from "react";
import axios from "axios";

function ImageUpload() {
  const [file, setFile] = useState(null);
  const [inputType, setInputType] = useState("image");
  const [resultUrl, setResultUrl] = useState(null);
  const [message, setMessage] = useState("");

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setResultUrl(null);
    setMessage("");
  };

  const handleTypeChange = (e) => {
    setInputType(e.target.value);
    setResultUrl(null);
    setMessage("");
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) return alert("Please upload a file!");

    const formData = new FormData();
    formData.append("file", file);
    formData.append("type", inputType);

    try {
      const response = await axios.post("http://localhost:5000/process", formData);
      setMessage(response.data.message);
      setResultUrl(response.data.result_url);
    } catch (err) {
      alert("Error processing file.");
      console.error(err);
    }
  };

  return (
    <div style={{ padding: 30 }}>
      <h2>Upload {inputType === "image" ? "Image" : "Video"}</h2>
      <form onSubmit={handleSubmit}>
        <select value={inputType} onChange={handleTypeChange}>
          <option value="image">Image</option>
          <option value="video">Video</option>
        </select>
        <br /><br />
        <input type="file" accept={inputType === "image" ? "image/*" : "video/*"} onChange={handleFileChange} />
        <br /><br />
        <button type="submit">Upload and Process</button>
      </form>

      {message && <p>{message}</p>}

      {resultUrl && (
        <div style={{ marginTop: 20 }}>
          <h4>Result:</h4>
          {inputType === "image" ? (
            <img src={resultUrl} alt="Processed Result" style={{ maxWidth: "100%" }} />
          ) : (
            <div>
              <video width="640" height="480" controls autoPlay>
                <source src={resultUrl} type="video/mp4" />
                Your browser does not support the video tag.
              </video>
              {/* Additional text or instructions for video playback */}
              <p>If the video does not load, try reloading the page.</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default ImageUpload;
