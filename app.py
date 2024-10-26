from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import json
import subprocess
from datetime import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Ensure necessary directories exist
os.makedirs('exports', exist_ok=True)
os.makedirs('sessions', exist_ok=True)
os.makedirs('uploads', exist_ok=True)
os.makedirs('clips', exist_ok=True)

ALLOWED_EXTENSIONS = {'mp4', 'mov', 'avi', 'mkv'}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/export', methods=['POST'])
def export():
    data = request.json
    tags = data.get('tags', [])
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"tags_{timestamp}.txt"
    filepath = os.path.join('exports', filename)
    with open(filepath, 'w') as f:
        for tag in tags:
            f.write(f"{tag['startTime']} - {tag['endTime']} [{tag['tagType']}] {tag['description']}\n")
    return jsonify({'message': 'Export successful', 'filename': filename})

@app.route('/exports/<filename>')
def download_file(filename):
    return send_from_directory('exports', filename, as_attachment=True)

@app.route('/save_session', methods=['POST'])
def save_session():
    data = request.json
    tags = data.get('tags', [])
    session_name = data.get('sessionName', 'session')
    filepath = os.path.join('sessions', f"{session_name}.json")
    with open(filepath, 'w') as f:
        json.dump(tags, f)
    return jsonify({'message': 'Session saved successfully'})

@app.route('/load_session', methods=['POST'])
def load_session():
    session_name = request.json.get('sessionName', 'session')
    filepath = os.path.join('sessions', f"{session_name}.json")
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            tags = json.load(f)
        return jsonify({'tags': tags})
    else:
        return jsonify({'error': 'Session not found'}), 404

# Endpoint to upload the video file to the server
@app.route('/upload_video', methods=['POST'])
def upload_video():
    print('Received upload request')
    if 'videoFile' not in request.files:
        print('No video file part in request')
        return jsonify({'error': 'No video file provided'}), 400
    file = request.files['videoFile']
    if file.filename == '':
        print('No selected file')
        return jsonify({'error': 'No selected file'}), 400
    if allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join('uploads', filename)
        file.save(filepath)
        print(f'File saved as {filename}')
        return jsonify({'message': 'Video uploaded successfully', 'filename': filename})
    else:
        print('Invalid file type')
        return jsonify({'error': 'Invalid file type'}), 400

# Endpoint to create clips from tags
@app.route('/create_clips', methods=['POST'])
def create_clips():
    data = request.json
    tags = data.get('tags', [])
    video_filename = data.get('videoFilename', '')
    output_name_base = data.get('outputNameBase', 'clip_output')
    if not tags or not video_filename:
        return jsonify({'error': 'Tags or video filename missing'}), 400
    video_filepath = os.path.join('uploads', secure_filename(video_filename))
    if not os.path.exists(video_filepath):
        return jsonify({'error': 'Video file not found on server'}), 404
    clips = []
    for i, tag in enumerate(tags):
        start_time = tag['startTime']
        end_time = tag['endTime']
        # Include original video name and timestamps in the clip filename
        clip_filename = f"{output_name_base}_clip_{i + 1}_{start_time.replace(':', '-')}_to_{end_time.replace(':', '-')}.mp4"
        output_path = os.path.join('clips', clip_filename)
        command = [
            "ffmpeg", "-y", "-i", video_filepath, "-ss", start_time, "-to", end_time,
            "-c", "copy", output_path
        ]
        process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if process.returncode != 0:
            return jsonify({'error': f"Error creating clip {i + 1}: {process.stderr}"}), 500
        clips.append(clip_filename)
    return jsonify({'message': 'Clips created successfully', 'clips': clips})

# Endpoint to concatenate clips
@app.route('/concatenate_clips', methods=['POST'])
def concatenate_clips():
    data = request.json
    clips = data.get('clips', [])
    output_name = data.get('outputName', 'concatenated_output.mp4')
    if not clips:
        return jsonify({'error': 'No clips provided'}), 400
    list_file_path = os.path.join('clips', 'concat_list.txt')
    with open(list_file_path, 'w') as f:
        for clip in clips:
            f.write(f"file '{clip}'\n")
    output_path = os.path.join('clips', output_name)
    command = [
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", list_file_path,
        "-c", "copy", output_path
    ]
    process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if process.returncode != 0:
        return jsonify({'error': f"Error concatenating clips: {process.stderr}"}), 500
    return jsonify({'message': 'Clips concatenated successfully', 'outputFile': output_name})

@app.route('/clips/<filename>')
def download_clip(filename):
    return send_from_directory('clips', filename, as_attachment=True)

# Utility function to check allowed file types
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == '__main__':
    app.run(debug=True)

