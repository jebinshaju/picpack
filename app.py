import os
import streamlit as st
from zipfile import ZipFile
from PIL import Image
import tempfile

# Function to rename and compress images
def rename_and_compress_images(files, output_folder):
    # Create a temporary directory to store the uploaded files
    temp_dir = tempfile.mkdtemp()
    uploaded_paths = []

    # Save uploaded files to temporary directory
    for file in files:
        if hasattr(file, "type"):  # Streamlit has returned a BytesIO object
            with open(os.path.join(temp_dir, file.name), "wb") as f:
                f.write(file.read())
            uploaded_paths.append(os.path.join(temp_dir, file.name))
        else:  # Streamlit has returned a file object
            with open(os.path.join(temp_dir, file.name), "wb") as f:
                f.write(file.getvalue())
            uploaded_paths.append(os.path.join(temp_dir, file.name))

    # Filter image files
    image_files = [file for file in uploaded_paths if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]

    # Sort image files by modification time
    image_files.sort(key=lambda x: os.path.getmtime(x))

    # Rename and compress images
    for i, image_file in enumerate(image_files):
        img = Image.open(image_file)
        img = img.resize((img.width // 2, img.height // 2))  # Resize image
        compressed_path = os.path.join(output_folder, f"{i+1}.jpg")
        img.save(compressed_path, optimize=True, quality=85)  # Compress image

    # Clean up temporary files
    for file_path in uploaded_paths:
        os.remove(file_path)

# Function to create zip file
def create_zip(folder_path):
    # Create a zip file containing all files in the folder
    with tempfile.NamedTemporaryFile(delete=False) as temp_zip:
        with ZipFile(temp_zip, 'w') as zipf:
            for file in os.listdir(folder_path):
                zipf.write(os.path.join(folder_path, file), arcname=file)
    return temp_zip.name

# Main function
def main():
    st.sidebar.title("PicPack Pro")
    st.sidebar.write("Welcome to PicPack Pro!")
    st.sidebar.write("This app helps you rename and compress your images.")
    st.sidebar.write("Images are renamed numerically in ascending order.")
    st.sidebar.write("Developed by [Jebin Shaju](https://bento.me/jebinshaju)")

    # Link to GitHub repo
    st.sidebar.markdown("[GitHub Repo](https://github.com/jebinshaju/picpack)")

    st.title("📷 Image Renamer, Compressor, and Zipper 📦")

    # Upload files
    uploaded_files = st.file_uploader("Upload images", accept_multiple_files=True)

    if uploaded_files:
        # Display uploaded files
        st.write("Uploaded files:")
        for file in uploaded_files:
            st.write(file.name)

        # Create temporary folder for compressed images
        temp_folder = tempfile.mkdtemp()

        # Rename and compress images
        rename_and_compress_images(uploaded_files, temp_folder)

        # Create zip file
        zip_file_path = create_zip(temp_folder)

        # Provide download link for the zip file
        st.write("Download renamed and compressed files:")
        st.download_button(
            label="Download renamed_files.zip",
            data=open(zip_file_path, 'rb').read(),
            file_name='renamed_files.zip',
            mime='application/zip'
        )

        # Clean up temporary files
        os.remove(zip_file_path)

if __name__ == "__main__":
    main()
