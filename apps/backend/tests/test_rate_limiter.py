import pytest


class TokenBucketRateLimiter:
    """Simple test double for 1RPS guarantee validation."""

    def __init__(self, requests_per_second: float = 1.0):
        self.requests_per_second = requests_per_second
        self._next_allowed_at = 0.0

    def acquire(self, now: float) -> float:
        wait = max(0.0, self._next_allowed_at - now)
        self._next_allowed_at = max(self._next_allowed_at, now) + (1 / self.requests_per_second)
        return wait


def test_rate_limiter_guarantees_one_request_per_second():
    limiter = TokenBucketRateLimiter(requests_per_second=1.0)

    first_wait = limiter.acquire(now=10.0)
    second_wait = limiter.acquire(now=10.1)
    third_wait = limiter.acquire(now=10.2)

    assert first_wait == pytest.approx(0.0)
    assert second_wait == pytest.approx(0.9)
    assert third_wait == pytest.approx(1.8)


def test_rate_limiter_allows_next_request_after_one_second_window():
    limiter = TokenBucketRateLimiter(requests_per_second=1.0)

    limiter.acquire(now=42.0)
    wait = limiter.acquire(now=43.0)

    assert wait == pytest.approx(0.0)
