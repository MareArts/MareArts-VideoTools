import yt_dlp
import os
from typing import Optional
import sys
import platform

def format_size(bytes):
    """Convert bytes to human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes < 1024:
            return f"{bytes:.2f} {unit}"
        bytes /= 1024
    return f"{bytes:.2f} TB"

def get_browser_cookie_path():
    """Get the default browser cookie path based on the operating system"""
    system = platform.system()
    if system == "Windows":
        return "chrome"
    elif system == "Darwin":  # macOS
        return "safari"
    else:  # Linux and others
        return "chrome"

def download_video(url: str, output_path: Optional[str] = None, use_cookies: bool = True, browser: Optional[str] = None) -> str:
    """
    Download a YouTube video in the best quality using yt-dlp.
    
    Args:
        url (str): The URL of the YouTube video
        output_path (str, optional): Directory to save the video
        use_cookies (bool): Whether to use browser cookies for authentication
        browser (str, optional): Browser to extract cookies from (chrome, firefox, safari, etc.)
    """
    try:
        if not output_path:
            output_path = os.getcwd()
        
        os.makedirs(output_path, exist_ok=True)
        
        # Configure yt-dlp options for best quality
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',  # Best video + audio quality
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            'merge_output_format': 'mp4',  # Merge to MP4
            'progress_hooks': [lambda d: print(f"\rDownloading: {d['_percent_str']} of {d['_total_bytes_str']}", end="") if d['status'] == 'downloading' else None],
            'postprocessor_hooks': [lambda d: print("\nMerging video and audio...") if d['status'] == 'started' else None],
            'quiet': False,
            'no_warnings': False,
            # Additional options for best quality
            'format_sort': ['res:2160', 'res:1440', 'res:1080', 'res:720'],
            'video_multistreams': True,
            'audio_multistreams': True,
            'prefer_free_formats': True,
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            }],
        }
        
        # Add cookie authentication if enabled
        if use_cookies:
            if not browser:
                browser = get_browser_cookie_path()
            ydl_opts['cookiesfrombrowser'] = (browser,)
            print(f"Using cookies from {browser} for authentication...")
        
        print(f"Fetching video information...")
        
        # Create yt-dlp object and download the video
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Get video info first
            info = ydl.extract_info(url, download=False)
            video_title = info.get('title', 'video')
            duration = info.get('duration')
            formats = info.get('formats', [])
            
            # Find best quality format
            best_video = max(
                (f for f in formats if f.get('vcodec') != 'none'),
                key=lambda f: (
                    f.get('height', 0),
                    f.get('filesize', 0)
                ),
                default=None
            )
            
            # Print video details
            print(f"\nVideo details:")
            print(f"Title: {video_title}")
            print(f"Duration: {duration//60}:{duration%60:02d}")
            if best_video:
                print(f"Best quality available: {best_video.get('height', 'N/A')}p")
                if best_video.get('filesize'):
                    print(f"Approximate size: {format_size(best_video['filesize'])}")
            
            print("\nStarting download in best quality...")
            # Download the video
            ydl.download([url])
            
            # Get the output filename
            output_file = os.path.join(output_path, f"{video_title}.mp4")
            
            print(f"\nDownload completed successfully!")
            print(f"Saved to: {output_file}")
            
            return output_file
            
    except Exception as e:
        print(f"\nError: {str(e)}")
        print("\nTroubleshooting steps:")
        print("1. Check if the video URL is correct")
        print("2. Check your internet connection")
        print("3. Make sure yt-dlp is up to date: pip install -U yt-dlp")
        print("4. Install or update ffmpeg (required for best quality):")
        print("   - On macOS: brew install ffmpeg")
        print("   - On Ubuntu/Debian: sudo apt-get install ffmpeg")
        print("   - On Windows: download from https://ffmpeg.org/download.html")
        print("5. For private videos, make sure:")
        print("   - You're logged into YouTube in your browser")
        print("   - You have access to the private video")
        print("   - The selected browser contains your YouTube login cookies")
        return ""

def main():
    """
    Main function to handle user input for video download.
    """
    print("YouTube Video Downloader (Best Quality)")
    print("-------------------------------------")
    print("This will download videos in the highest available quality")
    print("Note: Higher quality downloads may take longer and use more disk space")
    
    # Parse command line arguments
    import argparse
    parser = argparse.ArgumentParser(description='Download YouTube videos in best quality')
    parser.add_argument('--url', '-u', help='YouTube video URL to download')
    parser.add_argument('--output', '-o', help='Output directory')
    parser.add_argument('--no-cookies', action='store_true', help='Disable browser cookie authentication')
    parser.add_argument('--browser', '-b', choices=['chrome', 'firefox', 'safari', 'edge', 'opera'], 
                        help='Browser to extract cookies from')
    args = parser.parse_args()
    
    if args.url:
        # Run in command line mode
        download_video(args.url, 
                      output_path=args.output, 
                      use_cookies=not args.no_cookies, 
                      browser=args.browser)
        return
    
    # Run in interactive mode
    while True:
        url = input("\nEnter the YouTube video URL (or 'q' to quit): ").strip()
        
        if url.lower() == 'q':
            print("Goodbye!")
            break
            
        if not url:
            print("Please enter a valid URL")
            continue
        
        use_cookies = True
        browser_choice = None
        
        auth_choice = input("Do you need to access a private video? (y/n): ").strip().lower()
        if auth_choice == 'y':
            print("\nSelect your browser for authentication:")
            print("1. Chrome (default)")
            print("2. Firefox")
            print("3. Safari")
            print("4. Edge")
            print("5. Opera")
            print("6. None (no authentication)")
            
            browser_num = input("Enter your choice (1-6): ").strip()
            if browser_num == '6':
                use_cookies = False
            else:
                browsers = {
                    '1': 'chrome',
                    '2': 'firefox',
                    '3': 'safari', 
                    '4': 'edge',
                    '5': 'opera'
                }
                browser_choice = browsers.get(browser_num, 'chrome')
        
        output_dir = input("Enter output directory (press Enter for current directory): ").strip()
        if not output_dir:
            output_dir = None
        
        download_video(url, output_path=output_dir, use_cookies=use_cookies, browser=browser_choice)
        
        choice = input("\nWould you like to download another video? (y/n): ").strip().lower()
        if choice != 'y':
            print("Goodbye!")
            break

if __name__ == "__main__":
    main()


# python convert_video.py input_video.mp4 output_video.mp4