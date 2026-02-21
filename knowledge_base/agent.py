import os
import glob
from typing import Dict, List, Optional

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

try:
    import anthropic as _anthropic_mod
except ImportError:
    _anthropic_mod = None

# Default Ollama endpoint (no API key required)
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")

# Default models per provider
DEFAULT_MODELS = {
    "openai": "gpt-4o",
    "anthropic": "claude-sonnet-4-5-20250929",
    "ollama": OLLAMA_MODEL,
}


class DocumentationAgent:
    def __init__(
        self,
        knowledge_base_dir: str,
        api_key: Optional[str] = None,
        *,
        base_url: Optional[str] = None,
        model: Optional[str] = None,
        provider: str = "auto",
        include_patterns: Optional[List[str]] = None,
    ):
        self.knowledge_base_dir = knowledge_base_dir
        self.context = self._load_knowledge_base(include_patterns)
        self.provider = self._resolve_provider(provider, api_key, base_url)
        self.model = model or DEFAULT_MODELS.get(self.provider, "gpt-4o")

        # Initialize the appropriate client
        if self.provider == "anthropic":
            key = api_key or os.getenv("ANTHROPIC_API_KEY", "")
            if _anthropic_mod and key:
                self.anthropic_client = _anthropic_mod.Anthropic(api_key=key)
                self.client = None
                print(f"Using Anthropic API (model: {self.model})")
            else:
                self.anthropic_client = None
                self.client = None
                print("Warning: anthropic package not installed or ANTHROPIC_API_KEY not set.")
        elif self.provider == "openai":
            key = api_key or os.getenv("OPENAI_API_KEY", "")
            if OpenAI and key:
                self.client = OpenAI(api_key=key, base_url=base_url or None)
                self.anthropic_client = None
                print(f"Using OpenAI API (model: {self.model})")
            else:
                self.client = None
                self.anthropic_client = None
                print("Warning: openai package not installed or OPENAI_API_KEY not set.")
        elif self.provider == "ollama":
            ollama_url = base_url or os.getenv("OLLAMA_BASE_URL", OLLAMA_BASE_URL)
            if OpenAI:
                self.client = OpenAI(api_key="ollama", base_url=ollama_url.rstrip("/"))
                self.anthropic_client = None
                print(f"Using Ollama at {ollama_url} (model: {self.model})")
            else:
                self.client = None
                self.anthropic_client = None
                print("Warning: openai package not installed (needed for Ollama compatibility).")
        else:
            self.client = None
            self.anthropic_client = None
            print(f"Warning: Unknown provider '{self.provider}'.")

    @staticmethod
    def _resolve_provider(provider: str, api_key: Optional[str], base_url: Optional[str]) -> str:
        if provider != "auto":
            return provider
        if api_key and "anthropic" in api_key.lower()[:10]:
            return "anthropic"
        if os.getenv("ANTHROPIC_API_KEY"):
            return "anthropic"
        if api_key or os.getenv("OPENAI_API_KEY"):
            return "openai"
        if base_url or os.getenv("OLLAMA_BASE_URL"):
            return "ollama"
        return "ollama"

    def _load_knowledge_base(self, include_patterns: Optional[List[str]] = None) -> str:
        """Loads markdown files from the knowledge base directory.

        Args:
            include_patterns: If provided, only load files matching these glob
                patterns (relative to knowledge_base_dir). If None, loads all
                top-level *.md files.
        """
        context_parts = []

        if include_patterns:
            files = []
            for pat in include_patterns:
                files.extend(glob.glob(os.path.join(self.knowledge_base_dir, pat)))
            files = sorted(set(files))
        else:
            files = glob.glob(os.path.join(self.knowledge_base_dir, "*.md"))

        print(f"Loading {len(files)} files from knowledge base...")

        for file_path in files:
            if os.path.basename(file_path).startswith("rewritten_"):
                continue

            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                filename = os.path.basename(file_path)
                context_parts.append(f"--- START FILE: {filename} ---\n{content}\n--- END FILE: {filename} ---\n")

        return "\n".join(context_parts)

    def construct_system_prompt(self) -> str:
        """Builds the system prompt using the loaded knowledge base."""
        base_prompt = """You are an expert technical documentation writer for OptinMonster and Thrive Themes.
Your task is to rewrite documentation based on the following Knowledge Base rules and guides.

CONTEXT FROM KNOWLEDGE BASE:
{context}

INSTRUCTIONS:
1. Read the user-provided source documentation carefully.
2. Rewrite it following ALL rules in the "Documentation Master Guide" and other attached files.
3. You must produce FOUR distinct outputs, separating them clearly.
    - Output 1: The rewritten markdown file.
    - Output 2: A mapping table for images (Image ID, Description, Alt Text).
    - Output 3: A review report.
    - Output 4: A screenshot spec (JSON) for headless screenshot capture: one entry per image in the image mapping, with image_id, url (WP admin path or full URL), and optional steps (click/wait/fill), selector, full_page. Use the schema in docs/screenshot_spec_schema.md: base_url, captures array with image_id, url, steps, selector, full_page. Do not include login credentials; use placeholder base_url (e.g. https://staging.example.com).

FORMAT YOUR RESPONSE EXACTLY AS FOLLOWS using these separators:
<<<START_REWRITTEN_DOC>>>
[Markdown content here]
<<<END_REWRITTEN_DOC>>>

<<<START_IMAGE_MAPPING>>>
[Image mapping content here]
<<<END_IMAGE_MAPPING>>>

<<<START_REVIEW_REPORT>>>
[Review content here]
<<<END_REVIEW_REPORT>>>

<<<START_SCREENSHOT_SPEC>>>
[JSON screenshot spec: {{"base_url": "...", "captures": [{{"image_id": "...", "url": "...", "steps": [], "selector": "...", "full_page": false}}, ...]}}]
<<<END_SCREENSHOT_SPEC>>>
"""
        return base_prompt.format(context=self.context)

    def _call_llm(self, system_prompt: str, user_message: str) -> str:
        """Send a request to the configured LLM provider and return the text response."""
        if self.provider == "anthropic" and self.anthropic_client:
            response = self.anthropic_client.messages.create(
                model=self.model,
                max_tokens=8192,
                system=system_prompt,
                messages=[{"role": "user", "content": user_message}],
                temperature=0.7,
            )
            return response.content[0].text
        elif self.client:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message},
                ],
                temperature=0.7,
            )
            return response.choices[0].message.content
        else:
            raise RuntimeError("No LLM client configured. Set ANTHROPIC_API_KEY, OPENAI_API_KEY, or OLLAMA_BASE_URL.")

    def process_document(self, source_content: str) -> Dict[str, str]:
        """Sends the source content to the LLM and parses the response."""
        system_prompt = self.construct_system_prompt()
        user_message = f"Please rewrite the following documentation:\n\n{source_content}"

        try:
            full_response = self._call_llm(system_prompt, user_message)
            return self._parse_response(full_response)
        except Exception as e:
            return {"error": str(e)}

    def process_merge(
        self,
        source_contents: List[Dict[str, str]],
        target_title: str,
        merge_instructions: str = "",
    ) -> Dict[str, str]:
        """Merge multiple source documents into a single rewritten document.

        Args:
            source_contents: List of dicts with 'title' and 'content' keys.
            target_title: The desired title for the merged output.
            merge_instructions: Additional instructions for the merge (e.g.,
                what to prune, how to structure sections).
        """
        system_prompt = self.construct_system_prompt()

        combined = "\n\n".join(
            f"--- SOURCE ARTICLE: {s['title']} ---\n{s['content']}\n--- END SOURCE ---"
            for s in source_contents
        )
        user_message = (
            f"MERGE TASK: Combine the following {len(source_contents)} source articles "
            f"into a single comprehensive guide titled \"{target_title}\".\n\n"
        )
        if merge_instructions:
            user_message += f"MERGE INSTRUCTIONS:\n{merge_instructions}\n\n"
        user_message += combined

        try:
            full_response = self._call_llm(system_prompt, user_message)
            return self._parse_response(full_response)
        except Exception as e:
            return {"error": str(e)}

    def _parse_response(self, response_text: str) -> Dict[str, str]:
        """Extracts the four parts from the LLM response."""
        results = {}

        def extract(tag_name):
            start_tag = f"<<<START_{tag_name}>>>"
            end_tag = f"<<<END_{tag_name}>>>"
            start_idx = response_text.find(start_tag)
            end_idx = response_text.find(end_tag)

            if start_idx != -1 and end_idx != -1:
                return response_text[start_idx + len(start_tag):end_idx].strip()
            return ""

        results["rewritten_doc.md"] = extract("REWRITTEN_DOC")
        results["image_mapping.md"] = extract("IMAGE_MAPPING")
        results["review.md"] = extract("REVIEW_REPORT")
        results["screenshot_spec.json"] = _normalize_screenshot_spec(extract("SCREENSHOT_SPEC"))

        # Fallback if parsing fails
        if not results["rewritten_doc.md"]:
            results["rewritten_doc_fallback.md"] = response_text

        return results


def _normalize_screenshot_spec(raw: str) -> str:
    """Strip markdown code fences from screenshot spec block and return JSON string."""
    if not raw:
        return ""
    text = raw.strip()
    if text.startswith("```"):
        lines = text.split("\n")
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        text = "\n".join(lines)
    return text


if __name__ == "__main__":
    # Test loading
    agent = DocumentationAgent(".", provider="auto")
    print("System Prompt Preview (first 500 chars):")
    print(agent.construct_system_prompt()[:500])
