import streamlit as st
from PIL import Image
import openai
import io

# Streamlit app interface
st.title("Parasitus-AI")
st.write("Upload an image of a parasite, and ask questions about it!")

# File uploader for multiple file types
uploaded_file = st.file_uploader(
    "Upload a document (.txt, .md) or an image (.png, .jpg, .jpeg)", 
    type=["txt", "md", "png", "jpg", "jpeg"]
)

# Placeholder for user question
question = st.text_area(
    "Ask a question about the uploaded content!",
    placeholder="Can you summarize this document or describe the image?",
    disabled=not uploaded_file,
)

# Initialize file content
file_content = ""

if uploaded_file:
    file_type = uploaded_file.type

    if file_type in ["text/plain", "text/markdown"]:
        # Process text files
        file_content = uploaded_file.read().decode("utf-8")
        st.write("Uploaded Document:")
        st.text_area("Document Content", file_content, height=300)

    elif file_type in ["image/png", "image/jpeg"]:
        # Process image files
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        # Convert the image to a byte stream for GPT-4 Vision processing
        image_bytes = io.BytesIO()
        image.save(image_bytes, format=image.format)
        image_bytes.seek(0)  # Reset the stream position

# Answer questions
if uploaded_file and question:
    with st.spinner("Generating an answer..."):
        # Load OpenAI GPT-4 Vision model (replace "your-api-key" with your key)
        openai.api_key = "your-api-key"

        if file_type in ["text/plain", "text/markdown"]:
            # Process text files using GPT-4
            prompt = f"Here is the uploaded content:\n{file_content}\n\nQuestion: {question}\n\nAnswer:"
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
            )
            answer = response["choices"][0]["message"]["content"]

        elif file_type in ["image/png", "image/jpeg"]:
            # Use GPT-4 Vision for image analysis
            response = openai.ChatCompletion.create(
                model="gpt-4-vision",
                messages=[{"role": "user", "content": question}],
                files={"image": image_bytes},  # Pass the image bytes
            )
            answer = response["choices"][0]["message"]["content"]

        # Display the answer
        st.write("Answer:")
        st.success(answer)
