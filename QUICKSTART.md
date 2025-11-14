# Quick Start Guide

## 🚀 Get Started in 2 Steps

### 1. Setup (First Time Only)

Make sure you have the virtual environment set up:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Run the Crawler

The convenience script handles everything (auto-activates venv):

```bash
./run_crawler.sh full
```

That's it! The crawler will output to `archives/223-archive-<timestamp>.json` when complete.

Example: `archives/223-archive-2025-11-13-14-30-45.json`

---

## 🌐 Archive API Server

Start a lightweight web server to browse your archives via JSON API:

```bash
./start_server.sh
```

**Available endpoints:**
- `http://localhost:5000/` - API documentation
- `http://localhost:5000/archives` - List all archives with metadata
- `http://localhost:5000/archives/latest` - Get the most recent archive
- `http://localhost:5000/archives/<filename>` - Get specific archive file
- `http://localhost:5000/stats` - Aggregate statistics across all archives

**Example usage:**
```bash
# List all archives
curl http://localhost:5000/archives | python3 -m json.tool

# Get latest archive
curl http://localhost:5000/archives/latest > latest.json

# View stats
curl http://localhost:5000/stats
```

---

## 📊 Output Structure

The crawler produces a hierarchical JSON structure:

```json
{
  "stats": {
    "boards": 10,
    "threads": 150,
    "comments": 2500
  },
  "boards": [
    {
      "board_name": "223 Remington",
      "board_url": "...",
      "threads": [
        {
          "thread_title": "Wild 223 appears!",
          "thread_url": "...",
          "comments": [
            {
              "author": "John",
              "content": "...",
              "post_date": "2024-01-15",
              "post_id": "p12345"
            }
          ]
        }
      ]
    }
  ]
}
```

**Hierarchy:** `BOARD → THREAD → COMMENTS`

---

## 🎯 Common Commands

### Full Crawl (Default)
```bash
./run_crawler.sh        # Same as: ./run_crawler.sh full
```
✅ **Recommended** - Clears cache, then crawls entire forum

### Test Crawl
```bash
./run_crawler.sh test
```
Quick test (only 10 pages) with cache cleared

### Debug Mode
```bash
./run_crawler.sh debug
```
Full crawl with verbose DEBUG logging

### Slow/Polite Mode
```bash
./run_crawler.sh slow
```
Full crawl with 3-second delays (more polite to server)

### Help
```bash
./run_crawler.sh help
```

---

## 🔍 Checking Your Data

### View Stats
```bash
# Use the latest archive file
python3 << 'EOF'
import json
import glob

# Get the most recent archive
files = sorted(glob.glob('archives/223-archive-*.json'))
latest = files[-1] if files else None

if latest:
    data = json.load(open(latest))
    print(f"📁 File: {latest}")
    print(f"📊 Boards: {data['stats']['boards']}")
    print(f"📝 Threads: {data['stats']['threads']}")
    print(f"💬 Comments: {data['stats']['comments']}")
else:
    print("No archive files found!")
EOF
```

### Pretty Print JSON
```bash
# View the latest archive
ls -t archives/223-archive-*.json | head -1 | xargs cat | python3 -m json.tool | less
```

### Count Threads Per Board
```bash
python3 << 'EOF'
import json
import glob

# Get the most recent archive
files = sorted(glob.glob('archives/223-archive-*.json'))
if files:
    data = json.load(open(files[-1]))
    for board in data['boards']:
        print(f"{board['board_name']}: {len(board['threads'])} threads")
EOF
```

### Using the API Server (Easier!)
```bash
# Start the server first
./start_server.sh

# Then in another terminal, query the API
curl http://localhost:5000/stats | python3 -m json.tool
```

---

## ⚙️ Customization

### Adjust Crawl Speed

Use the built-in slow mode:
```bash
./run_crawler.sh slow   # 3 second delay between requests
```

Or edit `settings.py` for custom settings:
```python
DOWNLOAD_DELAY = 2  # Seconds between requests
CONCURRENT_REQUESTS_PER_DOMAIN = 1  # Parallel requests
```

### Debug Issues

Run with debug logging:
```bash
./run_crawler.sh debug
```

### Manual Scrapy Command

If you need full control:
```bash
source venv/bin/activate
scrapy runspider 223crawl.py -s ROBOTSTXT_OBEY=False -s LOG_LEVEL=INFO
```

---

## 🛑 Stopping a Crawl

- **Ctrl+C once** - Graceful stop (saves data collected so far)
- **Ctrl+C twice** - Force stop

---

## 📁 Files Explained

- `223crawl.py` - Main spider (defines crawl logic)
- `settings.py` - Scrapy configuration
- `run_crawler.sh` - Convenience script to run crawler
- `start_server.sh` - Convenience script to start API server
- `server.py` - Lightweight Flask API server for archives
- `archives/` - Directory containing all archive JSON files
- `httpcache/` - Cached HTTP responses (speeds up re-runs)
- `scrapy.cfg` - Scrapy project config

---

## 💡 Tips

- **Start small**: Use `./run_crawler.sh test` to verify everything works
- **Default behavior**: Just run `./run_crawler.sh` for a full crawl (no options needed!)
- **Cache management**: Cache is cleared before each run, then used during the crawl for efficiency
- **Monitor progress**: Watch the logs for "Threads discovered/completed" counters
- **Be polite**: Use `./run_crawler.sh slow` if you're concerned about server load

---

## 🐛 Common Issues

### "Virtual environment not found"
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### "Permission denied: run_crawler.sh"
```bash
chmod +x run_crawler.sh
```

### "Scrapy is not installed"
Make sure you activated the venv:
```bash
source venv/bin/activate
```

### No data extracted
The forum structure may have changed. Check CSS selectors in `223crawl.py`.

---

## ⚠️ Important Notes

- The crawler **disables** `robots.txt` by default (assuming you own the forum)
- Be respectful: default is 1 second between requests
- HTTP caching is enabled (24 hour expiration)
- The spider builds data in memory, outputs at the end

---

Happy crawling! 🕷️
