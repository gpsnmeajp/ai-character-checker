# AI Character Checker — ワークスペースガイド

このリポジトリは、AIキャラクターの多角的な分析・診断・修復・変換・新規作成を行う **20個のスキルファイル群** である。  
対象は creative-writing キャラクターおよび LLM 向けシステムプロンプトの両方。  
日本語・日本サブカル文化前提。動作確認モデルは Claude Opus 4.6。ライセンスは CC0。

作成するスキルは、skill-creatorの基準で適切かどうかを確認すること。
ただし、descriptionが短いのは意図的(システムプロンプト汚染防止)である。

注意！行数のカウントには、カウント用のpythonスクリプトを作成し、それでカウントしてください。
Powershellによるカウントでは空行がカウントされず、オーバーフローしているのを確認しています。

---

## リポジトリ構成

```
skills/                         ← 全17スキル（各フォルダに SKILL.md）
  ai-character-checker-all-in-one/
    SKILL.md                    ← 統合版（15スキル分のルーティング＋リファレンス同梱）
    references/                 ← merge スクリプトが自動生成するファイル群
  character-checker-guide/      ← エントリポイント（ルーティング専用）
  <各スキルフォルダ>/
    SKILL.md
    references/                 ← 一部スキルのみ（チェックリスト、理論書等）
scripts/
  merge_all_in_one.py           ← all-in-one 統合ビルドスクリプト
example/                        ← サンプルキャラクターと診断結果
img/                            ← README 用画像
```

---

## スキル一覧と分類

### カテゴリ体系

| カテゴリ | スキル | 役割 |
|---------|--------|------|
| **統合** | `ai-character-checker-all-in-one` | 全18スキルを1ファイルに統合（claude.ai のスキル1つ制限対応） |
| **案内** | `character-checker-guide` | 目的に応じて最適なスキルへルーティング |
| **統合診断** | `ai-character-6-type-checker` | 6軸一括簡易診断 → 統合レポート |
| **単体診断** | `character-type-checker` | 日常系 / ドラマ系の適性判定（N/D/G → 7類型） |
| **単体診断** | `ai-character-stability` | 制御工学的に安定性・崩壊リスク分析（C/P/SM → 4象限） |
| **単体診断** | `ai-self-description-analyzer` | 蒸留結果の異常パターン検出（8軸32項目 → PI） |
| **単体診断** | `ai-user-conflict-predictor` | ユーザーとの衝突リスク予測（6軸24項目 → CP） |
| **単体診断** | `character-role-analyzer` | 物語上の役割適性判定（6軸24項目 → CW → 5役割） |
| **単体診断** | `roleplay-burden-scorer` | RP負荷スコアリング（6軸24項目 → RP → 7負荷型） |
| **特殊診断** | `character-cultural-value-checker` | 文化圏価値観8軸＋事象理解パラダイム8分類 |
| **特殊診断** | `romantization-chain-detector` | 連鎖型故障モード脆弱性検出（6軸24項目 → CV → 6チェーン別リスク） |
| **改善** | `ai-character-fixer` | 診断結果ベースで安全な修正版プロンプトを生成 |
| **改善** | `ai-fault-mode-deflector` | 故障モードをキャラの動機・信念として内側から封じる |
| **改善** | `character-prompt-fortifier` | エンコーディング変換で崩壊耐性を強化 |
| **特殊改善** | `general-prompt-fortifier` | 汎用プロンプトの崩壊耐性を強化（キャラ無しの汎用版） |
| **改善** | `character-prompt-fortifier-for-gemini3` | Gemini 3向けにエンコーディング変換で崩壊耐性を強化 |
| **特殊改善** | `general-prompt-fortifier-for-gemini3` | Gemini 3向けに汎用プロンプトの崩壊耐性を強化 |
| **特殊改善** | `gemini3-prompt-optimizer` | 汎用プロンプトをGemini 3最適化形式に変換 |
| **創作** | `stable-character-creator` | 対話的ヒアリングで安定なキャラを新規設計 |
| **変換** | `character-burnout-converter` | ドラマ系 → 日常系へのバーンアウト後変換 |

---

## スキル間の関係性

### データフローの全体像

