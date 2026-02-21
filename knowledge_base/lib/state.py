import json
import os
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


class BatchState:
    """Manages batch processing state via a JSON file.

    The state file (batch_state.json) tracks progress for all articles
    in a product's documentation set. It supports resume after interruption.
    """

    def __init__(self, state_path: str):
        self.state_path = state_path
        self.data: Dict[str, Any] = {}

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------

    def load(self) -> "BatchState":
        """Load state from disk. Returns self for chaining."""
        if os.path.exists(self.state_path):
            with open(self.state_path, "r", encoding="utf-8") as f:
                self.data = json.load(f)
        else:
            self.data = {}
        return self

    def save(self) -> None:
        """Persist current state to disk."""
        self.data["updated_at"] = _now_iso()
        os.makedirs(os.path.dirname(self.state_path) or ".", exist_ok=True)
        with open(self.state_path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)

    # ------------------------------------------------------------------
    # Initialization
    # ------------------------------------------------------------------

    def initialize(self, product: str, articles: List[Dict[str, Any]]) -> None:
        """Create a fresh batch state for a product.

        Args:
            product: Product slug (e.g. 'thrive_leads').
            articles: List of article dicts, each with at minimum:
                - id: str
                - title: str
                - source_file: str (path relative to knowledge_base)
                Optional:
                - source_urls: List[str]
                - merge_sources: List[dict]  (for merge tasks)
                - merge_instructions: str
        """
        self.data = {
            "product": product,
            "created_at": _now_iso(),
            "updated_at": _now_iso(),
            "total_articles": len(articles),
            "articles": [],
        }
        for art in articles:
            self.data["articles"].append({
                "id": art["id"],
                "title": art.get("title", ""),
                "source_file": art.get("source_file", ""),
                "source_urls": art.get("source_urls", []),
                "merge_sources": art.get("merge_sources", []),
                "merge_instructions": art.get("merge_instructions", ""),
                "status": "pending",
                "started_at": None,
                "completed_at": None,
                "outputs": {},
                "error": None,
                "retry_count": 0,
            })
        self.save()

    # ------------------------------------------------------------------
    # Article lookup
    # ------------------------------------------------------------------

    def _articles(self) -> List[Dict[str, Any]]:
        return self.data.get("articles", [])

    def get_article(self, article_id: str) -> Optional[Dict[str, Any]]:
        for art in self._articles():
            if art["id"] == article_id:
                return art
        return None

    def get_next_pending(self) -> Optional[Dict[str, Any]]:
        """Return the first article with status 'pending'."""
        for art in self._articles():
            if art["status"] == "pending":
                return art
        return None

    def get_failed(self) -> List[Dict[str, Any]]:
        """Return all articles with status 'failed'."""
        return [a for a in self._articles() if a["status"] == "failed"]

    # ------------------------------------------------------------------
    # Status transitions
    # ------------------------------------------------------------------

    def mark_in_progress(self, article_id: str) -> None:
        art = self.get_article(article_id)
        if art:
            art["status"] = "in_progress"
            art["started_at"] = _now_iso()
            art["error"] = None
            self.save()

    def mark_completed(self, article_id: str, outputs: Dict[str, str]) -> None:
        art = self.get_article(article_id)
        if art:
            art["status"] = "completed"
            art["completed_at"] = _now_iso()
            art["outputs"] = outputs
            art["error"] = None
            self.save()

    def mark_failed(self, article_id: str, error: str) -> None:
        art = self.get_article(article_id)
        if art:
            art["status"] = "failed"
            art["error"] = error
            art["retry_count"] = art.get("retry_count", 0) + 1
            self.save()

    def mark_skipped(self, article_id: str) -> None:
        art = self.get_article(article_id)
        if art:
            art["status"] = "skipped"
            self.save()

    def reset_failed_to_pending(self) -> int:
        """Reset all failed articles back to pending. Returns count reset."""
        count = 0
        for art in self._articles():
            if art["status"] == "failed":
                art["status"] = "pending"
                art["error"] = None
                count += 1
        if count:
            self.save()
        return count

    # ------------------------------------------------------------------
    # Progress
    # ------------------------------------------------------------------

    def get_progress_summary(self) -> Dict[str, int]:
        articles = self._articles()
        summary = {"total": len(articles), "pending": 0, "in_progress": 0, "completed": 0, "failed": 0, "skipped": 0}
        for art in articles:
            status = art.get("status", "pending")
            if status in summary:
                summary[status] += 1
        return summary

    def can_resume(self) -> bool:
        """True if there are pending or failed articles."""
        return any(a["status"] in ("pending", "failed") for a in self._articles())

    def print_status(self) -> None:
        """Print a human-readable progress report."""
        s = self.get_progress_summary()
        product = self.data.get("product", "unknown")
        print(f"\n{'='*50}")
        print(f"  Batch Status: {product}")
        print(f"{'='*50}")
        print(f"  Total:       {s['total']}")
        print(f"  Completed:   {s['completed']}")
        print(f"  Pending:     {s['pending']}")
        print(f"  In Progress: {s['in_progress']}")
        print(f"  Failed:      {s['failed']}")
        print(f"  Skipped:     {s['skipped']}")
        pct = (s["completed"] / s["total"] * 100) if s["total"] > 0 else 0
        print(f"  Progress:    {pct:.0f}%")
        print(f"{'='*50}\n")

        # Show failed articles if any
        for art in self._articles():
            if art["status"] == "failed":
                print(f"  FAILED: {art['id']} — {art.get('error', 'unknown error')}")


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()
