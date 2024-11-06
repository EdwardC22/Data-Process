
import React, { useState } from "react";
import FileUpload from "./components/FileUpload";
import DataDisplay from "./components/DataDisplay";


function App() {
  const [processedData, setProcessedData] = useState(null);
  const [overrides, setOverrides] = useState({});

  const handleUploadSuccess = (data) => {
    setProcessedData(data);
    setOverrides({});
  };

  const handleOverride = (column, newType) => {
    setOverrides((prevOverrides) => ({
      ...prevOverrides,
      [column]: newType,
    }));
  };

  // const handleSubmitOverrides = () => {
  //   if (!processedData) return;
  //   const payload = {
  //     file_name: processedData.file_name, 
  //     overrides: overrides,
  //   };
  // };



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
            dtypes={{...processedData.dtypes, ...overrides}}
            onOverride={handleOverride}
          />

        </>
      )}
    </div>
  );
}

export default App;
