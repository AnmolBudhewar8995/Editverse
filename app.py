import streamlit as st
from rembg import remove
from PIL import Image
import io
import tempfile
import os
import numpy as np
from moviepy import VideoFileClip
from moviepy.video.fx.BlackAndWhite import BlackAndWhite
from moviepy.video.fx.MultiplySpeed import MultiplySpeed
from moviepy.video.fx.MirrorX import MirrorX

# Page setup
st.set_page_config(page_title="AI Studio: Photo & Video Editor", layout="wide")

st.title("🎨 AI Media Studio (Python)")
st.write("Remove image backgrounds and apply video edits with this web-based studio.")

# Create two tabs (image and video)
tab1, tab2 = st.tabs(["🖼️ Image Background Remover", "🎬 Video Editor (Basic)"])

# --- TAB 1: IMAGE BACKGROUND REMOVER ---
with tab1:
    st.header("Remove Background (High Quality)")
    
    # File upload
    uploaded_file = st.file_uploader("Upload your photo (JPG/PNG)", type=['png', 'jpg', 'jpeg'])

    if uploaded_file is not None:
        # Load the image
        image = Image.open(uploaded_file).convert("RGBA")
        image_format = image.format or "PNG"
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Original Photo")
            st.image(image, width="stretch")

        # Background removal process
        with st.spinner('Removing background... Please wait...'):
            try:
                # Convert PIL image to bytes
                img_byte_arr = io.BytesIO()
                image.save(img_byte_arr, format=image_format)
                img_byte_arr = img_byte_arr.getvalue()

                # Remove background via rembg (magic happens here)
                output_bytes = remove(img_byte_arr)
                
                # Convert back to image
                output_image = Image.open(io.BytesIO(output_bytes)).convert("RGBA")

                with col2:
                    st.subheader("Background Removed Photo (Result)")
                    st.image(output_image, width="stretch")
                    alpha_channel = np.array(output_image)[:, :, 3]
                    total_pixels = alpha_channel.size
                    if total_pixels:
                        transparent_pixels = np.sum(alpha_channel == 0)
                        removal_percentage = (transparent_pixels / total_pixels) * 100
                    else:
                        removal_percentage = 0.0
                    st.metric("Background Removed", f"{removal_percentage:.1f}%")
                    
                    # Download button
                    buf = io.BytesIO()
                    output_image.save(buf, format="PNG")
                    byte_im = buf.getvalue()
                    
                    st.download_button(
                        label="Download PNG",
                        data=byte_im,
                        file_name="removed_bg.png",
                        mime="image/png"
                    )
            except Exception as e:
                st.error(f"An error occurred: {e}")

# --- TAB 2: VIDEO EDITOR ---
with tab2:
    st.header("Video Editing (Basic Effects)")
    st.info("Note: Rendering large videos can take some time when running in Python.")

    video_file = st.file_uploader("Upload a video (MP4/MOV)", type=['mp4', 'mov'])

    if video_file is not None:
        # Save temporary file
        tfile = tempfile.NamedTemporaryFile(delete=False)
        tfile.write(video_file.read())
        
        # Display original video
        st.video(tfile.name)

        # Select effect
        effect_choice = st.selectbox(
            "Choose an effect",
            ["None", "Black & White", "2x Speed", "Mirror X"]
        )

        if st.button("Process Video"):
            with st.spinner('Editing video...'):
                try:
                    clip = VideoFileClip(tfile.name)
                    
                    # Apply selected effect
                    if effect_choice == "Black & White":
                        processed_clip = BlackAndWhite().apply(clip)
                    elif effect_choice == "2x Speed":
                        processed_clip = MultiplySpeed(factor=2).apply(clip)
                    elif effect_choice == "Mirror X":
                        processed_clip = MirrorX().apply(clip)
                    else:
                        processed_clip = clip

                    # Output file
                    output_path = os.path.join(tempfile.gettempdir(), "edited_video.mp4")
                    processed_clip.write_videofile(output_path, codec='libx264', audio_codec='aac')

                    # Display processed video
                    st.success("Video edited successfully!")
                    st.video(output_path)

                    # Download button
                    with open(output_path, "rb") as file:
                        btn = st.download_button(
                            label="📥 Download edited video",
                            data=file,
                            file_name="edited_video.mp4",
                            mime="video/mp4"
                        )
                except Exception as e:
                    st.error(f"Video processing error: {e}")