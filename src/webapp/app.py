from flask import Flask, request, render_template
import io
import joblib
import pandas as pd
from src.extract import extract_features  # hoặc extract_features_full nếu bạn dùng

ALLOWED_EXTENSIONS = {'pdf'}

app = Flask(__name__)

MODEL_PATH = 'model.joblib'
model = joblib.load(MODEL_PATH)

feature_columns = [
    'pdf_size', 'metadata_size', 'pages', 'xref_length', 'title_characters',
    'isEncrypted', 'embedded_files', 'images', 'contains_text',
    'obj', 'endobj', 'stream', 'endstream', 'xref', 'trailer', 'startxref',
    'pageno', 'encrypt', 'ObjStm', 'JS', 'Javascript', 'AA', 'OpenAction',
    'Acroform', 'JBIG2Decode', 'RichMedia', 'launch', 'EmbeddedFile', 'XFA',
    'URI', 'Colors'
]

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    prediction = None
    probability = None

    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file part"
        file = request.files['file']
        if file.filename == '':
            return "No selected file"
        if file and allowed_file(file.filename):
            # Đọc PDF trực tiếp từ memory
            file_bytes = file.read()
            file_stream = io.BytesIO(file_bytes)

            # Extract features (sửa extract_features nhận file-like object)
            df = extract_features(file_stream, name=file.filename)
            
            # Encode contains_text
            df['contains_text'] = df['contains_text'].map({'No': 0, 'Yes': 1})
            df_model = df[feature_columns]

            # Predict
            pred_value = model.predict(df_model)[0]
            if isinstance(pred_value, (int, float)):
                prediction = "Benign" if pred_value == 0 else "Malicious"
            else:
                prediction = pred_value

            # Predict proba
            if hasattr(model, "predict_proba"):
                probability = model.predict_proba(df_model)[0].tolist()
            else:
                probability = None

            return render_template('result.html', filename=file.filename,
                                   prediction=prediction, probability=probability)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)