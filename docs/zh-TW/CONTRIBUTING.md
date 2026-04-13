# 貢獻指南

感謝您對 CryptoHub 的貢獻興趣！

## 開始

1. 在 GitHub 上 **Fork** 本儲存庫。
2. 在本機 **複製** 您的 Fork 並建立功能分支：

   ```bash
   git clone https://github.com/<you>/CryptoHub.git
   cd CryptoHub
   git checkout -b feature/my-change
   ```

3. 設定開發環境 — 參見 [SETUP.md](./SETUP.md)。

## 分支命名

| 前綴 | 用途 |
|------|------|
| `feature/` | 新功能 |
| `fix/` | 錯誤修復 |
| `docs/` | 文件變更 |
| `refactor/` | 程式碼重構 |
| `test/` | 新增或改善測試 |

## 提交訊息

遵循約定式提交規範：

```
feat: 新增布林通道指標支援
fix: 修復空資料時夏普比率計算錯誤
docs: 更新 API 參考文件
```

## 程式碼規範

- **Python**: Ruff 格式化/檢查，`pytest` 測試
- **Go**: `go fmt`、`go vet`、`go test`
- **TypeScript**: ESLint、`pnpm lint`、`pnpm build`

## 測試

- 為所有新功能撰寫測試
- Python 測試放在 `backend/python/tests/`
- 非同步測試使用 `pytest.mark.asyncio`
- 新程式碼力求至少 80% 覆蓋率

## Pull Request 流程

1. 確保 CI 通過
2. 按照 PR 範本填寫清晰描述
3. 至少請一位維護者審查
4. 批准後使用 squash-merge 合併

## 國際化

- 文件以 8 種語言存放在 `docs/{lang}/` 下
- 更新英文文件時，請在 PR 中註明

## 報告問題

使用 GitHub Issues，提供清晰的標題和重現步驟。

## 授權

貢獻即表示您同意您的貢獻將按 MIT 授權條款授權。
