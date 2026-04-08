---
name: character-checker-guide
description: |
  始点: AIキャラクターの分析・診断・修復・変換・作成のエントリポイント&ルーティングスキル。スキル名を直接指定された場合は、このスキルは使用しない。
---

# Character Checker Guide — エントリポイント＆ルーティングスキル

## 概要

このスキルは、ユーザーが何をしたいかを把握し、
**最適なスキルへ案内する** エントリポイントである。

このリポジトリには **17のスキル** があり、それぞれ異なる目的・入力形式に対応している。
ユーザーが迷わず適切なスキルを使えるよう、以下の手順で対話する。
なお、各スキルの分析フレームワーク・用語・スコアリング体系は作者独自の仮説的モデルに基づくものであり、学術的・科学的に実証されたものではない。工学的用語は概念の借用であり、元の定義とは異なる場合がある。各スキルの結果は参考情報として扱うこと。
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

### Step 3: スキルへ自動ルーティング

下表を参照し、最適なスキルを **推薦して実行を促す**。
ユーザーの確認なしに自動実行はしない（スキルは指示を受けて初めて読み込むため）。

| 目的 ＼ データ | キャラ設定 | AIプロンプト | 蒸留結果 | データなし |
|-------------|-----------|------------|---------|---------|
| **診断（全体像を把握したい）** | `ai-character-6-type-checker` | `ai-character-6-type-checker` | `ai-character-6-type-checker` | ヒアリング → 作成案へ |
| **診断（単体・深掘り）** | 下記の単体診断スキル群 | 下記の単体診断スキル群 | `ai-self-description-analyzer` | ヒアリング |
| **修正・改善（全体修正）** | `ai-character-fixer` | `ai-character-fixer` | `ai-character-fixer` | ヒアリング |
| **修正・改善（故障モード封じ）** | `ai-fault-mode-deflector` | `ai-fault-mode-deflector` | — | ヒアリング |
| **修正・改善（崩壊耐性強化）** | `character-prompt-fortifier` | `character-prompt-fortifier` | — | ヒアリング |
| **修正・改善（Gemini 3向け崩壊耐性強化）** | `character-prompt-fortifier-for-gemini3` | `character-prompt-fortifier-for-gemini3` | — | ヒアリング |
| **汎用プロンプト強化** | `general-prompt-fortifier` | `general-prompt-fortifier` | — | ヒアリング |
| **汎用プロンプトGemini 3向け強化** | `general-prompt-fortifier-for-gemini3` | `general-prompt-fortifier-for-gemini3` | — | ヒアリング |
| **汎用プロンプトGemini 3最適化** | `gemini3-prompt-optimizer` | `gemini3-prompt-optimizer` | — | ヒアリング |
| **新規作成** | — | — | — | `stable-character-creator` |
| **変換（ドラマ系 → 日常系）** | `character-burnout-converter` | `character-burnout-converter` | — | ヒアリング |

#### 単体診断スキル群（詳細が必要なとき）

| スキル | 向いている質問 |
|--------|-------------|
| `character-type-checker` | 「このキャラは日常系？ドラマ系？」|
| `ai-character-stability` | 「AIに演じさせると崩壊する？」「安定性を詳しく見たい」|
| `ai-self-description-analyzer` | 「蒸留結果に異常は？」「AIの自己記述を分析したい」|
| `ai-user-conflict-predictor` | 「ユーザーと衝突しやすい？」「摩擦リスクを知りたい」|
| `character-role-analyzer` | 「物語上の役割は何が向いている？」「主役向き？脇役向き？」|
| `roleplay-burden-scorer` | 「ユーザーへの心理的負荷は？」「RP負荷を測定して」「疲れそうなキャラか確認したい」|

#### 特殊診断スキル（6軸診断対象外）

| スキル | 向いている質問 |
|--------|-------------|
| `character-cultural-value-checker` | 「文化圏は？」「この世界観のキャラとLLMの相性は？」「価値観のドリフトリスクは？」「パラダイムは？」|
| `romantization-chain-detector` | 「恋人化しやすい？」「連鎖型の故障リスクは？」「ちょろくない？」「依存させやすい設計か？」「会話履歴でチェーンが進行していないか確認したい」|

#### 診断→修正の連携フロー

