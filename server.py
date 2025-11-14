#!/usr/bin/env python3
"""
Lightweight web server for 223 Forum Archives
Serves archive metadata and files via JSON API
"""

from flask import Flask, jsonify, send_file
from flask_cors import CORS
import json
import glob
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend access

ARCHIVES_DIR = 'archives'

def get_archive_metadata(filepath):
    """Extract metadata from an archive file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return {
                'filename': os.path.basename(filepath),
                'filepath': filepath,
                'size_bytes': os.path.getsize(filepath),
                'size_mb': round(os.path.getsize(filepath) / 1024 / 1024, 2),
                'crawled_at': data.get('crawled_at', 'unknown'),
                'stats': data.get('stats', {}),
                'modified_at': datetime.fromtimestamp(os.path.getmtime(filepath)).isoformat()
            }
    except Exception as e:
        return {
            'filename': os.path.basename(filepath),
            'filepath': filepath,
            'error': str(e)
        }

@app.route('/')
def index():
    """Root endpoint - API documentation"""
    return jsonify({
        'name': '223 Forum Archive API',
        'version': '1.0',
        'endpoints': {
            '/': 'This help message',
            '/archives': 'List all archives with metadata',
            '/archives/<filename>': 'Get specific archive file',
            '/archives/latest': 'Get the most recent archive',
            '/stats': 'Aggregate statistics across all archives'
        }
    })

@app.route('/archives')
def list_archives():
    """List all available archives with metadata"""
    archive_files = sorted(glob.glob(f'{ARCHIVES_DIR}/223-archive-*.json'))
    
    archives = []
    for filepath in archive_files:
        archives.append(get_archive_metadata(filepath))
    
    # Sort by crawled_at descending (newest first)
    archives.sort(key=lambda x: x.get('crawled_at', ''), reverse=True)
    
    return jsonify({
        'count': len(archives),
        'archives': archives
    })

@app.route('/archives/<filename>')
def get_archive(filename):
    """Get a specific archive file"""
    filepath = os.path.join(ARCHIVES_DIR, filename)
    
    if not os.path.exists(filepath):
        return jsonify({'error': 'Archive not found'}), 404
    
    return send_file(filepath, mimetype='application/json')

@app.route('/archives/latest')
def get_latest_archive():
    """Get the most recent archive"""
    archive_files = sorted(glob.glob(f'{ARCHIVES_DIR}/223-archive-*.json'))
    
    if not archive_files:
        return jsonify({'error': 'No archives found'}), 404
    
    latest = archive_files[-1]
    return send_file(latest, mimetype='application/json')

@app.route('/stats')
def aggregate_stats():
    """Get aggregate statistics across all archives"""
    archive_files = sorted(glob.glob(f'{ARCHIVES_DIR}/223-archive-*.json'))
    
    if not archive_files:
        return jsonify({'error': 'No archives found'}), 404
    
    total_archives = len(archive_files)
    total_size_mb = 0
    latest_stats = None
    
    for filepath in archive_files:
        total_size_mb += os.path.getsize(filepath) / 1024 / 1024
        
        # Get stats from latest archive
        if filepath == archive_files[-1]:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                latest_stats = data.get('stats', {})
    
    return jsonify({
        'total_archives': total_archives,
        'total_size_mb': round(total_size_mb, 2),
        'oldest_archive': os.path.basename(archive_files[0]) if archive_files else None,
        'latest_archive': os.path.basename(archive_files[-1]) if archive_files else None,
        'latest_stats': latest_stats
    })

if __name__ == '__main__':
    # Ensure archives directory exists
    os.makedirs(ARCHIVES_DIR, exist_ok=True)
    
    print("=" * 60)
    print("🚀 223 Forum Archive Server")
    print("=" * 60)
    print(f"📁 Archives directory: {os.path.abspath(ARCHIVES_DIR)}")
    print(f"🌐 Server running at: http://localhost:5000")
    print()
    print("Available endpoints:")
    print("  • http://localhost:5000/")
    print("  • http://localhost:5000/archives")
    print("  • http://localhost:5000/archives/latest")
    print("  • http://localhost:5000/archives/<filename>")
    print("  • http://localhost:5000/stats")
    print()
    print("Press Ctrl+C to stop")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)

