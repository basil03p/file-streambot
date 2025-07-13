import aiohttp
import jinja2
import urllib.parse
import time
from FileStream.config import Telegram, Server
from FileStream.utils.database import Database
from FileStream.utils.human_readable import humanbytes
db = Database(Telegram.DATABASE_URL, Telegram.SESSION_NAME)

async def render_page(db_id):
    try:
        file_data = await db.get_file(db_id)
    except Exception:
        # Return a 404-style page for file not found
        return "<html><body><h1>File Not Found</h1><p>The requested file could not be found.</p></body></html>"
    
    # Check if file has expired
    current_time = time.time()
    expires_at = file_data.get('expires_at', current_time + 3600)  # Fallback for old files
    
    if current_time >= expires_at:
        # File has expired, delete it and show expired page
        await db.delete_one_file(file_data['_id'])
        await db.count_links(file_data['user_id'], "-")
        return "<html><body><h1>File Expired</h1><p>This file has expired and has been automatically deleted after 1 hour.</p></body></html>"
    
    src = urllib.parse.urljoin(Server.URL, f'dl/{file_data["_id"]}')
    file_size = humanbytes(file_data['file_size'])
    file_name = file_data['file_name'].replace("_", " ")
    
    # Calculate remaining time
    remaining_seconds = int(expires_at - current_time)
    remaining_minutes = remaining_seconds // 60
    remaining_hours = remaining_minutes // 60
    if remaining_hours > 0:
        time_remaining = f"{remaining_hours}h {remaining_minutes % 60}m"
    else:
        time_remaining = f"{remaining_minutes}m"

    if str((file_data['mime_type']).split('/')[0].strip()) == 'video':
        template_file = "FileStream/template/play.html"
    else:
        template_file = "FileStream/template/dl.html"
        async with aiohttp.ClientSession() as s:
            async with s.get(src) as u:
                file_size = humanbytes(int(u.headers.get('Content-Length')))

    with open(template_file) as f:
        template = jinja2.Template(f.read())

    return template.render(
        file_name=file_name,
        file_url=src,
        file_size=file_size,
        time_remaining=time_remaining
    )
