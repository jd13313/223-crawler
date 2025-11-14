export interface Comment {
    post_index: number;
    post_id: string;
    author: string;
    content: string;
    content_html: string;
    post_date: string;
}

export interface Thread {
    thread_title: string;
    thread_url: string;
    crawled_at: string;
    comments: Comment[];
}

export interface Board {
    board_name: string;
    board_url: string;
    discovered_at: string;
    threads: Thread[];
}

export interface ForumStats {
    boards_discovered: number;
    threads_discovered: number;
    threads_completed: number;
    comments_extracted: number;
    boards: number;
    threads: number;
    comments: number;
}

export interface ForumData {
    forum: string;
    crawled_at: string;
    stats: ForumStats;
    boards: Board[];
}

export interface Archive {
    filename: string;
    filepath: string;
    size_bytes: number;
    size_mb: number;
    crawled_at: string;
    stats: ForumStats;
}