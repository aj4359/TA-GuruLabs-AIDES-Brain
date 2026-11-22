"""FFmpeg backend consuming Astra shot lists, with source IDs instead of arbitrary model paths."""
import json,subprocess,tempfile,shutil
from pathlib import Path

def render(manifest, plan, output):
    clips={}
    for item in manifest["clips"]:
        p=Path(item["path"]).expanduser().resolve()
        if not p.is_file() or item["id"] in clips: raise ValueError("Missing/duplicate clip")
        clips[item["id"]]=(p,float(item["duration"]))
    if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
        raise RuntimeError("ffmpeg and ffprobe are required")
    shots=plan.get("shots",[])
    if not shots: raise ValueError("No shots to render")
    total=0
    for shot in shots:
        ident=shot["clip_id"]
        if ident not in clips: raise ValueError("Unapproved clip ID")
        start,end=float(shot["start"]),float(shot["end"])
        if not 0<=start<end<=clips[ident][1]+0.02: raise ValueError("Invalid trim")
        total+=end-start
    if not 1<=total<=65: raise ValueError("Duration out of bounds")
    output=Path(output).resolve()
    output.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="jingwu_") as folder:
        chunks=[]
        for i,shot in enumerate(shots):
            source=clips[shot["clip_id"]][0]
            target=Path(folder)/f"segment_{i:04}.mp4"
            subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y",
                "-ss",str(shot["start"]),"-i",str(source),
                "-t",str(float(shot["end"])-float(shot["start"])),"-an",
                "-vf","scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,setsar=1",
                "-r","30","-c:v","libx264","-pix_fmt","yuv420p",str(target)],check=True)
            chunks.append(target)
        concat=Path(folder)/"concat.txt"
        concat.write_text("".join("file '"+str(p)+"'\n" for p in chunks))
        silent=Path(folder)/"silent.mp4"
        subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y",
            "-f","concat","-safe","0","-i",str(concat),"-c","copy",str(silent)],check=True)
        music=manifest.get("music")
        if music:
            if not Path(music).is_file(): raise ValueError("Music missing")
            subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y",
                "-i",str(silent),"-i",str(Path(music).resolve()),"-map","0:v:0",
                "-map","1:a:0","-c:v","copy","-c:a","aac","-shortest",str(output)],check=True)
        else: shutil.copy2(silent,output)
    result=subprocess.run(["ffprobe","-v","error","-show_entries","format=duration",
        "-of","default=noprint_wrappers=1:nokey=1",str(output)],
        capture_output=True,text=True,check=True)
    duration=float(result.stdout.strip())
    if duration<1: raise RuntimeError("Unplayable or empty media")
    return {"path":str(output),"seconds":round(duration,2),"ffprobe_pass":True}
