# -*- coding: utf-8 -*-
"""
Item pipelines for processing scraped data

To enable a pipeline, add its class to the ITEM_PIPELINES setting in settings.py
Example:
    ITEM_PIPELINES = {
        'pipelines.JsonWriterPipeline': 300,
        'pipelines.DuplicateFilterPipeline': 200,
    }
"""

import json
from datetime import datetime
from scrapy.exceptions import DropItem


class DuplicateFilterPipeline:
    """Filter out duplicate threads based on URL"""
    
    def __init__(self):
        self.thread_urls_seen = set()
    
    def process_item(self, item, spider):
        if item.get('type') == 'thread':
            url = item.get('thread_url')
            if url in self.thread_urls_seen:
                raise DropItem(f"Duplicate thread found: {url}")
            else:
                self.thread_urls_seen.add(url)
        return item


class DataCleaningPipeline:
    """Clean and normalize scraped data"""
    
    def process_item(self, item, spider):
        if item.get('type') == 'thread':
            # Clean thread title
            if item.get('thread_title'):
                item['thread_title'] = item['thread_title'].strip()
            
            # Clean post data
            for post in item.get('posts', []):
                # Remove excessive whitespace from content
                if post.get('content'):
                    post['content'] = ' '.join(post['content'].split())
                
                # Ensure author has a value
                if not post.get('author'):
                    post['author'] = 'Anonymous'
        
        return item


class JsonWriterPipeline:
    """Write items to a JSON file with pretty formatting"""
    
    def open_spider(self, spider):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.file = open(f'output_{timestamp}.json', 'w', encoding='utf-8')
        self.file.write('[\n')
        self.first_item = True
    
    def close_spider(self, spider):
        self.file.write('\n]')
        self.file.close()
    
    def process_item(self, item, spider):
        if not self.first_item:
            self.file.write(',\n')
        self.first_item = False
        
        line = json.dumps(dict(item), ensure_ascii=False, indent=2)
        self.file.write(line)
        return item


class StatsPipeline:
    """Collect and log statistics about the crawl"""
    
    def __init__(self):
        self.stats = {
            'boards_count': 0,
            'threads_count': 0,
            'total_posts': 0,
        }
    
    def process_item(self, item, spider):
        if item.get('type') == 'board':
            self.stats['boards_count'] += 1
        elif item.get('type') == 'thread':
            self.stats['threads_count'] += 1
            self.stats['total_posts'] += len(item.get('posts', []))
        return item
    
    def close_spider(self, spider):
        spider.logger.info("=" * 50)
        spider.logger.info("CRAWL STATISTICS")
        spider.logger.info("=" * 50)
        spider.logger.info(f"Boards discovered: {self.stats['boards_count']}")
        spider.logger.info(f"Threads crawled: {self.stats['threads_count']}")
        spider.logger.info(f"Total posts extracted: {self.stats['total_posts']}")
        spider.logger.info("=" * 50)


# Example: Database storage pipeline (commented out - requires additional setup)
"""
class DatabasePipeline:
    '''Store items in a database (SQLite, PostgreSQL, MongoDB, etc.)'''
    
    def __init__(self):
        # Initialize database connection here
        pass
    
    def open_spider(self, spider):
        # Open database connection
        pass
    
    def close_spider(self, spider):
        # Close database connection
        pass
    
    def process_item(self, item, spider):
        # Insert item into database
        if item.get('type') == 'thread':
            # Store thread and posts
            pass
        elif item.get('type') == 'board':
            # Store board info
            pass
        return item
"""

