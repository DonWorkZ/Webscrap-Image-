import requests
import sqlite3
from PIL import Image
import PIL
from cloudinary import CloudinaryImage
import cloudinary
import cloudinary.uploader

conn = sqlite3.connect("tokens.db")
curr = conn.cursor()

query = """
CREATE TABLE IF NOT EXISTS token (id INTEGER PRIMARY KEY AUTOINCREMENT, token_id VARCHAR)
"""
curr.execute(query)
conn.commit()


while True:
    url = "https://scriptservice-dot-showtimenft.wl.r.appspot.com/api/v2/collection?limit=150&recache=1&order_by=random&collection=spotlights"
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",
        "Referer": "https://tryshowtime.com/"
    }
    res = requests.get(url, headers=headers)
    data = res.json()
    data = data['data']

    for img in data:
        try:
            curr.execute(f"SELECT * FROM token WHERE token_id={img['token_id']}")
            if len(curr.fetchall()) == 0:
                img_f = requests.get(img['token_img_url'], stream=True)
                with open(f"Image_{img['token_id']}.jpg", 'wb') as f:
                    f.write(img_f.content)

                image = Image.open(f"Image_{img['token_id']}.jpg")
                if image.mode != 'RGB':
                    image = image.convert('RGB')
                if image.size[0] > 1024 and image.size[1] > 1024:

                    img_final = image.resize((1024,1024), PIL.Image.ANTIALIAS)
                    img_final.save(f"Image_{img['token_id']}.jpg")
                else:
                    image.save(f"Image_{img['token_id']}.jpg")
                
                cloudinary.uploader.upload(f"Image_{img['token_id']}.jpg")
                print(img['token_id'])
        except:
            pass
