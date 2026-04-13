# コントリビューションガイド

CryptoHub へのコントリビューションに関心をお持ちいただきありがとうございます！

## はじめに

1. GitHub で本リポジトリを **Fork** します。
2. ローカルに **クローン** し、機能ブランチを作成：

   ```bash
   git clone https://github.com/<you>/CryptoHub.git
   cd CryptoHub
   git checkout -b feature/my-change
   ```

3. 開発環境をセットアップ — [SETUP.md](./SETUP.md) を参照。

## ブランチ命名規則

| プレフィックス | 用途 |
|-------------|------|
| `feature/` | 新機能 |
| `fix/` | バグ修正 |
| `docs/` | ドキュメント変更 |
| `refactor/` | リファクタリング |
| `test/` | テストの追加・改善 |

## コミットメッセージ

Conventional Commits 規約に従ってください：

```
feat: ボリンジャーバンドインジケーターの追加
fix: 空データ時のシャープレシオ計算の修正
docs: API リファレンスの更新
```

## コード規約

- **Python**: Ruff でフォーマット・リント、`pytest` でテスト
- **Go**: `go fmt`、`go vet`、`go test`
- **TypeScript**: ESLint、`pnpm lint`、`pnpm build`

## テスト

- 新機能にはテストを書いてください。
- Python テストは `backend/python/tests/` に配置。
- 非同期テストには `pytest.mark.asyncio` を使用。
- 新コードは最低 80% のカバレッジを目指してください。

## Pull Request のプロセス

1. CI が通ることを確認。
2. PR テンプレートに沿って明確な説明を記入。
3. 少なくとも 1 名のメンテナーにレビューを依頼。
4. 承認後、squash-merge で統合。

## 国際化

- ドキュメントは `docs/{lang}/` 以下に 8 言語で管理。
- 英語ドキュメントを更新した場合は PR に記載してください。

## 問題の報告

GitHub Issues を使用し、明確なタイトルと再現手順を記載してください。

## ライセンス

コントリビューションは MIT ライセンスの下でライセンスされることに同意したものとみなされます。
