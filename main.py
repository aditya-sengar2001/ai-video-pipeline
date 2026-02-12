from groq import Groq
import edge_tts
import asyncio
import os
import requests
from moviepy.editor import *
from dotenv import load_dotenv

load_dotenv()

os.makedirs("images", exist_ok=True)
os.makedirs("audio", exist_ok=True)
os.makedirs("output", exist_ok=True)

topic = input("Enter topic: ")

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

chat = client.chat.completions.create(
    messages=[{"role":"user","content":f"Write a short motivational YouTube script about {topic}"}],
    model="llama-3.1-8b-instant"
)

script = chat.choices[0].message.content
open("script.txt","w",encoding="utf8").write(script)

print("Script Generated")

async def voice():
    tts = edge_tts.Communicate(script, "en-IN-PrabhatNeural")
    await tts.save("audio/voice.mp3")

asyncio.run(voice())
print("Voice done")

# Download images
headers = {"Authorization": os.getenv("PEXELS_KEY")}
res = requests.get(f"https://api.pexels.com/v1/search?query={topic}&per_page=6", headers=headers)
data = res.json()

imgs = []
for i,p in enumerate(data["photos"]):
    img = requests.get(p["src"]["large"]).content
    path = f"images/{i}.jpg"
    open(path,"wb").write(img)
    imgs.append(path)

audio = AudioFileClip("audio/voice.mp3")

# FIXED timing
per_image = audio.duration / len(imgs)

clips = []
for img in imgs:
    clip = ImageClip(img).resize(height=720).set_duration(per_image)
    clips.append(clip)

video = concatenate_videoclips(clips, method="compose")

final = video.set_audio(audio)

final.write_videofile(
    "output/final.mp4",
    fps=24,
    codec="libx264",
    audio_codec="aac"
)

print("VIDEO READY: output/final.mp4")
