import os
import random
from django.shortcuts import render
import numpy as np
from openpyxl import load_workbook
from .forms import UploadFileForm
from .models import DataFile
import pandas as pd
from rest_framework.decorators import api_view
from rest_framework.response import Response
import dask.dataframe as dd
# from .serializers import DataTypeSerializer
# from typing import Dict, Any


CSV_SIZE_THRESHOLD = 10 * 1024 * 1024

@api_view(['POST'])
def api_infer_data_types(request):
    file = request.FILES['file']
    if not file:
        return Response({"error": "No file uploaded."}, status=400)
    
    data_file = DataFile(file=file)
    data_file.save()

    file_size = os.path.getsize(data_file.file.path)
    
    try:
        # Read the converted DataFrame for preview
        if data_file.file.path.endswith('.csv'):
            if file_size > CSV_SIZE_THRESHOLD:
                df_dask  = dd.read_csv(data_file.file.path, assume_missing=True)

                # Sample size is 10% of the total rows
                total_rows = df_dask.shape[0].compute()
                sample_size = max(1, total_rows // 10)

                # Randomly sample the data
                sampled_indices = sorted(random.sample(range(total_rows), sample_size))
                df_sampled = df_dask.loc[sampled_indices].compute()
                df = df_sampled
            else:
                df = pd.read_csv(data_file.file.path)
        elif data_file.file.path.endswith('.xlsx', '.xls'):
            wb = load_workbook(filename=data_file.file.path, read_only=True, data_only=True)
            ws = wb.active 

            data = ws.values

            if not data:
                return Response({"error": "Excel is empty."}, status=400)

            # Extract headers and data rows
            headers = data[0]
            data_rows = data[1:]

            # Sample size is 10% of the total rows
            sample_size = max(1, len(data_rows) // 10)

            # Randomly sample the data
            sampled_rows = random.sample(data_rows, sample_size) if len(data_rows) >= sample_size else data_rows

            # Create a DataFrame from the sampled data
            df = pd.DataFrame(sampled_rows, columns=headers)
        else:
            return Response({"error": "Unsupported file format."}, status=400)
            
        inferred_types = infer_and_convert_data_types(df)

        data_preview = {
            'data': df.head(100).to_dict(orient='records'),
            'columns': df.columns.tolist(),
            'dtypes': inferred_types
        }

        return Response(data_preview, status=200)

    except Exception as e:
        return Response({"error": str(e)}, status=500)

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            data_file = DataFile(file=request.FILES['file'])
            data_file.save()
            inferred_types = infer_and_convert_data_types(data_file.file.path)
            return render(request, 'data_processor/result.html', {
                'inferred_types': inferred_types
            })
    else:
        form = UploadFileForm()
    return render(request, 'data_processor/upload.html', {'form': form})

def infer_and_convert_data_types(df, tolerance=0.5):

    inferred_types = {} 
    for column in df.columns:
        series = df[column]
        non_na_series = series.dropna()
        total_values = len(non_na_series)

        # Initialize inferred type
        inferred_type = None

        # Attempt to convert to numeric
        numeric_series = pd.to_numeric(non_na_series, errors='coerce')
        num_numeric = numeric_series.notnull().sum()
        print("num",num_numeric)

        if num_numeric / total_values >= tolerance:
            # Further check if integers
            if (numeric_series.dropna() % 1 == 0).all():
                inferred_type = infer_integer_size(numeric_series.dropna().astype(int))
            else:
                inferred_type = 'float64'
        else:
            # Attempt to convert to datetime
            datetime_series = pd.to_datetime(non_na_series, errors='coerce', infer_datetime_format=True)
            num_datetime = datetime_series.notnull().sum()

            if num_datetime / total_values >= tolerance:
                inferred_type = 'datetime64[ns]'
            # Check for boolean-like values
            elif non_na_series.isin([True, False, 'True', 'False', 'true', 'false', 0, 1]).sum() / total_values >= tolerance:
                inferred_type = 'bool'
            # Check for categorical data
            elif non_na_series.nunique() / total_values < 0.5:
                inferred_type = 'category'
            # Default to object
            else:
                inferred_type = 'object'

        inferred_types[column] = inferred_type

    return inferred_types

def infer_integer_size(series):
    min_val = series.min()
    max_val = series.max()
    if np.iinfo(np.int8).min <= min_val <= np.iinfo(np.int8).max and np.iinfo(np.int8).min <= max_val <= np.iinfo(np.int8).max:
        return 'int8'
    elif np.iinfo(np.int16).min <= min_val <= np.iinfo(np.int16).max and np.iinfo(np.int16).min <= max_val <= np.iinfo(np.int16).max:
        return 'int16'
    elif np.iinfo(np.int32).min <= min_val <= np.iinfo(np.int32).max and np.iinfo(np.int32).min <= max_val <= np.iinfo(np.int32).max:
        return 'int32'
    else:
        return 'int64'




