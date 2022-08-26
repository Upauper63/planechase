from bs4 import BeautifulSoup
from urllib import request
import json
from PIL import Image

url = 'https://mtg.theuri.net/sim/plane_card.php'
response = request.urlopen(url)
soup = BeautifulSoup(response, "html.parser")
response.close()
items = soup.find_all('tr')
data = []
for item in items:
    name = item.find('h3')
    name = name.text
    name = name.strip()
    name = name.strip('（英語版のみ）')
    print(name)
    dd_elms = item.find_all('dd')
    name_jp = dd_elms[0].text.strip()
    print(name_jp)
    text_jp = ''
    for dd_elm in dd_elms[1:]:
        text_jp += dd_elm.text + "\n"
    text_jp = text_jp.strip()
    print(text_jp)
    data.append({
        'name':name,
        'name_jp':name_jp,
        'text_jp':text_jp
    })

    # 画像保存パート from scryfall
    # APIへアクセスして画像URL取得
    url_sf = 'https://api.scryfall.com/cards/named?fuzzy=' + name.replace(' ', '+')
    req_sf = request.Request(url_sf)
    with request.urlopen(req_sf) as res:
        body_sf = json.load(res)
        url_img = body_sf['image_uris']['large']
        print(url_img)
        # 取得したURLの画像を保存
        with request.urlopen(url_img) as res_img:
            data_img = res_img.read()
            with open('img/' + name.replace(' ', '') + '.jpg', 'wb') as f_img:
                f_img.write(data_img)
            # 画像の向きを制御
            data_img = Image.open('img/' + name.replace(' ', '') + '.jpg')
            data_img = data_img.rotate(-90, expand=True)
            data_img.save('img/' + name.replace(' ', '') + '.jpg')

f = open('planechase.json', 'w')
json.dump(data, f, indent=4, ensure_ascii=False)
f.close()