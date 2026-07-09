import os
import re
from gtts import gTTS

def srt_time_to_seconds(time_str):
    """Converts standard SRT timestamp (HH:MM:SS,mmm) into pure float seconds."""
    match = re.match(r"(\d+):(\d+):(\d+),(\d+)", time_str)
    if not match:
        return 0.0
    hours, minutes, seconds, milliseconds = map(int, match.groups())
    return (hours * 3600) + (minutes * 60) + seconds + (milliseconds / 1000.0)

def generate_voiceover_pipeline(input_srt_path="output/konkani_movie.srt", output_audio_dir="output/voiceover_clips"):
    """
    Reads the translated subtitle file, loops through blocks, and generates
    standalone audio clips safely using a stable phonetic wrapper.
    """
    print("[1/3] Initializing pure Python TTS storage directory...")
    if not os.path.exists(output_audio_dir):
        os.makedirs(output_audio_dir)

    if not os.path.exists(input_srt_path):
        print(f"Error: Missing subtitle track at {input_srt_path}. Execute Step 3 first!")
        return

    print("[2/3] Processing subtitle blocks into individual speech assets...")
    with open(input_srt_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Split files into individual subtitle blocks
    blocks = content.strip().split("\n\n")
    sync_log_path = os.path.join(output_audio_dir, "sync_map.txt")
    
    with open(sync_log_path, "w", encoding="utf-8") as log:
        for block in blocks:
            lines = block.strip().split("\n")
            if len(lines) < 3:
                continue
            
            clip_index = lines[0].strip()
            timestamp_line = lines[1].strip()
            dialogue_text = " ".join(lines[2:]) 
            
            # Parse time markers (e.g., 00:01:20,500 --> 00:01:23,120)
            times = timestamp_line.split("-->")
            start_sec = srt_time_to_seconds(times[0].strip())
            end_sec = srt_time_to_seconds(times[1].strip())
            max_duration = end_sec - start_sec

            if dialogue_text.strip():
                try:
                    # NOTE: We use 'hi' (Hindi phonetic voice engine) because it reads and pronounces
                    # Devanagari characters out loud beautifully without throwing a library error!
                    tts = gTTS(text=dialogue_text, lang='hi', slow=False)
                    
                    clip_filename = f"clip_{clip_index}.mp3"
                    clip_filepath = os.path.join(output_audio_dir, clip_filename)
                    tts.save(clip_filepath)
                    
                    # Log data: file mapping details for Step 5 mixing
                    log.write(f"{clip_filename}|{start_sec}|{max_duration}\n")
                    print(f"Generated Voice Clip {clip_index}: '{dialogue_text[:20]}...' (Limit: {max_duration:.2f}s)")
                    
                except Exception as e:
                    print(f"Error generating clip {clip_index}: {e}")

    print(f"[3/3] Audio generation complete! Files safely saved in: {output_audio_dir}/")

if __name__ == "__main__":
    generate_voiceover_pipeline()
