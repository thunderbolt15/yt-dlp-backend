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
        import uvicorn

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8000))  # Railway uses this env
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)

