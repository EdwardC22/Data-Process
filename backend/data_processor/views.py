import os
from django.conf import settings
from django.shortcuts import render
import numpy as np
from .forms import UploadFileForm
from .models import DataFile
import pandas as pd
from rest_framework.decorators import api_view
from rest_framework.response import Response
# from .serializers import DataTypeSerializer
# from typing import Dict, Any




@api_view(['POST'])
def api_infer_data_types(request):
    file = request.FILES['file']
    data_file = DataFile(file=file)
    data_file.save()
    inferred_types = infer_data_types(data_file.file.path)

    # Read the converted DataFrame for preview
    if data_file.file.path.endswith('.csv'):
        df = pd.read_csv(data_file.file.path)
    else:
        df = pd.read_excel(data_file.file.path)

    data_preview = {
        'data': df.head().to_dict(orient='records'),
        'columns': df.columns.tolist(),
        'dtypes': inferred_types
    }

    return Response(data_preview)

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            data_file = DataFile(file=request.FILES['file'])
            # data_file.save()
            inferred_types = infer_data_types(data_file.file.path)
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

def infer_data_types(file_path):
    # Read the file into a Pandas DataFrame
    if file_path.endswith('.csv'):
        df = pd.read_csv(file_path, low_memory=False)
    else:
        df = pd.read_excel(file_path)

    # Use the provided function to infer and convert data types
    
    inferred_types = infer_and_convert_data_types(df)
    

    # Prepare inferred types dictionary

    return inferred_types


def apply_overrides(df, overrides):
    for col, new_type in overrides.items():
        if new_type == 'int64':
            df[col] = pd.to_numeric(df[col], errors='coerce').astype('Int64')
        elif new_type == 'float64':
            df[col] = pd.to_numeric(df[col], errors='coerce')
        elif new_type == 'bool':
            df[col] = df[col].astype('bool')
        elif new_type == 'datetime64[ns]':
            df[col] = pd.to_datetime(df[col], errors='coerce')
        elif new_type == 'category':
            df[col] = df[col].astype('category')
        elif new_type == 'object':
            df[col] = df[col].astype('object')
    return df


@api_view(['POST'])
def api_apply_overrides(request):
    file_name = request.data.get('file_name')
    overrides = request.data.get('overrides', {})
    file_path = os.path.join(settings.MEDIA_ROOT, 'uploads', file_name)

    # Read the DataFrame
    if file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
    else:
        df = pd.read_excel(file_path)

    # Apply overrides
    df = apply_overrides(df, overrides)

    # Update data types
    inferred_types = {col: str(df[col].dtype) for col in df.columns}

    # Prepare response
    data_preview = {
        'data': df.head().to_dict(orient='records'),
        'columns': df.columns.tolist(),
        'dtypes': inferred_types,
        'file_name': file_name,
    }

    return Response(data_preview)
