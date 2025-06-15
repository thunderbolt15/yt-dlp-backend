from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import subprocess
import json

app = FastAPI()

class VideoRequest(BaseModel):
    url: str

@app.post("/fetch")
async def fetch_video_info(request: VideoRequest):
    try:
        result = subprocess.run(
            ["yt-dlp", "-J", request.url],
            capture_output=True,
            text=True,
            check=True
        )
        data = json.loads(result.stdout)
        return {"status": "success", "data": data}
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail="Error fetching video data")
