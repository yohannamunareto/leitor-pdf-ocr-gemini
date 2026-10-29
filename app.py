import os
from io import BytesIO

import fitz  # PyMuPDF
import pytesseract
import requests
import streamlit as st
from dotenv import load_dotenv
from fpdf import FPDF
from pdf2image import convert_from_bytes

load_dotenv()

# Configurações lidas do arquivo .env (nunca coloque chaves no código)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_API_ENDPOINT = os.getenv("GEMINI_API_ENDPOINT", "")
POPPLER_PATH = os.getenv("POPPLER_PATH") or None
if os.getenv("TESSERACT_CMD"):
    pytesseract.pytesseract.tesseract_cmd = os.getenv("TESSERACT_CMD")


def main():
    st.title("Leitura de PDF com OCR e Bate-papo com Gemini")
    uploaded_file = st.file_uploader("Escolha um arquivo PDF", type="pdf")

    if uploaded_file is not None:
        st.write("PDF carregado com sucesso!")
        pdf_bytes = uploaded_file.getvalue()

        if check_pdf_type(pdf_bytes) == "textual":
            text = extract_text_from_pdf(pdf_bytes)
            st.write("Texto extraído do PDF:")
        else:
            st.write("PDF contém imagens de texto digitalizado.")
            st.write("Aplicando OCR para extrair texto...")
            text = pdf_to_text_with_ocr(pdf_bytes)
            st.write("Texto extraído com OCR:")

        st.write(text)
        save_option(text)
        chat_with_gemini(text)


def check_pdf_type(pdf_bytes):
    try:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        for page in doc:
            if page.get_text().strip():
                return "textual"
        return "imagem"
    except Exception:
        return "imagem"


def extract_text_from_pdf(pdf_bytes):
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    return "".join(page.get_text() for page in doc)


def pdf_to_text_with_ocr(pdf_bytes):
    pages = convert_from_bytes(pdf_bytes, 300, poppler_path=POPPLER_PATH)
    text = ""
    progress_bar = st.progress(0)
    status_text = st.empty()
    total = len(pages)

    for i, page in enumerate(pages):
        text += pytesseract.image_to_string(page, config=r"--oem 3 --psm 6")
        progress_bar.progress((i + 1) / total)
        status_text.text(f"Processando OCR na página {i + 1} de {total}...")

    status_text.text("Processamento concluído!")
    return text


def save_option(text):
    st.write("Opções de salvamento:")
    st.download_button("Download TXT", data=text.encode("utf-8"),
                       file_name="output.txt", mime="text/plain")
    st.download_button("Download PDF", data=text_to_pdf(text),
                       file_name="output.pdf", mime="application/pdf")


def text_to_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    for line in text.split("\n"):
        line = line.encode("latin-1", "replace").decode("latin-1")
        pdf.multi_cell(0, 10, line)
    return BytesIO(pdf.output(dest="S").encode("latin1"))


def ask_gemini(text, question):
    if not GEMINI_API_KEY or not GEMINI_API_ENDPOINT:
        return "Configure GEMINI_API_KEY e GEMINI_API_ENDPOINT no arquivo .env."
    payload = {"text": text, "question": question}
    headers = {"Authorization": f"Bearer {GEMINI_API_KEY}",
               "Content-Type": "application/json"}
    try:
        response = requests.post(GEMINI_API_ENDPOINT, json=payload, headers=headers, timeout=60)
        response.raise_for_status()
        return response.json().get("answer", "Sem resposta.")
    except requests.exceptions.RequestException as e:
        return f"Erro ao comunicar com a API do Gemini: {e}"


def chat_with_gemini(text):
    st.write("Faça uma pergunta sobre o texto:")
    question = st.text_input("Digite sua pergunta:")
    if st.button("Perguntar ao Gemini") and question:
        st.write("Resposta do Gemini:")
        st.write(ask_gemini(text, question))


if __name__ == "__main__":
    main()
