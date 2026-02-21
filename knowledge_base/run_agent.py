import sys
import os
import argparse
from agent import DocumentationAgent
from dotenv import load_dotenv


def main():
    load_dotenv()

    parser = argparse.ArgumentParser(description="Run the documentation rewrite agent.")
    parser.add_argument("source_file", help="Path to the source markdown file to rewrite.")
    parser.add_argument(
        "--provider",
        choices=["auto", "anthropic", "openai", "ollama"],
        default="auto",
        help="LLM provider to use (default: auto-detect from env vars).",
    )
    parser.add_argument("--model", default=None, help="Override the LLM model name.")
    parser.add_argument("--output-dir", default=None, help="Output directory (default: same dir as source file).")
    args = parser.parse_args()

    source_file = args.source_file
    if not os.path.exists(source_file):
        print(f"Error: File '{source_file}' not found.")
        sys.exit(1)

    # Assume knowledge base is in the same directory as this script
    kb_dir = os.path.dirname(os.path.abspath(__file__))

    # Determine API key based on provider
    api_key = None
    base_url = None
    if args.provider == "anthropic" or (args.provider == "auto" and os.getenv("ANTHROPIC_API_KEY")):
        api_key = os.getenv("ANTHROPIC_API_KEY")
    elif args.provider == "openai" or (args.provider == "auto" and os.getenv("OPENAI_API_KEY")):
        api_key = os.getenv("OPENAI_API_KEY")
    elif args.provider == "ollama" or args.provider == "auto":
        base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")

    agent = DocumentationAgent(
        knowledge_base_dir=kb_dir,
        api_key=api_key,
        base_url=base_url,
        model=args.model,
        provider=args.provider,
    )

    print(f"Initializing agent with Knowledge Base from: {kb_dir}")

    print(f"Reading source file: {source_file}")
    with open(source_file, 'r', encoding='utf-8') as f:
        source_content = f.read()

    print("Processing document (this may take a minute)...")
    outputs = agent.process_document(source_content)

    if "error" in outputs:
        print(f"Error: {outputs['error']}")
        return

    # Write outputs
    output_dir = args.output_dir or os.path.dirname(source_file)
    os.makedirs(output_dir, exist_ok=True)
    for filename, content in outputs.items():
        if content:
            out_path = os.path.join(output_dir, filename)
            with open(out_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Generated: {out_path}")
        else:
            print(f"Warning: {filename} was empty.")


if __name__ == "__main__":
    main()
