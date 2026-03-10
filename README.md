# curator-desktop

현재 저장소는 **화면/스토어 소스 코드만 있는 최소 스켈레톤** 상태입니다.
즉, `package.json`, Electron main entry, 번들러(Vite 등) 설정이 아직 없어 그대로는 `npm run ...`으로 실행되지 않습니다.

## 지금 바로 확인 가능한 것
- 라우트 구성: `apps/desktop/src/routes/AppRoutes.tsx`
- 채팅 화면: `apps/desktop/src/routes/ChatPage.tsx`
- 설정 화면: `apps/desktop/src/routes/SettingsPage.tsx`
- 설정 암호화 저장소: `apps/desktop/src/main/settingsStore.ts`

## 내가 받아서 실행할 수 있나?
가능합니다. 다만 아래 2가지가 먼저 필요합니다.

1. Node.js 20+
2. Electron + React 실행용 프로젝트 기본 파일(`package.json`, main/preload 엔트리, Vite 설정)

아래는 **가장 빠른 실행 방법**입니다.

## 빠른 실행 가이드 (Windows / macOS)

### 1) 새 Electron+Vite 템플릿 생성
원하는 빈 폴더에서:

```bash
npm create @quick-start/electron@latest
```

템플릿 질문에서 React + TypeScript 조합을 선택합니다.

### 2) 현재 저장소의 `apps/desktop/src` 코드를 템플릿 프로젝트로 복사
- `apps/desktop/src/App.tsx`
- `apps/desktop/src/routes/*`
- `apps/desktop/src/types/*`
- `apps/desktop/src/main/settingsStore.ts`

복사 후, 템플릿의 main/preload에서 `settingsStore`를 노출하도록 IPC 연결을 추가하세요.

### 3) 의존성 설치
```bash
npm install
```

### 4) 개발 모드 실행
```bash
npm run dev
```

정상 동작하면 Electron 창에서:
- `#/chat`
- `#/settings`
경로를 확인할 수 있습니다.

## Windows/macOS 호환 포인트
- 라우터는 `HashRouter` 사용: 패키징 후 파일 기반 라우팅 이슈를 줄입니다.
- 설정 저장 경로는 `app.getPath('userData')` 사용: OS별 사용자 데이터 경로 자동 처리.
- 설정 암호화는 `safeStorage` 사용: Windows/macOS에서 OS 네이티브 암호화 사용.

## 트러블슈팅
- `safeStorage.isEncryptionAvailable()`가 `false`이면 OS 보안 스토어 사용 불가 상태입니다.
  - macOS: 키체인 접근 상태 확인
  - Linux: keyring/secret service 설치 상태 확인
- 라우팅이 안 보이면 주소가 `#/chat` 형태인지 확인하세요.

