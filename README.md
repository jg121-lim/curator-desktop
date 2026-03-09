# Curator Desktop Monorepo

Electron(React) 데스크톱 앱과 FastAPI 백엔드를 함께 관리하는 모노레포입니다.

## 운영 원칙

- 이 리포지토리는 사람이 직접 코드를 수정하기보다 Agent가 협업하여 구현합니다.
- 사람은 구현 상세 대신 결과물/변경 이력을 문서로 검토합니다.
- 문서는 아래 두 가지로 분리 운영합니다.
  - Agent 실행/인수인계용: `docs/agent-collaboration.md`
  - 사람 검토용 릴리스 노트: `docs/human-release-notes.md`

## 디렉터리 구조

- `apps/desktop`: Electron + React 클라이언트
- `apps/backend`: FastAPI 서버
- `packages/shared`: 공용 타입/스키마
- `docs`: 운영 문서

## 개발 실행 순서

1. 의존성 설치
   ```bash
   npm install
   ```
2. 백엔드 의존성 설치
   ```bash
   cd apps/backend
   uv sync
   cd ../..
   ```
3. 프론트/백엔드 동시 실행
   ```bash
   npm run dev
   ```

### 개별 실행

- 데스크톱 앱만 실행: `npm run dev:desktop`
- 백엔드만 실행: `npm run dev:backend`
