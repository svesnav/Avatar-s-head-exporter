from PIL import Image
import uvicorn
from fastapi import FastAPI, Request, WebSocket
from fastapi.responses import RedirectResponse

port = 23954  # порт, на котором будет запускаться скри
launcher_host = "127.0.0.1"  # Адресс к лаунчеру
skin_path = "updates/skins/"  # Путь до скинов
head_path = "updates/heads/"  # Путь до голов

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
        x, y = img.size
        standard_size = [(8, 8, 16, 16), (40, 8, 48, 16), 128]
        head_coord = []
        helm_coord = []
        for i in standard_size[0]:
            head_coord.append(i * (x // 64))
        for i in standard_size[1]:
            helm_coord.append(i * (x // 64))
        head = img.crop(head_coord)
        helm = img.crop(helm_coord)
        k = standard_size[2] // (x // 64)
        x, y = head.size
        head.paste(helm, (0, 0, x, y), helm)
        new_width = x * k
        new_height = y * k
        resized_head = Image.new('RGBA', (new_width, new_height))
        for i in range(x):
            for j in range(y):
                pixel = head.getpixel((i, j))
                resized_head.paste(pixel, (i * k, j * k, (i + 1) * k, (j + 1) * k))
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
