import os
import sys
import pandas as pd
from pdfid import pdfid
import io
import tempfile
import shutil

def extract_features(file, name=None):
    """
    file: str path hoặc file-like object (BytesIO)
    name: optional, tên file (dùng nếu file là BytesIO)
    """
    # --- PDFiD options ---
    options = pdfid.get_fake_options()
    options.scan = True
    options.json = True

    # --- Xử lý file ---
    if isinstance(file, str):
        # Nếu là path bình thường
        data = pdfid.PDFiDMain([file], options=options)
        file_name = os.path.basename(file)
        pdf_size = os.path.getsize(file) / 1024
    elif isinstance(file, io.BytesIO):
        # Nếu là BytesIO (memory)
        # pdfid chỉ nhận path, nên phải tạm lưu trong BytesIO
        # pdfid không hỗ trợ trực tiếp BytesIO
        # Một cách nhanh: lưu tạm file vào temp
        tmp_dir = tempfile.mkdtemp()
        tmp_path = os.path.join(tmp_dir, "temp.pdf")

        try:
            file.seek(0)
            with open(tmp_path, "wb") as f:
                f.write(file.read())

            data = pdfid.PDFiDMain([tmp_path], options=options)
            file_name = name if name else "temp.pdf"
            pdf_size = os.path.getsize(tmp_path) / 1024
        finally:
            shutil.rmtree(tmp_dir) 
    else:
        raise ValueError("file must be path or BytesIO")

    r = data['reports'][0]

    # --- Dataset columns theo eda ---
    feature_columns = [
        'name', 'pdf_size', 'metadata_size', 'pages', 'xref_length', 'title_characters',
        'isEncrypted', 'embedded_files', 'images', 'contains_text', 'header',
        'obj', 'endobj', 'stream', 'endstream', 'xref', 'trailer', 'startxref',
        'pageno', 'encrypt', 'ObjStm', 'JS', 'Javascript', 'AA', 'OpenAction',
        'Acroform', 'JBIG2Decode', 'RichMedia', 'launch', 'EmbeddedFile', 'XFA',
        'URI', 'Colors'
    ]

    features = {}

    # --- Basic ---
    features['name'] = file_name
    features['pdf_size'] = pdf_size

    # --- Mapping from PDFiD ---
    features['pages'] = r.get('/Page', 0)
    features['isEncrypted'] = r.get('/Encrypt', 0)
    features['ObjStm'] = r.get('/ObjStm', 0)
    features['JS'] = r.get('/JS', 0)
    features['Javascript'] = r.get('/JavaScript', 0)
    features['AA'] = r.get('/AA', 0)
    features['OpenAction'] = r.get('/OpenAction', 0)
    features['EmbeddedFile'] = r.get('/EmbeddedFile', 0)

    # --- Structural ---
    features['obj'] = r.get('obj', 0)
    features['endobj'] = r.get('endobj', 0)
    features['stream'] = r.get('stream', 0)
    features['endstream'] = r.get('endstream', 0)
    features['xref'] = r.get('xref', 0)
    features['trailer'] = r.get('trailer', 0)
    features['startxref'] = r.get('startxref', 0)

    # --- Custom ---
    features['contains_text'] = "Yes" if r.get('stream', 0) > 0 else "No"
    features['header'] = r.get('header', '')

    # --- Fill missing dataset columns ---
    default_numeric = 0
    default_string = ''
    for col in feature_columns:
        if col not in features:
            if col in ['contains_text', 'header', 'name']:
                features[col] = default_string
            else:
                features[col] = default_numeric

    df = pd.DataFrame([features])[feature_columns]
    return df

if __name__ == "__main__":
    print(extract_features(sys.argv[1]))