# Quick Start Guide

## 🚀 Get Started in 3 Steps

### 1. Verify Installation

Make sure Scrapy is installed (it looks like it already is in your venv):

```bash
scrapy version
```

If not installed:
```bash
pip install -r requirements.txt
```

### 2. Run Your First Crawl

**Option A: Using the convenience script**
```bash
./run_crawler.sh test
```

**Option B: Direct Scrapy command**
```bash
scrapy crawl 223_fetcher -o output.json -s CLOSESPIDER_PAGECOUNT=10
```

### 3. Check the Output

```bash
cat output.json | python -m json.tool | head -50
```

## 📊 What Gets Collected

The crawler extracts:

- **Boards**: Forum sections/categories
- **Threads**: Discussion topics with:
  - Title and URL
  - All posts in order
  - Post metadata (author, date, content)
  - User information (avatar, rank)
  - Engagement data (likes/reactions)

## 🎯 Common Use Cases

### Full Crawl
```bash
scrapy crawl 223_fetcher -o full_forum_data.json
```

### Export to CSV for Analysis
```bash
scrapy crawl 223_fetcher -o forum_data.csv
```

### Slower, Respectful Crawl
```bash
./run_crawler.sh slow
```

### With Statistics
```bash
./run_crawler.sh stats
```

## 🔍 Debugging Tips

### View What's Being Crawled
```bash
scrapy crawl 223_fetcher --loglevel=INFO
```

### Test a Specific URL
```bash
scrapy parse --spider=223_fetcher "https://www.tapatalk.com/groups/223/forums/some-board/"
```

### Check Scrapy Shell (Interactive)
```bash
scrapy shell "https://www.tapatalk.com/groups/223"
```

Then try selectors:
```python
response.css('a.forumtitle::attr(href)').getall()
response.css('.post').getall()
```

## ⚙️ Customization

### Adjust Crawl Speed

Edit `settings.py`:
```python
DOWNLOAD_DELAY = 2  # seconds between requests
CONCURRENT_REQUESTS_PER_DOMAIN = 1  # parallel requests
```

### Enable Pipelines

Edit `settings.py` and uncomment:
```python
ITEM_PIPELINES = {
    'pipelines.DuplicateFilterPipeline': 200,
    'pipelines.DataCleaningPipeline': 300,
    'pipelines.StatsPipeline': 400,
}
```

### Modify Selectors

If the crawler isn't finding data correctly, you may need to adjust CSS selectors in `223crawl.py`:

1. Open the forum in your browser
2. Right-click → Inspect Element
3. Find the correct CSS classes
4. Update the selectors in the spider

Common places to check:
- Board links: Line 47-50
- Thread links: Line 79-82
- Post content: Line 150-180

## 📁 Output Files

The crawler creates:
- `output.json` - Full data in JSON format
- `output.jsonl` - JSON Lines format (one item per line)
- `httpcache/` - Cached pages (helps during development)

## 🛑 Stopping a Crawl

Press `Ctrl+C` once to stop gracefully (saves partial data)

Press `Ctrl+C` twice to force stop

## 📝 Next Steps

1. Run a test crawl: `./run_crawler.sh test`
2. Inspect the output: `cat output_test.json`
3. Adjust selectors if needed (check browser DevTools)
4. Run a full crawl: `./run_crawler.sh basic`
5. Process the data with your favorite tools!

## ⚠️ Important Notes

- The crawler respects `robots.txt` by default
- Be respectful: don't crawl too fast
- Some data may require login (not currently supported)
- Check the forum's Terms of Service before crawling

## 🐛 Common Issues

**"No data extracted"**
- CSS selectors may need adjustment
- Try running with `--loglevel=DEBUG`
- Use Scrapy shell to test selectors

**"Connection refused"**
- Server may be blocking requests
- Try increasing `DOWNLOAD_DELAY`
- Check if you need authentication

**"Permission denied: run_crawler.sh"**
```bash
chmod +x run_crawler.sh
```

## 💡 Tips

- Start with small test runs before full crawls
- Use JSON Lines (`.jsonl`) for large datasets
- Monitor the logs for errors
- Enable HTTP cache during development
- Consider adding rate limiting in production

Happy crawling! 🕷️

