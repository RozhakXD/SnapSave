try:
    import requests, time, re, sys, os, urllib.parse
    from requests.exceptions import TooManyRedirects
    from rich.progress import Progress
    from rich.console import Console
    from rich.panel import Panel
    from rich import print as Println
    from requests.exceptions import RequestException
except Exception as error:
    exit(f"{str(error).capitalize()}!")

def BANNER() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')
    Println(
        Panel(r"""[bold red]● [bold yellow]● [bold green]●
[bold red]       _____                   _____                 
      /  ___|                 /  ___|                
      \ `--. _ __   __ _ _ __ \ `--.  __ ___   _____ 
       `--. \ '_ \ / _` | '_ \ `--. \/ _` \ \ / / _ \\
      /\__/ / | | | (_| | |_) /\__/ / (_| |\ V /  __/
[bold white]      \____/|_| |_|\__,_| .__/\____/ \__,_| \_/ \___|
                        | | [bold white][[bold green]+[bold white]] Threads Video Downloader
                        |_| [bold white][[bold green]+[bold white]] Coded by Rozhak""", width=65, style="bold dark_goldenrod"
        )
    )
    return

class MAIN:

    def __init__(self) -> None:
        pass

    def MASUKAN_TAUTAN(self) -> None:
        try:
            BANNER()
            Println(Panel(f"[bold white]Silakan Masukkan Tautan Video Yang Ingin Anda Unduh. Anda Bis\na Menggunakan \"[bold green],[bold white]\" Untuk Memasukkan Banyak Tautan, Misalnya:[bold red] https://www.threads.net/@rozhak_official/post/C7Ef9OXNzSl/", width=65, style="bold dark_goldenrod", title="[bold bold dark_goldenrod]>> [[bold green]Tautan Unduhan[bold bold dark_goldenrod]] <<", subtitle="[bold dark_goldenrod]╭──────", subtitle_align="left"))
            self.all_link = Console().input(f"[bold dark_goldenrod]   ╰─> ")
            if len(self.all_link) != 0:
                Println(Panel(f"[bold white]Silakan Masukkan Nama File Untuk Menyimpan Video. Anda Bisa Menekan \"[bold green]Enter[bold white]\" Untuk Folder\nBawaan, Misalnya:[bold red] /sdcard/Download/C7Ef9OXNzSl.mp4", width=65, style="bold dark_goldenrod", title="[bold bold dark_goldenrod]>> [[bold green]Nama File[bold bold dark_goldenrod]] <<", subtitle="[bold dark_goldenrod]╭──────", subtitle_align="left"))
                self.file_name = Console().input(f"[bold dark_goldenrod]   ╰─> ")
                Println(Panel(f"[bold white]Program Sedang Mengunduh Video Ini, Pastikan Koneksi Anda Lancar Agar Tidak Terjadi Kesalahan. Anda Juga Bisa Membatalkan Proses Pengunduhan Dengan Menekan[bold red] CTRL + Z[bold white]!", width=65, style="bold dark_goldenrod", title="[bold bold dark_goldenrod]>> [[bold green]Catatan[bold bold dark_goldenrod]] <<"))
                for media_urls in self.all_link.split(','):
                    media_code = re.search(r"\/post\/([^\/]+)", str(media_urls)).group(1)
                    if len(self.file_name) == 0:
                        self.file_name = self.FILE_DEFAULT(media_code)
                    else:
                        self.file_name = f'{self.file_name.split(".mp4")[0]}-{int(time.time())}.mp4'
                    self.MENDAPATKAN_TAUTAN_UNDUHAN(media_urls, self.file_name)
                exit()
            else:
                Println(Panel(f"[bold red]Maaf, Anda Harus Memasukan Setidaknya Satu Video Tautan Untuk Di Unduh!", width=65, style="bold dark_goldenrod", title="[bold bold dark_goldenrod]>> [[bold red]Tidak Boleh Kosong[bold bold dark_goldenrod]] <<"))
                exit()
        except Exception as error:
            Println(Panel(f"[bold red]{str(error).title()}!", width=65, style="bold dark_goldenrod", title="[bold bold dark_goldenrod]>> [[bold red]Error[bold bold dark_goldenrod]] <<"))
            exit()

    def MENDAPATKAN_TAUTAN_UNDUHAN(self, video_url: str, file_name: str) -> None:
        with requests.Session() as session:
            session.headers.update(
                {
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                    "Accept-Language": "en-US,en;q=0.9",
                    "Sec-Fetch-Dest": "document",
                    "Connection": "keep-alive",
                    "Sec-Fetch-Site": "none",
                    "Host": "www.threads.net",
                    "Sec-Fetch-Mode": "navigate",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
                    "Sec-Fetch-User": "?1",
                }
            )
            response = session.get(video_url, allow_redirects=True, verify=True)

            search_video_url = re.search(r'"video_versions":\[{"type":.*?,"url":"(.*?)"}', response.text).group(1).replace(r"\/", "/")
            decode_escape = search_video_url.encode().decode('unicode_escape')
            end_video_url = urllib.parse.unquote(decode_escape).replace('+', '%2B').replace('==', '%3D%3D')

            self.UNDUH(end_video_url, session, file_name)
        return

    def UNDUH(self, video_url: str, session: requests.Session, file_name: str) -> None:
        try:
            if 'Sec-Fetch-User' in dict(session.headers):
                session.headers.pop('Sec-Fetch-User')
            session.headers.update(
                {
                    'Host': 'scontent.cdninstagram.com',
                }
            )
            try:
                response = session.get(video_url, allow_redirects = True)
            except TooManyRedirects:
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
                with open(f'{file_name}', 'wb') as w:
                    for data in response2.iter_content(chunk_size = 1024):
                        w.write(data)
                        self.downloaded_size += len(data)
                        progress.update(self.task, completed = self.downloaded_size)
                w.close()
            self.file_size_mb = str(self.total_size / (1024 * 1024))[:4]
            sys.stdout.write("\033[F")
            time.sleep(1.0)
            Println(
                Panel(f"""[bold white]Status :[bold green] Successfully...[/]
[bold white]Tersimpan Di:[bold yellow] {file_name}
[bold white]Ukuran :[bold red] {self.file_size_mb} MB""", width=65, style="bold dark_goldenrod", title="[bold bold dark_goldenrod]>> [[bold green]Sukses[bold bold dark_goldenrod]] <<"
                )
            )
            return
        except RequestException:
            Println(f"[bold dark_goldenrod]   ──>[bold yellow] KONEKSI ERROR!     ", end='\r')
            time.sleep(10.5)
            self.UNDUH(video_url, session, file_name)

    def FILE_DEFAULT(self, media_code: str) -> str:
        return f'Temporary/{media_code}.mp4'

if __name__ == '__main__':
    try:
        if os.path.exists('Temporary') == False:
            os.mkdir('Temporary')
        MAIN().MASUKAN_TAUTAN()
    except KeyboardInterrupt:
        exit()