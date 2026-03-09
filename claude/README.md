# Confluence Agent 🔍

> 사내 Atlassian Confluence 문서를 기반으로 인사이트를 제공하는 AI 데스크탑 애플리케이션

## 📋 개요

Confluence Agent는 사내 Confluence에 축적된 지식을 활용하여, 자연어 질문에 대해 관련 문서를 검색하고 AI 분석을 통해 인사이트를 제공하는 Windows 데스크탑 애플리케이션입니다.

### 주요 기능

- **지능형 문서 검색**: BM25 기반 전문 검색(Full-Text Search)으로 관련 문서를 빠르게 찾습니다
- **RAG 기반 AI 분석**: 검색된 문서 컨텍스트를 LLM에 전달하여 정확한 답변을 생성합니다
- **ChatGPT 스타일 UI**: 친숙한 채팅 인터페이스로 자연스러운 질의/응답이 가능합니다
- **Rate Limiting**: Confluence API 초당 1회 호출 제한을 준수하는 Token Bucket 방식
- **오프라인 검색**: 한 번 동기화하면 로컬 SQLite DB에서 빠른 검색 가능
- **대화 기록 관리**: 대화를 저장하고 이전 대화를 다시 참조할 수 있습니다

## 🏗️ 아키텍처

```
┌─────────────────────────────────────────────────────┐
│                    Electron App                      │
│  ┌─────────────┐  ┌──────────────────────────────┐  │
│  │   Sidebar    │  │        Main Content          │  │
│  │ ┌─────────┐  │  │  ┌──────────────────────┐   │  │
│  │ │ Sync    │  │  │  │   Chat / Settings    │   │  │
│  │ │ Control │  │  │  │                      │   │  │
│  │ ├─────────┤  │  │  │  Messages + Input    │   │  │
│  │ │ Chat    │  │  │  │                      │   │  │
│  │ │ History │  │  │  └──────────────────────┘   │  │
│  │ ├─────────┤  │  └──────────────────────────────┘  │
│  │ │Settings │  │                                     │
│  │ └─────────┘  │           Backend (Main Process)    │
│  └─────────────┘  ┌──────────────────────────────┐   │
│                   │  Confluence → Indexer → SQLite │   │
│                   │  SearchEngine → RAG → LLM API │   │
│                   └──────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
```

### 데이터 흐름

1. **동기화**: Confluence API → (Rate Limited: 1 req/sec) → HTML 파싱 → SQLite FTS5
2. **질의**: 사용자 질문 → BM25 검색 → Top-K 문서 → LLM Context → 스트리밍 응답

## 🚀 설치 및 실행

### 사전 요구사항

- **Node.js**: 18.x 이상
- **npm**: 9.x 이상
- **Windows 10/11** (권장)
- **Confluence API 토큰**: Atlassian 계정에서 발급
- **OpenAI Compatible API**: 사내 LLM API 엔드포인트

### 설치

```bash
# 프로젝트 클론
git clone <repository-url>
cd confluence-agent

# 의존성 설치
npm install

# 개발 모드 실행
npm run dev

# 프로덕션 빌드 (Windows)
npm run build:win
```

### 초기 설정

1. 앱 실행 후 좌측 하단 **설정** 버튼 클릭
2. **Confluence** 탭에서:
   - Base URL 입력 (예: `https://your-company.atlassian.net`)
   - 사용자 이메일 입력
   - API Token 입력
   - 연결 테스트 → 스페이스 목록 조회 → 동기화할 스페이스 선택
3. **LLM API** 탭에서:
   - API Base URL 입력 (사내 OpenAI 호환 API 주소)
   - API Key 입력 (필요시)
   - 모델명 설정
   - 연결 테스트
4. **저장** 클릭
5. 사이드바에서 **문서 동기화** 실행

## 📁 프로젝트 구조

