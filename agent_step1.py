import os
import subprocess
from moviepy.video.io.VideoFileClip import VideoFileClip


def extract_and_separate_audio(video_path, output_dir="output"):
    """
    Extracts audio from a movie file and splits it into 'vocals' and 'background music'.
    """
    # Create output directories if they do not exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    print("[1/3] Extracting main audio track from movie...")
    # Open the video file
    video = VideoFileClip(video_path)
    audio_path = os.path.join(output_dir, "original_audio.wav")
    
    # Save the audio track as a high-quality WAV file
    video.audio.write_audiofile(audio_path, fps=44100, nbytes=2, codec='pcm_s16le')
    video.close()
    print(f"Success: Audio saved to {audio_path}")
    
    print("[2/3] Running Demucs AI to isolate voices from background noises...")
    # Call Demucs via a system command to split the audio track into two stems: vocals and no_vocals
    command = f"demucs --two-stems=vocals {audio_path} -o {output_dir}"
    subprocess.run(command, shell=True, check=True)
    
    print("[3/3] Audio separation complete!")
    print(f"Your isolated voices file is located in: {output_dir}/htdemucs/original_audio/vocals.wav")

if __name__ == "__main__":
    # The script will look for a video file named 'test_clip.mp4' in your folder
    video_file = "test_clip.mp4"
    
    if os.path.exists(video_file):
        extract_and_separate_audio(video_file)
    else:
        print(f"Error: Please upload or rename a short video clip to '{video_file}' in your workspace folder.")
