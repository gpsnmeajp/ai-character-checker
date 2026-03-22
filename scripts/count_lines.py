"""Count lines in all SKILL.md and reference files (including empty lines)."""
import os
import sys

SKILLS_DIR = os.path.join(os.path.dirname(__file__), "..", "skills")

def count_lines(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return sum(1 for _ in f)

def main():
    results = []
    for skill_name in sorted(os.listdir(SKILLS_DIR)):
        skill_dir = os.path.join(SKILLS_DIR, skill_name)
        if not os.path.isdir(skill_dir):
            continue
        skill_md = os.path.join(skill_dir, "SKILL.md")
        if os.path.isfile(skill_md):
            lines = count_lines(skill_md)
            flag = " *** OVER 500 ***" if lines > 500 else ""
            results.append((f"skills/{skill_name}/SKILL.md", lines, flag))
        refs_dir = os.path.join(skill_dir, "references")
        if os.path.isdir(refs_dir):
            for ref_name in sorted(os.listdir(refs_dir)):
                ref_path = os.path.join(refs_dir, ref_name)
                if os.path.isfile(ref_path):
                    lines = count_lines(ref_path)
                    flag = " (>300, needs TOC?)" if lines > 300 else ""
                    results.append((f"skills/{skill_name}/references/{ref_name}", lines, flag))

    print(f"{'File':<75} {'Lines':>6}  Notes")
    print("-" * 100)
    for path, lines, flag in results:
        print(f"{path:<75} {lines:>6}  {flag}")

if __name__ == "__main__":
    main()
