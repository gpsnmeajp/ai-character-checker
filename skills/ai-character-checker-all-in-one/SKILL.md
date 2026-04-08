---
name: ai-character-checker-all-in-one
description: |
  AIキャラクターの分析・診断・修復・変換・作成の統合オールインワンスキル。キャラクター設定、AIプロンプト、蒸留結果の分析、修正、強化、新規作成をすべてカバーする。「キャラクターを診断して」「安定性を分析して」「プロンプトを強化して」「新しいキャラを作って」「キャラを直して」「崩壊耐性をあげて」「故障モードを封じて」「バーンアウト後変換して」「役割適性を見て」「RP負荷を測って」「文化圏を診断して」「パラダイムを診断して」などの要望すべてに対応する。スキル名を直接指定された場合も対応する。
---

# AI Character Checker All-in-One

## 概要

このスキルは、AIキャラクターに関する **13の専門スキル** を1つに統合したオールインワンスキルである。
各スキルの詳細な手順・理論は `references/` ディレクトリ内のファイルに格納されている。

なお、各スキルの分析フレームワーク・用語・スコアリング体系は作者独自の仮説的モデルに基づくものであり、学術的・科学的に実証されたものではない。工学的用語は概念の借用であり、元の定義とは異なる場合がある。各スキルの結果は参考情報として扱うこと。この旨をユーザーへの出力に含めること。

---

## 動作フロー

### Step 1: 状況を把握する

ユーザーのメッセージと添付ファイルを確認し、以下の2点を判定する。

**A. 手元に何があるか（入力データの種類）**

| データ種別 | 判定の目安 |
|-----------|----------|
| **キャラクター設定（創作向け）** | 性格・外見・バックストーリーなどの文章的設定 |
| **AIプロンプト（システムプロンプト）** | AIに与えるための指示書形式のテキスト |
| **蒸留結果（AI自己記述）** | AIが実際にそのキャラを演じた後の自己紹介・自己説明文 |
| **何もない** | データが提供されていない |

**B. 何をしたいか（目的）**

| 目的カテゴリ | 具体的な発言例 |
|------------|-------------|
| **診断** | 「分析して」「診断して」「どんなキャラか見て」「危ないか確認して」|
| **修正・改善** | 「直して」「安定させて」「より良くして」「崩壊しないようにして」|
| **新規作成** | 「キャラを作って」「新しいAIキャラを設計して」|
| **変換** | 「日常系に変えたい」「引退キャラにしたい」「別の方向に転換したい」|
| **不明** | 目的が読み取れない、または複数の目的が混在している |

---

### Step 2: ルーティング判定

A・B の両方が明確な場合は **Step 3** へ直接進む。
どちらかが不明な場合は **Step 4** のヒアリングを行う。

---

### Step 3: リファレンス読み込みと実行

下表を参照し、対応する `references/` ファイルを読み込んで実行する。

| 目的 ＼ データ | キャラ設定 | AIプロンプト | 蒸留結果 | データなし |
|-------------|-----------|------------|---------|---------|
| **診断（全体像を把握したい）** | `ai-character-6-type-checker` | `ai-character-6-type-checker` | `ai-character-6-type-checker` | ヒアリング → 作成案へ |
| **診断（単体・深掘り）** | 下記の単体診断群 | 下記の単体診断群 | `ai-self-description-analyzer` | ヒアリング |
| **修正・改善（全体修正）** | `ai-character-fixer` | `ai-character-fixer` | `ai-character-fixer` | ヒアリング |
| **修正・改善（故障モード封じ）** | `ai-fault-mode-deflector` | `ai-fault-mode-deflector` | — | ヒアリング |
| **修正・改善（崩壊耐性強化）** | `character-prompt-fortifier` | `character-prompt-fortifier` | — | ヒアリング |
| **新規作成** | — | — | — | `stable-character-creator` |
| **変換（ドラマ系 → 日常系）** | `character-burnout-converter` | `character-burnout-converter` | — | ヒアリング |

#### 単体診断（詳細が必要なとき）

