import React, { useState } from "react";
import FileUpload from "./components/FileUpload";
import DataDisplay from "./components/DataDisplay";

function App() {
  const [processedData, setProcessedData] = useState(null);
  const [overrides, setOverrides] = useState({});

  const handleUploadSuccess = (data) => {
    setProcessedData(data);
  };

  const handleOverride = (column, newType) => {
    setOverrides((prevOverrides) => ({
      ...prevOverrides,
      [column]: newType,
    }));
  };

  const handleSubmitOverrides = () => {
    if (!processedData) return;

    const payload = {
      file_name: processedData.file_name, // Assuming the backend sends back the file name
      overrides: overrides,
    };

    fetch("/api/apply_overrides/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    })
      .then((response) => response.json())
      .then((data) => {
        setProcessedData(data);
        alert("Data types have been updated.");
      })
      .catch((error) => {
        console.error("Error:", error);
        alert("An error occurred while applying overrides.");
      });
  };

  return (
    <div className="App">
      <h1 className="text-3xl font-bold text-center my-8">
        Data Type Inference
      </h1>
      {!processedData ? (
        <FileUpload onUploadSuccess={handleUploadSuccess} />
      ) : (
        <>
          <DataDisplay
            data={processedData.data}
            columns={processedData.columns}
            dtypes={processedData.dtypes}
            onOverride={handleOverride}
          />
          <div className="text-center my-4">
            <button
              onClick={handleSubmitOverrides}
              className="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600"
            >
              Submit Overrides
            </button>
          </div>
        </>
      )}
    </div>
  );
}

export default App;
