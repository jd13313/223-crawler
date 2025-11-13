# Tapatalk Forum Crawler for 223

A Scrapy-based web crawler designed to scrape Tapatalk forum data, specifically targeting the forum at `https://www.tapatalk.com/groups/223`.

## Features

- **Board Discovery**: Automatically discovers all boards/subforums on the main forum page
- **Thread Crawling**: Crawls all threads within each board
- **Post Extraction**: Extracts detailed information from each post including:
  - Author name and avatar
  - Post content (text and HTML)
  - Post date/timestamp
  - User rank
  - Post ID
  - Likes/reactions (if available)
- **Pagination Handling**: Automatically handles pagination for both board listings and long threads
- **Respectful Crawling**: Includes rate limiting and respects robots.txt

## Installation

1. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Linux/Mac
# or
venv\Scripts\activate  # On Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Crawl

Run the spider and output to JSON:
```bash
scrapy crawl 223_fetcher -o output.json
```

### Output to Different Formats

JSON Lines (recommended for large datasets):
```bash
scrapy crawl 223_fetcher -o output.jsonl
```

CSV:
```bash
scrapy crawl 223_fetcher -o output.csv
```

XML:
```bash
scrapy crawl 223_fetcher -o output.xml
```

### Advanced Usage

Limit the crawl depth:
```bash
scrapy crawl 223_fetcher -s DEPTH_LIMIT=2 -o output.json
```

Adjust download delay (in seconds):
```bash
scrapy crawl 223_fetcher -s DOWNLOAD_DELAY=2 -o output.json
```

Enable verbose logging:
```bash
scrapy crawl 223_fetcher -o output.json --loglevel=DEBUG
```

## Output Structure

The crawler produces two types of items:

### Board Item
```json
{
  "type": "board",
  "board_name": "General Discussion",
  "board_url": "https://www.tapatalk.com/groups/223/forums/general/",
  "discovered_at": "2025-11-13T12:00:00"
}
```

### Thread Item
```json
{
  "type": "thread",
  "thread_url": "https://www.tapatalk.com/groups/223/forums/general/123-thread-title.html",
  "thread_title": "Example Thread Title",
  "board_url": "https://www.tapatalk.com/groups/223/forums/general/",
  "crawled_at": "2025-11-13T12:00:00",
  "posts": [
    {
      "post_index": 0,
      "post_id": "p12345",
      "author": "username",
      "content": "Post content text...",
      "content_html": "<div>Post content HTML...</div>",
      "post_date": "2025-01-15T10:30:00",
      "avatar_url": "https://example.com/avatar.jpg",
      "user_rank": "Member",
      "likes": "5"
    }
  ]
}
```

## Customization

### Adjusting CSS Selectors

If the forum structure doesn't match the default selectors, you can modify the CSS selectors in `223crawl.py`:

- **Board links**: Line 47-50 in `parse_start_url()`
- **Thread links**: Line 79-82 in `parse_board()`
- **Post content**: Line 150-180 in `extract_post_data()`

### Modifying Crawl Rules

The spider uses Scrapy's `CrawlSpider` with rules defined at lines 21-34. You can modify these rules to change which URLs are followed or how they're processed.

### Rate Limiting

Adjust the crawl rate in `settings.py`:
- `DOWNLOAD_DELAY`: Time to wait between requests
- `CONCURRENT_REQUESTS_PER_DOMAIN`: Number of simultaneous requests
- `AUTOTHROTTLE_ENABLED`: Auto-adjust based on server response

## Debugging

### Test the Spider

Test without saving output:
```bash
scrapy crawl 223_fetcher
```

### Parse a Specific URL

Test parsing a specific page:
```bash
scrapy parse --spider=223_fetcher https://www.tapatalk.com/groups/223
```

### Check Robots.txt

View what's allowed by robots.txt:
```bash
scrapy view https://www.tapatalk.com/robots.txt
```

## Notes

- The crawler respects robots.txt by default
- HTTP caching is enabled to avoid re-downloading pages during development
- All timestamps are in ISO 8601 format
- The crawler includes multiple fallback CSS selectors for robustness

## Troubleshooting

**No data being extracted?**
- Check if the CSS selectors match the actual HTML structure
- Use browser DevTools to inspect the page and adjust selectors
- Try running with `--loglevel=DEBUG` to see what's happening

**Being blocked or rate-limited?**
- Increase the `DOWNLOAD_DELAY` setting
- Reduce `CONCURRENT_REQUESTS_PER_DOMAIN`
- Check if you need to adjust the `USER_AGENT`

**Missing some posts?**
- Check if pagination is working correctly
- Verify the pagination selectors on lines 90, 124, and 143

## License

MIT License - Feel free to modify and use as needed.

