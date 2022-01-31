from abc import ABC, abstractmethod
from enum import Enum
from typing import TYPE_CHECKING, Any, Callable, Union

from prompt_toolkit.enums import EditingMode
from prompt_toolkit.key_binding.vi_state import InputMode

if TYPE_CHECKING:
    from .application import Application

__all__ = [
    "CursorShape",
    "CursorShapeConfig",
    "SimpleCursorShapeConfig",
    "ModalCursorShapeConfig",
]


class CursorShape(Enum):
    BLOCK = "BLOCK"
    BEAM = "BEAM"
    UNDERLINE = "UNDERLINE"
    BLINKING_BLOCK = "BLINKING_BLOCK"
    BLINKING_BEAM = "BLINKING_BEAM"
    BLINKING_UNDERLINE = "BLINKING_UNDERLINE"


class CursorShapeConfig(ABC):
    @abstractmethod
    def get_cursor_shape(self, application: "Application[Any]") -> CursorShape:
        ...


AnyCursorShapeConfig = Union[CursorShape, CursorShapeConfig, None]


class SimpleCursorShapeConfig(CursorShapeConfig):
    """
    Always show the given cursor shape.
    """

    def __init__(self, cursor_shape: CursorShape = CursorShape.BLOCK) -> None:
        self.cursor_shape = cursor_shape

    def get_cursor_shape(self, application: "Application[Any]") -> CursorShape:
        return self.cursor_shape


class ModalCursorShapeConfig(CursorShapeConfig):
    """
    Show cursor shape according to the current input mode.
    """

    def get_cursor_shape(self, application: "Application[Any]") -> CursorShape:
        if application.editing_mode == EditingMode.VI:
            if application.vi_state.input_mode == InputMode.INSERT:
                return CursorShape.BEAM
            if application.vi_state.input_mode == InputMode.REPLACE:
                return CursorShape.UNDERLINE

        # Default
        return CursorShape.BLOCK


class DynamicCursorShapeConfig(CursorShapeConfig):
    def __init__(
        self, get_cursor_shape_config: Callable[[], AnyCursorShapeConfig]
    ) -> None:
        self.get_cursor_shape_config = get_cursor_shape_config

    def get_cursor_shape(self, application: "Application[Any]") -> CursorShape:
        return to_cursor_shape_config(self.get_cursor_shape_config()).get_cursor_shape(
            application
        )


def to_cursor_shape_config(value: AnyCursorShapeConfig) -> CursorShapeConfig:
    if value is None:
        return SimpleCursorShapeConfig()

    if isinstance(value, CursorShape):
        return SimpleCursorShapeConfig(value)

    return value
