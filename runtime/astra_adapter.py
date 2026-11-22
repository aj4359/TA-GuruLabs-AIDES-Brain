"""Astra planning adapter for JingWu Media. Disabled unless explicitly enabled."""
import json,os,urllib.request

MODEL=os.getenv("OPENAI_VIDEO_REASONING_MODEL","gpt-6.2-astra")

def create_edit_plan(manifest, *, allow_paid=False):
    """Convert a validated manifest into an edit decision list; NEVER render video."""
    if not (allow_paid and os.getenv("AI_ENABLED","false").lower()=="true"):
        raise RuntimeError("AI disabled: explicit allow_paid and AI_ENABLED=true required")
    if float(os.getenv("AI_MAX_COST_GBP_PER_JOB","0"))<=0:
        raise RuntimeError("API budget not authorised")
    key=os.getenv("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("Server-side OPENAI_API_KEY missing")
    assets=manifest.get("clips",[])
    if not assets or any(not c.get("id") or float(c.get("duration",0))<=0 for c in assets):
        raise ValueError("Manifest requires clips with id and duration")
    # Send metadata only, never founder images, private audio or media paths.
    safe=[{"id":c["id"],"duration":float(c["duration"])} for c in assets]
    prompt=("Return only JSON {\"shots\":[{\"clip_id\":\"id\",\"start\":0,\"end\":5}]}."
        " Create a coherent non-repeating 60-second shot list using only supplied clip IDs,"
        " preserving timing and avoiding invented material. Assets: "+json.dumps(safe)+
        " Brief: "+str(manifest.get("brief",""))[:1500])
    req=urllib.request.Request("https://api.openai.com/v1/responses",
        data=json.dumps({"model":MODEL,"input":prompt,"store":False}).encode(),
        headers={"Authorization":"Bearer "+key,"Content-Type":"application/json"},method="POST")
    with urllib.request.urlopen(req,timeout=120) as response: body=json.load(response)
    raw="".join(c.get("text","") for m in body.get("output",[])
        for c in m.get("content",[]) if c.get("type")=="output_text")
    plan=json.loads(raw)
    permitted={c["id"]:float(c["duration"]) for c in safe}
    if not isinstance(plan.get("shots"),list) or not plan["shots"]: raise ValueError("No shots")
    total=0
    for shot in plan["shots"]:
        clip=shot.get("clip_id")
        if clip not in permitted: raise ValueError("Unknown clip")
        start,end=float(shot["start"]),float(shot["end"])
        if not 0<=start<end<=permitted[clip]+0.02: raise ValueError("Out-of-range trim")
        total+=end-start
    if not 55<=total<=65: raise ValueError("Edit must be close to 60 seconds")
    plan["model"]=MODEL
    return plan

# Adapter has no direct payment limit: project-level OpenAI usage caps must also be configured.
