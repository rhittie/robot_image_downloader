# Google Custom Search API Setup Guide

This guide walks you through setting up Google's Custom Search API for image searching.

## Overview

You need two things:
1. **API Key** - Authenticates your requests
2. **Search Engine ID (CX)** - Identifies your custom search engine

Total setup time: ~10 minutes

---

## Step 1: Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)

2. Sign in with your Google account

3. Click the project dropdown at the top (next to "Google Cloud")

4. Click **"New Project"**
   - Project name: `robot-image-downloader` (or whatever you prefer)
   - Click **Create**

5. Wait for the project to be created, then select it from the dropdown

---

## Step 2: Enable the Custom Search API

1. In Google Cloud Console, go to **APIs & Services** > **Library**
   - Or direct link: https://console.cloud.google.com/apis/library

2. Search for **"Custom Search API"**

3. Click on **Custom Search API**

4. Click **Enable**

---

## Step 3: Create an API Key

1. Go to **APIs & Services** > **Credentials**
   - Or direct link: https://console.cloud.google.com/apis/credentials

2. Click **+ CREATE CREDENTIALS** at the top

3. Select **API key**

4. Your new API key will appear - **copy it now**
   - It looks like: `AIzaSyB1234567890abcdefghijklmnop`

5. (Optional but recommended) Click **Edit API key** to restrict it:
   - Under "API restrictions", select **Restrict key**
   - Choose **Custom Search API**
   - Click **Save**

---

## Step 4: Create a Programmable Search Engine

1. Go to [Programmable Search Engine](https://programmablesearchengine.google.com/controlpanel/all)

2. Click **Add** (or **Get Started** if first time)

3. Fill in the form:
   - **Name**: `Robot Image Search` (or whatever you prefer)
   - **What to search**: Select **"Search the entire web"**
   - Click **Create**

4. You'll see a success page with code - ignore it, click **Customize**

5. In the settings:
   - Find **"Image search"** and toggle it **ON**
   - Ensure **"Search the entire web"** is enabled

6. In the left sidebar, click **Overview**

7. Find your **Search engine ID** (also called CX)
   - It looks like: `a1234567890bcdefg`
   - Copy this value

---

## Step 5: Test Your Setup

Run a quick test to verify everything works:

```bash
# Replace with your actual values
API_KEY="AIzaSyB1234567890abcdefghijklmnop"
CX="a1234567890bcdefg"

curl "https://www.googleapis.com/customsearch/v1?key=${API_KEY}&cx=${CX}&q=robot&searchType=image&num=1"
```

You should get a JSON response with image results. If you get an error:
- `403` - API not enabled or key restricted incorrectly
- `400` - Invalid CX or parameters
- `429` - Rate limit exceeded

---

## Step 6: Save Your Credentials

**Option A: Environment Variables (Recommended)**

Add to your shell profile (`~/.bashrc`, `~/.zshrc`, etc.):

```bash
export GOOGLE_API_KEY="your_api_key_here"
export GOOGLE_CX="your_search_engine_id_here"
```

Then reload: `source ~/.bashrc`

**Option B: Create a `.env` file**

Create a file named `.env` in the project folder:

```
GOOGLE_API_KEY=your_api_key_here
GOOGLE_CX=your_search_engine_id_here
```

Note: The current script reads environment variables but not `.env` files. You can add `python-dotenv` if you prefer that approach.

**Option C: Pass directly on command line**

```bash
python robot_image_downloader.py robots.csv ./images \
    --api-key YOUR_API_KEY \
    --cx YOUR_CX
```

---

## API Quotas & Billing

### Free Tier
- 100 search queries per day
- Resets at midnight Pacific Time

### Paid Usage
- $5 per 1,000 queries
- Must enable billing on your Google Cloud project

### To Enable Billing (if needed)
1. Go to **Billing** in Google Cloud Console
2. Link a billing account or create one
3. The API will automatically use paid quota when free is exhausted

### Check Your Usage
1. Go to **APIs & Services** > **Dashboard**
2. Click on **Custom Search API**
3. View the **Quotas** tab

---

## Security Best Practices

1. **Never commit API keys to git**
   - Add `.env` to your `.gitignore`
   - Use environment variables

2. **Restrict your API key**
   - Limit to Custom Search API only
   - Consider IP restrictions if running from a fixed server

3. **Monitor usage**
   - Set up billing alerts in Google Cloud
   - Review API dashboard periodically

---

## Troubleshooting

### "API key not valid"
- Check for typos or extra spaces
- Verify the key exists at https://console.cloud.google.com/apis/credentials
- Make sure Custom Search API is enabled

### "Request had insufficient authentication scopes"
- Your key may be restricted to wrong APIs
- Edit the key and ensure Custom Search API is allowed

### "Daily limit exceeded"
- Wait for quota reset (midnight PT)
- Or enable billing for more queries

### "Invalid Value" for cx parameter
- Double-check your Search Engine ID
- Go back to Programmable Search Engine and copy it again

### Images not appearing / wrong results
- Verify "Image search" is enabled in your search engine settings
- Verify "Search the entire web" is enabled
- Try the search manually at google.com to see what results exist
