# Leitor de PDF com OCR e chat com IA

Minha primeira automação: uma interface web que transforma PDFs digitalizados em texto e permite fazer perguntas sobre o documento ao Gemini.


## Problema

Muitos processos chegam em PDF não editável ou com páginas escaneadas. Sem texto, não dá para pesquisar no documento nem usar IA sobre ele.

## Como funciona

- A pessoa sobe o PDF numa interface em Streamlit.
- O sistema verifica se o arquivo já tem texto. Se tiver, extrai direto. Se for digitalizado, converte cada página em imagem de 300 dpi e aplica OCR com Tesseract.
- Barra de progresso página por página.
- O texto pode ser baixado em TXT ou PDF.
- Campo de perguntas para conversar com o Gemini sobre o conteúdo.

## Como rodar

1. Instale o [Tesseract](https://github.com/tesseract-ocr/tesseract) e o [Poppler](https://poppler.freedesktop.org/).
2. Instale as dependências: `pip install -r requirements.txt`
3. Copie `.env.example` para `.env` e preencha suas configurações.
4. Rode: `streamlit run app.py`

## Ferramentas

Python, Streamlit, PyMuPDF, pdf2image, Tesseract (pytesseract), FPDF e API do Gemini.

## Resultados

- Primeiro passo para usar IA sobre os processos do escritório.
- Foi a base do [conversor de PDF para Markdown](https://github.com/yohannamunareto/pdf-para-markdown-ocr), que evoluiu para documentos de milhares de páginas.
