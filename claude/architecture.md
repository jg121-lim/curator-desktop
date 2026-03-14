# Confluence Agent Desktop App - Architecture

## Overview
사내 Confluence 문서를 지능적으로 검색하고 분석하는 AI 기반 데스크탑 애플리케이션

## Tech Stack
- **Runtime**: Electron 28 (Windows 최적화)
- **Frontend**: React 18 + Tailwind CSS (ChatGPT-like UI)
- **Backend**: Electron Main Process (Node.js)
- **Database**: SQLite (better-sqlite3) - 로컬 문서 인덱싱
- **LLM**: OpenAI Compatible API (사내 API)
- **Search**: TF-IDF + BM25 기반 로컬 검색 + LLM RAG

## Data Flow
```
[Confluence API] --(rate limited: 1req/s)--> [Crawler/Indexer]
                                                    |
                                              [SQLite DB]
                                                    |
[User Query] --> [Search Engine] --> [Context Builder] --> [LLM API] --> [Response]
```

## Key Components
1. **ConfluenceConnector**: Rate-limited API client (1 req/sec)
2. **DocumentIndexer**: 문서 크롤링 및 로컬 인덱싱
3. **SearchEngine**: BM25 + TF-IDF 기반 관련 문서 검색
4. **RAGPipeline**: 검색된 문서 컨텍스트 + LLM 분석
5. **ChatInterface**: ChatGPT-style 대화 인터페이스
6. **SettingsManager**: 설정 관리 (API 키, 엔드포인트 등)

## Rate Limiting Strategy
- Token bucket algorithm (1 token/second)
- Request queue with FIFO processing
- Exponential backoff on 429 responses
