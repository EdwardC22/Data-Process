import React from "react";
import jsPDF from "jspdf";
import html2canvas from "html2canvas";
import { useState } from "react";

function DataDisplay({ data, columns, dtypes, onOverride }) {
  const [hideOverrideType, setHideOverrideType] = useState(false);
  const [selectedType, setSelectedType] = useState("");

  const userFriendlyTypes = {
    object: "Text",
    bool: "Boolean",
    category: "Category",
  };

  const getFriendlyType = (dtype) => {
    dtype = dtype.toLowerCase();

    if (dtype.startsWith("int")) {
      return "Integer";
    } else if (dtype.startsWith("float")) {
      return "Decimal Number";
    } else if (dtype.startsWith("datetime")) {
      return "Date";
    } else {
      return userFriendlyTypes[dtype] || dtype;
    }
  };

  const dataTypesOptions = [
    { value: "object", label: "Text" },
    { value: "int64", label: "Integer" },
    { value: "float64", label: "Decimal Number" },
    { value: "bool", label: "Boolean" },
    { value: "datetime64[ns]", label: "Date" },
    { value: "category", label: "Category" },
  ];

  const handleSaveAsPDF = () => {
    const input = document.getElementById("data-display");

    if (!input) {
      alert("Data display element not found.");
      return;
    }
    setHideOverrideType(true);

    setTimeout(() => {
      html2canvas(input).then((canvas) => {
        const imgData = canvas.toDataURL("image/png");
        const pdf = new jsPDF("p", "mm", "a4");
        const imgProps = pdf.getImageProperties(imgData);
        const pdfWidth = pdf.internal.pageSize.getWidth();
        const pdfHeight = (imgProps.height * pdfWidth) / imgProps.width;

        pdf.addImage(imgData, "PNG", 0, 0, pdfWidth, pdfHeight);
        pdf.save("data_types.pdf");

        setHideOverrideType(false);
      });
    }, 0);
  };

  return (
    <div className="max-w-4xl mx-auto my-8">
      <div id="data-display">
        <h2 className="text-2xl font-bold mb-4">Inferred Data Types</h2>
        <table className="min-w-full bg-white shadow-md rounded">
          <thead>
            <tr>
              <th className="py-2 px-4 border-b">Column</th>
              <th className="py-2 px-4 border-b">Inferred Type</th>
              {!hideOverrideType && (
                <th className="py-2 px-4 border-b">Override Type</th>
              )}
            </tr>
          </thead>
          <tbody>
            {columns.map((col, index) => (
              <tr key={index} className="text-center">
                <td className="border px-4 py-2">{col}</td>
                <td className="border px-4 py-2">
                  {getFriendlyType(dtypes[col])}
                </td>
                {!hideOverrideType && (
                  <td className="border px-4 py-2">
                    <select
                      defaultValue={dtypes[col]}
                      onChange={(e) => setSelectedType(e.target.value)}
                      className="border rounded p-1 mr-4"
                    >
                      {dataTypesOptions.map((option) => (
                        <option key={option.value} value={option.value}>
                          {option.label}
                        </option>
                      ))}
                    </select>
                    <button
                      className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
                      onClick={() => onOverride(col, selectedType)}
                    >
                      Override
                    </button>
                  </td>
                )}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <h2 className="text-2xl font-bold mt-8 mb-4">Data Preview</h2>
      <div className="overflow-x-auto">
        <table className="min-w-full bg-white shadow-md rounded">
          <thead>
            <tr>
              {columns.map((col, index) => (
                <th key={index} className="py-2 px-4 border-b">
                  {col}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {data.map((row, rowIndex) => (
              <tr key={rowIndex} className="text-center">
                {columns.map((col, colIndex) => (
                  <td key={colIndex} className="border px-4 py-2">
                    {row[col] !== null ? row[col].toString() : ""}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <div className="text-center my-4">
        <button
          onClick={handleSaveAsPDF}
          className="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600"
        >
          Save Results as PDF
        </button>
      </div>
    </div>
  );
}

export default DataDisplay;
