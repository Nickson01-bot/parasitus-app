import streamlit as st
from langchain.text_splitter import CharacterTextSplitter
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
from PIL import Image
import pytesseract

# Configure pytesseract (ensure you have it installed locally)
pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'  # Update with the Tesseract path on your machine

# Streamlit app interface
st.title("PARASITUS-AI")
st.write("Upload a microscopic image of a malaria parasite and ask questions about it!")

# File uploader for multiple file types
uploaded_file = st.file_uploader(
    "Upload a document (.txt, .md) or an image (.png, .jpg, .jpeg)", 
    type=["txt", "md", "png", "jpg", "jpeg"]
)

# Ask the user for a question
question = st.text_area(
    "Now ask a question about the uploaded content!",
    placeholder="Can you give me a short summary?",
    disabled=not uploaded_file,
)

# Process the uploaded file
file_content = ""

if uploaded_file:
    file_type = uploaded_file.type

    if file_type in ["text/plain", "text/markdown"]:
        # Read and display text file content
        file_content = uploaded_file.read().decode("utf-8")
        st.write("Uploaded Document:")
        st.text_area("Document Content", file_content, height=300)

    elif file_type in ["image/png", "image/jpeg"]:
        # Read and display image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        # Perform OCR to extract text
        st.write("Extracting text from the image...")
        file_content = pytesseract.image_to_string(image)
        st.text_area("Extracted Text", file_content, height=300)

# Answer questions using GPT
if uploaded_file and question and file_content.strip():
    with st.spinner("Analyzing content and generating an answer..."):
        # Load the OpenAI model
        llm = OpenAI(model_name="gpt-4o", temperature=0)
        chain = load_qa_chain(llm)

        # Split the content into chunks
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
        doc_chunks = text_splitter.split_text(file_content)

        # Run the chain to answer the question
        answer = chain.run({"input_documents": doc_chunks, "question": question})

    # Display the answer
    st.write("Answer:")
    st.success(answer)


