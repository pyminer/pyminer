import glob
import logging
import os
import socket
import webbrowser
from functools import cached_property
import waitress
from flask import Flask, send_file, render_template, redirect

from .renderer import MarkdownRenderer
import threading

# flask_logger = logging.getLogger('werkzeug')
# flask_logger.setLevel(logging.ERROR)
logger = logging.getLogger('pm_alg_doc_server')


class Server(object):
    app = Flask(__name__)
    thread: threading.Thread

    def __init__(self, path: str):
        self.base_path = path
        self.static_path = os.path.join(os.path.dirname(__file__), 'static')
        self.initiate_app()
        self.renderer = MarkdownRenderer()

    def initiate_app(self):
        app = self.app

        @app.route('/')
        def home():
            return redirect('/README.md')

        @app.route('/<path:path>')
        def markdown(path: str):
            path = os.path.join(self.base_path, path)
            path = os.path.join(self.base_path, path)
            if os.path.isdir(path):
                path = os.path.join(path, 'README.md')
            if not os.path.exists(path):
                return render_template(
                    'content.html',
                    title=os.path.split(path)[1],
                    content=self.renderer.render('# 文件不存在\n\n请查实路径，或在左侧选择您需要的文档'),
                    file_tree=self.file_tree,
                )
            if path.endswith('.md'):
                with open(path, mode='r', encoding='utf-8') as f:
                    return render_template(
                        'content.html',
                        title=os.path.split(path)[1],
                        content=self.renderer.render(f.read()),
                        file_tree=self.file_tree,
                    )
            return send_file(path)

        @app.route('/<path:path>')
        def static_file(path):
            return app.send_static_file(path)

    @cached_property
    def port(self):
        sock = socket.socket()
        sock.bind(('', 0))
        port = sock.getsockname()[1]
        sock.close()
        return port

    @cached_property
    def file_tree(self):

        def get_file_tree(directory_path):
            files = glob.glob(os.path.join(directory_path, '*'))
            directory_info = []
            for file in files:
                if os.path.isdir(file) and os.path.split(file)[1] != '__pycache__':
                    directory_info.append(
                        {
                            'is_directory': True,
                            'text': os.path.split(file)[1],
                            'url': '/' + os.path.relpath(file, self.base_path) + '/',
                            'children': get_file_tree(file)
                        })
                elif os.path.isfile(file) and os.path.splitext(file)[1] == '.md':
                    if os.path.split(file)[1] == 'README.md':
                        continue
                    directory_info.append({
                        'text': os.path.splitext(os.path.split(file)[1])[0],
                        'url': '/' + os.path.relpath(file, self.base_path),
                    })
            return directory_info

        return get_file_tree(self.base_path)

    def show(self, path: str):
        if path.startswith('/'):
            path = path[1:]
        if path.startswith('\\'):
            path = path[1:]
        path = f'http://127.0.0.1:{self.port}/{path}'
        webbrowser.open(path)

    def run(self):
        logger.debug(f'启动服务器：http://127.0.0.1:{self.port}')
        self.thread = threading.Thread(target=waitress.serve, args=(self.app,),
                                       kwargs={'port': self.port, '_quiet': True}, daemon=True)
        self.thread.start()
