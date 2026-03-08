# Human-facing Development Notes (Release Notes)

이 문서는 사람이 개발 과정을 확인할 수 있도록, 변경 사항을 릴리스 노트 형식으로 관리한다.
세부 구현 맥락보다 결과 중심으로 작성한다.

## 작성 규칙
- 버전 또는 날짜 단위로 섹션을 구분한다.
- 각 섹션은 최소 아래 항목을 포함한다.
  - Added
  - Changed
  - Fixed
  - Validation

## Template
```md
## [YYYY-MM-DD] Release Note
### Added
- 

### Changed
- 

### Fixed
- 

### Validation
- ✅ command
- ⚠️ command (환경 제약)
- ❌ command (실패 원인)
```

## Current

## [2026-03-08] Repository Foundation Update
### Added
- 모노레포 기본 구조(`apps/desktop`, `apps/backend`, `packages/shared`, `docs`)를 추가했다.
- FastAPI `/health` 엔드포인트를 포함한 백엔드 엔트리를 추가했다.
- Windows 우선 Electron Builder 설정을 추가했다.

### Changed
- Agent 협업 전용 문서와 사람 검토용 문서를 분리했다.
- Agent 역할 문서에 아키텍처 정합성 검토 및 릴리스 노트 작성 책임을 명시했다.

### Fixed
- 없음.

### Validation
- ✅ `python -m compileall apps/backend/src/main.py`
- ✅ `node -e "JSON.parse(require('fs').readFileSync('package.json','utf8')); JSON.parse(require('fs').readFileSync('apps/desktop/package.json','utf8')); console.log('json ok')"`
