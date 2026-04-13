# 贡献指南

感谢您对 CryptoHub 的贡献兴趣！本指南介绍了贡献代码、文档和提交错误报告的流程。

## 开始

1. 在 GitHub 上 **Fork** 本仓库。
2. 在本地 **克隆** 你的 Fork 并创建功能分支：

   ```bash
   git clone https://github.com/<you>/CryptoHub.git
   cd CryptoHub
   git checkout -b feature/my-change
   ```

3. **搭建** 开发环境 — 参见 [SETUP.md](./SETUP.md)。

## 开发流程

### 分支命名

| 前缀 | 用途 |
|------|------|
| `feature/` | 新功能 |
| `fix/` | Bug 修复 |
| `docs/` | 文档变更 |
| `refactor/` | 代码重构 |
| `test/` | 添加或改进测试 |

### 提交信息

遵循 [约定式提交](https://www.conventionalcommits.org/zh-hans/) 规范：

```
feat: 添加布林带指标支持
fix: 修复空数据时夏普比率计算错误
docs: 更新 API 参考文档
test: 添加回测引擎边界用例测试
```

## 代码规范

### Python（backend-python）

- 格式化/检查工具：**Ruff**
- 提交前运行：`ruff check app/ --fix`
- 测试：`pytest tests/ -v`
- 公共 API 建议添加类型注解。

### Go（backend-go）

- 遵循标准 `go fmt` 和 `go vet`。
- 运行测试：`go test ./... -v`

### TypeScript / React（frontend）

- 检查工具：**ESLint**
- 运行：`pnpm lint`
- 构建检查：`pnpm build`

## 测试

- 为所有新功能编写测试。
- Python 测试放在 `backend-python/tests/`，对应 `app/` 的目录结构。
- 异步测试使用 `pytest.mark.asyncio`。
- 新代码力争至少 80% 的覆盖率。

## Pull Request 流程

1. 确保 CI 通过 — 仓库会运行前端 lint/build、Go vet/test、Python ruff/pytest 和 Docker build。
2. 按照 PR 模板填写清晰的描述。
3. 至少请一位维护者审查。
4. 及时处理审查意见。
5. 批准后使用 squash-merge 合并。

## 国际化 (i18n)

- 文档以 8 种语言存放在 `docs/{lang}/` 下。
- 更新英文文档时，请在 PR 中注明，以便翻译者同步更新。
- 前端翻译位于 `frontend/src/i18n/messages/`。

## 报告问题

- 使用 GitHub Issues，提供清晰的标题和复现步骤。
- 使用 `bug`、`enhancement`、`documentation` 或 `question` 标签。
- 包含环境信息（操作系统、浏览器、Docker 版本）。

## 许可证

贡献即表示您同意您的贡献将按 MIT 许可证授权。
