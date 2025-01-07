import yt_dlp
import os
import sys
import requests
import zipfile
import shutil
from pathlib import Path
import argparse
from tqdm import tqdm
import time

def show_banner():
    """Display the application banner"""
    banner = """
╭──────────────────────────────╮
│    YouTube Video Downloader  │
│        Simple & Efficient    │
╰──────────────────────────────╯
    """
    print(banner)

def download_with_progress(url, output_path):
    """Download a file with progress bar"""
    try:
        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()
        total_size = int(response.headers.get('content-length', 0))
        
        with open(output_path, 'wb') as file, tqdm(
            desc="Downloading FFmpeg",
            total=total_size,
            unit='iB',
            unit_scale=True,
            unit_divisor=1024,
        ) as pbar:
            for data in response.iter_content(chunk_size=8192):
                size = file.write(data)
                pbar.update(size)
    except requests.exceptions.RequestException as e:
        print(f"Download error: {e}")
        raise

def ensure_ffmpeg():
    """Download and set up FFmpeg if not present in the application directory"""
    ffmpeg_dir = Path('ffmpeg')
    ffmpeg_exe = ffmpeg_dir / 'ffmpeg.exe'
    
    if ffmpeg_exe.exists():
        return str(ffmpeg_exe.parent)
    
    print("FFmpeg not found. Setting up...")
    
    ffmpeg_url = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"
    
    try:
        ffmpeg_dir.mkdir(exist_ok=True)
        zip_path = ffmpeg_dir / "ffmpeg.zip"
        
        download_with_progress(ffmpeg_url, zip_path)
        
        print("\nExtracting FFmpeg...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(ffmpeg_dir)
        
        extracted_dir = next(ffmpeg_dir.glob('ffmpeg-master-*'))
        bin_dir = extracted_dir / 'bin'
        
        if not ffmpeg_exe.parent.exists():
            ffmpeg_exe.parent.mkdir(parents=True)
        
        shutil.move(str(bin_dir / 'ffmpeg.exe'), str(ffmpeg_exe))
        
        print("Cleaning up...")
        shutil.rmtree(str(extracted_dir))
        zip_path.unlink()
        
        print("FFmpeg setup completed successfully!")
        return str(ffmpeg_dir)
        
    except Exception as e:
        print(f"Error setting up FFmpeg: {e}")
        return None

def get_video_quality_format(quality):
    """Convert quality argument to yt-dlp format string"""
    quality_formats = {
        'best': 'bestvideo+bestaudio/best',
        '1080p': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]',
        '720p': 'bestvideo[height<=720]+bestaudio/best[height<=720]',
        '480p': 'bestvideo[height<=480]+bestaudio/best[height<=480]',
        'audio': 'bestaudio/best',
    }
    return quality_formats.get(quality, 'bestvideo+bestaudio/best')

def format_bytes(bytes_num):
    """Format bytes into human readable string"""
    if bytes_num is None:
        return "Unknown"
    
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_num < 1024.0:
            return f"{bytes_num:3.1f}{unit}"
        bytes_num /= 1024.0
    return f"{bytes_num:.1f}TB"

def create_progress_hook():
    """Create a progress hook for yt-dlp with better formatting"""
    last_time = [time.time()]
    
    def progress_hook(d):
        if d['status'] == 'downloading':
            current_time = time.time()
            if current_time - last_time[0] > 0.5:  # Update every 0.5 seconds
                last_time[0] = current_time
                
                # Safely get values with fallbacks
                try:
                    if '_total_bytes_str' in d:
                        total = d['_total_bytes_str']
                    elif 'total_bytes_estimate' in d:
                        total = format_bytes(d['total_bytes_estimate'])
                    else:
                        total = 'Unknown'
                        
                    downloaded = format_bytes(d.get('downloaded_bytes', 0))
                    speed = format_bytes(d.get('speed', 0)) + '/s' if d.get('speed') else 'Unknown'
                    eta = d.get('eta', None)
                    eta_str = f'{eta}s' if eta is not None else 'Unknown'
                    
                    # Fragment information
                    frag_index = d.get('fragment_index', 0)
                    frag_count = d.get('fragment_count', 0)
                    frag_str = f'(frag {frag_index}/{frag_count})' if frag_count else ''
                    
                    progress = f"\rDownloading: {downloaded}/{total} at {speed} ETA {eta_str} {frag_str}"
                    print(progress, end='')
                    sys.stdout.flush()
                except Exception as e:
                    # Fallback to simple progress in case of formatting errors
                    print("\rDownloading...", end='')
                    sys.stdout.flush()
    
    return progress_hook

