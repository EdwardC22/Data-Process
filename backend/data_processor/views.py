# data_processor/views.py

from django.shortcuts import render
from .forms import UploadFileForm
from .models import DataFile
import pandas as pd
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import DataTypeSerializer



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
            data_file.save()
            inferred_types = infer_data_types(data_file.file.path)
            return render(request, 'data_processor/result.html', {
                'inferred_types': inferred_types
            })
    else:
        form = UploadFileForm()
    return render(request, 'data_processor/upload.html', {'form': form})

# data_processor/views.py

def infer_and_convert_data_types(df):
    for col in df.columns:
        # Attempt to convert to numeric first
        df_converted = pd.to_numeric(df[col], errors='coerce')
        if not df_converted.isna().all():  # If at least one value is numeric
            df[col] = df_converted
            continue

        # Attempt to convert to datetime
        try:
            df[col] = pd.to_datetime(df[col], errors='coerce')
            if df[col].notnull().any():
                continue
        except (ValueError, TypeError):
            pass

        # Check if the column should be categorical
        unique_ratio = len(df[col].unique()) / len(df[col])
        if unique_ratio < 0.5:  # Example threshold for categorization
            df[col] = pd.Categorical(df[col])

    return df

def infer_data_types(file_path):
    # Read the file into a Pandas DataFrame
    if file_path.endswith('.csv'):
        df = pd.read_csv(file_path, low_memory=False)
    else:
        df = pd.read_excel(file_path)

    # Use the provided function to infer and convert data types
    df = infer_and_convert_data_types(df)

    # Prepare inferred types dictionary
    inferred_types = {}
    for column in df.columns:
        dtype = df[column].dtype
        inferred_types[column] = str(dtype)

    return inferred_types

