import requests, json
from ddd_objects.infrastructure.repository_impl import error_factory
from ddd_objects.domain.exception import return_codes
from .do import APIGatewayRequestDO


class APIGatewayAccessOperator:
    """Redis访问接口类。
    """
    def __init__(self, ip: str, port: int, token: str) -> None:
        self.url = f"http://{ip}:{port}"
        self.header = {"api-token":token}


    def _check_error(self, status_code, info):
        if status_code>299:
            if isinstance(info['detail'], str):
                return_code = return_codes['OTHER_CODE']
                error_traceback = info['detail']
            else:
                return_code = info['detail']['return_code']
                error_traceback = info['detail']['error_traceback']
            raise error_factory.make(return_code)(error_traceback)


    def check_connection(self, timeout=3):
        response=requests.get(f'{self.url}', headers=self.header, timeout=timeout)
        info = json.loads(response.text)
        self._check_error(response.status_code, info)
        if info['message']=='Hello World':
            return True
        else:
            return False


    def send_request(self, request:APIGatewayRequestDO, timeout=3)->str:
        data = request.dict()
        data = json.dumps(data)
        response=requests.post(f'{self.url}/request', headers=self.header, data=data, timeout=timeout)
        info = json.loads(response.text)
        self._check_error(response.status_code, info)
        return info
        


    