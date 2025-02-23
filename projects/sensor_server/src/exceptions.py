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


class AuthorizationException(ClientException):
    """인증 오류"""


class InvalidRequestException(ClientException):
    """클라이언트로부터 잘못된 요청 왔을 때"""


class InvalidTokenException(AuthorizationException):
    """유효하지 않은 정보가 들어왔을 때"""


class InvalidUserException(ClientException):
    """삭제 등의 이유로 유효하지 않은 유저일 때"""


class NotExistUserException(ClientException):
    """사용자가 존재하지 않을 때"""


class WrongPasswordException(ClientException):
    """비밀번호가 잘못 되었을 때"""


class PermissionDeniedException(ClientException):
    """권한 맞지 않을 때 ( 어드민 / 매니저 / 일반 유저 )"""


class ExpiredTokenException(InvalidTokenException):
    """만료된 토큰"""


class FileTypeException(ClientException):
    """파일 형식 오류"""


class UnsupportedModelException(ClientException):
    """지원하지 않는 모델 예외처리"""


"""
서버 측 오류
"""


class ServerException(SensorAppException):
    """서버 측 오류"""


class ModelNotFoundException(ServerException):
    """LLM 모델을 찾지 못했을 때"""


class DatabaseException(ServerException):
    """데이터 베이스에서 발생한 Exception"""


class ElasticsearchException(ServerException):
    """Elasticsearch에서 발생한 Exception"""


class NotFoundException(DatabaseException):
    """데이터를 찾지 못했을 때"""


class DBIntegrityException(DatabaseException):
    """데이터베이스 무결성 오류"""


class AlreadyExistsException(DatabaseException):
    """이미 존재한 경우"""


class EmbeddingException(ServerException):
    """임베딩 과정 중  예외 발생"""


class CustomLLMException(ServerException):
    """Custom LLM 예외"""
