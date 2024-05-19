from flask import Flask, render_template, request
import requests, re, os, tempfile
from flask import send_file
from requests.exceptions import TooManyRedirects

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/app.py', methods=['POST'])
def DAPATKAN_TAUTAN_UNDUHAN():
    with requests.Session() as r:
        try:
            tautan_video = request.form['VideoLink']
            folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Penyimpanan')
            post_code = re.search("\/post\/([^\/]+)\/", str(tautan_video)).group(1)
            r.headers.update({
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'Accept-Language': 'en-US,en;q=0.9',
                'Sec-Fetch-Dest': 'document',
                'Connection': 'keep-alive',
                'Sec-Fetch-Site': 'none',
                'Host': 'www.threads.net',
                'Sec-Fetch-Mode': 'navigate',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
                'Sec-Fetch-User': '?1',
            })
            response = r.get(tautan_video)
            video_url = re.search(r'"code":"' + str(post_code) + '","carousel_media":.*?,"image_versions2":.*?,"url":\s*"([^"]*)"}', str(response.text)).group(1).replace('\\', '')
            with tempfile.NamedTemporaryFile(dir='/tmp', suffix='.mp4') as temp_file:
                UNDUH(r, video_url, temp_file.name)
                return (send_file(temp_file.name, as_attachment=True))
        except (Exception) as e:
            return (f"{type(e).__name__}: {str(e)}")

def UNDUH(r, video_url, file_path):
    if 'Sec-Fetch-User' in dict(r.headers):
        r.headers.pop('Sec-Fetch-User')
    r.headers.update({
        'Host': 'scontent.cdninstagram.com',
    })
    try:
        response = r.get(video_url, allow_redirects = True)
    except (TooManyRedirects):
        response = r.get(video_url, allow_redirects = False)
    r.headers.update({
        'Accept-Encoding': 'identity;q=1, *;q=0',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'no-cors',
        'Accept': '*/*',
        'Range': 'bytes=0-',
        'Referer': response.url,
        'Sec-Fetch-Dest': 'video',
    })
    response2 = r.get(response.url, stream = True)
    with open(file_path, 'wb') as w:
        for chunk in response2.iter_content(chunk_size=1024):
            if chunk:
                w.write(chunk)
    w.close()

if __name__ == '__main__':
    app.run()