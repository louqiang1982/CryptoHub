# 기여 가이드

CryptoHub에 기여해 주셔서 감사합니다!

## 시작하기

1. GitHub에서 이 저장소를 **Fork**합니다.
2. 로컬에 **클론**하고 기능 브랜치를 생성합니다:

   ```bash
   git clone https://github.com/<you>/CryptoHub.git
   cd CryptoHub
   git checkout -b feature/my-change
   ```

3. 개발 환경을 설정합니다 — [SETUP.md](./SETUP.md) 참조.

## 브랜치 명명 규칙

| 접두사 | 용도 |
|--------|------|
| `feature/` | 새 기능 |
| `fix/` | 버그 수정 |
| `docs/` | 문서 변경 |
| `refactor/` | 코드 리팩토링 |
| `test/` | 테스트 추가 및 개선 |

## 커밋 메시지

Conventional Commits 규약을 따라 주세요:

```
feat: 볼린저 밴드 인디케이터 지원 추가
fix: 빈 데이터에서 샤프 비율 계산 오류 수정
docs: API 레퍼런스 업데이트
```

## 코드 표준

- **Python**: Ruff 포맷팅/린팅, `pytest` 테스트
- **Go**: `go fmt`, `go vet`, `go test`
- **TypeScript**: ESLint, `pnpm lint`, `pnpm build`

## 테스트

- 모든 새 기능에 테스트를 작성합니다.
- Python 테스트는 `backend-python/tests/`에 배치합니다.
- 비동기 테스트에는 `pytest.mark.asyncio`를 사용합니다.
- 새 코드의 최소 80% 커버리지를 목표로 합니다.

## Pull Request 프로세스

1. CI가 통과하는지 확인합니다.
2. PR 템플릿에 따라 명확한 설명을 작성합니다.
3. 최소 1명의 메인테이너에게 리뷰를 요청합니다.
4. 승인 후 squash-merge로 병합합니다.

## 국제화

- 문서는 `docs/{lang}/` 아래에 8개 언어로 관리됩니다.
- 영어 문서를 업데이트할 때 PR에 기재해 주세요.

## 문제 보고

GitHub Issues를 사용하여 명확한 제목과 재현 단계를 기재해 주세요.

## 라이선스

기여는 MIT 라이선스 하에 라이선스됩니다.
