#!/bin/bash

# Tapatalk Forum Crawler Runner Script
# This script provides easy ways to run the crawler with common configurations

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo "================================"
echo "223 Tapatalk Forum Crawler"
echo "================================"
echo ""

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
else
    echo "⚠️  Warning: Virtual environment not found."
    echo "   Run: python -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Function to display help
show_help() {
    echo "Usage: ./run_crawler.sh [option]"
    echo ""
    echo "Options:"
    echo "  full (default) - Full crawl of entire forum"
    echo "  test           - Test crawl (only 10 pages)"
    echo "  debug          - Full crawl with debug logging"
    echo "  slow           - Slower crawl (3s delay, more polite)"
    echo "  help           - Show this help message"
    echo ""
    echo "Examples:"
    echo "  ./run_crawler.sh          # Runs full crawl"
    echo "  ./run_crawler.sh test     # Quick test"
    echo "  ./run_crawler.sh debug    # Debug mode"
    echo ""
}

# Check if scrapy is installed
if ! command -v scrapy &> /dev/null; then
    echo "Error: Scrapy is not installed."
    echo "Please run: pip install -r requirements.txt"
    exit 1
fi

# Parse command line argument (default to full)
OPTION="${1:-full}"

case $OPTION in
    full)
        echo "Clearing cache for fresh data..."
        rm -rf httpcache/ .scrapy/httpcache/
        echo "Running FULL crawl of entire forum..."
        echo "Output: archives/223-archive-<timestamp>.json"
        echo "Note: This will take several minutes"
        scrapy runspider 223crawl.py \
            -s ROBOTSTXT_OBEY=False \
            -s LOG_LEVEL=INFO
        ;;
    test)
        echo "Clearing cache for fresh data..."
        rm -rf httpcache/ .scrapy/httpcache/
        echo "Running test crawl (limited to 10 requests)..."
        echo "Output: output_test.json"
        scrapy runspider 223crawl.py -o output_test.json \
            -s ROBOTSTXT_OBEY=False \
            -s CLOSESPIDER_PAGECOUNT=10
        ;;
    debug)
        echo "Clearing cache for fresh data..."
        rm -rf httpcache/ .scrapy/httpcache/
        echo "Running FULL crawl with DEBUG logging..."
        echo "Output: archives/223-archive-<timestamp>.json"
        echo "Note: This will be VERY verbose"
        scrapy runspider 223crawl.py \
            -s ROBOTSTXT_OBEY=False \
            -s LOG_LEVEL=DEBUG
        ;;
    slow)
        echo "Clearing cache for fresh data..."
        rm -rf httpcache/ .scrapy/httpcache/
        echo "Running slower, more polite crawl..."
        echo "Output: archives/223-archive-<timestamp>.json"
        echo "Note: 3 second delay between requests"
        scrapy runspider 223crawl.py \
            -s ROBOTSTXT_OBEY=False \
            -s LOG_LEVEL=INFO \
            -s DOWNLOAD_DELAY=3 \
            -s CONCURRENT_REQUESTS_PER_DOMAIN=1
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

