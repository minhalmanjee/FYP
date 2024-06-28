from flask import Flask, jsonify, request, render_template, send_file
from Personalization import extract_caption, process_caption
from Translation import process_video
from flask_cors import CORS
import moviepy.editor as mp
import os

app = Flask('code1000try')
CORS(app)

app.config['DEBUG'] = False

@app.route('/get_chunk', methods=['POST'])
def get_chunk():
    # Check if the request contains the video path
    if 'video_path' not in request.form:
        return jsonify({'error': 'No video path provided'}), 400

    # Get the video path from the request form
    video_path = request.form['video_path']

    # Check if the video file exists
    if not os.path.exists(video_path):
        return jsonify({'error': 'Video file does not exist'}), 400

    # Process the video and get the paths of generated video chunks
    video_chunk_paths = list(process_video(video_path))

    # Concatenate all video chunks into one final video
    final_video_path = "./final_video.mp4"
    video_clips = [mp.VideoFileClip(chunk_path) for chunk_path in video_chunk_paths]
    final_video = mp.concatenate_videoclips(video_clips)
    final_video.write_videofile(final_video_path, codec="libx264")

    # Delete the temporary video file and video chunks
    for chunk_path in video_chunk_paths:
        os.remove(chunk_path)

    # Return the path of the final video as a JSON response
    return jsonify({'final_video_path': final_video_path})


@app.route('/personalization', methods=['POST'])
def personalization():
    
    video_path = request.form['video_path']
    video_text=extract_caption(video_path)
    explanation=process_caption(video_text)
    
    return jsonify({'explanation': explanation})
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
