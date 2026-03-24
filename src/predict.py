import sys
import joblib
import pandas as pd
from src.extract import extract_features

MODEL_PATH = "model.joblib"
model = joblib.load(MODEL_PATH)

feature_columns = [
    'pdf_size', 'metadata_size', 'pages', 'xref_length', 'title_characters',
    'isEncrypted', 'embedded_files', 'images', 'contains_text',
    'obj', 'endobj', 'stream', 'endstream', 'xref', 'trailer', 'startxref',
    'pageno', 'encrypt', 'ObjStm', 'JS', 'Javascript', 'AA', 'OpenAction',
    'Acroform', 'JBIG2Decode', 'RichMedia', 'launch', 'EmbeddedFile', 'XFA',
    'URI', 'Colors'
]

def predict_pdf(pdf_path):
    df = extract_features(pdf_path)

    df['contains_text'] = df['contains_text'].map({'No': 0, 'Yes': 1})

    df_model = df[feature_columns]

    prediction = model.predict(df_model)
    probability = model.predict_proba(df_model) if hasattr(model, "predict_proba") else None

    print(f"PDF: {pdf_path}")
    print(f"Prediction: {prediction[0]}")
    if probability is not None:
        print(f"Probability: {probability[0]}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python predict.py <pdf_file>")
        sys.exit(1)

    pdf_file = sys.argv[1]
    predict_pdf(pdf_file)