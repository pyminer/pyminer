from threading import Thread

from jsonrpc import JSONRPCResponseManager, Dispatcher
from werkzeug.serving import run_simple
from werkzeug.wrappers import Request, Response

from pyminer2.workspace.datamanager.converter import ConvertError
from pyminer2.workspace.datamanager.datamanager import DataManager
from pyminer2.workspace.datamanager.exceptions import ConflictError, NotFoundError
from pyminer2.workspace.datamanager.metadataset import WouldBlockError


class DataServer(Thread):
    def __init__(self, datamanager: DataManager, url: str,
                 port: int, callback=lambda r: None):
        super().__init__()
        self.datamanager = datamanager
        self.url = url
        self.port = port
        self.callback = callback
        self._define_errors()
        self.dispatcher = Dispatcher()
        self.setDaemon(True)

        @self.dispatcher.add_method
        def read(dataname: str):
            try:
                return {dataname: self.datamanager.read_data(
                    dataname), 'message': 'success'}
            except WouldBlockError as e:
                return self._error(e, self.WOULD_BLOCK_ERROR)
            except NotFoundError as e:
                return self._error(e, self.NOT_FOUND_ERROR)
            except ConvertError as e:
                # This mean unsupported type obj is requested
                # Users should regard this as not found error
                return self._error(e, self.NOT_FOUND_ERROR)
            except Exception as e:
                return self._error(e, self.INTERNAL_ERROR)

        @self.dispatcher.add_method
        def write(dataname: str, data: dict, provider: str = 'server'):
            try:
                self.datamanager.write_data(dataname, data, provider)
                return {'message': 'success'}
            except WouldBlockError as e:
                return self._error(e, self.WOULD_BLOCK_ERROR)
            except AssertionError as e:
                return self._error(e, self.INVALID_VALUE_ERROR)
            except ConflictError as e:
                return self._error(e, self.CONFLICT_ERROR)
            except Exception as e:
                return self._error(e, self.INTERNAL_ERROR)

    @Request.application
    def application(self, request):
        response = JSONRPCResponseManager.handle(
            request.get_data(cache=False, as_text=True), self.dispatcher)
        self.callback(response)
        if response and 'error' not in response.json:
            return Response(response.json, mimetype='application/json')
        elif response:
            return Response(response.json, status=400,
                            mimetype='application/json')
        else:
            return Response(self._error('not known', self.INTERNAL_ERROR),
                            status=400, mimetype='application/json')

    def run(self):
        run_simple(self.url, self.port, self.application)

    def _define_errors(self):
        self.WOULD_BLOCK_ERROR = 'WOULD_BLOCK_ERROR'
        self.NOT_FOUND_ERROR = 'NOT_FOUND_ERROR'
        self.INTERNAL_ERROR = 'INTERNAL_ERROR'
        self.INVALID_VALUE_ERROR = 'INVALID_VALUE_ERROR'
        self.CONFLICT_ERROR = 'CONFLICT_ERROR'

    def _error(self, e, code):
        return {'error': code, 'message': str(e)}