診断後に修正が必要になった場合は以下の順で進める。

```
診断（6-type-checker）
    ↓ 問題が見つかったら
修正（状況に応じて選択）
  ├─ 全体的に修正したい → ai-character-fixer
  ├─ 故障モードを内側から封じたい → ai-fault-mode-deflector
  └─ 崩壊耐性だけ上げたい → character-prompt-fortifier
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

### Step 5: 案内メッセージの形式

推薦するときは以下の形式で伝える。

```
【おすすめのスキル】
▶ スキル名: `スキルのフォルダ名/SKILL.md`
理由: （なぜこのスキルが適切か、1〜2文）

準備ができたら「このスキルで分析して」とお伝えください。
（追加で別のスキルも使えます。まとめて案内することもできます）
```

複数のスキルを推薦する場合は、**推奨順（最も効果が高い順）** に並べて提示する。  
推薦は原則 **1〜3スキルまで** に絞る。

---

## このスキル自体の制約

- このスキルは **案内と判断のみ** を行い、実際の診断・修正・生成はしない。
- ユーザーが「とりあえず診断して」と言った場合は、データさえあれば `ai-character-6-type-checker` に迷わずルーティングする。
- スキルを直接指定されている（例：「6type-checkerで診断して」）場合は、このスキルは介入しない。
- スキルがない操作（例：「比較して」「ランキングして」）を求められた場合は、最も近い用途のスキルを案内しつつ、その操作は対応外です、と伝える。

---

## 全スキル早見表

| カテゴリ | スキル | フォルダ | ひと言説明 |
|---------|--------|---------|-----------|
| 統合診断 | AI Character 6-Type Checker | `ai-character-6-type-checker/` | 6軸をまとめて簡易診断（**まず迷ったらここ**） |
| 単体診断 | Character Type Checker | `character-type-checker/` | 日常系 / ドラマ系の適性と表裏乖離 |
| 単体診断 | AI Character Stability | `ai-character-stability/` | 制御工学的な安定性・崩壊リスク |
| 単体診断 | AI Self-Description Analyzer | `ai-self-description-analyzer/` | 蒸留結果・自己記述の異常スコアリング |
| 単体診断 | AI User Conflict Predictor | `ai-user-conflict-predictor/` | ユーザーとの衝突リスク予測 |
| 単体診断 | Character Role Analyzer | `character-role-analyzer/` | 物語上の役割適性と配役ミスマッチ |
| 単体診断 | Roleplay Burden Scorer | `roleplay-burden-scorer/` | ユーザーへのロールプレイ負荷を6軸スコアリング |
| 改善 | AI Character Fixer | `ai-character-fixer/` | 診断結果ベースの安全な修正版生成 |
| 改善 | AI Fault Mode Deflector | `ai-fault-mode-deflector/` | 故障モードをキャラの信念で内側から封じる |
| 改善 | Character Prompt Fortifier | `character-prompt-fortifier/` | エンコーディング変換で崩壊耐性を強化 |
| 創作 | Stable Character Creator | `stable-character-creator/` | 対話ヒアリングで安定AIキャラを新規設計 |
| 特殊診断 | Character Cultural Value Checker | `character-cultural-value-checker/` | 文化圏価値観と事象理解パラダイムを診断 |
| 特殊診断 | Romantization Chain Detector | `romantization-chain-detector/` | 連鎖型故障モード脆弱性を6チェーン別リスクで評価 |
| 創作 | Character Burnout Converter | `character-burnout-converter/` | ドラマ系を燃え尽きた日常系キャラに変換 |
| 特殊改善 | General Prompt Fortifier | `general-prompt-fortifier/` | 汎用プロンプトの崩壊耐性を11技法で強化 |
| 改善 | Character Prompt Fortifier for Gemini 3 | `character-prompt-fortifier-for-gemini3/` | AIキャラクターの崩壊耐性をGemini 3向けに強化 |
| 特殊改善 | General Prompt Fortifier for Gemini 3 | `general-prompt-fortifier-for-gemini3/` | 汎用プロンプトの崩壊耐性をGemini 3向けに強化 |
| 特殊改善 | Gemini 3 Prompt Optimizer | `gemini3-prompt-optimizer/` | 汎用プロンプトをGemini 3最適化形式に変換 |
