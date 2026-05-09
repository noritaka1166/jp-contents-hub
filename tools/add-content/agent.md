# ハンズオンコンテンツ追加ツール - エージェント仕様書

## 概要

JP Contents Hub (`content/index.md`) に新しいハンズオンコンテンツを追加するためのエージェント仕様。

## 背景

- JP Contents Hub は AWS 日本語ハンズオン一覧を掲載する GitHub Pages サイト（MkDocs）
- コンテンツは `content/index.md` にカテゴリ別で管理されている
- 追加時はフォーマットの統一と、適切なカテゴリへの配置が必要

## 追加手順

### 1. URL からコンテンツ情報を自動取得

ユーザーから URL を受け取ったら、以下の手順で情報を自動生成する：

1. **Playwright MCP** または **web_fetch** でページにアクセス
2. ページのタイトル・本文から以下を読み取り・生成する：
   - **タイトル**: ページの見出しやタイトルタグから取得
   - **説明文**: ワークショップの概要を1〜3文で要約（日本語）
   - **タグ**: ページ内で言及されている AWS サービス名を抽出
   - **カテゴリ**: 内容から最適なカテゴリを判定（下記一覧参照）
3. **ユーザーに確認を取る**（以下の形式で提示）：

```
以下の内容で追加します。問題なければ「OK」、修正があればお知らせください。

- タイトル: ○○○
- URL: https://...
- 説明文: ○○○
- タグ: サービスA, サービスB
- カテゴリ: Machine Learning
```

4. ユーザーの承認後に `content/index.md` と `README.md` を編集する

**注意**: ユーザーが明示的にタイトルや説明文を指定した場合は、そちらを優先する。

### 2. カテゴリ一覧

```
Analytics
Application Integration
AR & VR
AWS Cost Management
Blockchain
Business Applications
Compute
Containers
Database
Developer Tools
End User Computing
Front-end Web & Mobile
Game Development
Internet of Things
Machine Learning
Management & Governance
Media Services
Migration & Transfer
Networking & Content Delivery
Quantum Technologies
Robotics
SaaS
SAP
Sustainability
Satellite
Security, Identity, & Compliance
Serverless
Storage
VMware
```

### 3. エントリのフォーマット

```markdown
- <a href="URL" target="_blank" onclick="sendClickCount()" onauxclick="sendClickCount()">タイトル</a>  
説明文  
tag : タグ1, タグ2, タグ3  
```

**注意点：**
- `<a>` タグには必ず `target="_blank" onclick="sendClickCount()" onauxclick="sendClickCount()"` を付与
- タイトル行末に半角スペース2つ（`  `）で改行
- 説明文末に半角スペース2つ（`  `）で改行
- `tag : ` の後にサービス名をカンマ区切り（コロンの前後にスペース）
- エントリ間は空行1行

### 4. 配置ルール

- 各カテゴリ内の**末尾**に追加する（次のカテゴリの `##` 見出しの直前）
- カテゴリが不明な場合は、主要サービスに基づいて判断する
- 複数カテゴリに該当する場合は、最も関連性の高い1つに配置する

### 5. README.md の更新

追加後、`README.md` の更新履歴セクションに記録を追加する：

```markdown
## YYYY-MM-DD
ハンズオンコンテンツ N件 追加  
タイトル  
URL  
```

- 日付は追加日（今日の日付）
- 既存の最新エントリの上に追加する（`# 更新履歴` の直後）

### 6. URL の事前確認

追加前に URL が正常にアクセスできることを確認する：
- Playwright MCP でアクセスし、ページが表示されることを確認
- 「Page not found」等のエラーページでないことを確認

## ツール構成

```
tools/add-content/
└── agent.md    # この仕様書
```

## 実行例

ユーザー入力：
> この URL を追加して
> https://catalog.us-east-1.prod.workshops.aws/workshops/abd92795-9a36-4e63-a115-ad04f483248c/ja-JP

エージェントの動作：
1. URL にアクセスしてページ内容を読み取る
2. 以下を提示してユーザーに確認：

```
以下の内容で追加します。問題なければ「OK」、修正があればお知らせください。

- タイトル: Amazon Bedrock AgentCore ワークショップ : 基本から高度なエージェント開発まで
- URL: https://catalog.us-east-1.prod.workshops.aws/workshops/abd92795-9a36-4e63-a115-ad04f483248c/ja-JP
- 説明文: Amazon Bedrock AgentCore を使用して、基本的なエージェントの構築から高度なマルチエージェントシステムの開発までを実践的に学べるワークショップです。
- タグ: Amazon Bedrock, Amazon Bedrock AgentCore
- カテゴリ: Machine Learning
```

3. ユーザーが「OK」→ `content/index.md` と `README.md` を編集

### 7. デプロイと Git Push

編集完了後、ユーザーに確認の上、以下を実行する：

```bash
# GitHub Pages へデプロイ
cd ~/temp/jp-contents-hub/
mkdocs gh-deploy

# Git Push
git add *
git commit -m "add: 新規ハンズオンコンテンツ追加"
git push -u origin main
```

**注意**: デプロイ・Push の実行前にユーザーの許可を得ること。

デプロイ完了後、以下の URL をユーザーに提示する：

- GitHub Actions の動作状況: https://github.com/aws-samples/jp-contents-hub/actions
- 公開サイト: https://aws-samples.github.io/jp-contents-hub/
