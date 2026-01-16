"""
Robot Image Downloader using Google Custom Search API

Downloads images of robots from specified manufacturers, prioritizing
images from the manufacturer's own website when possible.

Setup:
1. Get API key: https://console.cloud.google.com/apis/credentials
2. Create Custom Search Engine: https://programmablesearchengine.google.com/
   - Enable "Image search" in settings
   - Enable "Search the entire web"
3. Enable Custom Search API in Google Cloud Console

Usage:
    python robot_image_downloader.py robots.csv ./robot_images --api-key YOUR_KEY --cx YOUR_CX

CSV Format:
    manufacturer,manufacturer_url,robots
    Boston Dynamics,bostondynamics.com,"SPOT, Atlas, Stretch"
    Dusty Robotics,dustyrobotics.com,FieldPrinter
    Built Robotics,builtrobotics.com,"ExoTrack, RPD 35"
"""

import csv
import requests
import os
import sys
import time
import argparse
import json
import re
import glob
from urllib.parse import urlparse, quote_plus
from pathlib import Path
from dotenv import load_dotenv


class GoogleImageSearch:
    """Google Custom Search API client for image searches."""
    
    BASE_URL = "https://www.googleapis.com/customsearch/v1"
    
    def __init__(self, api_key: str, cx: str):
        self.api_key = api_key
        self.cx = cx
    
    def search(self, query: str, site_restrict: str = None, num_results: int = 5) -> list:
        """
        Search for images using Google Custom Search API.
        
        Args:
            query: Search query string
            site_restrict: Optional domain to restrict search to (e.g., 'bostondynamics.com')
            num_results: Number of results to return (max 10 per request)
        
        Returns:
            List of image result dicts with 'url', 'title', 'source', 'thumbnail'
        """
        params = {
            'key': self.api_key,
            'cx': self.cx,
            'q': query,
            'searchType': 'image',
            'num': min(num_results, 10),  # API max is 10
        }
        
        # Optionally restrict to a specific site
        if site_restrict:
            params['siteSearch'] = site_restrict
            params['siteSearchFilter'] = 'i'  # 'i' = include only this site
        
        try:
            response = requests.get(self.BASE_URL, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()
            
            results = []
            for item in data.get('items', []):
                results.append({
                    'url': item.get('link'),
                    'title': item.get('title'),
                    'source': item.get('displayLink'),
                    'thumbnail': item.get('image', {}).get('thumbnailLink'),
                    'width': item.get('image', {}).get('width'),
                    'height': item.get('image', {}).get('height'),
                    'context_url': item.get('image', {}).get('contextLink'),
                })
            
            return results
        
        except requests.exceptions.RequestException as e:
            print(f"    API Error: {e}")
            return []


def download_image(url: str, filepath: str, timeout: int = 15) -> dict:
    """
    Download an image from a URL.
    
    Returns:
        dict with 'success', 'filepath', 'size_kb', 'error'
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=timeout, stream=True)
        response.raise_for_status()
        
        # Verify it's actually an image
        content_type = response.headers.get('content-type', '').lower()
        if not any(img_type in content_type for img_type in ['image/', 'octet-stream']):
            return {'success': False, 'error': f'Not an image: {content_type}'}
        
        # Determine file extension from content-type or URL
        ext = '.jpg'  # default
        if 'png' in content_type or url.lower().endswith('.png'):
            ext = '.png'
        elif 'gif' in content_type or url.lower().endswith('.gif'):
            ext = '.gif'
        elif 'webp' in content_type or url.lower().endswith('.webp'):
            ext = '.webp'
        elif 'svg' in content_type or url.lower().endswith('.svg'):
            ext = '.svg'
        
        # Add extension if not present
        if not any(filepath.lower().endswith(e) for e in ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg']):
            filepath = filepath + ext
        
        # Download and save
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        size_kb = os.path.getsize(filepath) / 1024
        
        # Verify file isn't too small (probably an error page)
        if size_kb < 1:
            os.remove(filepath)
            return {'success': False, 'error': 'File too small (likely error page)'}
        
        return {
            'success': True,
            'filepath': filepath,
            'size_kb': size_kb
        }
    
    except requests.exceptions.RequestException as e:
        return {'success': False, 'error': str(e)}
    except IOError as e:
        return {'success': False, 'error': f'File write error: {e}'}


def sanitize_filename(name: str) -> str:
    """Convert a string to a safe filename."""
    # Replace problematic characters
    safe = re.sub(r'[<>:"/\\|?*]', '_', name)
    safe = re.sub(r'\s+', '_', safe)
    safe = re.sub(r'_+', '_', safe)
    return safe.strip('_')


def parse_robots(robots_str: str) -> list:
    """Parse comma-separated robot names, handling quoted strings."""
    robots_str = robots_str.strip().strip('"\'')
    
    # Split by comma, but handle potential whitespace
    robots = [r.strip() for r in robots_str.split(',')]
    
    # Filter out empty strings
    return [r for r in robots if r]


def extract_domain(url: str) -> str:
    """Extract clean domain from URL."""
    url = url.strip()
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    parsed = urlparse(url)
    domain = parsed.netloc or parsed.path
    
    if domain.startswith('www.'):
        domain = domain[4:]
    
    return domain.split('/')[0]


def check_existing_images(output_dir: str, robot_name: str, manufacturer_name: str = None) -> bool:
    """
    Check if robot already has images in output directory.

    Args:
        output_dir: Base directory to search
        robot_name: Name of the robot to check
        manufacturer_name: Optional manufacturer folder name

    Returns:
        True if images exist for this robot, False otherwise
    """
    safe_name = sanitize_filename(robot_name)

    # Check in manufacturer folder if provided
    if manufacturer_name:
        manuf_folder = os.path.join(output_dir, sanitize_filename(manufacturer_name))
        pattern = os.path.join(manuf_folder, f"{safe_name}_*.*")
        existing = glob.glob(pattern)
        if existing:
            return True

    # Also check recursively in output dir
    pattern = os.path.join(output_dir, '**', f"{safe_name}_*.*")
    existing = glob.glob(pattern, recursive=True)
    return len(existing) > 0


def process_csv(
    csv_path: str,
    output_dir: str,
    api_key: str,
    cx: str,
    images_per_robot: int = 3,
    manufacturer_col: str = None,
    url_col: str = None,
    robots_col: str = None,
    skip_site_search: bool = False,
    skip_existing: bool = False
):
    """
    Process CSV and download robot images.

    Args:
        csv_path: Path to input CSV
        output_dir: Base directory for downloaded images
        api_key: Google API key
        cx: Google Custom Search Engine ID
        images_per_robot: Number of images to download per robot
        manufacturer_col: Column name for manufacturer (auto-detect if None)
        url_col: Column name for manufacturer URL (auto-detect if None)
        robots_col: Column name for robots (auto-detect if None)
        skip_site_search: If True, skip manufacturer site search and go straight to web search
        skip_existing: If True, skip robots that already have images in output directory
    """
    searcher = GoogleImageSearch(api_key, cx)
    
    # Create base output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Track results
    results = {
        'downloaded': [],
        'failed': []
    }
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames
        
        # Auto-detect columns
        if not manufacturer_col:
            for h in headers:
                if any(x in h.lower() for x in ['manufacturer', 'company', 'maker', 'brand']):
                    manufacturer_col = h
                    break
            manufacturer_col = manufacturer_col or headers[0]
        
        if not url_col:
            for h in headers:
                if any(x in h.lower() for x in ['url', 'website', 'site', 'domain']):
                    url_col = h
                    break
        
        if not robots_col:
            for h in headers:
                if any(x in h.lower() for x in ['robot', 'product', 'model', 'equipment']):
                    robots_col = h
                    break
            robots_col = robots_col or headers[-1]
        
        print(f"Columns detected:")
        print(f"  Manufacturer: '{manufacturer_col}'")
        print(f"  URL: '{url_col}'")
        print(f"  Robots: '{robots_col}'")
        print("-" * 60)
        
        for row in reader:
            manufacturer = row.get(manufacturer_col, '').strip()
            manuf_url = row.get(url_col, '').strip() if url_col else ''
            robots_raw = row.get(robots_col, '').strip()
            
            if not manufacturer or not robots_raw:
                continue
            
            robots = parse_robots(robots_raw)
            domain = extract_domain(manuf_url) if manuf_url else None
            
            # Create manufacturer folder
            manuf_folder = os.path.join(output_dir, sanitize_filename(manufacturer))
            os.makedirs(manuf_folder, exist_ok=True)
            
            print(f"\n{'='*60}")
            print(f"MANUFACTURER: {manufacturer}")
            if domain:
                print(f"WEBSITE: {domain}")
            print(f"ROBOTS: {', '.join(robots)}")
            print('='*60)
            
            for robot in robots:
                print(f"\n  [{robot}]")

                # Skip if images already exist for this robot
                if skip_existing and check_existing_images(output_dir, robot, manufacturer):
                    print(f"    [SKIP] Already has images")
                    continue

                images_downloaded = 0
                search_query = f"{manufacturer} {robot} robot"
                
                # Strategy 1: Search manufacturer's site first (if URL provided)
                if domain and not skip_site_search:
                    print(f"    Searching {domain}...", end=' ')
                    site_results = searcher.search(
                        query=f"{robot}",
                        site_restrict=domain,
                        num_results=images_per_robot
                    )
                    print(f"found {len(site_results)} results")
                    
                    for i, result in enumerate(site_results):
                        if images_downloaded >= images_per_robot:
                            break
                        
                        filename = f"{sanitize_filename(robot)}_{images_downloaded + 1}_official"
                        filepath = os.path.join(manuf_folder, filename)
                        
                        dl_result = download_image(result['url'], filepath)
                        
                        if dl_result['success']:
                            images_downloaded += 1
                            print(f"    [OK] Downloaded: {os.path.basename(dl_result['filepath'])} ({dl_result['size_kb']:.1f} KB)")
                            results['downloaded'].append({
                                'manufacturer': manufacturer,
                                'robot': robot,
                                'source': 'manufacturer_site',
                                'filepath': dl_result['filepath'],
                                'url': result['url']
                            })
                        
                        time.sleep(0.3)
                
                # Strategy 2: Search entire web for remaining needed images
                if images_downloaded < images_per_robot:
                    remaining = images_per_robot - images_downloaded
                    print(f"    Searching web for {remaining} more...", end=' ')
                    
                    web_results = searcher.search(
                        query=search_query,
                        num_results=remaining + 3  # Get extras in case some fail
                    )
                    print(f"found {len(web_results)} results")
                    
                    for result in web_results:
                        if images_downloaded >= images_per_robot:
                            break
                        
                        # Skip if we already have from this URL
                        filename = f"{sanitize_filename(robot)}_{images_downloaded + 1}_web"
                        filepath = os.path.join(manuf_folder, filename)
                        
                        dl_result = download_image(result['url'], filepath)
                        
                        if dl_result['success']:
                            images_downloaded += 1
                            print(f"    [OK] Downloaded: {os.path.basename(dl_result['filepath'])} ({dl_result['size_kb']:.1f} KB) from {result['source']}")
                            results['downloaded'].append({
                                'manufacturer': manufacturer,
                                'robot': robot,
                                'source': 'web_search',
                                'filepath': dl_result['filepath'],
                                'url': result['url']
                            })
                        
                        time.sleep(0.3)
                
                if images_downloaded == 0:
                    print(f"    [FAIL] No images found for {robot}")
                    results['failed'].append({
                        'manufacturer': manufacturer,
                        'robot': robot,
                        'reason': 'No downloadable images found'
                    })
                elif images_downloaded < images_per_robot:
                    print(f"    [WARN] Only found {images_downloaded}/{images_per_robot} images")
                
                # Rate limit between robots
                time.sleep(0.5)
    
    return results


def print_summary(results: dict, output_dir: str):
    """Print download summary."""
    print("\n" + "=" * 60)
    print("DOWNLOAD SUMMARY")
    print("=" * 60)
    print(f"Total images downloaded: {len(results['downloaded'])}")
    print(f"Failed robots: {len(results['failed'])}")
    print(f"Output directory: {output_dir}")
    
    if results['failed']:
        print("\nFailed:")
        for fail in results['failed']:
            print(f"  - {fail['manufacturer']} {fail['robot']}: {fail['reason']}")
    
    # Summary by manufacturer
    from collections import defaultdict
    by_manuf = defaultdict(list)
    for dl in results['downloaded']:
        by_manuf[dl['manufacturer']].append(dl['robot'])
    
    print("\nBy manufacturer:")
    for manuf, robots in sorted(by_manuf.items()):
        print(f"  {manuf}: {len(robots)} images")


def create_sample_csv(path: str):
    """Create a sample CSV file for reference."""
    sample_data = [
        ['manufacturer', 'manufacturer_url', 'robots'],
        ['Boston Dynamics', 'bostondynamics.com', 'SPOT, Atlas, Stretch'],
        ['Dusty Robotics', 'dustyrobotics.com', 'FieldPrinter'],
        ['Built Robotics', 'builtrobotics.com', 'ExoTrack, RPD 35'],
        ['Canvas Construction', 'canvas.build', 'Canvas'],
        ['Hilti', 'hilti.com', 'Jaibot'],
        ['Trimble', 'trimble.com', 'X7 Scanner'],
        ['Sarcos', 'sarcos.com', 'Guardian XO, Guardian XT'],
        ['ANYbotics', 'anybotics.com', 'ANYmal'],
    ]
    
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(sample_data)
    
    print(f"Sample CSV created: {path}")


def main():
    # Load environment variables from .env file if it exists
    load_dotenv()

    parser = argparse.ArgumentParser(
        description='Download robot images using Google Custom Search API',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s robots.csv ./images --api-key YOUR_KEY --cx YOUR_CX
  %(prog)s robots.csv ./images --api-key YOUR_KEY --cx YOUR_CX --num 5
  %(prog)s --create-sample sample_robots.csv

CSV Format:
  manufacturer,manufacturer_url,robots
  Boston Dynamics,bostondynamics.com,"SPOT, Atlas, Stretch"
        """
    )
    
    parser.add_argument('csv_path', nargs='?', help='Path to input CSV file')
    parser.add_argument('output_dir', nargs='?', default='./robot_images', help='Output directory for images')
    parser.add_argument('--api-key', required=False, help='Google API key')
    parser.add_argument('--cx', required=False, help='Google Custom Search Engine ID')
    parser.add_argument('--num', type=int, default=3, help='Number of images per robot (default: 3)')
    parser.add_argument('--skip-site-search', action='store_true', help='Skip manufacturer site search')
    parser.add_argument('--skip-existing', action='store_true', help='Skip robots that already have images downloaded')
    parser.add_argument('--create-sample', metavar='PATH', help='Create a sample CSV file')
    
    args = parser.parse_args()
    
    # Create sample CSV if requested
    if args.create_sample:
        create_sample_csv(args.create_sample)
        return
    
    # Validate required arguments
    if not args.csv_path:
        parser.print_help()
        print("\nError: CSV path required. Use --create-sample to generate a template.")
        sys.exit(1)
    
    if not args.api_key or not args.cx:
        # Check environment variables
        api_key = args.api_key or os.environ.get('GOOGLE_API_KEY')
        cx = args.cx or os.environ.get('GOOGLE_CX')
        
        if not api_key or not cx:
            print("Error: --api-key and --cx required (or set GOOGLE_API_KEY and GOOGLE_CX env vars)")
            print("\nSetup instructions:")
            print("1. Get API key: https://console.cloud.google.com/apis/credentials")
            print("2. Create search engine: https://programmablesearchengine.google.com/")
            print("3. Enable 'Image search' and 'Search entire web' in search engine settings")
            sys.exit(1)
    else:
        api_key = args.api_key
        cx = args.cx
    
    # Run the downloader
    print("=" * 60)
    print("ROBOT IMAGE DOWNLOADER")
    print("=" * 60)
    
    results = process_csv(
        csv_path=args.csv_path,
        output_dir=args.output_dir,
        api_key=api_key,
        cx=cx,
        images_per_robot=args.num,
        skip_site_search=args.skip_site_search,
        skip_existing=args.skip_existing
    )
    
    print_summary(results, args.output_dir)
    
    # Save results manifest
    manifest_path = os.path.join(args.output_dir, 'download_manifest.json')
    with open(manifest_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nManifest saved: {manifest_path}")


if __name__ == '__main__':
    main()
