# 이기종 장비 실시간 3D 통합관제시스템 개발 계획서

## 1. 문서 개요

### 1.1 목적

본 문서는 AGV 4대, AMR 4대, ABCS 2대 등 총 10대 이하의 이기종 장비를 대상으로 하는 실시간 3D 통합관제시스템의 개발 계획을 정의한다. PRD에서 정의한 제품 요구사항을 실제 개발 가능한 단위로 나누고, MVP 구현 범위, 시스템 구성, 일정, 역할, 테스트 계획, 리스크 대응 방안을 명확히 한다.

### 1.2 개발 대상

| 장비 유형 | 수량 | 주요 표시 정보 |
| --- | ---: | --- |
| AGV | 4대 | 위치, 방향, 속도, 상태, 배터리, 현재 작업, 목적지, 경로 |
| AMR | 4대 | 위치, 방향, 속도, 상태, 배터리, 현재 작업, 목적지, 경로 |
| ABCS | 2대 | 설비 위치, 동작 상태, 처리량, 센서 상태, 알람 |
| 합계 | 10대 | 실시간 상태, 알람, 이력, KPI |

### 1.3 개발 목표

- 10대 이하 장비의 실시간 상태를 3D 맵에서 안정적으로 표시한다.
- AGV, AMR, ABCS 장비 데이터를 표준 상태 모델로 통합한다.
- 운영자가 장비 상태, 알람, 위치, 작업 흐름을 한 화면에서 확인할 수 있도록 한다.
- 향후 장비 수 확대와 실제 장비 연동을 고려한 확장 가능한 구조로 개발한다.
- 초기 버전은 실제 장비 연동 전에도 시뮬레이터 데이터로 동작 가능해야 한다.

## 2. 개발 범위

### 2.1 MVP 포함 범위

- 웹 기반 3D 관제 화면
- AGV 4대, AMR 4대, ABCS 2대 표시
- 장비별 실시간 위치 및 상태 갱신
- 장비 상세 정보 패널
- 장비 검색 및 상태 필터
- 실시간 알람 목록
- 알람 발생 장비 강조
- 기본 KPI 대시보드
- 장비 상태 시뮬레이터
- 백엔드 API
- WebSocket 기반 실시간 데이터 전송
- 장비/맵/상태 기본 설정 파일 또는 관리자 초기 데이터
- 기본 이력 저장 및 조회

### 2.2 MVP 제외 범위

- 실제 장비 제어 명령
- 복잡한 사용자 권한 체계
- 다중 사이트 지원
- 고급 리플레이 기능
- 예측 정비
- 외부 WMS/MES/MCS 정식 연동
- 모바일 전용 화면
- CAD/BIM 편집 기능

### 2.3 개발 전제

- 초기 개발은 실제 장비 대신 시뮬레이터를 통해 상태 데이터를 생성한다.
- 장비 수는 총 10대로 제한한다.
- 3D 맵은 간단한 물류센터 또는 공장 레이아웃 모델로 구성한다.
- 좌표계는 시스템 내부 기준 좌표를 먼저 정의하고, 실제 장비 좌표 변환은 후속 단계에서 확장한다.
- MVP는 단일 현장, 단일 서버, 단일 관제 화면 기준으로 개발한다.

## 3. 권장 시스템 구성

### 3.1 전체 아키텍처

```text
[Equipment Simulator]
        |
        | HTTP / Internal Event
        v
[Backend API Server] <----> [Database]
        |
        | WebSocket
        v
[Web 3D Control Client]
```

### 3.2 구성 요소

| 구성 요소 | 역할 |
| --- | --- |
| 3D Web Client | 3D 맵 렌더링, 장비 표시, 상세 패널, 알람/KPI UI |
| Backend API Server | 장비 상태 관리, REST API, WebSocket 이벤트 송신 |
| Equipment Simulator | AGV, AMR, ABCS 상태 데이터 생성 |
| Database | 장비 마스터, 상태 이력, 알람 이력 저장 |
| Config Module | 장비 목록, 초기 위치, 맵 구역, 알람 기준 관리 |

### 3.3 권장 기술 스택

| 영역 | 권장 기술 |
| --- | --- |
| Frontend | HTML, CSS, JavaScript |
| 3D Rendering | Babylon.js |
| UI 상태 관리 | 브라우저 내 로컬 상태 |
| Backend | Node.js 정적 HTTP 서버 |
| Realtime | 브라우저 내 로컬 시뮬레이터, 후속 단계에서 WebSocket 확장 |
| Database | MVP 미적용, 후속 단계에서 SQLite 또는 PostgreSQL 적용 |
| API 문서 | MVP 미적용, 후속 단계에서 OpenAPI/Swagger 적용 |
| 테스트 | Node.js 기반 더미 데이터 검증 테스트 |
| 코드 품질 | 단순 정적 구조, 후속 단계에서 ESLint/Prettier 적용 |

