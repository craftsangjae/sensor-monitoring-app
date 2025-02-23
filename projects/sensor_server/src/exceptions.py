class SensorAppException(Exception):

    def __init__(self, message):
        self.message = message


"""
클라이언트 측 예외
  (1) 클라이언트의 잘못된 요청에 의해 발생된 것들을 잡기 위함
  (2) 4xx status code로 응답
"""


class ClientException(SensorAppException):
    """클라이언트 측 오류"""


"""
서버 측 오류
"""


class ServerException(SensorAppException):
    """서버 측 오류"""


class DatabaseException(ServerException):
    """데이터 베이스에서 발생한 Exception"""


class NotFoundException(DatabaseException):
    """데이터를 찾지 못했을 때"""


class DBIntegrityException(DatabaseException):
    """데이터베이스 무결성 오류"""


class AlreadyExistsException(DatabaseException):
    """이미 존재한 경우"""
