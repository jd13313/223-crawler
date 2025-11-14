# 223 Forum Archive API Documentation

## Quick Start

Start the server:
```bash
./start_server.sh
```

The server will run on `http://localhost:5000` (accessible from anywhere on your network at `http://YOUR_IP:5000`)

## API Endpoints

### 1. Root - API Information
```bash
GET http://localhost:5000/
```

Returns API version and available endpoints.

**Example:**
```bash
curl http://localhost:5000/ | python3 -m json.tool
```

---

### 2. List All Archives
```bash
GET http://localhost:5000/archives
```

Returns all available archives with metadata (sorted newest first).

**Response:**
```json
{
  "count": 2,
  "archives": [
    {
      "filename": "223-archive-2025-11-13-18-43-31.json",
      "filepath": "archives/223-archive-2025-11-13-18-43-31.json",
      "size_bytes": 937,
      "size_mb": 0.0,
      "crawled_at": "2025-11-13T18:43:31.694473",
      "modified_at": "2025-11-13T18:43:31.694415",
      "stats": {
        "boards": 3,
        "threads": 0,
        "comments": 0
      }
    }
  ]
}
```

**Example:**
```bash
curl http://localhost:5000/archives | python3 -m json.tool
```

---

### 3. Get Latest Archive
```bash
GET http://localhost:5000/archives/latest
```

Returns the complete JSON data from the most recent archive.

**Example:**
```bash
curl http://localhost:5000/archives/latest > latest_archive.json
```

---

### 4. Get Specific Archive
```bash
GET http://localhost:5000/archives/<filename>
```

Returns the complete JSON data from a specific archive file.

**Example:**
```bash
curl http://localhost:5000/archives/223-archive-2025-11-13-18-43-31.json > specific_archive.json
```

---

### 5. Aggregate Statistics
```bash
GET http://localhost:5000/stats
```

Returns aggregate statistics across all archives.

**Response:**
```json
{
  "total_archives": 2,
  "total_size_mb": 2.5,
  "oldest_archive": "223-archive-2025-11-13-18-18-24.json",
  "latest_archive": "223-archive-2025-11-13-18-43-31.json",
  "latest_stats": {
    "boards": 10,
    "threads": 150,
    "comments": 2500
  }
}
```

**Example:**
```bash
curl http://localhost:5000/stats | python3 -m json.tool
```

---

## CORS Support

The API has CORS enabled, so you can call it from web applications running on different ports/domains.

**Example from JavaScript:**
```javascript
fetch('http://localhost:5000/archives')
  .then(response => response.json())
  .then(data => console.log(data));
```

---

## Development vs Production

**Current Setup (Development):**
- Flask development server
- Debug mode enabled
- Runs on port 5000
- Auto-reloads on code changes

**For Production:**
Consider using a production WSGI server like Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 server:app
```

---

## Integration Examples

### Python
```python
import requests

# Get all archives
response = requests.get('http://localhost:5000/archives')
archives = response.json()

print(f"Total archives: {archives['count']}")
for archive in archives['archives']:
    print(f"  • {archive['filename']}: {archive['stats']['comments']} comments")
```

### Shell Script
```bash
#!/bin/bash
# Download the latest archive
curl -s http://localhost:5000/archives/latest -o latest.json
echo "Downloaded latest archive"
```

### React/TypeScript
```typescript
interface Archive {
  filename: string;
  crawled_at: string;
  stats: {
    boards: number;
    threads: number;
    comments: number;
  };
}

async function fetchArchives(): Promise<Archive[]> {
  const response = await fetch('http://localhost:5000/archives');
  const data = await response.json();
  return data.archives;
}
```

---

## Error Responses

All errors return appropriate HTTP status codes and JSON responses:

**404 - Not Found:**
```json
{
  "error": "Archive not found"
}
```

**500 - Internal Server Error:**
```json
{
  "error": "Detailed error message"
}
```

---

## Tips

1. **Keep the server running** while developing your viewer app
2. **Use /archives/latest** for quick testing
3. **Use /stats** for dashboard displays
4. **The server auto-discovers** new archive files as they're created
5. **CORS is enabled** so you can call from any origin

---

## Troubleshooting

**Server won't start:**
```bash
# Check if port 5000 is in use
lsof -i :5000

# Kill existing process if needed
kill $(lsof -t -i :5000)
```

**Archives not showing:**
```bash
# Verify archives directory exists and has files
ls -lh archives/
```

**Connection refused:**
- Make sure the server is running
- Check firewall settings
- Verify you're using the correct IP/port