초기 실행 가능한 MVP는 개발 속도와 배포 단순성을 위해 `Node.js 정적 서버 + Babylon.js CDN + 로컬 시뮬레이터` 조합으로 구현한다.

## 4. 장비 구성 계획

### 4.1 장비 목록

| 장비 ID | 유형 | 초기 구역 | 초기 상태 | 비고 |
| --- | --- | --- | --- | --- |
| AGV-001 | AGV | Inbound | RUNNING | 입고 구역 운반 |
| AGV-002 | AGV | Storage | IDLE | 보관 구역 대기 |
| AGV-003 | AGV | Outbound | CHARGING | 출고 구역 인근 충전 |
| AGV-004 | AGV | MainRoute | RUNNING | 메인 라인 이동 |
| AMR-001 | AMR | Picking | RUNNING | 피킹 구역 이동 |
| AMR-002 | AMR | Picking | IDLE | 작업 대기 |
| AMR-003 | AMR | Packing | RUNNING | 포장 구역 이동 |
| AMR-004 | AMR | Charging | WARNING | 배터리 부족 경고 |
| ABCS-001 | ABCS | ConveyorLine-A | RUNNING | 컨베이어/분류 설비 |
| ABCS-002 | ABCS | ConveyorLine-B | IDLE | 버퍼/이송 설비 |

### 4.2 상태 정의

| 상태 | 적용 장비 | 표시 방식 |
| --- | --- | --- |
| RUNNING | AGV, AMR, ABCS | 녹색 |
| IDLE | AGV, AMR, ABCS | 파란색 |
| CHARGING | AGV, AMR | 하늘색 |
| WARNING | AGV, AMR, ABCS | 노란색 |
| ERROR | AGV, AMR, ABCS | 빨간색 |
| OFFLINE | AGV, AMR, ABCS | 회색 |
| E_STOP | AGV, AMR, ABCS | 빨간색 점멸 |

### 4.3 시뮬레이터 동작

- AGV/AMR은 미리 정의된 경로를 따라 이동한다.
- ABCS는 고정 위치에서 상태와 처리량 값만 변경된다.
- 장비 상태는 정상 상태 위주로 순환하되, 일정 확률로 WARNING 또는 ERROR 이벤트를 발생시킨다.
- 배터리는 이동 중 감소하고 충전 상태에서 증가한다.
- 모든 상태 변경은 서버를 통해 WebSocket으로 클라이언트에 전달된다.

## 5. 데이터 모델 계획

### 5.1 Equipment

| 필드 | 타입 | 설명 |
| --- | --- | --- |
| id | string | 장비 ID |
| type | enum | AGV, AMR, ABCS |
| name | string | 표시명 |
| vendor | string | 제조사 |
| zoneId | string | 현재 또는 소속 구역 |
| modelKey | string | 3D 모델 키 |
| createdAt | datetime | 생성 시각 |
| updatedAt | datetime | 수정 시각 |

### 5.2 EquipmentState

| 필드 | 타입 | 설명 |
| --- | --- | --- |
| equipmentId | string | 장비 ID |
| status | enum | RUNNING, IDLE, CHARGING, WARNING, ERROR, OFFLINE, E_STOP |
| x | number | X 좌표 |
| y | number | Y 좌표 |
| z | number | Z 좌표 |
| heading | number | 방향 |
| speed | number | 속도 |
| batteryLevel | number | 배터리 |
| taskId | string | 작업 ID |
| destination | string | 목적지 |
| throughput | number | ABCS 처리량 |
| alarmCode | string | 알람 코드 |
| timestamp | datetime | 상태 발생 시각 |

### 5.3 AlarmEvent

| 필드 | 타입 | 설명 |
| --- | --- | --- |
| id | string | 알람 ID |
| equipmentId | string | 장비 ID |
| severity | enum | LOW, MEDIUM, HIGH, CRITICAL |
| code | string | 알람 코드 |
| message | string | 알람 메시지 |
| status | enum | OPEN, ACKNOWLEDGED, RESOLVED |
| occurredAt | datetime | 발생 시각 |
| acknowledgedAt | datetime | 확인 시각 |
| resolvedAt | datetime | 해결 시각 |

## 6. API 개발 계획

### 6.1 REST API

