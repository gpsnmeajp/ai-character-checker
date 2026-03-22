#!/usr/bin/env python3
"""
ai-character-checker-all-in-one 統合スクリプト

skills/ 配下の各スキルの SKILL.md と関連ファイルを
ai-character-checker-all-in-one/references/ に決定論的にコピーし、
親 SKILL.md のマニフェストセクションを更新する。

Usage:
    python scripts/merge_all_in_one.py
    python scripts/merge_all_in_one.py --dry-run
"""

import argparse
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "skills"
ALL_IN_ONE_DIR = SKILLS_DIR / "ai-character-checker-all-in-one"
REFERENCES_DIR = ALL_IN_ONE_DIR / "references"
SKILL_MD = ALL_IN_ONE_DIR / "SKILL.md"

EXCLUDE_SKILLS = {"ai-character-checker-all-in-one", "character-checker-guide"}

CATEGORY_MAP: dict[str, str] = {
    "ai-character-6-type-checker": "統合診断",
    "character-type-checker": "単体診断",
    "ai-character-stability": "単体診断",
    "ai-self-description-analyzer": "単体診断",
    "ai-user-conflict-predictor": "単体診断",
    "character-role-analyzer": "単体診断",
    "roleplay-burden-scorer": "単体診断",
    "ai-character-fixer": "改善",
    "ai-fault-mode-deflector": "改善",
    "character-prompt-fortifier": "改善",
    "stable-character-creator": "創作",
    "character-burnout-converter": "変換",
    "character-cultural-value-checker": "特殊診断",
    "romantization-chain-detector": "特殊診断",
}

MANIFEST_START = "<!-- MANIFEST:START -->"
MANIFEST_END = "<!-- MANIFEST:END -->"


def collect_skills() -> list[Path]:
    """skills/ 配下のスキルディレクトリを収集する（ソート済み）。"""
    skills = []
    for d in sorted(SKILLS_DIR.iterdir()):
        if d.is_dir() and d.name not in EXCLUDE_SKILLS:
            skill_md = d / "SKILL.md"
            if skill_md.exists():
                skills.append(d)
    return skills


def parse_frontmatter(filepath: Path) -> dict[str, str]:
    """YAML フロントマターから name と description を抽出する。"""
    content = filepath.read_text(encoding="utf-8")
    if not content.startswith("---"):
        return {}

    end_idx = content.index("---", 3)
    frontmatter = content[3:end_idx]

    result: dict[str, str] = {}
    current_key = None
    current_lines: list[str] = []

    for line in frontmatter.split("\n"):
        # トップレベルキーの検出（インデントなし）
        key_match = re.match(r"^(\w+):\s*(.*)", line)
        if key_match:
            # 前のキーを保存
            if current_key is not None:
                result[current_key] = "\n".join(current_lines).strip()
            current_key = key_match.group(1)
            value = key_match.group(2).strip()
            if value == "|":
                current_lines = []
            else:
                current_lines = [value]
        elif current_key is not None and (line.startswith("  ") or line.startswith("\t")):
            current_lines.append(line.strip())

    # 最後のキーを保存
    if current_key is not None:
        result[current_key] = "\n".join(current_lines).strip()

    return result


def rewrite_internal_refs(content: str, skill_name: str) -> str:
    """スキル内部の references/X 参照を references/{skill_name}--X に書き換える。

    `references/` で始まるパスのうち、バッククォート内またはプレーンテキスト内の
    参照パスを書き換える。他スキルへの参照（スキル名そのもの）は書き換えない。
    """
    # バッククォート内の references/X を書き換え
    # 例: `references/output-guide.md` → `references/character-prompt-fortifier--output-guide.md`
    def replace_ref(m: re.Match) -> str:
        prefix = m.group(1)  # ` or 空
        filename = m.group(2)
        suffix = m.group(3)  # ` or 空
        return f"{prefix}references/{skill_name}--{filename}{suffix}"

    # バッククォート内のパス
    content = re.sub(
        r"(`references/)([^`]+?)(`)",
        lambda m: f"`references/{skill_name}--{m.group(2)}`",
        content,
    )
    return content


