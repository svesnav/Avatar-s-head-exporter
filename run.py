from PIL import Image
import uvicorn
from fastapi import FastAPI, Request, WebSocket
from fastapi.responses import RedirectResponse

port = 23954 #порт, на котором будет запускаться скри 
launcher_host = "127.0.0.1" #Адресс к лаунчеру
skin_path = "updates/skins/" #Путь до скинов
head_path = "updates/heads/" #Путь до голов

app = FastAPI()

async def check_head(uuid):
    try:
        open(f"{head_path}/{uuid}.png")
        return True
    except:
        return False
        
async def create_head(uuid):
    try:
        img = Image.open(f"{skin_path}/{uuid}.png").convert("RGBA")
        head = img.crop((8, 8, 16, 16))
        helm = img.crop((40, 8, 48, 16))
        x, y = head.size
        head.paste(helm, (0, 0, x, y), helm)
        conv = head.convert("P")
        resized_head = conv.resize((180, 180), resample=5)
        resized_head.save(f"{head_path}/{uuid}.png")
        return f"http://{launcher_host}/heads/{uuid}.png"
    except:
        return f"http://{launcher_host}/heads/default_head.png"
        
        
@app.get("/head/{uuid}")
async def head(uuid):
    if await check_head(uuid) == True:
        path = f"http://{launcher_host}/heads/{uuid}.png"
        return RedirectResponse(path)
    else:
        path = await create_head(uuid)
        return RedirectResponse(path)
        
       
uvicorn.run(app, host="0.0.0.0", port=port)

