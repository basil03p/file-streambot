from aiohttp import web
from .stream_routes import routes, cache_middleware

def web_server():
    # Optimize for high performance
    web_app = web.Application(
        client_max_size=50000000,  # Increased for larger files
        middlewares=[cache_middleware]
    )
    web_app.add_routes(routes)
    return web_app
