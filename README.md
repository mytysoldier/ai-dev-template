# ai-dev-template

GitHub Issueを作業単位に、Codexと人が個人開発を進めるためのテンプレートです。初期リリースの範囲を絞り、公開可能な最小構成を優先します。エージェントの詳細な作業ルールは [AGENTS.md](AGENTS.md) を参照してください。

## 新しいリポジトリの初期設定

1. GitHubのテンプレート機能から新しいリポジトリを作成し、クローンする。
2. [初期リリース計画](docs/planning-template.md) をコピーしてプロジェクト用の計画を書き、目的、初期リリースの範囲とスコープ外、技術・保存・公開方針を決める。例示項目はプロジェクトに合わせて変更する。
3. READMEをプロジェクトの説明、起動方法、検証コマンド、公開方法に書き換える。`AGENTS.md` にはプロジェクト固有の構成、制約、検証コマンドや計画の場所を追記し、共通ルールと矛盾しないようにする。未決定の項目は未決定と明記する。
4. 採用した技術に合わせてlint・型チェック・テスト・buildなど適用可能な検証を決め、GitHub Actionsと必要なブランチ保護を各リポジトリで設定する。付属のCIはテンプレートのリンクとIssue記入欄を確認する。アプリの検証は別途追加する。[Codexのコードレビュー設定](https://chatgpt.com/settings/code-review)でリポジトリを接続し、必要に応じて自動レビューを有効にする。
5. 設計Issueを作成し、決定事項から小さな実装Issueに分解する。Issueテンプレートのラベルは各リポジトリに合わせて作成・変更する。

## 機能をCodexに渡す

新しいリポジトリをCodexで開き、`/goal` で機能の完成を依頼する。たとえば次のように、使う人、できること、制約と完成条件を伝える。

```text
/goal 買い物リストを追加する。項目の追加・完了・削除ができ、端末内に保存する。ログインや外部APIは追加しない。AGENTS.mdに従い、必要なIssueへの分解から実装、検証、PR、レビュー対応、条件を満たすPRのマージと全体確認まで進める。
```

Codexは機能全体の親Issueを作り、子Issueに分解して依存順に実装・検証・PR作成する。CIとCodexレビューを確認して明確な指摘に対応し、`AGENTS.md` の条件を満たしたPRをマージする。全子Issueの完了後に機能全体を検証し、条件を満たした場合だけ親IssueとGoalを完了する。ユーザーは必要に応じて同じチャットで指示や確認を行える。

GitHubとGitの認証・権限、Codexレビュー、適用するCIの設定は事前に必要。Goalは権限を拡張しないため、レビュー未完了、必須承認、認証・環境不足、仕様判断などで進めない場合は停止して報告する。自走の依頼は公開・デプロイの許可を含まない。Issueを作成しただけではCodexは自動起動しない。

単独のIssueを依頼する場合は `Issue #12 を AGENTS.md に従って対応して` と伝える。自走依頼がない単独Issueでは人がマージを判断する。

PRレビューは、設定済みの自動レビューを使うか、PRのコメントで `@codex review` を依頼する。反応がない場合はリポジトリ接続とコードレビュー設定を確認する。

## 進捗の確認

`python3 scripts/factory-status.py 親Issue番号` で、親Issueの「子Issueと進捗」に `- [ ] #番号` として記載した子IssueのGitHub上の状態とOpen PRを取得できる。チェック欄の状態は完了判定に使わない。GitHub CLIの認証とリポジトリへのアクセスが必要。依存関係、レビュー、CI、機能全体の完成は別途確認する。

## 共通の検証

`python3 scripts/verify.py` でテンプレートのリンクとIssueテンプレートの基本項目を確認できる。`python3 -m unittest discover -s tests` で進捗確認コマンドを検証できる。PRとmainへのpushでもGitHub Actionsが同じ確認を実行する。プロジェクト固有のテスト・buildは別途設定し、`AGENTS.md` にコマンドを記載する。

## テンプレート

- [機能の親Issue](.github/ISSUE_TEMPLATE/feature.md): 完成条件と子Issueの進捗
- [設計Issue](.github/ISSUE_TEMPLATE/design.md): 企画・要件・技術設計
- [実装Issue](.github/ISSUE_TEMPLATE/implementation.md): 実装範囲と受け入れ条件
- [QA Issue](.github/ISSUE_TEMPLATE/qa.md): 動作確認・公開前チェック
- [PRテンプレート](.github/PULL_REQUEST_TEMPLATE.md): 変更と検証結果
- [初期リリース計画](docs/planning-template.md): プロジェクト固有の方針
