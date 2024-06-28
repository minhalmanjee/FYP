import streamlit as st
from Translation import process_video
from Personalization import extract_caption,process_caption
import moviepy.editor as mp

# Define website name and video details
website_name = "EdZuban.AI"
video_urls = [
    "./1.mp4",
    "./2.mp4",
    "./3.mp4",
    "./4.mp4",
    "./5.mp4",
    "./6.mp4",  
]

def navigate_to_video_page(video_url):
    st.write(f"Navigating to video page: {video_url}")

# Streamlit app layout
st.set_page_config(page_title=website_name, page_icon=None)
st.sidebar.title("")
st.header(website_name)

# Create columns for video layout
col1, col2, col3 = st.columns(3)  # Adjusted for 3 columns

# Display videos in a grid-like manner
for i, video_url in enumerate(video_urls):
    # Distribute videos across 3 columns
    if i < 2:
        target_col = col1
    elif i < 4:
        target_col = col2
    else:
        target_col = col3
    with target_col:
        st.video(video_url)
        
        if st.button(f"Open Video {i+1}", key=f"video_button_{i}"):
            st.session_state["selected_video_index"] = i  # Store selected video index

# Separate page to display selected video
if "selected_video_index" in st.session_state:
    selected_video_index = st.session_state["selected_video_index"]
    selected_video_url = video_urls[selected_video_index]

    st.subheader(f"Video: {selected_video_url.split('/')[-1]}")  # Display video name
    st.video(selected_video_url)  # Display selected video
    
    explanation_generator=""
    
    if st.button("Personalized Glossary"):
        # Call the process function here
        print(selected_video_url)
        
        caption_generator = extract_caption(selected_video_url)
        st.write(caption_generator)
        explanation_generator = process_caption(caption_generator)
        
    with st.sidebar:
        st.header("Explanation")
        st.write(explanation_generator)
    
    
    # Translate to Urdu button
    if st.button("Translate to Urdu (without Lip Sync)"):
        # Call the process function here
        print(selected_video_url)
            
        video_chunk_paths = list(process_video(selected_video_url))
        final_video_path = "./final_video.mp4"
        video_clips = [mp.VideoFileClip(chunk_path) for chunk_path in video_chunk_paths]
        final_video = mp.concatenate_videoclips(video_clips)
        final_video.write_videofile(final_video_path, codec="libx264")
        st.video(final_video_path, format='mp4')
        
    if st.button("Translate to Urdu (with Lip Sync)"):
        reanimated_video_path="./reanimated_final_video.mp4"
        st.video(reanimated_video_path, format='mp4')
        
        
   