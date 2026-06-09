# 리타게팅 및 클린업 — 실무 절차

모션캡처 등으로 녹화한 FBX를 MotionBuilder 2025에서 리타게팅·클린업하여 FBX로 export하는 **단계별 절차**.

개념·옵션·원인 분석은 [retargeting-fundamentals.md](retargeting-fundamentals.md) 참고.

---

## 전체 흐름

```text
VRM or FBX 캐릭터
    ↓ (툴로 FBX export)
MotionBuilder — 타겟 characterize + Reference pose 확인
    ↓
원본 모션 FBX merge (fps·축 확인)
    ↓
모션 스켈레톤 characterize (소스) + Mapping 확인
    ↓
스케일을 모션(소스)에 맞춤
    ↓
Retarget — Match Source Off, 라이브처럼 프리뷰
    ↓
Bake / Plot to Control Rig
    ↓
Control Rig — foot / hand / spine 클린업
    ↓
Bake / Plot to Skeleton
    ↓
FBX export → Unity / Timeline / Cinemachine
```

---

## Phase 0 — 씬·Take 준비

### 확인 항목

| 항목 | 방법 |
|------|------|
| Mobu 버전 | 2025 |
| Timeline fps | 모캡 take와 일치 (60 / 120 등) |
| Up axis · unit | Y-up, cm — import 시 틀리면 여기서 수정 |
| 타겟 캐릭터 | characterize 완료, T-pose(또는 파이프 기준 pose) 정상 |

### VRM / FBX 캐릭터 → Mobu