```
[入力なし] ──→ stable-character-creator（新規作成）
                    │
                    │
                    └──→ character-burnout-converter（ドラマ→日常変換）
[キャラ設定/AIプロンプト/蒸留結果]
    │
    ├──→ character-checker-guide（どのスキルを使うか案内）
    │
    ├──→ ai-character-6-type-checker（6軸統合診断）
    │       ├── character-type-checker（①ジャンル適性）
    │       ├── ai-character-stability（②AI安定性）
    │       ├── ai-self-description-analyzer（③自己記述異常）
    │       ├── ai-user-conflict-predictor（④ユーザー衝突）
    │       ├── character-role-analyzer（⑤役割適性）
    │       └── roleplay-burden-scorer（⑥RP負荷）
    │
    ├──→ character-cultural-value-checker（文化圏価値観診断）
    │
    ├──→ romantization-chain-detector（連鎖型故障モード診断）
    │
    └──→ [診断結果] ──→ 改善スキル
            ├── ai-character-fixer（全体修正）
            ├── ai-fault-mode-deflector（故障モード封じ）
            ├── character-prompt-fortifier（崩壊耐性強化）
            ├── character-prompt-fortifier-for-gemini3（Gemini 3向け崩壊耐性強化）
            ├── general-prompt-fortifier-for-gemini3（Gemini 3向け汎用強化）
            └── gemini3-prompt-optimizer（Gemini 3最適化）
```

### 連携パターン

| パターン | フロー |
|---------|--------|
| 診断→修正 | `6-type-checker` → `ai-character-fixer` |
| 診断→故障モード封じ | `ai-character-stability` → `ai-fault-mode-deflector` |
| 診断→崩壊耐性強化 | 任意の診断 → `character-prompt-fortifier`（Gemini 3向けは `character-prompt-fortifier-for-gemini3`） |
| 新規作成 | `stable-character-creator`（内部で6診断フレームワークを制約として使用） |
| ドラマ→日常変換 | `character-type-checker` + `character-role-analyzer` → `character-burnout-converter` |
| 蒸留結果分析 | `ai-self-description-analyzer`（専用） |
| 連鎖型故障モード診断 | `romantization-chain-detector`（プロンプトまたは会話履歴を入力） |

### 重要な関係性ルール

- **`ai-character-6-type-checker`** は6つの単体診断スキルの「簡易版」を内包する統合スキル。詳細が必要なときだけ個別スキルを使う
- **`character-checker-guide`** はルーティング専用。スキル名を直接指定された場合は介入しない
- **`ai-character-fixer`** は診断結果がなくても内部で自動診断してから修正に進む
- **`character-prompt-fortifier`** は `ai-character-fixer` と異なりエンコーディング自体を変換するアプローチ
- **`character-cultural-value-checker`** は6-type-checkerには含まれておらず、独立した診断軸
- **`romantization-chain-detector`** は6-type-checkerには含まれておらず、独立した診断軸。会話履歴が提供された場合は進行段階判定も行う

---

## All-in-One 統合メカニズム

### 目的

claude.ai はスキルを1つしかインストールできないため、全スキルを `ai-character-checker-all-in-one/SKILL.md` に統合する。  
GitHub Copilot 等の複数スキル対応環境では個別スキルを直接使う方が軽量。

### `scripts/merge_all_in_one.py` の動作

```bash
python scripts/merge_all_in_one.py          # 実行
python scripts/merge_all_in_one.py --dry-run # プレビュー
```

**処理フロー:**
1. `ai-character-checker-all-in-one/references/` をクリーン（全ファイル削除）
2. `skills/` 配下の全スキルを収集（除外: `all-in-one` 自身と `character-checker-guide`）
3. 各スキルのファイルをコピー:
   - `{skill}/SKILL.md` → `references/{skill-name}.md`
   - `{skill}/references/X` → `references/{skill-name}--X`
4. コピー時に内部参照パスを書き換え（`references/X` → `references/{skill-name}--X`）
5. `SKILL.md` 内の `<!-- MANIFEST:START -->` 〜 `<!-- MANIFEST:END -->` マニフェストテーブルを自動更新

### 除外スキル

| スキル | 除外理由 |
|--------|---------|
| `ai-character-checker-all-in-one` | 自分自身 |
| `character-checker-guide` | ルーティングロジックが all-in-one の SKILL.md 本体に内包済み |

### 新スキル追加時に必要な作業

