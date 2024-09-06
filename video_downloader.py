import yt_dlp as youtube_dl
import argparse
import os

class YouTubeDownloader:
    def __init__(self, url, output_folder):
        self.url = url
        self.output_folder = output_folder

    def download_video(self):
        """
        Downloads a YouTube video using the URL and saves it to the specified output folder with a customized filename.
        """
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': f'{self.output_folder}/%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',  # Convert video to mp4 if necessary
            }]
        }
        try:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(self.url, download=True)
                title = info_dict.get('title', 'downloaded_video')
                filename = f"{title[:50]}.mp4"  # Custom filename
                old_filename = ydl.prepare_filename(info_dict)
                new_filename = os.path.join(self.output_folder, filename)
                os.rename(old_filename, new_filename)
            print(f"Video downloaded successfully and saved as {new_filename}")
        except Exception as e:
            print(f"Failed to download video: {e}")

def main():
    parser = argparse.ArgumentParser(description="Download a video from YouTube with a custom filename.")
    parser.add_argument('--url', type=str, required=True, help='YouTube video URL')
    parser.add_argument('--output_folder', type=str, required=True, help='Output folder to save the video')

    args = parser.parse_args()
    downloader = YouTubeDownloader(args.url, args.output_folder)
    downloader.download_video()

if __name__ == "__main__":
    main()
