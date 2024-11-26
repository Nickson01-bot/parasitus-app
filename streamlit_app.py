import streamlit as st
from PIL import Image

# Streamlit app interface
st.title("Parasitus-AI")
st.write("Upload an image of a parasite, and ask questions about it!")

# File uploader for multiple file types
uploaded_file = st.file_uploader(
    "Upload an image (.png, .jpg, .jpeg)", 
    type=["txt", "md", "png", "jpg", "jpeg"]
)

# Placeholder for user question
question = st.text_area(
    "Ask a question about the uploaded content!",
    placeholder="Can you summarize this document?",
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
        st.write("Note: Text extraction from images is not supported in this version.")
        file_content = "Please provide a description of the image content in your own words."

# Answer questions
if uploaded_file and question and file_content.strip():
    with st.spinner("Generating an answer..."):
        # Simple GPT-based response
        from openai import ChatCompletion

        # Load OpenAI GPT model (replace "your-api-key" with your key)
        openai.api_key = "your-api-key"

        # Compose a prompt
        prompt = f"Here is the uploaded content:\n{file_content}\n\nQuestion: {question}\n\nAnswer:"

        # Call OpenAI's ChatCompletion API
        response = ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": prompt}],
        )
        answer = response["choices"][0]["message"]["content"]

    # Display the answer
    st.write("Answer:")
    st.success(answer)

