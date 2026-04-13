"""Circuit breaker for external data provider calls.

Prevents cascading failures by automatically opening the circuit when
too many consecutive errors occur, then allowing a probe call after a
cooldown period.
"""

from __future__ import annotations

import logging
import time
from enum import Enum, auto
from typing import Any, Callable, Awaitable

logger = logging.getLogger(__name__)


class CircuitState(Enum):
    CLOSED = auto()   # Normal operation
    OPEN = auto()     # Failing fast
    HALF_OPEN = auto()  # Probing recovery


class CircuitBreakerOpen(Exception):
    """Raised when a call is attempted while the circuit is OPEN."""


class CircuitBreaker:
    """Async circuit breaker implementation.

    Parameters
    ----------
    name:
        Human-readable identifier used in log messages.
    failure_threshold:
        Number of consecutive failures before the circuit opens.
    recovery_timeout:
        Seconds to wait in the OPEN state before moving to HALF_OPEN.
    half_open_max_calls:
        Number of probe calls allowed in HALF_OPEN state.
    """

    def __init__(
        self,
        name: str = "default",
        failure_threshold: int = 5,
        recovery_timeout: float = 30.0,
        half_open_max_calls: int = 1,
    ) -> None:
        self.name = name
        self._failure_threshold = failure_threshold
        self._recovery_timeout = recovery_timeout
        self._half_open_max_calls = half_open_max_calls

        self._state = CircuitState.CLOSED
        self._failure_count = 0
        self._success_count = 0
        self._opened_at: float = 0.0
        self._half_open_calls = 0

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def state(self) -> CircuitState:
        if self._state == CircuitState.OPEN:
            if time.monotonic() - self._opened_at >= self._recovery_timeout:
                logger.info("Circuit %s transitioning to HALF_OPEN", self.name)
                self._state = CircuitState.HALF_OPEN
                self._half_open_calls = 0
        return self._state

    def is_closed(self) -> bool:
        return self.state == CircuitState.CLOSED

    # ------------------------------------------------------------------
    # Core call wrapper
    # ------------------------------------------------------------------

    async def call(self, fn: Callable[..., Awaitable[Any]], *args: Any, **kwargs: Any) -> Any:
        """Execute *fn* respecting circuit state.

        Raises ``CircuitBreakerOpen`` when the circuit is OPEN.
        """
        current = self.state

        if current == CircuitState.OPEN:
            raise CircuitBreakerOpen(
                f"Circuit '{self.name}' is OPEN – calls are being blocked"
            )

        if current == CircuitState.HALF_OPEN:
            if self._half_open_calls >= self._half_open_max_calls:
                raise CircuitBreakerOpen(
                    f"Circuit '{self.name}' is HALF_OPEN and probe quota reached"
                )
            self._half_open_calls += 1

        try:
            result = await fn(*args, **kwargs)
            self._on_success()
            return result
        except CircuitBreakerOpen:
            raise
        except Exception as exc:
            self._on_failure(exc)
            raise

    # ------------------------------------------------------------------
    # Internal state transitions
    # ------------------------------------------------------------------

    def _on_success(self) -> None:
        if self._state == CircuitState.HALF_OPEN:
            logger.info("Circuit %s recovered – closing", self.name)
            self._state = CircuitState.CLOSED
        self._failure_count = 0

    def _on_failure(self, exc: Exception) -> None:
        self._failure_count += 1
        logger.warning(
            "Circuit %s failure %d/%d: %s",
            self.name,
            self._failure_count,
            self._failure_threshold,
            exc,
        )
        if self._failure_count >= self._failure_threshold:
            if self._state != CircuitState.OPEN:
                logger.error("Circuit %s OPENED", self.name)
                self._state = CircuitState.OPEN
                self._opened_at = time.monotonic()

    def reset(self) -> None:
        """Manually reset the circuit to CLOSED state."""
        self._state = CircuitState.CLOSED
        self._failure_count = 0
        self._success_count = 0
        self._half_open_calls = 0

    def stats(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "state": self.state.name,
            "failure_count": self._failure_count,
            "failure_threshold": self._failure_threshold,
        }