| Method | Endpoint | 설명 |
| --- | --- | --- |
| GET | /api/equipment | 장비 목록 조회 |
| GET | /api/equipment/:id | 장비 상세 조회 |
| GET | /api/equipment/:id/state | 장비 현재 상태 조회 |
| GET | /api/equipment/:id/history | 장비 상태 이력 조회 |
| GET | /api/alarms | 알람 목록 조회 |
| PATCH | /api/alarms/:id/ack | 알람 확인 처리 |
| PATCH | /api/alarms/:id/resolve | 알람 해결 처리 |
| GET | /api/kpi/summary | 기본 KPI 조회 |
| GET | /api/map/layout | 맵 레이아웃 조회 |

### 6.2 WebSocket 이벤트

| 이벤트 | 방향 | 설명 |
| --- | --- | --- |
| equipment.state.updated | Server -> Client | 장비 상태 변경 |
| equipment.position.updated | Server -> Client | 장비 위치 변경 |
| alarm.created | Server -> Client | 알람 발생 |
| alarm.updated | Server -> Client | 알람 상태 변경 |
| kpi.summary.updated | Server -> Client | KPI 요약 변경 |
| simulator.status | Server -> Client | 시뮬레이터 상태 |

## 7. 프론트엔드 개발 계획

### 7.1 주요 화면

| 화면 | 기능 |
| --- | --- |
| Main Control View | 3D 맵, 장비 실시간 표시, 검색, 필터, 상세 패널 |
| Alarm Panel | 실시간 알람 목록, 알람 확인/해결 |
| KPI Summary | 장비 수, 상태별 수량, 알람 수, 처리량 |
| Equipment Detail | 장비 상세 상태, 작업 정보, 최근 이벤트 |
| History View | 장비별 상태 이력 목록 |
| Settings Basic View | 장비 목록 및 기본 설정 확인 |

### 7.2 3D 화면 구현 항목

- 기본 바닥, 구역, 경로, 스테이션, 충전소 표시
- AGV 모델은 낮은 높이의 운반차 형태로 표현
- AMR 모델은 원형 또는 사각 자율주행 로봇 형태로 표현
- ABCS는 고정 설비 또는 컨베이어 형태로 표현
- 장비 상태별 색상 적용
- 장비 선택 시 외곽선 또는 하이라이트 표시
- 장비 위에 ID 또는 상태 라벨 표시
- 카메라 줌, 회전, 이동, 리셋 지원
- 필터 적용 시 해당 장비만 강조 또는 표시

### 7.3 UI 구성

- 상단 바: 시스템명, 연결 상태, 현재 시각, 사용자 영역
- 좌측 패널: 장비 검색, 유형 필터, 상태 필터, 장비 목록
- 중앙 영역: 3D 관제 맵
- 우측 패널: 선택 장비 상세 또는 알람 상세
- 하단 바: KPI 카드, 알람 카운트, 시뮬레이터 상태

## 8. 백엔드 개발 계획

### 8.1 주요 모듈

| 모듈 | 역할 |
| --- | --- |
| Equipment Module | 장비 마스터 및 현재 상태 관리 |
| State Module | 상태 수신, 정규화, 저장 |
| Alarm Module | 알람 생성, 조회, 확인, 해결 |
| KPI Module | 장비 수, 상태별 수량, 처리량 계산 |
| Map Module | 맵/구역/경로 데이터 제공 |
| Realtime Module | WebSocket 이벤트 송신 |
| Simulator Module | 장비 상태 데이터 생성 |

### 8.2 백엔드 처리 흐름

1. 시뮬레이터가 장비별 상태를 주기적으로 생성한다.
2. 서버가 상태 데이터를 표준 모델로 정규화한다.
3. 현재 상태를 메모리 또는 DB에 갱신한다.
4. 상태 이력을 DB에 저장한다.
5. 알람 조건을 평가한다.
6. 알람이 발생하면 알람 이력을 저장한다.
7. WebSocket으로 클라이언트에 상태와 알람을 송신한다.
8. 클라이언트는 3D 맵과 UI 패널을 갱신한다.

## 9. 데이터베이스 계획

### 9.1 초기 MVP 테이블

| 테이블 | 설명 |
| --- | --- |
| equipment | 장비 마스터 |
| equipment_state_current | 장비 현재 상태 |
| equipment_state_history | 장비 상태 이력 |
| alarm_event | 알람 이력 |
| map_zone | 구역 정보 |
| map_path | 장비 이동 경로 |
| app_config | 시스템 설정 |

### 9.2 데이터 보관 정책

