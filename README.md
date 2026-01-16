# Robot Image Downloader

A Python tool to batch download images of robots from manufacturers, using Google's Custom Search API. Prioritizes official images from manufacturer websites before falling back to general web search.

## Features

- **CSV-based input** - Define manufacturers, their websites, and robot models in a simple spreadsheet
- **Smart sourcing** - Searches manufacturer sites first for official product images
- **Organized output** - Downloads organized into folders by manufacturer
- **Manifest tracking** - JSON log of all downloads with source URLs
- **Rate limiting** - Built-in delays to respect API limits

## Quick Start

```bash
# 1. Install dependencies
pip install requests

# 2. Set up Google API (see GOOGLE_API_SETUP.md)

# 3. Edit sample_robots.csv with your robots

# 4. Run
python robot_image_downloader.py sample_robots.csv ./robot_images \
    --api-key YOUR_API_KEY \
    --cx YOUR_SEARCH_ENGINE_ID
```

## CSV Format

Your input CSV needs three columns:

| Column | Description | Example |
|--------|-------------|---------|
| `manufacturer` | Company name | Boston Dynamics |
| `manufacturer_url` | Company website domain | bostondynamics.com |
| `robots` | Robot names (comma-separated) | "SPOT, Atlas, Stretch" |

**Example CSV:**
```csv
manufacturer,manufacturer_url,robots
Boston Dynamics,bostondynamics.com,"SPOT, Atlas, Stretch"
Dusty Robotics,dustyrobotics.com,FieldPrinter
Built Robotics,builtrobotics.com,"ExoTrack, RPD 35"
```

Note: Wrap multiple robots in quotes if they contain commas.

## Command Line Options

```
python robot_image_downloader.py <csv_file> <output_dir> [options]

Required:
  csv_file              Path to your CSV file
  output_dir            Where to save images (default: ./robot_images)
  --api-key KEY         Google API key
  --cx ID               Google Custom Search Engine ID

Optional:
  --num N               Images per robot (default: 3)
  --skip-site-search    Skip manufacturer site, search web only
  --create-sample PATH  Generate a sample CSV template
```

## Environment Variables

Instead of passing credentials every time, set environment variables:

```bash
# Linux/Mac
export GOOGLE_API_KEY="your_api_key_here"
export GOOGLE_CX="your_search_engine_id_here"

# Windows (Command Prompt)
set GOOGLE_API_KEY=your_api_key_here
set GOOGLE_CX=your_search_engine_id_here

# Windows (PowerShell)
$env:GOOGLE_API_KEY="your_api_key_here"
$env:GOOGLE_CX="your_search_engine_id_here"
```

Then run without credentials:
```bash
python robot_image_downloader.py robots.csv ./images
```

## Output Structure

```
robot_images/
├── Boston_Dynamics/
│   ├── SPOT_1_official.jpg      # From manufacturer site
│   ├── SPOT_2_official.png      
│   ├── SPOT_3_web.jpg           # From web search
│   ├── Atlas_1_official.jpg
│   ├── Atlas_2_web.png
│   └── Stretch_1_web.jpg
├── Dusty_Robotics/
│   ├── FieldPrinter_1_official.png
│   └── FieldPrinter_2_web.jpg
├── Built_Robotics/
│   ├── ExoTrack_1_official.jpg
│   └── RPD_35_1_web.png
└── download_manifest.json       # Complete log of all downloads
```

**Filename convention:**
- `{robot_name}_{number}_official.{ext}` - Image from manufacturer website
- `{robot_name}_{number}_web.{ext}` - Image from general web search

## Download Manifest

The `download_manifest.json` file tracks all downloads:

```json
{
  "downloaded": [
    {
      "manufacturer": "Boston Dynamics",
      "robot": "SPOT",
      "source": "manufacturer_site",
      "filepath": "./robot_images/Boston_Dynamics/SPOT_1_official.jpg",
      "url": "https://bostondynamics.com/images/spot-background.jpg"
    }
  ],
  "failed": [
    {
      "manufacturer": "Some Company",
      "robot": "Unknown Robot",
      "reason": "No downloadable images found"
    }
  ]
}
```

## API Costs

Google Custom Search API pricing:
- **Free tier**: 100 queries/day
- **Paid**: $5 per 1,000 queries

Each robot requires 1-2 API calls (site search + web search fallback), so:
- 50 robots ≈ 100 queries (free tier limit)
- 500 robots ≈ $5

## Troubleshooting

**"No images found"**
- Try `--skip-site-search` to only search the web
- Check that robot name is spelled correctly
- Some smaller companies may have few indexed images

**"API key invalid"**
- Verify key at https://console.cloud.google.com/apis/credentials
- Ensure Custom Search API is enabled

**"Rate limit exceeded"**
- Wait until quota resets (daily)
- Or enable billing for higher limits

**Images are wrong/low quality**
- Increase `--num` to download more options
- Manually curate the results afterward

## License

MIT License - Use freely for personal or commercial projects.
