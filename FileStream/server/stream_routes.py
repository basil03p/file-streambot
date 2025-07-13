import time
import math
import logging
import mimetypes
import traceback
from aiohttp import web
from aiohttp.http_exceptions import BadStatusLine
from FileStream.bot import multi_clients, work_loads, FileStream
from FileStream.config import Telegram, Server
from FileStream.server.exceptions import FIleNotFound, InvalidHash
from FileStream import utils, StartTime, __version__
from FileStream.utils.render_template import render_page

routes = web.RouteTableDef()

@routes.get("/status", allow_head=True)
async def root_route_handler(_):
    return web.json_response(
        {
            "server_status": "running",
            "uptime": utils.get_readable_time(time.time() - StartTime),
            "telegram_bot": "@" + FileStream.username,
            "connected_bots": len(multi_clients),
            "loads": dict(
                ("bot" + str(c + 1), l)
                for c, (_, l) in enumerate(
                    sorted(work_loads.items(), key=lambda x: x[1], reverse=True)
                )
            ),
            "version": __version__,
        }
    )

@routes.get("/watch/{path}", allow_head=True)
async def stream_handler(request: web.Request):
    try:
        path = request.match_info["path"]
        return web.Response(text=await render_page(path), content_type='text/html')
    except InvalidHash as e:
        raise web.HTTPForbidden(text=e.message)
    except FIleNotFound as e:
        raise web.HTTPNotFound(text=e.message)
    except (AttributeError, BadStatusLine, ConnectionResetError):
        pass


@routes.get("/dl/{path}", allow_head=True)
async def stream_handler(request: web.Request):
    try:
        path = request.match_info["path"]
        return await media_streamer(request, path)
    except InvalidHash as e:
        raise web.HTTPForbidden(text=e.message)
    except FIleNotFound as e:
        raise web.HTTPNotFound(text=e.message)
    except (AttributeError, BadStatusLine, ConnectionResetError):
        pass
    except Exception as e:
        traceback.print_exc()
        logging.critical(e.with_traceback(None))
        logging.debug(traceback.format_exc())
        raise web.HTTPInternalServerError(text=str(e))

class_cache = {}

async def media_streamer(request: web.Request, db_id: str):
    range_header = request.headers.get("Range", 0)
    
    # Enhanced error handling for empty work_loads
    if not work_loads:
        logging.error("No clients available - work_loads is empty")
        raise web.HTTPServiceUnavailable(text="No clients available")
    
    try:
        # Safe client selection with fallback
        index = min(work_loads, key=work_loads.get)
        if index not in multi_clients:
            # Fallback to first available client
            index = next(iter(multi_clients.keys()))
            logging.warning(f"Selected client {index} not in multi_clients, using fallback")
        
        faster_client = multi_clients[index]
    except (ValueError, KeyError) as e:
        logging.error(f"Error selecting client: {e}")
        # Emergency fallback to any available client
        if multi_clients:
            index = next(iter(multi_clients.keys()))
            faster_client = multi_clients[index]
            logging.warning(f"Using emergency fallback client {index}")
        else:
            raise web.HTTPServiceUnavailable(text="No clients available")
    
    if Telegram.MULTI_CLIENT:
        logging.info(f"Client {index} is now serving {request.headers.get('X-FORWARDED-FOR',request.remote)}")

    if faster_client in class_cache:
        tg_connect = class_cache[faster_client]
        logging.debug(f"Using cached ByteStreamer object for client {index}")
    else:
        logging.debug(f"Creating new ByteStreamer object for client {index}")
        tg_connect = utils.ByteStreamer(faster_client)
        class_cache[faster_client] = tg_connect
    logging.debug("before calling get_file_properties")
    file_id = await tg_connect.get_file_properties(db_id, multi_clients)
    logging.debug("after calling get_file_properties")
    
    file_size = file_id.file_size

    if range_header:
        from_bytes, until_bytes = range_header.replace("bytes=", "").split("-")
        from_bytes = int(from_bytes)
        until_bytes = int(until_bytes) if until_bytes else file_size - 1
    else:
        from_bytes = request.http_range.start or 0
        until_bytes = (request.http_range.stop or file_size) - 1

    if (until_bytes > file_size) or (from_bytes < 0) or (until_bytes < from_bytes):
        return web.Response(
            status=416,
            body="416: Range not satisfiable",
            headers={"Content-Range": f"bytes */{file_size}"},
        )

    # Optimize chunk size for better performance
    chunk_size = 1024 * 1024 * 2  # 2MB chunks for better speed
    until_bytes = min(until_bytes, file_size - 1)

    offset = from_bytes - (from_bytes % chunk_size)
    first_part_cut = from_bytes - offset
    last_part_cut = until_bytes % chunk_size + 1

    req_length = until_bytes - from_bytes + 1
    part_count = math.ceil(until_bytes / chunk_size) - math.floor(offset / chunk_size)
    
    # Enhanced headers for better download speed
    headers = {
        "Content-Type": f"{mime_type}",
        "Content-Range": f"bytes {from_bytes}-{until_bytes}/{file_size}",
        "Content-Length": str(req_length),
        "Content-Disposition": f'{disposition}; filename="{file_name}"',
        "Accept-Ranges": "bytes",
        "Cache-Control": "public, max-age=86400",  # 24 hours cache
        "ETag": f'"{db_id}-{file_size}"',
        "Connection": "keep-alive",
    }
    body = tg_connect.yield_file(
        file_id, index, offset, first_part_cut, last_part_cut, part_count, chunk_size
    )

    mime_type = file_id.mime_type
    file_name = utils.get_name(file_id)
    disposition = "attachment"

    if not mime_type:
        mime_type = mimetypes.guess_type(file_name)[0] or "application/octet-stream"

    # if "video/" in mime_type or "audio/" in mime_type:
    #     disposition = "inline"

    return web.Response(
        status=206 if range_header else 200,
        body=body,
        headers=headers,
    )

@routes.get("/health", allow_head=True)
async def health_check(_):
    """Health check endpoint for Koyeb"""
    return web.json_response({
        "status": "healthy",
        "timestamp": int(time.time()),
        "clients": len(multi_clients),
        "service": "FileStreamBot"
    })

@routes.get("/", allow_head=True)
async def home_route(_):
    """Home route to prevent 404 on root"""
    return web.json_response({
        "service": "FileStreamBot",
        "status": "running",
        "version": __version__
    })

# Add caching middleware for better performance
@web.middleware
async def cache_middleware(request, handler):
    # Add cache headers for static content
    if request.path.startswith(('/dl/', '/watch/')):
        response = await handler(request)
        if response.status == 200:
            response.headers['Cache-Control'] = 'public, max-age=86400'
            response.headers['X-Content-Type-Options'] = 'nosniff'
        return response
    return await handler(request)
