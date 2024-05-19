try:
    import requests, time, re, sys, os
    from requests.exceptions import TooManyRedirects, RequestException
    from rich.progress import Progress
    from rich.panel import Panel
    from rich.console import Console
    from rich import print as printf
except (Exception) as e:
    exit(f"{str(e).capitalize()}!")

def BANNER():
    os.system('cls' if os.name == 'nt' else 'clear')
    printf(Panel(f"""[bold red]● [bold yellow]● [bold green]●
[bold red]       _____                   _____                 
      /  ___|                 /  ___|                
      \ `--. _ __   __ _ _ __ \ `--.  __ ___   _____ 
       `--. \ '_ \ / _` | '_ \ `--. \/ _` \ \ / / _ \\
      /\__/ / | | | (_| | |_) /\__/ / (_| |\ V /  __/
[bold white]      \____/|_| |_|\__,_| .__/\____/ \__,_| \_/ \___|
                        | | [bold white][[bold green]+[bold white]] Threads Video Downloader
                        |_| [bold white][[bold green]+[bold white]] Coded by Rozhak""", width=65, style="bold dark_goldenrod"))
    return ("0_0")

class MAIN:

    def __init__(self) -> None:
        pass

    def MASUKAN_TAUTAN(self):
        try:
            BANNER()
            printf(Panel(f"[italic white]Silahkan Masukan Tautan Video Yang Ingin Anda Unduh. Anda Bisa Menggunakan \"[italic green],[italic white]\" Untuk Memasukan Banyak Tautan, Misalnya:[italic red] https://www.threads.net/@rozhak_official/post/C7Ef9OXNzSl/", width=65, style="bold dark_goldenrod", title="[bold bold dark_goldenrod]>>> [[bold green]Tautan Unduhan[bold bold dark_goldenrod]] <<<", subtitle="╭──────", subtitle_align="left"))
            self.all_link = Console().input(f"[bold dark_goldenrod]   ╰─> ")
            if len(self.all_link) != 0:
                printf(Panel(f"[italic white]Silahkan Masukan Nama File Untuk Menyimpan Video. Anda Bisa Menekan \"[italic green]Enter[italic white]\" Untuk Penyimpanan Secara Default, Misalnya:[italic red] /sdcard/Download/Hello-World.mp4", width=65, style="bold dark_goldenrod", title="[bold bold dark_goldenrod]>>> [[bold green]Nama File[bold bold dark_goldenrod]] <<<", subtitle="╭──────", subtitle_align="left"))
                self.nama_file = Console().input(f"[bold dark_goldenrod]   ╰─> ")
                printf(Panel(f"[italic white]Program Sedang Mengunduh Video Ini, Pastikan Koneksi Anda Lancar Agar Tidak Terjadi Kesalahan. Anda Juga Bisa Membatalkan Proses Pengunduhan Dengan Menekan[italic red] CTRL + Z[italic white]!", width=65, style="bold dark_goldenrod", title="[bold bold dark_goldenrod]>>> [[bold yellow]Catatan[bold bold dark_goldenrod]] <<<"))
                for url in self.all_link.split(','):
                    self.code = re.search("\/post\/([^\/]+)\/", str(url)).group(1)
                    if len(self.nama_file) == 0:
                        self.final_nama_file = (self.FILE_DEFAULT(self.code))
                    else:
                        self.final_nama_file = (f'{self.nama_file.split(".mp4")[0]}-{int(time.time())}.mp4')
                    self.MENDAPATKAN_TAUTAN_UNDUHAN(url, self.code, self.final_nama_file)
            else:
                printf(Panel(f"[italic red]Maaf, Anda Harus Memasukan Setidaknya Satu Video Tautan Untuk Di Unduh!", width=65, style="bold dark_goldenrod", title="[bold bold dark_goldenrod]>>> [[bold red]Tidak Boleh Kosong[bold bold dark_goldenrod]] <<<"))
                exit()
        except (Exception) as e:
            printf(Panel(f"[italic red]{str(e).title()}!", width=65, style="bold dark_goldenrod", title="[bold bold dark_goldenrod]>>> [[bold red]Error[bold bold dark_goldenrod]] <<<"))
            exit()

    def MENDAPATKAN_TAUTAN_UNDUHAN(self, video_url, code, nama_file):
        with requests.Session() as session:
            session.headers.update({
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                "Accept-Language": "en-US,en;q=0.9",
                "Sec-Fetch-Dest": "document",
                "Connection": "keep-alive",
                "Sec-Fetch-Site": "none",
                "Host": "www.threads.net",
                "Sec-Fetch-Mode": "navigate",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
                "Sec-Fetch-User": "?1",
            })
            response = session.get(video_url)
            self.video_url = str(re.search(r'"code":"' + str(code) + '","carousel_media":.*?,"image_versions2":.*?,"url":\s*"([^"]*)"}', str(response.text)).group(1)).replace('\\', '')
            self.UNDUH(self.video_url, session, nama_file)
        return ("0_0")

    def UNDUH(self, video_url, session, nama_file):
        try:
            if 'Sec-Fetch-User' in dict(session.headers):
                session.headers.pop('Sec-Fetch-User')
            session.headers.update({
                'Host': 'scontent.cdninstagram.com',
            })
            try:
                response = session.get(video_url, allow_redirects = True)
            except (TooManyRedirects):
                response = session.get(video_url, allow_redirects = False)
            session.headers.update({
                "Accept-Encoding": "identity;q=1, *;q=0",
                "Sec-Fetch-Site": "same-origin",
                "Sec-Fetch-Mode": "no-cors",
                "Accept": "*/*",
                "Range": "bytes=0-",
                "Referer": str(response.url),
                "Sec-Fetch-Dest": "video",
            })
            response2 = session.get(response.url, stream = True)
            self.total_size = int(response2.headers.get('Content-Length', 0))
            self.downloaded_size = 0
            with Progress() as progress:
                self.task = progress.add_task("[bold dark_goldenrod]Downloading", total = self.total_size)
                with open(f'{nama_file}', 'wb') as w:
                    for data in response2.iter_content(chunk_size = 1024):
                        w.write(data)
                        self.downloaded_size += len(data)
                        progress.update(self.task, completed = self.downloaded_size)
                w.close()
            self.file_size_mb = str(self.total_size / (1024 * 1024))[:4]
            sys.stdout.write("\033[F")
            time.sleep(1.0)
            printf(Panel(f"""[bold white]Status :[italic green] Successfully...[/]
[bold white]Tersimpan Di:[bold yellow] {nama_file}
[bold white]Ukuran :[bold red] {self.file_size_mb} MB""", width=65, style="bold dark_goldenrod", title="[bold bold dark_goldenrod]>>> [[bold green]Sukses[bold bold dark_goldenrod]] <<<"))
            return ("0_0")
        except (RequestException):
            printf(f"[bold dark_goldenrod]   ──>[bold yellow] Koneksi Anda Terputus!     ", end='\r')
            time.sleep(10.5)
            self.UNDUH(video_url, session, nama_file)

    def FILE_DEFAULT(self, code):
        return (
            f'Penyimpanan/{code}-{int(time.time())}.mp4'
        )

if __name__ == '__main__':
    try:
        if os.path.exists('Penyimpanan') == False:
            os.mkdir('Penyimpanan')
        MAIN().MASUKAN_TAUTAN()
    except (KeyboardInterrupt):
        exit()