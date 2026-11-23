#!/usr/bin/env python3
"""JingWu FilmOS: deterministic full-song still-motion renderer (no paid AI calls).
Private input media stays on the runner; repo stores only the code.
Install: pip install opencv-python-headless pillow numpy; apt install ffmpeg.
Run: python runtime/jingwu_production.py manifest.json output.mp4 --report report.json
"""
import argparse, hashlib, json, math, shutil, subprocess, time
from pathlib import Path
import cv2
import numpy as np
from PIL import Image, ImageOps

def probe(p):
    x = subprocess.run(["ffprobe","-v","error","-show_entries","format=duration",
                        "-of","default=noprint_wrappers=1:nokey=1",str(p)],
                       capture_output=True,text=True,check=True)
    return float(x.stdout.strip())

def checksum(p):
    h=hashlib.sha256()
    with open(p,"rb") as f:
        for block in iter(lambda:f.read(1024*1024),b""): h.update(block)
    return h.hexdigest()

def image_as_bgr(path,w,h):
    im=Image.open(path).convert("RGB")
    im=ImageOps.fit(im,(int(w*1.14),int(h*1.14)),centering=(.5,.5))
    return cv2.cvtColor(np.asarray(im),cv2.COLOR_RGB2BGR)

def move(im,progress,index,w,h):
    p=max(0.,min(1.,progress))
    # 3.5% zoom over entire hold; gentle opposing diagonal drift.
    zoom=1+.035*(p if index%2==0 else 1-p)
    cw=int(w/zoom); ch=int(h/zoom)
    mx=im.shape[1]-cw; my=im.shape[0]-ch
    x=int(mx*(.34+.26*p if index%2==0 else .60-.26*p))
    y=int(my*(.48+.08*p if index%3==0 else .56-.08*p))
    return cv2.resize(im[y:y+ch,x:x+cw],(w,h),interpolation=cv2.INTER_LINEAR)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("manifest"); ap.add_argument("output")
    ap.add_argument("--report",default=None)
    args=ap.parse_args()
    m=json.loads(Path(args.manifest).read_text())
    music=Path(m["music"]).expanduser().resolve()
    if not music.is_file(): raise ValueError("Audio file missing")
    images=[Path(p).expanduser().resolve() for p in m["images"]]
    if len(images)<2 or any(not p.is_file() for p in images): raise ValueError("Need 2+ valid images")
    w,h=int(m.get("width",640)),int(m.get("height",360))
    fps=int(m.get("fps",24))
    if (w,h) not in [(640,360),(854,480),(1280,720)] or fps not in (24,25,30):
        raise ValueError("Unsupported mobile export dimensions/frame rate")
    if not shutil.which("ffmpeg") or not shutil.which("ffprobe"): raise RuntimeError("FFmpeg unavailable")
    duration=probe(music)
    if not 3<=duration<=900: raise ValueError("Music length invalid")
    # Measured, human-reviewed speech end / first beat drop: never guessed by renderer.
    intro=float(m["intro_to_montage_seconds"])
    fade=float(m.get("dissolve_seconds",2.2))
    if not 0<intro<duration-2 or not .4<=fade<=4: raise ValueError("Timing invalid")
    # Constraint: a genuine intro -> first montage dissolve with no hard visual cut.
    # Each timeline image gets one slot; first image is intro, rest are narrative scenes.
    scenes=images[1:]
    remaining=duration-intro
    N=len(scenes)
    slot=(remaining+(N-1)*fade)/N
    step=slot-fade
    if step<=0: raise ValueError("Too many images for duration")
    prep=[image_as_bgr(p,w,h) for p in images]
    output=Path(args.output).resolve();output.parent.mkdir(parents=True,exist_ok=True)
    cmd=["ffmpeg","-hide_banner","-loglevel","error","-y",
         "-f","rawvideo","-pix_fmt","bgr24","-s",f"{w}x{h}","-r",str(fps),"-i","-",
         "-i",str(music),"-map","0:v:0","-map","1:a:0","-t",str(duration),
         "-c:v","libx264","-preset","ultrafast","-crf","25","-pix_fmt","yuv420p",
         "-profile:v","main","-level","3.1","-c:a","aac","-b:a","128k",
         "-movflags","+faststart",str(output)]
    started=time.time(); proc=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    frames=round(duration*fps)
    try:
        for k in range(frames):
            t=k/fps
            if t<intro:
                # Keep narrator on screen THROUGH the final spoken syllable.
                frame=move(prep[0],t/intro,0,w,h)
            else:
                # Start the FIRST dissolve exactly at the approved music entrance.
                t-=intro
                idx=min(N-1,int(t/step))
                local=t-idx*step
                if local<fade:
                    if idx==0:
                        prev=move(prep[0],1,0,w,h)
                    else:
                        prev=move(prep[idx],min(1,(local+step)/slot),idx,w,h)
                    new=move(prep[idx+1],min(1,local/slot),idx+1,w,h)
                    weight=(1-math.cos(math.pi*local/fade))/2
                    frame=cv2.addWeighted(prev,1-weight,new,weight,0)
                else:
                    frame=move(prep[idx+1],min(1,local/slot),idx+1,w,h)
            proc.stdin.write(frame.tobytes())
        proc.stdin.close()
        stderr=proc.stderr.read().decode("utf-8","replace")
        rc=proc.wait()
        if rc: raise RuntimeError("FFmpeg failed: "+stderr[-2000:])
    except BaseException:
        proc.kill()
        raise
    out_duration=probe(output)
    if abs(out_duration-duration)>.15: raise RuntimeError("Duration mismatch")
    decode=subprocess.run(["ffmpeg","-v","error","-i",str(output),"-f","null","-"],capture_output=True,text=True)
    if decode.returncode: raise RuntimeError("Decode error: "+decode.stderr[-1000:])
    report={"status":"RENDERED_TECHNICALLY_VERIFIED_NOT_CREATIVELY_APPROVED",
            "input_audio":str(music),"input_audio_sha256":checksum(music),
            "asset_count":len(images),"seconds":round(out_duration,3),
            "intro_boundary_seconds":intro,"dissolve_seconds":fade,
            "scene_slot_seconds":round(slot,3),"width":w,"height":h,"fps":fps,
            "output":str(output),"output_sha256":checksum(output),
            "output_bytes":output.stat().st_size,"elapsed_seconds":round(time.time()-started,2),
            "next_gate":"Human audio beat alignment, character continuity and founder creative signoff"}
    if args.report: Path(args.report).write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps(report,indent=2))
if __name__=="__main__": main()
