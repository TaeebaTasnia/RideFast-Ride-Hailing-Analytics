"""
Export all Mermaid charts from problem_statement.md and problem_statement_2.md as PNGs.
Output directory: e:/pathao/chart_pngs/
Requires: @mermaid-js/mermaid-cli (npm install -g @mermaid-js/mermaid-cli)
"""

import re
import subprocess
import sys
import os
from pathlib import Path

OUTPUT_DIR = Path("E:/pathao/chart_pngs")
OUTPUT_DIR.mkdir(exist_ok=True)

SOURCE_FILES = {
    "ps1": Path("E:/pathao/problem_statement.md"),
    "ps2": Path("E:/pathao/problem_statement_2.md"),
}

MERMAID_BLOCK = re.compile(r"```mermaid\n(.*?)```", re.DOTALL)


def extract_charts(filepath):
    text = filepath.read_text(encoding="utf-8")
    return MERMAID_BLOCK.findall(text)


def render_chart(mermaid_src: str, output_path: Path):
    # Write temp .mmd file
    tmp = output_path.with_suffix(".mmd")
    tmp.write_text(mermaid_src.strip(), encoding="utf-8")

    # On Windows, mmdc is a .cmd script — use shell=True or the .cmd path
    mmdc = r"C:\Users\ASUS\AppData\Roaming\npm\mmdc.cmd"
    result = subprocess.run(
        [mmdc, "-i", str(tmp), "-o", str(output_path), "-b", "white", "-w", "900", "-H", "500"],
        capture_output=True,
        text=True,
        shell=False,
    )

    tmp.unlink(missing_ok=True)

    if result.returncode != 0:
        print(f"  ERROR: {result.stderr.strip()[:200]}")
        return False
    return True


def main():
    total = 0
    success = 0

    for prefix, filepath in SOURCE_FILES.items():
        if not filepath.exists():
            print(f"File not found: {filepath}")
            continue

        charts = extract_charts(filepath)
        print(f"\n{filepath.name} — {len(charts)} Mermaid charts found")

        for i, chart_src in enumerate(charts, 1):
            # Derive a name from the first content line
            first_line = chart_src.strip().splitlines()[0].strip().lstrip("%").strip()
            slug = re.sub(r"[^\w]+", "_", first_line)[:40].strip("_").lower()
            name = f"{prefix}_chart{i:02d}_{slug}.png"
            out_path = OUTPUT_DIR / name

            print(f"  [{i}] {name} ...", end=" ", flush=True)
            total += 1

            ok = render_chart(chart_src, out_path)
            if ok:
                size_kb = out_path.stat().st_size // 1024 if out_path.exists() else 0
                print(f"OK ({size_kb} KB)")
                success += 1
            else:
                print("FAILED")

    print(f"\nDone: {success}/{total} charts exported to {OUTPUT_DIR}")
    if success < total:
        sys.exit(1)


if __name__ == "__main__":
    main()
