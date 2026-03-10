from dataclasses import dataclass
from datetime import datetime


@dataclass
class ConfluencePage:
    page_id: str
    updated_at: datetime


def select_incremental_pages(pages: list[ConfluencePage], last_synced_at: datetime) -> list[ConfluencePage]:
    return [p for p in pages if p.updated_at > last_synced_at]


def test_incremental_sync_selects_only_pages_updated_after_checkpoint():
    checkpoint = datetime.fromisoformat("2025-01-01T10:00:00")
    pages = [
        ConfluencePage("a", datetime.fromisoformat("2025-01-01T09:59:59")),
        ConfluencePage("b", datetime.fromisoformat("2025-01-01T10:00:01")),
        ConfluencePage("c", datetime.fromisoformat("2025-01-01T12:30:00")),
    ]

    synced = select_incremental_pages(pages, checkpoint)

    assert [page.page_id for page in synced] == ["b", "c"]


def test_incremental_sync_skips_all_pages_when_nothing_changed():
    checkpoint = datetime.fromisoformat("2025-01-01T10:00:00")
    pages = [ConfluencePage("a", datetime.fromisoformat("2025-01-01T10:00:00"))]

    synced = select_incremental_pages(pages, checkpoint)

    assert synced == []