def copy_skill_files(skill_dir: Path, dry_run: bool = False) -> list[str]:
    """スキルのファイルを references/ にコピーする。"""
    skill_name = skill_dir.name
    copied: list[str] = []

    # SKILL.md → references/{skill_name}.md
    src = skill_dir / "SKILL.md"
    dst = REFERENCES_DIR / f"{skill_name}.md"

    has_refs = (skill_dir / "references").is_dir()

    if dry_run:
        print(f"  [DRY-RUN] {src.relative_to(ROOT)} → {dst.relative_to(ROOT)}")
    else:
        content = src.read_text(encoding="utf-8")
        if has_refs:
            content = rewrite_internal_refs(content, skill_name)
        dst.write_text(content, encoding="utf-8")
    copied.append(f"{skill_name}.md")

    # references/* → references/{skill_name}--{filename}
    refs_dir = skill_dir / "references"
    if refs_dir.is_dir():
        for ref_file in sorted(refs_dir.iterdir()):
            if ref_file.is_file():
                ref_dst = REFERENCES_DIR / f"{skill_name}--{ref_file.name}"
                if dry_run:
                    print(
                        f"  [DRY-RUN] {ref_file.relative_to(ROOT)} → {ref_dst.relative_to(ROOT)}"
                    )
                else:
                    shutil.copy2(ref_file, ref_dst)
                copied.append(f"{skill_name}--{ref_file.name}")

    return copied


def generate_manifest(skills: list[Path]) -> str:
    """マニフェスト（Markdown テーブル）を生成する。"""
    lines: list[str] = []
    lines.append("| カテゴリ | スキル名 | 説明 | ファイル |")
    lines.append("|---------|---------|------|---------|")

    for skill_dir in skills:
        skill_name = skill_dir.name
        skill_md = skill_dir / "SKILL.md"

        # フロントマターから説明を取得
        meta = parse_frontmatter(skill_md)
        description = meta.get("description", "").replace("\n", " ").strip()

        # カテゴリ
        category = CATEGORY_MAP.get(skill_name, "その他")

        # ファイル一覧
        files = [f"`references/{skill_name}.md`"]
        refs_dir = skill_dir / "references"
        if refs_dir.is_dir():
            for ref_file in sorted(refs_dir.iterdir()):
                if ref_file.is_file():
                    files.append(f"`references/{skill_name}--{ref_file.name}`")

        files_str = ", ".join(files)
        lines.append(f"| {category} | {skill_name} | {description} | {files_str} |")

    return "\n".join(lines)


def update_skill_md(manifest: str, dry_run: bool = False) -> None:
    """SKILL.md のマニフェストセクションを更新する。"""
    content = SKILL_MD.read_text(encoding="utf-8")

    if MANIFEST_START not in content or MANIFEST_END not in content:
        print(f"WARNING: マニフェストマーカーが {SKILL_MD.name} に見つかりません。")
        print(f"  {MANIFEST_START} と {MANIFEST_END} を SKILL.md に追加してください。")
        return

    start = content.index(MANIFEST_START)
    end = content.index(MANIFEST_END) + len(MANIFEST_END)

    new_content = (
        content[:start]
        + MANIFEST_START
        + "\n\n"
        + manifest
        + "\n\n"
        + MANIFEST_END
        + content[end:]
    )

    if dry_run:
        print(f"\n  [DRY-RUN] SKILL.md マニフェスト更新（{manifest.count(chr(10)) + 1} 行）")
    else:
        SKILL_MD.write_text(new_content, encoding="utf-8")


def clean_references(dry_run: bool = False) -> int:
    """references/ 内の既存ファイルをすべて削除する。"""
    removed = 0
    if REFERENCES_DIR.exists():
        for f in sorted(REFERENCES_DIR.iterdir()):
            if f.is_file():
                if dry_run:
                    print(f"  [DRY-RUN] 削除: {f.relative_to(ROOT)}")
                else:
                    f.unlink()
                removed += 1
    return removed


def main() -> None:
    parser = argparse.ArgumentParser(
        description="ai-character-checker-all-in-one 統合スクリプト"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="実際にファイルを変更せず、何が行われるかを表示する",
    )
    args = parser.parse_args()
    dry_run: bool = args.dry_run

    if dry_run:
        print("=== DRY RUN モード ===\n")

    # ディレクトリ準備
    if not dry_run:
        REFERENCES_DIR.mkdir(parents=True, exist_ok=True)

    # 既存ファイルのクリーン
    print("1. references/ をクリーン中...")
    removed = clean_references(dry_run)
    print(f"   {removed} ファイル削除")

    # スキル収集
    skills = collect_skills()
    print(f"\n2. {len(skills)} スキルを検出:")
    for s in skills:
        print(f"   - {s.name}")

    # ファイルコピー
    print("\n3. ファイルをコピー中...")
    total_files: list[str] = []
    for skill_dir in skills:
        files = copy_skill_files(skill_dir, dry_run)
        total_files.extend(files)
        print(f"   {skill_dir.name}: {len(files)} ファイル")

    # マニフェスト生成・更新
    print("\n4. マニフェストを生成・更新中...")
    manifest = generate_manifest(skills)
    update_skill_md(manifest, dry_run)

    # サマリー
    print(f"\n完了: {len(total_files)} ファイルを references/ にコピーしました。")
    if not dry_run:
        print("SKILL.md のマニフェストを更新しました。")


if __name__ == "__main__":
    main()