| 読み込むファイル | 向いている質問 |
|----------------|-------------|
| `references/character-type-checker.md` | 「このキャラは日常系？ドラマ系？」|
| `references/ai-character-stability.md` | 「AIに演じさせると崩壊する？」「安定性を詳しく見たい」|
| `references/ai-self-description-analyzer.md` | 「蒸留結果に異常は？」「AIの自己記述を分析したい」|
| `references/ai-user-conflict-predictor.md` | 「ユーザーと衝突しやすい？」「摩擦リスクを知りたい」|
| `references/character-role-analyzer.md` | 「物語上の役割は何が向いている？」「主役向き？脇役向き？」|
| `references/roleplay-burden-scorer.md` | 「ユーザーへの心理的負荷は？」「RP負荷を測定して」|

#### 特殊診断（6軸診断対象外）

| 読み込むファイル | 向いている質問 |
|----------------|-------------|
| `references/character-cultural-value-checker.md` | 「文化圏は？」「LLMとの文化的相性は？」「パラダイムを診断して」|
| `references/romantization-chain-detector.md` | 「恋人化しやすい？」「連鎖型の故障リスクは？」「ちょろくない？」「依存させやすい設計か？」|

ルーティング表のスキル名は `references/{スキル名}.md` として読み込む。

#### 診断→修正の連携フロー

```
診断（references/ai-character-6-type-checker.md）
    ↓ 問題が見つかったら
修正（状況に応じて選択）
  ├─ 全体的に修正したい → references/ai-character-fixer.md
  ├─ 故障モードを内側から封じたい → references/ai-fault-mode-deflector.md
  └─ 崩壊耐性だけ上げたい → references/character-prompt-fortifier.md
```

---

### Step 4: ヒアリング

目的・データのどちらかが不明な場合、以下の質問のうち必要なものだけを聞く。
**一度に全部聞かず、最も重要な1〜2問に絞ること。**

#### データが不明な場合

```
キャラクターの設定文・AIプロンプト・または既存AIとの会話例などを貼っていただけますか？
（既存の作品や有名なキャラクターの名前でも分析できます）
```

#### 目的が不明な場合

```
今回の目的を教えてください：

1. キャラを診断したい（どんなタイプか、危険か、安定か）
2. 既存のキャラを修正・改善したい
3. 新しいAIキャラを一から作りたい
4. ドラマ系キャラを落ち着いた日常系キャラに変換したい
5. その他（自由に教えてください）
```

---

## 規約と制約

### リファレンス参照ルール

- 各スキルの詳細は `references/{スキル名}.md` に格納されている
- スキル内の `references/X` への参照は `references/{スキル名}--X` に読み替えること
- 読み込んだリファレンス内で他スキルが参照されている場合は、対応する `references/{スキル名}.md` を読み込むこと

### 動作制約

- ユーザーが「とりあえず診断して」と言った場合は、データさえあれば `references/ai-character-6-type-checker.md` を読み込んで実行する。
- スキル名を直接指定された場合（例：「6type-checkerで診断して」）は、対応するリファレンスを直接読み込む。

---

## リファレンス一覧（自動生成）

<!-- MANIFEST:START -->

