import json, subprocess, sys, os
from faster_whisper import WhisperModel
R="/Users/marerobert/OpenMontage/channels/poke-capnv/research/reference-shorts"
m=WhisperModel("base",compute_type="int8")
for vid in sorted(os.listdir(R)):
    d=f"{R}/{vid}"
    if not os.path.isdir(d): continue
    v=f"{d}/video.mp4"
    info=json.load(open(f"{d}/video.info.json"))
    dur=float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",v]).strip())
    ts=[0,0.5,1,2,3]+[max(0,dur-x) for x in (6,4,2,0.5)]
    for i,t in enumerate(ts):
        subprocess.run(["ffmpeg","-y","-v","error","-ss",f"{t:.2f}","-i",v,"-frames:v","1","-vf","scale=360:-2",f"{d}/f{i}_{t:.1f}.jpg"])
    subprocess.run(["ffmpeg","-y","-v","error","-i",v,"-vf","fps=1/5,scale=160:-2,tile=8x3","-frames:v","1",f"{d}/mid.jpg"])
    # montage of key frames
    subprocess.run(["ffmpeg","-y","-v","error"]+sum([["-i",f"{d}/f{i}_{t:.1f}.jpg"] for i,t in enumerate(ts)],[])+["-filter_complex","hstack=inputs=9","-frames:v","1",f"{d}/keys.jpg"])
    import numpy as np
    raw=subprocess.run(["ffmpeg","-v","error","-i",v,"-f","f32le","-ac","1","-ar","16000","-"],capture_output=True).stdout
    segs,_=m.transcribe(np.frombuffer(raw,dtype=np.float32),word_timestamps=True)
    out=[]
    for s in segs:
        out.append(f"[{s.start:.1f}-{s.end:.1f}] {s.text.strip()}")
    open(f"{d}/transcript.txt","w").write("\n".join(out))
    print(vid,info.get("uploader"),info.get("view_count"),round(dur,1),info.get("upload_date"),info.get("title"))
    print("\n".join(out)[:1500]); print()
