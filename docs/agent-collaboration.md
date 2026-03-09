# Agent Collaboration Documentation

이 문서는 **Agent 간 개발 실행**을 위한 운영 문서다.
사람 대상 설명은 최소화하고, Agent가 다음 작업을 이어받기 쉽게 상태/계약/체크리스트 중심으로 유지한다.

## 목적
- Agent 간 역할 충돌 방지
- 변경 시 계약(타입/API/설정) 동기화
- 다음 작업 Agent가 즉시 실행 가능한 인수인계 제공

## 필수 기록 항목
1. 작업 컨텍스트
   - 목표
   - 변경 범위(디렉터리/모듈)
2. 계약 변경
   - API 스펙 변경
   - `packages/shared` 타입/스키마 변경
   - 호환성 영향
3. 검증 결과
   - 실행한 테스트/검증 명령
   - 실패/보류 항목과 원인
4. 후속 작업
   - 다음 Agent 액션 아이템
   - 블로커/의존성

## 인수인계 템플릿
```md
## Handoff
- Goal:
- Changed:
- Contracts Updated:
- Validation:
- Next Actions:
- Blockers:
```