- 현재 상태: 최신 상태만 유지
- 상태 이력: MVP 기준 최근 7일 보관
- 알람 이력: MVP 기준 최근 30일 보관
- 시뮬레이터 로그: 개발 환경에서만 보관

## 10. 개발 일정

총 개발 기간은 6주를 기준으로 한다. 실제 일정은 투입 인원과 기존 코드베이스 유무에 따라 조정한다.

### Week 1: 프로젝트 기반 구축

- 요구사항 확정
- 기술 스택 확정
- 프로젝트 구조 생성
- 프론트엔드/백엔드 개발 환경 구성
- DB 스키마 초안 작성
- 장비 10대 초기 데이터 정의
- 3D 맵 기본 레이아웃 설계

### Week 2: 백엔드 기본 기능

- 장비 마스터 API 개발
- 장비 현재 상태 API 개발
- SQLite 또는 PostgreSQL 연동
- 시뮬레이터 기본 구현
- WebSocket 서버 구성
- 장비 상태 업데이트 이벤트 송신

### Week 3: 3D 관제 화면

- React 앱 기본 레이아웃 구현
- Babylon.js 적용
- 3D 맵 기본 오브젝트 구현
- AGV, AMR, ABCS 모델 표시
- 실시간 위치 갱신 연동
- 장비 선택 및 상세 패널 구현

### Week 4: 알람 및 KPI

- 알람 생성 조건 구현
- 알람 목록 API 개발
- 알람 WebSocket 이벤트 연동
- 알람 패널 구현
- 장비 상태별 KPI 계산
- KPI 요약 UI 구현
- 검색 및 필터 구현

### Week 5: 이력 및 품질 개선

- 장비 상태 이력 저장
- 장비별 이력 조회 API 개발
- 간단한 이력 화면 구현
- 3D 화면 성능 개선
- UI 반응성 및 레이아웃 정리
- 오류 처리 및 연결 상태 표시

### Week 6: 통합 테스트 및 배포 준비

- 프론트엔드/백엔드 통합 테스트
- 시뮬레이터 시나리오 테스트
- 알람 발생/확인/해결 테스트
- 장비 10대 동시 표시 성능 확인
- 배포 스크립트 또는 실행 가이드 작성
- 사용자 검수용 데모 데이터 정리

## 11. 작업 분해 구조

### 11.1 Frontend

| 작업 ID | 작업명 | 우선순위 |
| --- | --- | --- |
| FE-001 | Vite React TypeScript 프로젝트 구성 | Must |
| FE-002 | 전체 레이아웃 구성 | Must |
| FE-003 | 3D 맵 렌더링 구성 | Must |
| FE-004 | 장비 3D 모델 컴포넌트 구현 | Must |
| FE-005 | WebSocket 상태 수신 처리 | Must |
| FE-006 | 장비 선택 및 상세 패널 구현 | Must |
| FE-007 | 장비 검색 및 필터 구현 | Must |
| FE-008 | 알람 패널 구현 | Must |
| FE-009 | KPI 요약 카드 구현 | Must |
| FE-010 | 이력 조회 화면 구현 | Should |
| FE-011 | 화면 반응형 및 스타일 개선 | Should |

### 11.2 Backend

| 작업 ID | 작업명 | 우선순위 |
| --- | --- | --- |
| BE-001 | Node.js 서버 프로젝트 구성 | Must |
| BE-002 | DB 스키마 및 초기 데이터 구성 | Must |
| BE-003 | 장비 목록 API 구현 | Must |
| BE-004 | 장비 상태 API 구현 | Must |
| BE-005 | WebSocket 서버 구현 | Must |
| BE-006 | 시뮬레이터 구현 | Must |
| BE-007 | 알람 생성 로직 구현 | Must |
| BE-008 | 알람 조회/처리 API 구현 | Must |
| BE-009 | KPI 계산 API 구현 | Must |
| BE-010 | 상태 이력 저장 및 조회 구현 | Should |
| BE-011 | API 문서 작성 | Should |

### 11.3 3D/Map

| 작업 ID | 작업명 | 우선순위 |
| --- | --- | --- |
| MAP-001 | 현장 좌표계 정의 | Must |
| MAP-002 | 구역 정보 정의 | Must |
| MAP-003 | 이동 경로 정의 | Must |
| MAP-004 | 충전소/스테이션/컨베이어 배치 | Must |
| MAP-005 | 장비 유형별 3D 표현 방식 정의 | Must |
| MAP-006 | 상태별 색상 및 하이라이트 정의 | Must |

### 11.4 QA