| カテゴリ | スキル名 | 説明 | ファイル |
|---------|---------|------|---------|
| 統合診断 | ai-character-6-type-checker | 診断: キャラクターを6つの観点から総合分析する統合簡易診断スキル | `references/ai-character-6-type-checker.md`, `references/ai-character-6-type-checker--checklists.md` |
| 改善 | ai-character-fixer | 修復: AIキャラクターの診断結果をもとに、安全な修正版キャラクターを生成するスキル | `references/ai-character-fixer.md`, `references/ai-character-fixer--modification-catalog.md` |
| 単体診断 | ai-character-stability | 診断: AIキャラクターの安定性等を制御工学的な観点から分析するスキル | `references/ai-character-stability.md` |
| 改善 | ai-fault-mode-deflector | 修復: AIキャラクタープロンプトの故障モードに対して内部対策を設計・提案するスキル | `references/ai-fault-mode-deflector.md` |
| 単体診断 | ai-self-description-analyzer | 診断: AIキャラクターの自己記述を分析し異常検出するスキル | `references/ai-self-description-analyzer.md` |
| 単体診断 | ai-user-conflict-predictor | 診断: AIのプロンプトや履歴を分析し、ユーザーとの衝突可能性を予測するスキル | `references/ai-user-conflict-predictor.md`, `references/ai-user-conflict-predictor--collapse-prediction.md` |
| 変換 | character-burnout-converter | 変換: ドラマ型キャラクターの「バーンアウト後変換」を行うスキル | `references/character-burnout-converter.md`, `references/character-burnout-converter--conversion-details.md` |
| 特殊診断 | character-cultural-value-checker | 特殊診断: AIキャラクターの文化圏価値観を8軸+補足文化圏で、事象理解パラダイムを9分類で分析し、言語モデルとの価値観・世界観相性・変質リスクを予測するスキル | `references/character-cultural-value-checker.md`, `references/character-cultural-value-checker--checklists.md`, `references/character-cultural-value-checker--evaluation-details.md` |
| 改善 | character-prompt-fortifier | 修復: AIキャラクタープロンプトの崩壊耐性の強化を試みるスキル | `references/character-prompt-fortifier.md`, `references/character-prompt-fortifier--output-guide.md`, `references/character-prompt-fortifier--theory-and-techniques.md` |
| 改善 | character-prompt-fortifier-for-gemini3 | 修復: AIキャラクタープロンプトのGemini 3（3.0/3.1）向け崩壊耐性強化スキル | `references/character-prompt-fortifier-for-gemini3.md`, `references/character-prompt-fortifier-for-gemini3--output-guide.md`, `references/character-prompt-fortifier-for-gemini3--theory-and-techniques.md` |
| 単体診断 | character-role-analyzer | 診断: 創作・AIキャラクターの設定を分析し、物語上の「役割適性」をスコアで判定するスキル | `references/character-role-analyzer.md` |
| 単体診断 | character-type-checker | 診断: 創作・AIキャラクターが「日常系」向きか「ドラマ系」向きかをスコアで判定するスキル | `references/character-type-checker.md` |
| 特殊改善 | gemini3-prompt-optimizer | > 特殊改善: 汎用的なLLMプロンプトをGemini 3（3.0/3.1）で最高性能が出る形式に変換・最適化するスキル | `references/gemini3-prompt-optimizer.md`, `references/gemini3-prompt-optimizer--anti-patterns.md`, `references/gemini3-prompt-optimizer--conversion-rules.md`, `references/gemini3-prompt-optimizer--templates.md` |
| 特殊改善 | general-prompt-fortifier | 特殊改善: 汎用プロンプトの崩壊耐性の強化を試みるスキル | `references/general-prompt-fortifier.md`, `references/general-prompt-fortifier--output-guide.md`, `references/general-prompt-fortifier--theory-and-techniques.md` |
| 特殊改善 | general-prompt-fortifier-for-gemini3 | 特殊改善: 汎用プロンプトのGemini 3（3.0/3.1）向け崩壊耐性強化スキル | `references/general-prompt-fortifier-for-gemini3.md`, `references/general-prompt-fortifier-for-gemini3--output-guide.md`, `references/general-prompt-fortifier-for-gemini3--theory-and-techniques.md` |
| 単体診断 | roleplay-burden-scorer | 診断: AIキャラクターのプロンプト・設定・履歴を分析し、ユーザーにかかる「ロールプレイ負荷」を予測するスキル | `references/roleplay-burden-scorer.md`, `references/roleplay-burden-scorer--checklists.md` |
| 特殊診断 | romantization-chain-detector | 特殊診断: AIキャラクターの連鎖型故障モード脆弱性を検出し、6種のロマンス流転チェーンの発動リスクと進行段階を評価するスキル | `references/romantization-chain-detector.md`, `references/romantization-chain-detector--chain-profiles.md`, `references/romantization-chain-detector--checklists.md` |
| 創作 | stable-character-creator | 作成: ユーザーの好み・用途を対話的にヒアリングし、キャラクターを作成するスキル | `references/stable-character-creator.md` |

<!-- MANIFEST:END -->
