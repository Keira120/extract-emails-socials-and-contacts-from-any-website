thonfrom collections import deque
from dataclasses import dataclass, field
from typing import Deque, Iterable, Set, Tuple

@dataclass
class PageQueue:
    """
    Simple breadth-first queue with a visited set and depth tracking.

    Items are (url, depth) tuples.
    """

    queue: Deque[Tuple[str, int]] = field(default_factory=deque)
    visited: Set[str] = field(default_factory=set)

    def push(self, url: str, depth: int) -> None:
        if url in self.visited:
            return
        self.queue.append((url, depth))
        self.visited.add(url)

    def push_many(self, urls: Iterable[str], depth: int) -> None:
        for url in urls:
            self.push(url, depth)

    def pop(self) -> Tuple[str, int] | None:
        if not self.queue:
            return None
        return self.queue.popleft()

    def __len__(self) -> int:
        return len(self.queue)