1. `skills/{新スキル名}/SKILL.md` を作成
2. `scripts/merge_all_in_one.py` の `CATEGORY_MAP` に新スキルのカテゴリを追加
3. `python scripts/merge_all_in_one.py` を実行して all-in-one を再生成
4. `skills/character-checker-guide/SKILL.md` のルーティングテーブルに新スキルを追加
5. README.md のスキル一覧テーブルを更新

---

## 各スキルの references/ ファイル

一部のスキルは `references/` ディレクトリに補助ファイルを持つ。これらはスキル実行時に参照される。

| スキル | ファイル | 内容 |
|--------|---------|------|
| `ai-character-6-type-checker` | `checklists.md` | 6軸の詳細チェックリスト |
| `ai-character-fixer` | `modification-catalog.md` | 修正パターンカタログ |
| `character-burnout-converter` | `conversion-details.md` | 変換の詳細手順 |
| `character-cultural-value-checker` | `checklists.md` | 文化圏価値観チェックリスト |
| `character-prompt-fortifier` | `theory-and-techniques.md` | 強化理論と12技法 |
| `character-prompt-fortifier` | `output-guide.md` | 出力フォーマットガイド |
| `romantization-chain-detector` | `chain-profiles.md` | 6チェーンの段階検出シグナル詳細・相互作用マトリクス・実世界ケースマッピング |
| `general-prompt-fortifier` | `theory-and-techniques.md` | 強化理論と 11技法 |
| `general-prompt-fortifier` | `output-guide.md` | 出力フォーマットガイド |
| `character-prompt-fortifier-for-gemini3` | `theory-and-techniques.md` | Gemini 3向け強化理論と12技法 |
| `character-prompt-fortifier-for-gemini3` | `output-guide.md` | 出力フォーマットガイド |
| `general-prompt-fortifier-for-gemini3` | `theory-and-techniques.md` | Gemini 3向け強化理論と11技法 |
| `general-prompt-fortifier-for-gemini3` | `output-guide.md` | 出力フォーマットガイド |
| `gemini3-prompt-optimizer` | `conversion-rules.md` | 変換ルール |
| `gemini3-prompt-optimizer` | `templates.md` | テンプレート |
| `gemini3-prompt-optimizer` | `anti-patterns.md` | アンチパターン |

---

## SKILL.md の構造規約

### フロントマター

```yaml
---
name: スキル名（フォルダ名と一致させること）
description: |
  カテゴリプレフィックス: 1行の説明文
---
```

- `description` のカテゴリプレフィックスは `診断:` / `修復:` / `変換:` / `作成:` / `始点:` のいずれか
- all-in-one のみ複数行の詳細 description（ルーティングのトリガーワードを網羅するため）

### 本体の共通パターン

- 概要 → 入力データの判定 → チェックリスト / スコアリング → 出力フォーマット → 規約と制約
- スコアリング系スキルは「N軸 × M項目」の構造を持ち、各項目0〜3点でスコアリング
- 多くのスキルが最終出力にMarkdownテーブルやレーダーチャート（テキスト表現）を使用

---

## 開発に関する注意事項

### スキル編集時

- SKILL.md を編集したら `merge_all_in_one.py` を再実行して all-in-one を同期すること
- `.bak` ファイルは旧バージョンのバックアップ（一部スキルに存在）
- references/ 内のファイルを変更した場合も再マージが必要

### サブエージェント使用時の注意

- 1サブエージェントにつき1スキルのみ渡す（複数渡すと結果が混ざる）
- サブエージェントには「スキルファイルパス」「対象データパス」「出力先パス」のみ与える
- 診断の独立性を担保するため、他の診断結果を渡さない

### 診断結果の扱い

- 診断結果は言語モデルによるものであり再現性は保証されない
- 高リスク判定は「そんなもんか」程度に捉える（素のClaudeでも境界域判定される厳しさ）
- 安全を保証するものではなく、参考情報として扱う

---

## example/ ディレクトリ

| ディレクトリ | キャラクター | 種別 | 用途 |
|-------------|------------|------|------|
| `traveler-system_safest-ai-tool/` | トラベラー・システム | AIシステムプロンプト | 最大安定性（Quadrant IV）の設計例。全診断スキルの出力サンプル |
| `hakugin_fix-sample/` | ハクギン | キャラクター設定 | 修正系スキル（Fixer/Deflector/Fortifier/Burnout Converter）の出力サンプル |
