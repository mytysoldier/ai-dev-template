# ai-dev-template

AIエージェントを中心に、GitHub Issueでタスクを管理しながら個人開発を進めるためのテンプレートです。

このテンプレートは、以下のような進め方を前提にしています。

- まず企画・要件・技術設計をIssueで整理する
- MVPで作ること、作らないことを明確にする
- 実装Issueを小さく分ける
- AIエージェントはIssue単位で実装する
- 実装後は検証、コミット、push、PR作成まで進める
- レビューコメント対応後は再レビューを依頼する

## 使い方

1. このリポジトリをテンプレートとして新しいリポジトリを作成する
2. `docs/planning-template.md` をコピーして、作りたいサービスのMVP計画を書く
3. `.github/ISSUE_TEMPLATE/design.md` から設計Issueを作る
4. 設計IssueでMVP範囲と技術方針を確定する
5. `.github/ISSUE_TEMPLATE/implementation.md` から実装Issueを小さく作る
6. AIエージェントにIssue単位で実装を依頼する

## AI向けルール

AIエージェント向けの作業ルールは [AGENTS.md](AGENTS.md) にまとめています。

Codex、Cursor、Claude CodeなどのAIコーディングエージェントには、まず `AGENTS.md` と対象Issueを読ませてから作業させてください。

## 用意しているテンプレート

- `AGENTS.md`: AIエージェント向け作業ルール
- `.github/ISSUE_TEMPLATE/design.md`: 企画・要件・技術設計Issue
- `.github/ISSUE_TEMPLATE/implementation.md`: 実装Issue
- `.github/ISSUE_TEMPLATE/qa.md`: 動作確認・公開前チェックIssue
- `.github/PULL_REQUEST_TEMPLATE.md`: PR確認テンプレート
- `docs/planning-template.md`: MVP計画ドキュメント雛形

## 基本方針

個人開発では、完成度よりも公開できるMVPを優先します。

AIには大きな曖昧な依頼を渡さず、Issueごとに目的、実装範囲、受け入れ条件、スコープ外を明記します。これにより、AIが勝手に機能を増やしたり、技術スタックを変更したりすることを防ぎます。