| 작업 ID | 작업명 | 우선순위 |
| --- | --- | --- |
| QA-001 | API 단위 테스트 | Must |
| QA-002 | 시뮬레이터 상태 전환 테스트 | Must |
| QA-003 | WebSocket 실시간 갱신 테스트 | Must |
| QA-004 | 3D 장비 표시 테스트 | Must |
| QA-005 | 알람 발생 및 처리 테스트 | Must |
| QA-006 | 10대 장비 동시 표시 성능 테스트 | Must |
| QA-007 | 브라우저 호환성 테스트 | Should |

## 12. 테스트 계획

### 12.1 기능 테스트

- 장비 10대가 초기 화면에 모두 표시되는지 확인한다.
- AGV 4대와 AMR 4대가 지정 경로를 따라 이동하는지 확인한다.
- ABCS 2대가 고정 설비로 표시되고 상태가 갱신되는지 확인한다.
- 장비 선택 시 상세 패널 정보가 정확히 표시되는지 확인한다.
- 상태 필터를 적용했을 때 목록과 3D 표시가 일치하는지 확인한다.
- 알람 발생 시 알람 목록과 3D 강조 표시가 동시에 반영되는지 확인한다.
- 알람 확인 및 해결 처리가 정상 반영되는지 확인한다.

### 12.2 성능 테스트

- 10대 장비 기준 실시간 갱신 지연이 1초 이내인지 확인한다.
- 3D 화면이 일반 개발 PC에서 30 FPS 이상 유지되는지 확인한다.
- WebSocket 연결이 끊겼을 때 재연결 또는 상태 표시가 정상 동작하는지 확인한다.

### 12.3 통합 테스트

- 시뮬레이터, 백엔드, 프론트엔드 전체 흐름을 검증한다.
- 서버 재시작 후 초기 상태가 정상 로딩되는지 확인한다.
- 장비 상태 이력과 현재 상태가 일관되게 저장되는지 확인한다.
- 알람 상태 변경이 API, DB, WebSocket, UI에 모두 반영되는지 확인한다.

## 13. 완료 기준

MVP는 다음 조건이 충족되면 완료로 판단한다.

- AGV 4대, AMR 4대, ABCS 2대가 3D 맵에 표시된다.
- AGV/AMR 위치가 실시간으로 갱신된다.
- ABCS 상태 및 처리량이 실시간으로 갱신된다.
- 장비 상세 패널에서 주요 상태 정보를 확인할 수 있다.
- 알람 발생, 목록 표시, 장비 강조가 동작한다.
- 기본 KPI가 화면에 표시된다.
- 장비 검색과 필터가 동작한다.
- 상태 이력 조회가 가능하다.
- 로컬 환경에서 실행 가능한 가이드가 제공된다.
- 주요 기능 테스트가 통과한다.

## 14. 주요 리스크 및 대응

| 리스크 | 영향 | 대응 |
| --- | --- | --- |
| 3D 구현 복잡도 증가 | 일정 지연 | 초기에는 단순 지오메트리 기반 모델로 구현 |
| 실시간 상태와 UI 불일치 | 관제 신뢰도 저하 | 서버 상태 모델을 단일 기준으로 유지 |
| 장비 좌표계 미확정 | 실제 장비 연동 지연 | MVP는 내부 좌표계 사용, 변환 계층은 별도 설계 |
| 알람 조건 과도한 복잡화 | 개발 범위 증가 | MVP는 배터리 부족, 오류 상태, 통신 두절 중심으로 제한 |
| UI 정보 과다 | 사용성 저하 | 메인 화면은 핵심 상태 중심, 상세는 패널로 분리 |
| 실제 장비 연동 지연 | 데모 불가 | 시뮬레이터를 정식 MVP 구성 요소로 포함 |

## 15. 개발 산출물

| 산출물 | 설명 |
| --- | --- |
| 소스 코드 | 프론트엔드, 백엔드, 시뮬레이터 |
| DB 스키마 | 장비, 상태, 알람, 맵 테이블 정의 |
| API 문서 | REST API 및 WebSocket 이벤트 명세 |
| 실행 가이드 | 로컬 실행 및 환경 변수 설정 |
| 테스트 결과 | 주요 기능 및 통합 테스트 결과 |
| 데모 시나리오 | 장비 이동, 알람 발생, KPI 확인 시나리오 |

## 16. 후속 확장 계획

- 실제 장비 연동 어댑터 추가
- WMS/MES/MCS 연동
- 리플레이 기능 고도화
- 병목 히트맵
- 다중 현장 지원
- 사용자 권한 체계 강화
- 예측 정비 및 이상 탐지
- 운영 리포트 자동 생성
