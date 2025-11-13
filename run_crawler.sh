#!/bin/bash

# Tapatalk Forum Crawler Runner Script
# This script provides easy ways to run the crawler with common configurations

echo "================================"
echo "223 Tapatalk Forum Crawler"
echo "================================"
echo ""

# Function to display help
show_help() {
    echo "Usage: ./run_crawler.sh [option]"
    echo ""
    echo "Options:"
    echo "  1, basic       - Basic crawl, output to JSON"
    echo "  2, jsonl       - Output to JSON Lines format (better for large datasets)"
    echo "  3, debug       - Run with debug logging"
    echo "  4, fast        - Faster crawl (less polite, use carefully)"
    echo "  5, slow        - Slower, more respectful crawl"
    echo "  6, stats       - Run with statistics pipeline enabled"
    echo "  7, test        - Test run (max 10 requests)"
    echo "  help           - Show this help message"
    echo ""
}

# Check if scrapy is installed
if ! command -v scrapy &> /dev/null; then
    echo "Error: Scrapy is not installed."
    echo "Please run: pip install -r requirements.txt"
    exit 1
fi

# Parse command line argument
OPTION="${1:-basic}"

case $OPTION in
    1|basic)
        echo "Running basic crawl..."
        echo "Output: output.json"
        echo "Note: robots.txt is disabled for archival purposes"
        scrapy runspider 223crawl.py -o output.json -s ROBOTSTXT_OBEY=False
        ;;
    2|jsonl)
        echo "Running crawl with JSON Lines output..."
        echo "Output: output.jsonl"
        scrapy runspider 223crawl.py -o output.jsonl -s ROBOTSTXT_OBEY=False
        ;;
    3|debug)
        echo "Running with debug logging..."
        echo "Output: output_debug.json"
        scrapy runspider 223crawl.py -o output_debug.json -s ROBOTSTXT_OBEY=False --loglevel=DEBUG
        ;;
    4|fast)
        echo "Running faster crawl (reduced delays)..."
        echo "Output: output_fast.json"
        echo "WARNING: This may be considered less polite to the server"
        scrapy runspider 223crawl.py -o output_fast.json \
            -s ROBOTSTXT_OBEY=False \
            -s DOWNLOAD_DELAY=0.5 \
            -s CONCURRENT_REQUESTS_PER_DOMAIN=4
        ;;
    5|slow)
        echo "Running slower, more respectful crawl..."
        echo "Output: output_slow.json"
        scrapy runspider 223crawl.py -o output_slow.json \
            -s ROBOTSTXT_OBEY=False \
            -s DOWNLOAD_DELAY=3 \
            -s CONCURRENT_REQUESTS_PER_DOMAIN=1
        ;;
    6|stats)
        echo "Running with statistics pipeline..."
        echo "Output: output_with_stats.json"
        scrapy runspider 223crawl.py -o output_with_stats.json \
            -s ROBOTSTXT_OBEY=False \
            -s ITEM_PIPELINES='{"pipelines.StatsPipeline": 100}'
        ;;
    7|test)
        echo "Running test crawl (limited to 10 requests)..."
        echo "Output: output_test.json"
        scrapy runspider 223crawl.py -o output_test.json \
            -s ROBOTSTXT_OBEY=False \
            -s CLOSESPIDER_PAGECOUNT=10
        ;;
    help|--help|-h)
        show_help
        exit 0
        ;;
    *)
        echo "Unknown option: $OPTION"
        echo ""
        show_help
        exit 1
        ;;
esac

echo ""
echo "================================"
echo "Crawl completed!"
echo "================================"