def validate_url(url):
    """Validate if the URL is a supported YouTube URL"""
    return 'youtube.com' in url or 'youtu.be' in url

def download_video(url, path='.', format='mp4', quality='best'):
    """Download video with specified options"""
    if not validate_url(url):
        print("Error: Only YouTube URLs are supported.")
        return
    
    ffmpeg_location = ensure_ffmpeg()
    if not ffmpeg_location:
        print("Failed to set up FFmpeg. Cannot continue.")
        return
    
    # Ensure output directory exists
    output_path = Path(path)
    output_path.mkdir(parents=True, exist_ok=True)
    
    ydl_opts = {
        'outtmpl': str(output_path / '%(title)s.%(ext)s'),
        'format': get_video_quality_format(quality),
        'merge_output_format': format,
        'ffmpeg_location': ffmpeg_location,
        'progress_hooks': [create_progress_hook()],
        'ignoreerrors': True,
        'no_warnings': True,
        'quiet': False,
        'verbose': False,
        'extract_flat': False,
        'fragment_retries': 10,
        'retries': 10,
        'file_access_retries': 5,
        'http_chunk_size': 10485760,  # 10MB per chunk
    }
    
    if quality == 'audio':
        ydl_opts.update({
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        })
    
    try:
        print(f"\nPreparing to download...")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                info = ydl.extract_info(url, download=False)
                if not info:
                    print("Error: Could not fetch video information.")
                    return
                    
                title = info.get('title', 'video')
                duration = info.get('duration', 0)
                
                print(f"Title: {title}")
                if duration:
                    print(f"Duration: {duration // 60}:{duration % 60:02d}")
                print(f"Quality: {quality}")
                print(f"Format: {format}")
                print(f"Output directory: {output_path.absolute()}")
                
                print("\nStarting download...")
                ydl.download([url])
                
                print(f"\n\nDownload completed successfully!")
                print(f"Saved to: {output_path.absolute()}")
            except yt_dlp.utils.DownloadError as e:
                print(f"\nDownload error: {str(e)}")
            except Exception as e:
                print(f"\nAn unexpected error occurred: {str(e)}")
    
    except Exception as e:
        print(f"\nFatal error: {str(e)}")

def main():
    show_banner()
    
    # Check if arguments were passed
    if len(sys.argv) > 1:
        parser = argparse.ArgumentParser(description='Download YouTube videos efficiently.')
        parser.add_argument('url', help='YouTube video URL')
        parser.add_argument('-o', '--output', default='.', 
                           help='Output directory (default: current directory)')
        parser.add_argument('-f', '--format', default='mp4',
                           choices=['mp4', 'mkv', 'webm'],
                           help='Output format (default: mp4)')
        parser.add_argument('-q', '--quality', default='best',
                           choices=['best', '1080p', '720p', '480p', 'audio'],
                           help='Video quality or audio-only (default: best)')
        
        args = parser.parse_args()
        
    else:
        # Interactive mode
        print("\nEnter the following information:")
        while True:
            url = input("YouTube URL: ").strip()
            if validate_url(url):
                break
            print("Error: Please enter a valid YouTube URL.")
        
        output = input("Output directory (press Enter for current directory): ").strip()
        output = output if output else '.'
        
        print("\nAvailable formats: mp4, mkv, webm")
        format = input("Format (press Enter for mp4): ").strip().lower()
        format = format if format in ['mp4', 'mkv', 'webm'] else 'mp4'
        
        print("\nAvailable qualities: best, 1080p, 720p, 480p, audio")
        quality = input("Quality (press Enter for best): ").strip().lower()
        quality = quality if quality in ['best', '1080p', '720p', '480p', 'audio'] else 'best'
        
        class Args:
            pass
        args = Args()
        args.url = url
        args.output = output
        args.format = format
        args.quality = quality
    
    download_video(args.url, args.output, args.format, args.quality)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {str(e)}")
    finally:
        print("\nPress Enter to exit...")
        input()