from __future__ import annotations

from typing import List, TYPE_CHECKING

from components.base_component import BaseComponent


if TYPE_CHECKING:
    from entity import Fixture


class Information(BaseComponent):
    parent: Fixture

    def __init__(self, pages: List[str]):
        self.pages = pages
        self.idx = 0

    @property
    def text(self):
        return self.pages[self.idx]

    @property
    def total_pages(self):
        return len(self.pages)

    def clear(self):
        self.pages = []
        self.idx = 0

    def jump_to_page(self, index):
        if 0 <= index <= self.total_pages:
            self.idx = index

    def increment_next_page(self):
        self.idx = (self.idx + 1) % self.total_pages

    def increment_prev_page(self):
        self.idx = (self.idx - 1) % self.total_pages

    def add_page(self, text):
        self.pages.append(text)
