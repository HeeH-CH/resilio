# [Project Proposal] Resilio: 자가 치유형 자동화 에이전트

## 1. 개요 (Executive Summary)

### 1.1 프로젝트명

**Project Resilio** (Resilience + I/O)
*부제: 외부 환경 변화에 적응하여 스스로 코드를 복구하는 Self-Healing Automation Pipeline*

### 1.2 추진 배경 및 문제 정의

* **The Problem:** 사내 자동화 파이프라인(RPA)의 가장 큰 적은 내부 로직 오류가 아닌 **"외부 환경(Web UI, API Schema)의 조용한 변화"**임. 이로 인해 운영팀은 1년마다 코드를 재작성하는 "무한 유지보수 늪"에 빠짐.
* **The Solution:** 에러 발생 시점을 단순 로그가 아닌 **"Live State(DOM, Screenshot)"**로 포착하고, LLM을 통해 변경된 환경에 맞는 코드로 **"수술(Patch)"**하여 복구 시간을 단축함.

### 1.3 핵심 목표

1. **Observation:** 실패 시점의 환경(DOM, Network)을 완벽히 재현 가능한 형태로 캡처 (Blackbox Recorder).
2. **Adaptation:** UI 변경, 스키마 변경 등 "환경 변화"에 대한 코드 수정안 자동 생성.
3. **Safety:** 검증되지 않은 코드는 절대 반영하지 않는 **PR(Pull Request) 기반의 Human-in-the-Loop** 체계 구축.

---

## 2. 시스템 아키텍처 (The Resilio Engine)

### 2.1 Core Components

1. **Runtime Sentry (감시)**
* Python 데코레이터/미들웨어 형태로 동작.
* 예외 발생 시 즉시 실행을 멈추고 제어권을 `State Snapshotter`로 이관.


2. **State Snapshotter (수집)**
* **Live Context:** Screenshot, Reduced DOM, Console Logs, Network Trace(HAR).
* **Intent Context:** 마지막으로 실행하려던 함수명과 매개변수 (`last_action`).


3. **Context Distiller (정제)**
* Raw HTML을 LLM이 이해하기 쉬운 구조로 압축 (Token Optimization).
* 비주요 태그 제거, 핵심 인터랙션 요소(Button, Input) 중심의 Tree 재구성.


4. **Root Cause Analyzer (진단)**
* 규칙 기반(Rule-based) 1차 필터링 (단순 타임아웃, 권한 에러).
* LLM 기반 2차 심층 분석 ("버튼 ID가 `btn_submit`에서 `btn_submit_v2`로 변경됨").


5. **Patch Architect (설계)**
* 엄격한 JSON Schema(`PatchSpec`)에 맞춰 수정안 생성.
* 기존 코드를 덮어쓰는 것이 아니라, **"최소 변경(Minimal Change)"** 원칙 준수.


6. **Safety Gatekeeper (검증)**
* **Hallucination Check:** 제안된 Selector가 실제 Snapshot DOM에 존재하는지 검증.
* **Lint/AST Check:** 문법적 오류 및 금지된 패턴(보안 위배) 검사.


7. **Sandbox Validator (테스트)**
* 실패한 Step만 격리하여 재실행(Replay).
* 성공 시 Git Branch 생성 및 PR 발송.



### 2.2 데이터 흐름 (Workflow)

`Capture` → `Distill` → `Analyze` → `Patch` → `Verify` → `Deliver`

---

## 3. 핵심 전략 및 원칙

### 3.1 Live State First (현장 증거 우선)

* "로그"는 과거를 말하지만, "스냅샷"은 현재를 말한다.
* 모든 디버깅과 수정은 텍스트 로그가 아닌 **캡처된 DOM과 스크린샷**을 기준으로 수행한다.

### 3.2 Surgical Fix (수술적 패치)

* 코드 전체를 다시 짜는 것은 금지한다.
* 문제가 발생한 **특정 Selector 변수**, **Wait 조건**, **함수 로직**만 국소적으로 도려내어 수정한다.

### 3.3 Defense in Depth (심층 방어)

* **1차 방어:** Gatekeeper가 존재하지 않는 Selector 제안을 즉시 기각.
* **2차 방어:** Sandbox에서 실제 실행(Replay) 실패 시 기각.
* **3차 방어:** 개발자(운영자)가 PR을 승인해야만 배포 (Master Branch 보호).

---

## 4. 단계별 구현 로드맵

### Phase 0: Observability (관측성 확보) - *Now*

* 목표: "왜 죽었는지 100% 알 수 있게 한다."
* 구현: `Sentry` & `Snapshotter` 구현. 에러 발생 시 HTML/Screenshot/Trace 저장.
* 산출물: Artifact Viewer, 표준 로그 포맷.

### Phase 1: Assisted Healing (추천형 힐링)

* 목표: "AI가 해결책을 제안하고, 사람이 적용한다."
* 구현: `Distill`, `Analyzer`, `Patch Architect` 구현.
* 산출물: 에러 발생 시 Teams로 "수정 제안 코드" 알림 발송.

### Phase 2: Autonomous Recovery (반자동 복구)

* 목표: "저위험군은 스스로 고치고 보고한다."
* 구현: `Gatekeeper`, `Validator`, `Git 연동`.
* 산출물: 자동 생성된 PR, 성공적인 Self-healing 케이스 축적.

### Phase 3: Collective Intelligence (집단 지성)

* 목표: "한 번 겪은 오류는 다시 겪지 않는다."
* 구현: Vector DB 기반의 `Adaptive Knowledge Base`. 유사 에러 발생 시 과거 패치 기록을 먼저 참조.

---

## 5. 기대 효과 (KPI)

* **MTTR (평균 복구 시간):** 장애 인지부터 코드 수정 PR 생성까지 **수동(1~2시간) → 자동(3분)** 단축.
* **유지보수 비용:** 단순 UI 변경으로 인한 유지보수 공수 **70% 절감**.
* **코드 자산화:** 개인의 경험이 아닌, 시스템의 **Knowledge Base**로 장애 대응 지식 축적.

---

## 6. 결론

**Project Resilio**는 단순한 에러 처리가 아닌, 자동화 시스템의 **생존성(Survivability)**을 높이는 프로젝트입니다. 잦은 UI 변경으로 고통받는 RPA/자동화 파이프라인에 "자가 치유" 능력을 부여하여 운영 효율을 혁신적으로 개선하겠습니다.

---

제안서가 훨씬 전문적이고 설득력 있게 바뀌었죠? 이 버전으로 검토해 보시고 필요한 부분을 가감하시면 될 것 같습니다. **바로 실행(Phase 0)**을 위한 스켈레톤 코드가 필요하시면 말씀해 주세요.