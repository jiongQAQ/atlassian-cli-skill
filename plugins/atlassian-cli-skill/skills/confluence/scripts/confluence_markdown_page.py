#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import subprocess
import sys
import tempfile
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
RUNNER = SCRIPT_DIR / "run_atlassian_cli.sh"
H1_PATTERN = re.compile(r"^\s*#\s+(.+?)\s*$")


def read_markdown(markdown_file: Path) -> tuple[str | None, str]:
    text = markdown_file.read_text(encoding="utf-8")
    lines = text.splitlines()

    index = 0
    while index < len(lines) and not lines[index].strip():
        index += 1

    derived_title = None
    if index < len(lines):
        match = H1_PATTERN.match(lines[index])
        if match:
            derived_title = match.group(1).strip()
            index += 1

    body_lines = lines[index:]
    while body_lines and not body_lines[0].strip():
        body_lines.pop(0)
    body = "\n".join(body_lines).rstrip()
    if body:
        body += "\n"
    return derived_title, body


def build_command(args: argparse.Namespace, body_file: Path, title: str) -> list[str]:
    command = [str(RUNNER), "confluence", "page", args.action]

    if args.action == "update":
        command.append(args.page_id)

    if args.action == "create":
        command.extend(["--space-key", args.space_key])

    command.extend(["--title", title, "--body-file", str(body_file), "--body-format", args.body_format])

    if args.parent_id:
        command.extend(["--parent-id", args.parent_id])
    if args.minor_edit and args.action == "update":
        command.append("--minor-edit")
    if args.version_comment and args.action == "update":
        command.extend(["--version-comment", args.version_comment])
    if args.enable_heading_anchors:
        command.append("--enable-heading-anchors")
    if args.emoji:
        command.extend(["--emoji", args.emoji])
    if args.page_width:
        command.extend(["--page-width", args.page_width])
    if args.json:
        command.append("--json")
    return command


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Create or update a Confluence page from a Markdown file."
    )
    subparsers = parser.add_subparsers(dest="action", required=True)

    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--title", help="Explicit page title. Defaults to the first H1.")
    common.add_argument(
        "--body-format",
        choices=("markdown", "wiki", "storage"),
        default="markdown",
        help="Body format passed to atlassian-cli.",
    )
    common.add_argument("--parent-id", help="Parent page ID.")
    common.add_argument("--enable-heading-anchors", action="store_true")
    common.add_argument("--emoji", help="Page emoji.")
    common.add_argument(
        "--page-width",
        choices=("full-width", "max", "default"),
        help="Confluence page width.",
    )
    common.add_argument("--json", action="store_true", help="Emit machine JSON.")
    common.add_argument("--dry-run", action="store_true", help="Print the final CLI command only.")

    create_parser = subparsers.add_parser("create", parents=[common], help="Create a page.")
    create_parser.add_argument("markdown_file", type=Path, help="Markdown file to upload.")
    create_parser.add_argument("--space-key", required=True, help="Confluence space key.")

    update_parser = subparsers.add_parser("update", parents=[common], help="Update a page.")
    update_parser.add_argument("page_id", help="Confluence page ID.")
    update_parser.add_argument("markdown_file", type=Path, help="Markdown file to upload.")
    update_parser.add_argument("--minor-edit", action="store_true")
    update_parser.add_argument("--version-comment", help="Version comment.")

    return parser


def main() -> int:
    parser = create_parser()
    args = parser.parse_args()

    if not RUNNER.exists():
        parser.error(f"Missing runner script: {RUNNER}")

    markdown_file = args.markdown_file
    if not markdown_file.exists():
        parser.error(f"Markdown file not found: {markdown_file}")

    derived_title, body = read_markdown(markdown_file)
    title = args.title or derived_title
    if not title:
        parser.error("Page title is required. Add --title or start the Markdown with an H1.")

    with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".md", delete=False) as handle:
        body_file = Path(handle.name)
        handle.write(body)

    command = build_command(args, body_file, title)
    if args.dry_run:
        print(" ".join(command))
        body_file.unlink(missing_ok=True)
        return 0

    try:
        completed = subprocess.run(command, check=False)
        return completed.returncode
    finally:
        body_file.unlink(missing_ok=True)


if __name__ == "__main__":
    sys.exit(main())
