import React from "react";

function DataDisplay({ data, columns, dtypes, onOverride }) {
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

  return (
    <div className="max-w-4xl mx-auto my-8">
      <h2 className="text-2xl font-bold mb-4">Inferred Data Types</h2>
      <table className="min-w-full bg-white shadow-md rounded">
        <thead>
          <tr>
            <th className="py-2 px-4 border-b">Column</th>
            <th className="py-2 px-4 border-b">Inferred Type</th>
            <th className="py-2 px-4 border-b">Override Type</th>
          </tr>
        </thead>
        <tbody>
          {columns.map((col, index) => (
            <tr key={index} className="text-center">
              <td className="border px-4 py-2">{col}</td>
              <td className="border px-4 py-2">
                {getFriendlyType(dtypes[col])}
              </td>
              <td className="border px-4 py-2">
                <select
                  defaultValue={dtypes[col]}
                  onChange={(e) => onOverride(col, e.target.value)}
                  className="border rounded p-1"
                >
                  {dataTypesOptions.map((option) => (
                    <option key={option.value} value={option.value}>
                      {option.label}
                    </option>
                  ))}
                </select>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

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
    </div>
  );
}

export default DataDisplay;