```
confluence-agent/
├── src/
│   ├── main/                      # Electron Main Process
│   │   ├── main.js                # 앱 진입점, IPC 핸들러
│   │   ├── preload.js             # 보안 IPC 브릿지
│   │   └── services/
│   │       ├── confluence.js      # Confluence API 커넥터 (Rate Limiting)
│   │       ├── database.js        # SQLite DB 관리 (FTS5)
│   │       ├── llm.js             # OpenAI 호환 LLM 서비스 (Streaming)
│   │       ├── search.js          # 검색 엔진
│   │       └── settings.js        # 설정 관리 (electron-store)
│   └── renderer/                  # React Frontend
│       ├── index.js               # React 진입점
│       ├── App.jsx                # 메인 앱 컴포넌트
│       ├── components/
│       │   ├── Sidebar.jsx        # 사이드바 (대화 목록, 동기화)
│       │   ├── ChatWindow.jsx     # 채팅 창
│       │   ├── MessageBubble.jsx  # 메시지 버블 (마크다운 렌더링)
│       │   └── WelcomeScreen.jsx  # 환영 화면
│       ├── pages/
│       │   └── SettingsPage.jsx   # 설정 페이지
│       └── styles/
│           └── app.css            # 전체 스타일시트
├── tests/
│   └── unit.test.js               # 유닛 테스트
├── public/
│   └── index.html                 # HTML 진입점
├── assets/                        # 아이콘 등 정적 리소스
├── ARCHITECTURE.md                # 아키텍처 문서
├── package.json
├── jest.config.js
└── README.md
```

## 🔧 핵심 기술 구현

### Rate Limiting (Confluence API 초당 1회 제한)

Token Bucket 알고리즘 기반으로 구현되어 있습니다:

```javascript
class RateLimiter {
  constructor(requestsPerSecond = 1) {
    this.minInterval = 1000 / requestsPerSecond;  // 1000ms
    this.lastRequestTime = 0;
    this.queue = [];  // FIFO 큐
  }

  async acquire() {
    // 큐에 요청 추가 후 순차 처리
    // 마지막 요청 이후 minInterval 미만이면 대기
  }
}
```

- 429 응답 시 `Retry-After` 헤더를 참조한 지수 백오프
- 동시 요청은 큐에 순차적으로 처리

### 검색 엔진 (SQLite FTS5 + BM25)

- SQLite FTS5 가상 테이블로 한국어/영어 전문 검색 지원
- `unicode61` 토크나이저 사용
- BM25 랭킹 알고리즘으로 관련도 순 정렬
- 트리거 기반 자동 인덱스 동기화

### RAG Pipeline

1. 사용자 질문 수신
2. FTS5 검색으로 관련 문서 Top-5 추출
3. 문서 스니펫을 LLM 시스템 프롬프트에 컨텍스트로 추가
4. OpenAI 호환 API로 스트리밍 응답 생성
5. 출처 문서 링크 제공

## ⚙️ 설정 항목

| 항목 | 설명 | 기본값 |
|------|------|--------|
| confluence.baseUrl | Confluence 서버 URL | - |
| confluence.username | 사용자 이메일 | - |
| confluence.apiToken | API 토큰 | - |
| confluence.spaces | 동기화 대상 스페이스 키 | [] |
| llm.apiUrl | OpenAI 호환 API URL | - |
| llm.apiKey | API 키 | - |
| llm.model | 모델명 | gpt-4 |
| llm.temperature | 생성 온도 | 0.7 |
| llm.maxTokens | 최대 토큰 수 | 4096 |
| llm.systemPrompt | 시스템 프롬프트 | (한국어 기본 프롬프트) |
| sync.autoSync | 자동 동기화 | false |
| sync.syncInterval | 동기화 주기 (분) | 60 |

## 🧪 테스트

```bash
# 유닛 테스트 실행
npm test

# 워치 모드
npm run test:watch
```

### 테스트 커버리지

- Rate Limiter: 인터벌 준수, 동시 요청 순서, 즉시 실행
- FTS Query Builder: 토큰화, 한국어, 특수문자 처리
- Snippet Extraction: 관련 스니펫 추출, 빈 입력 처리
- Settings Validation: URL 검증, 파라미터 범위 검증
- Markdown Rendering: 볼드, 이탤릭, 코드 블록

## 🐛 트러블슈팅

### 동기화가 느린 경우
Confluence API는 초당 1회 제한이 있으므로, 문서가 많은 스페이스는 시간이 걸립니다.
예: 1000개 문서 ≈ 약 40분 (페이지네이션 포함)

### LLM 연결 실패
- API URL 끝에 `/v1/chat/completions`가 자동 추가됩니다
- Base URL만 입력하세요 (예: `http://localhost:8000`)
- 사내 프록시 설정을 확인하세요

### 검색 결과가 부정확한 경우
- 더 구체적인 키워드를 사용해보세요
- 최신 문서가 반영되지 않았다면 동기화를 다시 실행하세요
- 시스템 프롬프트를 조정하여 답변 품질을 개선할 수 있습니다
