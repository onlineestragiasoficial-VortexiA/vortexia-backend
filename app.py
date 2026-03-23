from flask import Flask, request, send_file, render_template
import os, uuid
from moviepy.editor import *
import whisper

app = Flask(__name__)
model = whisper.load_model("base")

for folder in ["uploads", "output_videos"]:
    os.makedirs(folder, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        audio = request.files["audio"]
        format_type = request.form.get("format", "tiktok")

        uid = str(uuid.uuid4())
        audio_path = f"uploads/{uid}.mp3"
        output_path = f"output_videos/{uid}.mp4"
        audio.save(audio_path)

        result = model.transcribe(audio_path)
        segments = result["segments"]

        clips = []
        size = (720, 1280) if format_type=="tiktok" else (1280, 720)

        for seg in segments[:10]:
            text = seg["text"]
            duration = max(seg["end"] - seg["start"], 1.5)

            bg = ColorClip(size, color=(0,0,0)).set_duration(duration)
            txt = TextClip(text.upper(), fontsize=60, color='white',
                           size=size, method='caption').set_position("center").set_duration(duration)
            clip = CompositeVideoClip([bg, txt])
            clips.append(clip)

        video = concatenate_videoclips(clips)
        video = video.set_audio(AudioFileClip(audio_path))
        video.write_videofile(output_path, fps=24)

        return send_file(output_path, as_attachment=True)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