1. VRM 또는 FBX를 **export 툴**로 FBX export. (툴 이름·옵션 세션마다 기록)
2. Mobu에 merge.
3. **Characterize** (HumanIK).
4. Viewer에서 **Reference Pose** — 팔·다리·지면 관계 확인.  
   VRM 변환본은 어깨 각도 깨짐 빈번 → [fundamentals §3](retargeting-fundamentals.md#3-reference-pose-rest-pose--retarget-전-필수).

---

## Phase 1 — 모션 import (소스)

1. 모캡 **원본 모션 FBX** merge.
2. take 길이·fps가 타임라인과 맞는지 확인.
3. 모션 FBX 안 **스켈레톤 characterize** → **소스 캐릭터**.
4. **Character Mapping:** 소스 ↔ 타겟 본 연결. Auto 실패 시 수동.
5. 0프레임 pose 확인 — rest pose 이상하면 reference 정리 후 진행.

---

## Phase 2 — 스케일 · Retarget

### 2.1 스케일

타겟 캐릭터 scale을 **모션(소스) 스케일에 맞춤**.  
발·무릎·손 reach를 Viewer에서 대표 프레임 몇 개로 확인.

### 2.2 Retarget 설정

| 항목 | 본인 파이프 설정 | 비고 |
|------|------------------|------|
| **Match Source** | **Off** | root·접지는 Control Rig에서 확정 |
| **스케일** | 모션에 맞춤 (Phase 2.1) | [fundamentals §5](retargeting-fundamentals.md#5-스케일--비율-proportion) |
| **Source → Target** | Character Controls / Story — 소스 선택 | UI 경로는 버전·레이아웃에 따라 다름 |

### 2.3 프리뷰 체크 (Plot 전)

재생하며 아래만 빠르게 본다.

- [ ] 발이 대략 지면에 있는가
- [ ] 손·팔 penetration 없는가
- [ ] 골반·root drift 과한가
- [ ] 머리·neck 자연스러운가

큰 문제는 **Plot 전**에 스케일·mapping·reference pose로 돌아가서 수정.

---

## Phase 3 — Plot to Control Rig

1. 타겟 캐릭터 선택.
2. **Bake / Plot to Control Rig** (메뉴: Character Controls 또는 Animation 맥락).
3. Plot 옵션:
   - Frame range: **전체 take**
   - Sample: **take fps와 동일**
   - Constant Key Reducer: **Off** 또는 보수적 (접지 키 보존)

Control Rig 컨트롤이 활성화되면 Phase 4로.

---

## Phase 4 — Control Rig 클린업

**FBX 애니메이션 품질의 핵심 구간.** 발 sliding 1차 해결은 여기서.

### 4.1 Foot sliding

1. Foot IK 켜고 접지 프레임에서 ankle·ball 위치 고정.
2. 필요 시 **hip counter-translate** (발은 고정, 골반만 미세 이동).
3. 계단·경사면은 프레임별로 contact 키.

### 4.2 손 · 머리

- Reach / Hand IK로 그립·터치 위치.
- Neck/Head FK로 look 방향 미세 조정 (시네머신 연동 시 과도한 head key는 피할 수 있음).

### 4.3 Spine / Hip

- 상체 각도, 좌우 무게 중심.
- Retarget에서 남은 “robotic” 느낌 완화.

### 4.4 작업 습관

- 큰 수정 후 **구간 loop 재생**으로 sliding 재확인.
- 만족할 때까지 Skeleton plot 하지 않기.

---

## Phase 5 — Plot to Skeleton

1. **Bake / Plot to Skeleton** (Control Rig → 본).
2. Plot 옵션 기록:

| 옵션 | 권장 |
|------|------|
| Plot Translation on Root | root motion 필요 시 **On** |
| Plot on Frame | **On** (take rate) |
| Constant Key Reducer | **Off** 또는 낮은 threshold |
| Rotation + Translation | 전신 |

3. Plot 후 **Skeleton**에서 키 확인 — Control Rig가 아닌 본에 키가 있어야 export 대상.

---

## Phase 6 — FBX Export

1. export 대상: **타겟 캐릭터 skeleton** (+ 필요 시 mesh).
2. **제외:** 소스 모캡 캐릭터, Control Rig 컨트롤, constraint helper.
3. take / animation stack에 plot된 take가 있는지 확인.
4. export 옵션·fps·unit 기록.

Unity import 시 foot sliding 등은 [unity-import.md](../unity-import.md).

---

## Match Source — 용도별 정리

| 목적 | Match Source |
|------|--------------|
| **클린업 → FBX export (본인 기본)** | **Off** |
| 라이브 프리뷰·비슷한 체형·소스 이동 그대로 | On |
| root·접지를 Control Rig에서 전부 잡을 예정 | Off |

---

## 세션 체크리스트

### MotionBuilder

- [ ] 타겟 characterize + reference pose OK
- [ ] 모션 merge — fps·축 OK
- [ ] 소스 characterize + mapping OK
- [ ] 스케일 모션에 맞춤
- [ ] Retarget — Match Source Off
- [ ] Plot to Control Rig (reducer 보수적)
- [ ] Foot / hand / spine 클린업
- [ ] Plot to Skeleton
- [ ] Export — skeleton only, 옵션 기록

### Unity (downstream)

- [ ] [unity-import.md](../unity-import.md) 설정
- [ ] Foot sliding 없음
- [ ] Timeline / Cinemachine 연동

---

## 세션 로그 (복붙용)

| 항목 | 값 |
|------|-----|
| 날짜 | |
| Mobu 버전 | 2025 |
| 소스 모션 (파일·fps) | |
| 타겟 캐릭터 (VRM/FBX·export 툴) | |
| Match Source | Off |
| Plot 옵션 (reducer, root translation) | |
| Export fps / unit | |
| 이슈·조치 | |

---

## TODO (본인 보강)

- [ ] 캐릭터 FBX export 툴 이름·옵션
- [ ] Retarget / Plot 메뉴 경로 스크린샷 (Mobu 2025 UI)
- [ ] 대표 캐릭터별 reference scale 메모
- [ ] Control Rig foot IK 프리셋

---

## 관련 문서

- [retargeting-fundamentals.md](retargeting-fundamentals.md) — 개념·옵션·원인
- [unity-import.md](../unity-import.md) — Unity import
