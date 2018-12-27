"""
    项目部署
"""

from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from ginger import app


if __name__ == '__main__':
    app.logger.info('服务正在启动中...')
    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(8888)  # flask默认的端口
    IOLoop.instance().start()