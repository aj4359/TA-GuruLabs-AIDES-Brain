"""Smoke test: render a complete playable JingWu video from local synthetic assets, with no user files or paid AI calls."""
import json, subprocess, sys, tempfile
from pathlib import Path
from PIL import Image, ImageDraw

def main():
    root=Path(__file__).resolve().parents[1]
    with tempfile.TemporaryDirectory() as tmp:
        d=Path(tmp)
        images=[]
        for i,color in enumerate(["#181c2c","#43282d","#1b3041","#3a3641"]):
            p=d/f"shot{i}.jpg"
            im=Image.new("RGB",(960,540),color)
            draw=ImageDraw.Draw(im)
            draw.text((40,40),f"SYNTHETIC SHOT {i} - TEST ONLY",fill="white")
            im.save(p)
            images.append(str(p))
        audio=d/"sound.wav"
        subprocess.run(["ffmpeg","-y","-v","error","-f","lavfi","-i",
                        "sine=frequency=440:sample_rate=44100:duration=18",
                        "-c:a","pcm_s16le",str(audio)],check=True)
        manifest=d/"manifest.json"
        manifest.write_text(json.dumps({"music":str(audio),"images":images,
          "intro_to_montage_seconds":4.0,"dissolve_seconds":1.7,
          "width":640,"height":360,"fps":24}))
        video=d/"render.mp4"; report=d/"report.json"
        subprocess.run([sys.executable,str(root/"runtime/jingwu_production.py"),
                        str(manifest),str(video),"--report",str(report)],
                       check=True,timeout=150)
        data=json.loads(report.read_text())
        assert video.exists() and video.stat().st_size>30000
        assert data["status"]=="RENDERED_TECHNICALLY_VERIFIED_NOT_CREATIVELY_APPROVED"
        assert 17.8<data["seconds"]<18.2
        assert data["intro_boundary_seconds"]==4.0
        print("JINGWU END-TO-END SMOKE TEST PASSED",video.stat().st_size)
if __name__=="__main__": main()
