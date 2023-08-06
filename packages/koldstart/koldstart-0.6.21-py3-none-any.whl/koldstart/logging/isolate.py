from __future__ import annotations

from isolate.logs import Log
from structlog.dev import ConsoleRenderer
from structlog.processors import TimeStamper
from structlog.typing import EventDict

from .style import LEVEL_STYLES

_renderer = ConsoleRenderer(level_styles=LEVEL_STYLES)

_timestamper = TimeStamper(fmt="%Y-%m-%d %H:%M:%S", utc=False)


def format_log(log: Log) -> str:
    level = log.level.lower()
    # bound_env = log.bound_env.key if log.bound_env is not None else "global"
    event: EventDict = {
        "event": log.message,
        "level": level,
        # "logger_name": log.source,
        # "bound_env": bound_env,
    }
    event = _timestamper.__call__(logger={}, name=level, event_dict=event)
    message = _renderer.__call__(logger={}, name=level, event_dict=event)
    return message
