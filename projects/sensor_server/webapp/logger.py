import logging
import json
from datetime import datetime
import traceback
from pytz import timezone


KST = timezone("Asia/Seoul")


class JSONFormatter(logging.Formatter):
    """JSONFormatter"""

    def format(self, record):
        # KST 시간대 설정
        def timetz(*args, **kwargs):
            return datetime.now(KST).timetuple()

        # asctime을 수동으로 설정
        logging.Formatter.converter = timetz
        record.asctime = self.formatTime(record, self.datefmt)

        # JSON 형태로 로그 메시지 구성
        log_message = {
            "timestamp": record.asctime,
            "level": record.levelname,
            "trace_id": getattr(record, "otelTraceID", "N/A"),
            "span_id": getattr(record, "otelSpanID", "N/A"),
            "name": record.name,
            "method": record.funcName,
            "message": record.getMessage(),
            "extra": getattr(record, "extra", {}),
        }

        if record.exc_info:
            # 예외 정보가 있는 경우 추가
            formatted_tb = "".join(traceback.format_exception(*record.exc_info))
            log_message["exception"] = {
                "type": record.exc_info[0].__name__,
                "message": str(record.exc_info[1]),
                "traceback": formatted_tb,
            }

        return json.dumps(log_message, ensure_ascii=False, indent=2)


def initialize_tracer():
    """tracer 초기화"""
    from opentelemetry import trace
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.instrumentation.logging import LoggingInstrumentor

    # 트레이서 프로바이더 설정
    trace.set_tracer_provider(TracerProvider())

    # 로깅 인스트루멘테이션 활성화
    LoggingInstrumentor().instrument()


def initialize_logger():
    """로거 초기화"""
    initialize_tracer()

    # 루트 로거 설정
    logger = logging.getLogger()
    logger.setLevel("INFO")
    logger.propagate = False

    # 기존 핸들러 제거
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # 새로운 핸들러 추가
    handler = logging.StreamHandler()
    handler.setFormatter(JSONFormatter())
    logger.addHandler(handler)
    return logger
