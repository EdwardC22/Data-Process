# Data-Process

## Project Overview

The **Data Type Inference Project** is designed to provide a user-friendly interface for uploading CSV or Excel files, automatically inferring data types for each column, and allowing users to override these inferred types. Processed data can be saved as a PDF for easy sharing and archiving. To enhance performance, the project leverages Dask for handling large CSV files and OpenPyXL in read-only mode for efficient Excel file reading.

## Technology Stack

- **Backend**:
  - Python
  - Django
  - Django REST Framework
  - Dask
  - OpenPyXL
- **Frontend**:
  - JavaScript
  - React
  - Tailwind CSS
  - html2canvas
  - jsPDF

## Features

1. **File Upload**: Supports uploading CSV and Excel files.
2. **Data Type Inference**: Automatically infers data types for each column (e.g., Integer, Decimal Number, Date, Boolean, Category, Text).
3. **Data Type Override**: Allows users to edit and override inferred data types.
4. **Save as PDF**: Saves processed results as a PDF file, excluding the "Override Type" column.
5. **Large File Handling**:
   - Utilizes Dask to read large CSV files (>10MB) and randomly samples 10% of the data rows for inference.
   - Uses OpenPyXL in read-only mode to efficiently read Excel files without modifying the original files.


## Environment Requirements

- **Backend**:
  - Python 3.8+
  - Django 3.2+
  - Django REST Framework
  - Dask
  - OpenPyXL
- **Frontend**:
  - Node.js 14+
  - npm or yarn
  - React 17+
  - Tailwind CSS

## Project Setup and Running

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/data-type-inference-project.git
cd data-type-inference-project
```

### 2. Create a Virtual Environment
It's recommended to use venv to create a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate  # On Linux/macOS
# or
venv\Scripts\activate  # On Windows
```

### 3. Install Dependencies (backend)

```bash
cd backend
pip install -r requirements.txt
```
### 4. Run Database Migrations and Start Server
```bash
python manage.py migrate
python manage.py runserver
```

### 5. Open a New Terminal to Setup Frontend
```bash
cd frontend
npm install
# or using yarn
yarn install
```
### 6. Start the Frontend Server
```bash
npm start
# or using yarn
yarn start
```


## Additional Notes and Comments

### 1. Large File Handling
1. CSV Files:
        For CSV files larger than 10MB, the backend utilizes Dask to efficiently read and process the data.
        Dask reads the large CSV file and randomly samples 10% of the data rows to perform data type inference, ensuring optimal performance and memory usage.
2. Excel Files:
        Excel files are read using OpenPyXL in read-only mode (read_only=True), ensuring that the original files remain unmodified and are read efficiently.