import React, { useState } from "react";

function FileUpload({ onUploadSuccess }) {
  const [file, setFile] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    if (!file) {
      alert("Please select a file.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    fetch("/api/infer/", {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        onUploadSuccess(data);
      })
      .catch((error) => {
        console.error("Error:", error);
        alert("An error occurred during file upload.");
      });
  };

  return (
    <div className="max-w-md mx-auto my-8">
      <form onSubmit={handleSubmit} className="flex flex-col items-center">
        <input
          type="file"
          onChange={handleFileChange}
          className="mb-4"
          accept=".csv, .xlsx, .xls"
        />
        <button
          type="submit"
          className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
        >
          Upload and Infer Data Types
        </button>
      </form>
    </div>
  );
}

export default FileUpload;
