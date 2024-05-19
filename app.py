from flask import Flask, render_template, request
import re, tempfile, urllib.request
from flask import send_file

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/app.py', methods=['POST'])
def DAPATKAN_TAUTAN_UNDUHAN():
    try:
        tautan_video = request.form['VideoLink']
        post_code = re.search("\/post\/([^\/]+)\/", str(tautan_video)).group(1)
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-US,en;q=0.9',
            'Sec-Fetch-Dest': 'document',
            'Connection': 'keep-alive',
            'Sec-Fetch-Site': 'none',
            'Host': 'www.threads.net',
            'Sec-Fetch-Mode': 'navigate',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        }
        requests = urllib.request.Request(tautan_video, headers=headers)
        response = urllib.request.urlopen(requests)
        video_url = re.search(r'"code":"' + str(post_code) + '","carousel_media":.*?,"image_versions2":.*?,"url":\s*"([^"]*)"}', str(response.read().decode('utf-8'))).group(1).replace('\\', '')
        with tempfile.NamedTemporaryFile(dir='/tmp', suffix='.mp4') as temp_file:
            UNDUH(video_url, temp_file.name, headers)
            return (send_file(temp_file.name, as_attachment=True))
    except (Exception) as e:
        return (f"{type(e).__name__}: {str(e)}")

def UNDUH(video_url, file_path, headers):
    headers.update({
        'Host': 'scontent.cdninstagram.com',
    })
    requests = urllib.request.Request(video_url, headers=headers)
    response = urllib.request.urlopen(requests)
    headers.update({
        'Accept-Encoding': 'identity;q=1, *;q=0',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'no-cors',
        'Accept': '*/*',
        'Range': 'bytes=0-',
        'Referer': response.url,
        'Sec-Fetch-Dest': 'video',
    })
    response2 = urllib.request.urlopen(response.url)
    with open(file_path, 'wb') as w:
        while True:
            chunk = response2.read(1024)
            if not chunk:
                break
            w.write(chunk)
    w.close()

if __name__ == '__main__':
    app.run()