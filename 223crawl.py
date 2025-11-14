import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re
from datetime import datetime


class TapatalkForumSpider(CrawlSpider):
    name = '223_fetcher'
    allowed_domains = ['tapatalk.com']
    start_urls = ['https://www.tapatalk.com/groups/223']
    
    custom_settings = {
        'DOWNLOAD_DELAY': 1,  # Be respectful to the server
        'CONCURRENT_REQUESTS_PER_DOMAIN': 2,
        'ROBOTSTXT_OBEY': True,
        'USER_AGENT': 'Mozilla/5.0 (compatible; ForumCrawler/1.0)',
    }
    
    # Define rules for crawling
    # Based on actual Tapatalk URL structure observed at the site:
    # - Boards: /groups/223/board-name-fNUM/
    # - Threads: /groups/223/thread-title-tNUM.html (first page only!)
    # - Pagination: /groups/223/thread-title-tNUM-sNUM.html (handled by parse_thread, not rules)
    rules = (
        # Rule for board/forum pages (ending with -fNUMBER/)
        Rule(LinkExtractor(allow=r'/groups/223/.+-f\d+/$'), 
             callback='parse_board', 
             follow=True),
        
        # Rule for FIRST PAGE of threads only (ending with -tNUMBER.html, NO -s pagination)
        # This ensures pagination pages aren't treated as separate threads
        Rule(LinkExtractor(allow=r'/groups/223/.+-t\d+\.html$', deny=r'-s\d+\.html'),  
             callback='parse_thread', 
             follow=True),
    )
    
    def __init__(self, *args, **kwargs):
        super(TapatalkForumSpider, self).__init__(*args, **kwargs)
        # Hierarchical data structure: boards contain threads, threads contain comments
        self.forum_data = {}
        # Progress tracking
        self.boards_discovered = 0
        self.threads_discovered = 0
        self.threads_completed = 0
        self.comments_extracted = 0
    
    def parse_start_url(self, response):
        """Parse the main forum index page to discover boards"""
        self.logger.info(f"Parsing main forum page: {response.url}")
        
        # Extract all board/subforum links
        # Based on actual Tapatalk HTML structure - boards have class="forumtitle"
        board_links = response.css('a.forumtitle::attr(href)').getall()
        if not board_links:
            # Fallback: look for links ending with -fNUMBER/
            board_links = response.xpath('//a[contains(@href, "-f") and contains(@href, "/")]/@href').getall()
            board_links = [link for link in board_links if re.search(r'-f\d+/$', link)]
        
        for link in board_links:
            full_url = response.urljoin(link)
            board_name = response.css(f'a[href="{link}"]::text').get()
            
            if not board_name:
                board_name = 'Unknown Board'
            else:
                board_name = board_name.strip()
            
            # Normalize board URL (remove query params)
            normalized_url = re.sub(r'\?.*$', '', full_url)
            
            # Initialize board in hierarchical structure
            if normalized_url not in self.forum_data:
                self.forum_data[normalized_url] = {
                    'board_name': board_name,
                    'board_url': normalized_url,
                    'discovered_at': datetime.now().isoformat(),
                    'threads': []
                }
                self.boards_discovered += 1
                self.logger.info(f"📁 Board discovered: '{board_name}' (Total: {self.boards_discovered})")
            
            # Follow the board link
            yield response.follow(link, callback=self.parse_board)
    
    def parse_board(self, response):
        """Parse a board/forum page to discover threads"""
        self.logger.info(f"Parsing board page: {response.url}")
        
        # Extract board information
        board_title = response.css('h1::text, .forum-title::text').get()
        
        # Find all thread links on this board
        thread_links = response.css('a.topictitle::attr(href)').getall()
        if not thread_links:
            # Fallback selectors
            thread_links = response.css('a[href*=".html"]::attr(href)').getall()
        
        for link in thread_links:
            # Filter to only get thread links (not other pages)
            if re.search(r'\d+-.+\.html', link):
                yield response.follow(link, callback=self.parse_thread)
        
        # Handle pagination for boards
        next_page = response.css('a.next::attr(href), a[rel="next"]::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse_board)
    
    def parse_thread(self, response):
        """Parse a thread page to extract posts and comments"""
        # Extract thread title - it's inside an anchor tag within h2.topic-title
        thread_title = response.css('h2.topic-title a::text, h1[itemprop="headline"]::text, .topic-title::text').get()
        if not thread_title:
            thread_title = response.css('h1::text, h2::text').get()
        
        # Extract posts - select the parent row that contains both profile and post content
        # Structure: div.post (parent) contains dl.postprofile (user info) and div#post_container* (content)
        posts = response.css('div.post.postrow, div[id^="p_"]')
        
        if not posts:
            self.logger.warning(f"⚠️  No posts found on {response.url}")
            return
        
        # Track thread discovery
        self.threads_discovered += 1
        
        # Determine which board this thread belongs to
        board_url = self.extract_board_from_breadcrumbs(response)
        
        # Get thread metadata  
        thread_data = {
            'thread_title': thread_title.strip() if thread_title else 'Untitled Thread',
            'thread_url': response.url,
            'crawled_at': datetime.now().isoformat(),
            'comments': []  # Renamed from 'posts' to 'comments' per user request
        }
        
        # Extract all posts (comments) in the thread
        for idx, post in enumerate(posts):
            post_data = self.extract_post_data(post, idx)
            thread_data['comments'].append(post_data)
        
        self.logger.info(f"📝 Thread: '{thread_title.strip() if thread_title else 'Untitled'}' - {len(posts)} comments")
        
        # Check for pagination in thread
        # Tapatalk uses <li class="arrow next"><a rel="next">
        next_page = response.css('li.arrow.next a::attr(href), a[rel="next"]::attr(href), li.next a::attr(href)').get()
        if next_page:
            # If there's pagination, we need to handle it
            yield response.follow(next_page, callback=self.parse_thread_continuation,
                                cb_kwargs={'thread_data': thread_data, 'board_url': board_url})
        else:
            # No more pages, add thread to board
            num_comments = len(thread_data['comments'])
            was_added = self.add_thread_to_board(board_url, thread_data)
            if was_added:
                self.threads_completed += 1
                self.comments_extracted += num_comments
                self.logger.info(f"✅ Progress: {self.threads_completed}/{self.threads_discovered} threads completed | {self.comments_extracted} total comments")
    
    def parse_thread_continuation(self, response, thread_data, board_url):
        """Parse continuation pages of a thread"""
        posts = response.css('div.post.postrow, div[id^="p_"]')
        
        start_idx = len(thread_data['comments'])
        for idx, post in enumerate(posts, start=start_idx):
            post_data = self.extract_post_data(post, idx)
            thread_data['comments'].append(post_data)
        
        self.logger.info(f"   ↳ Continuation page: +{len(posts)} comments (total: {len(thread_data['comments'])})")
        
        # Check for more pages
        next_page = response.css('li.arrow.next a::attr(href), a[rel="next"]::attr(href), li.next a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse_thread_continuation,
                                cb_kwargs={'thread_data': thread_data, 'board_url': board_url})
        else:
            # All pages processed, add thread to board
            num_comments = len(thread_data['comments'])
            was_added = self.add_thread_to_board(board_url, thread_data)
            if was_added:
                self.threads_completed += 1
                self.comments_extracted += num_comments
                self.logger.info(f"✅ Progress: {self.threads_completed}/{self.threads_discovered} threads completed | {self.comments_extracted} total comments")
    
    def extract_post_data(self, post_selector, index):
        """Extract data from a single post"""
        # Author information - Tapatalk uses span with itemprop="name"
        author = post_selector.css('span[itemprop="name"]::text').get()
        if not author:
            # Fallback selectors
            author = post_selector.css('.username-coloured span::text, .username span::text').get()
        if not author:
            # Try direct text from username elements
            author = post_selector.css('.display_username::text, .username::text, .author a::text').get()
        
        # Post content - extract text from the content div
        content = post_selector.css('.content.noskim ::text').getall()
        content_html = post_selector.css('.content.noskim').get()
        
        # Post metadata - use time element's datetime attribute (most reliable)
        post_date = post_selector.css('time::attr(datetime)').get()
        if not post_date:
            # Fallback to timespan title
            post_date = post_selector.css('.timespan::attr(title)').get()
        
        post_id = post_selector.css('::attr(id)').get()
        
        return {
            'post_index': index,
            'post_id': post_id,
            'author': author.strip() if author else 'Anonymous',
            'content': ' '.join(content).strip() if content else '',
            'content_html': content_html,
            'post_date': post_date.strip() if post_date else None,
        }
    
    def extract_board_from_breadcrumbs(self, response):
        """Extract board URL from breadcrumbs on thread page"""
        # Look for the last breadcrumb before the current page (the board link)
        breadcrumb_links = response.css('.nav-breadcrumbs .crumb a::attr(href)').getall()
        
        # Filter for board URLs (containing -fNUMBER/)
        board_links = [link for link in breadcrumb_links if re.search(r'-f\d+/$', link)]
        
        if board_links:
            # Return the last board URL (most specific/deepest level)
            return response.urljoin(board_links[-1])
        
        # Fallback: return base forum URL
        return 'https://www.tapatalk.com/groups/223/'
    
    def add_thread_to_board(self, board_url, thread_data):
        """Add a thread to its parent board in the hierarchical structure
        Returns: True if thread was added, False if it was a duplicate
        """
        # Normalize board URL (remove session ID and pagination params)
        board_url = re.sub(r'\?.*$', '', board_url)  # Remove query params
        board_url = re.sub(r'-s\d+\.html$', '.html', board_url)  # Remove pagination from URL
        
        # Ensure board exists in forum_data
        if board_url not in self.forum_data:
            # Create board entry if it doesn't exist
            self.forum_data[board_url] = {
                'board_name': 'Unknown Board',
                'board_url': board_url,
                'discovered_at': datetime.now().isoformat(),
                'threads': []
            }
        
        # Normalize thread URL to check for duplicates
        thread_base_url = re.sub(r'\?.*$', '', thread_data['thread_url'])  # Remove query params
        thread_base_url = re.sub(r'-s\d+\.html$', '.html', thread_base_url)  # Remove pagination
        
        # Check if thread already exists in board
        existing_thread_urls = [re.sub(r'\?.*$', '', re.sub(r'-s\d+\.html$', '.html', t['thread_url'])) 
                               for t in self.forum_data[board_url]['threads']]
        
        if thread_base_url not in existing_thread_urls:
            # Normalize the thread URL in the data
            thread_data['thread_url'] = thread_base_url
            self.forum_data[board_url]['threads'].append(thread_data)
            self.logger.debug(f"Added thread '{thread_data['thread_title']}' to board")
            return True
        else:
            self.logger.debug(f"Thread '{thread_data['thread_title']}' already exists in board, skipping")
            return False
    
    def closed(self, reason):
        """Called when spider closes - output the hierarchical forum data"""
        import json
        
        self.logger.info("=" * 80)
        self.logger.info(f"Spider closing: {reason}")
        self.logger.info("=" * 80)
        
        # Convert forum_data dict to list of boards for output
        boards_list = list(self.forum_data.values())
        
        # Sort boards by name
        boards_list.sort(key=lambda b: b['board_name'])
        
        # Log statistics
        total_threads = sum(len(board['threads']) for board in boards_list)
        total_comments = sum(
            len(thread['comments']) 
            for board in boards_list 
            for thread in board['threads']
        )
        
        self.logger.info("📊 CRAWL STATISTICS:")
        self.logger.info(f"   📁 Boards discovered: {self.boards_discovered}")
        self.logger.info(f"   📝 Threads discovered: {self.threads_discovered}")
        self.logger.info(f"   ✅ Threads completed: {self.threads_completed}")
        self.logger.info(f"   💬 Comments extracted: {self.comments_extracted}")
        self.logger.info(f"   📦 Total in output: {len(boards_list)} boards, {total_threads} threads, {total_comments} comments")
        
        # Write hierarchical structure to file with timestamp
        timestamp = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        output_file = f'archives/223-archive-{timestamp}.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({
                'forum': '223',
                'crawled_at': datetime.now().isoformat(),
                'stats': {
                    'boards_discovered': self.boards_discovered,
                    'threads_discovered': self.threads_discovered,
                    'threads_completed': self.threads_completed,
                    'comments_extracted': self.comments_extracted,
                    'boards': len(boards_list),
                    'threads': total_threads,
                    'comments': total_comments
                },
                'boards': boards_list
            }, f, indent=2, ensure_ascii=False)
        
        self.logger.info("=" * 80)
        self.logger.info(f"✅ Hierarchical forum data written to {output_file}")
        self.logger.info("=" * 80)
