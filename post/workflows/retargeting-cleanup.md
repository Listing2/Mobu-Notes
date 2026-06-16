# 리타게팅 및 클린업 — 실무 절차

모션캡처 등으로 녹화한 FBX를 MotionBuilder 2025에서 리타게팅·클린업하여 FBX로 export하는 **단계별 절차**.

개념·옵션·원인 분석은 [retargeting-fundamentals.md](retargeting-fundamentals.md) 참고.

---

## 전체 흐름

```text
타겟 characterize → 모션 merge·retarget → Plot to CR → CR 클린업(Layer·발) → Plot to Skeleton → FBX → Unity
```

**일상 작업 순서:** [실무 순서 — Animation Layer 파이프](#실무-순서--animation-layer-파이프-권장)  
**개념:** [retargeting-fundamentals.md](retargeting-fundamentals.md)

---

## 실무 순서 — Animation Layer 파이프 (권장)

모션 FBX open → 캐릭터 merge → Source retarget → **Plot to CR** → **CR cleanup / layer** → Plot to Skeleton → Unity.  
Phase 번호와 1:1 대응은 아래 표 참고.

| # | 할 일 | Phase | 주의 (흔한 실수) |
|---|--------|-------|------------------|
| 1 | **모션-only FBX** open / merge | 1 | RT 풀 export 재merge 금지 |
| 2 | **타겟 캐릭터** merge + characterize + Reference pose | 0 | VRM 변환본 어깨·T-pose 확인 |
| 3 | **모션** characterize → 타겟 **Source**에 연결 | 1~2 | Mapping·0프레임 pose |
| 4 | **Source QC / cleanup** — 원본 튐·누락 먼저 확인 | 1.1 | 소스에서 튄 키는 Plot 전 보간/flat/smooth |
| 5 | Definition **스케일**을 모션(액터)에 맞춤 (예: 1.3) | 2.1 | Plot **전** 발·손 reach 몇 프레임 확인 |
| 6 | **Match Source Off** · Live Retarget **프리뷰** | 2.2~2.3 | Plot 전 큰 문제는 여기서 해결 |
| 7 | **Hand IK T/R 100은 preview / reach pass로 사용** | 2 | 손목 reach를 맞추는 데 도움. finger hold와는 역할 분리 → [판단 기준](#판단-기준--어디서-고칠까) |
| 8 | **Plot to Control Rig** (전신+손가락, Reducer Off) | 3 | Base 레이어 = Plot 결과 |
| 9 | **소스 캐릭터 제거** · Source/Relation **Off** | 3~4 | 소스 남으면 CR cleanup과 finger curve 싸움 |
| 10 | **CR Animation Layer** — 손/머리 보정 | 4.2 | hard finger hold는 [Layer 가이드](layer-override-hands-head.md#base-finger-reference-only-아이디어) 참고 |
| 11 | 발 **Foot IK** (필요 시) | 4.1 | 발 sliding은 Layer 비추 |
| 12 | **Plot to Skeleton** (Reducer Off) | 5 | Layer·CR 만족 **후** 한 번만 |
| 13 | FBX export (skeleton anim) → Unity | 6 | CR·소스·mesh 불필요 시 제외 |

### 판단 기준 — 어디서 고칠까

| 문제 | 먼저 볼 곳 | 고칠 곳 |
|------|------------|---------|
| 원본이 몇 프레임 튐 | 소스 캐릭터 solo | **Plot 전 Source cleanup** |
| 손목 reach가 안 맞음 | Live Retarget preview | Hand IK T/R 100 preview/pass |
| 주먹·검지 등 손 모양 고정 | CR Layer 결과 | [Layer 가이드](layer-override-hands-head.md) |
| Plot 후 한두 프레임 튐 | CR curve | **Plot 후 CR cleanup** |

**비유:** Live Retarget = **통역**, Source QC = **원문 교정**, Plot to CR = **초고**, CR cleanup/layer = **연필 수정**, Plot to Skeleton = **인쇄**, Unity = **배포**.

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

### 1.1 Source QC / cleanup — 모캡 원본 튐

모캡 스튜디오 작업에서는 원본 데이터 자체가 몇 프레임씩 튀는 경우가 있다. 이건 타겟 캐릭터 문제가 아니라 **입력 데이터 결함**이므로, retarget / Plot 전에 먼저 잡는 편이 깨끗하다.

| 어디서 튀나 | 처리 위치 |
|-------------|-----------|
| 소스 캐릭터만 봐도 튐 | **Source cleanup** 후 retarget |
| 소스는 정상, 타겟 preview만 튐 | scale · mapping · reference · reach 확인 |
| preview는 정상, Plot 후 CR에서 튐 | **CR cleanup** 에서 키 삭제/보간/smooth |
| Unity에서만 튐 | Skeleton plot · FBX export · Unity import 확인 |

**원칙:** 소스에서 이미 튄 키는 소스에서 먼저 보간한다. 소스가 깨진 상태로 Plot하면, 타겟 CR에 깨진 키가 bake되어 뒤에서 더 많은 보정이 필요해진다.

### 1.2 Source cleanup 방법

| 증상 | 우선 처리 |
|------|-----------|
| 1~2프레임 pop | 튄 키 삭제 → 앞뒤 정상 프레임 보간 |
| 짧은 jitter 구간 | 해당 source joint / marker curve만 약하게 smoothing |
| marker occlusion / 순간 이동 | 구간 제거 → 앞뒤 pose bridge → 필요 시 손키 |
| 발 contact 구간 튐 | smoothing 과용 금지. 접지 프레임을 보존하며 보간 |
| 손가락 원본이 계속 흔들림 | 최종 손 포즈가 중요하면 CR 단계에서 [Base finger reference-only](layer-override-hands-head.md#base-finger-reference-only-아이디어) 옵션 고려 |

**팁**

- 먼저 **소스만 solo로 재생**해서 결함 프레임을 적는다. 타겟까지 같이 보면 retarget 문제와 섞여 보인다.
- 전체 take smoothing보다 **문제 joint + 문제 구간만** 처리한다.
- 빠른 액션, 타격, 손짓은 노이즈처럼 보여도 의도 동작일 수 있다. smoothing 전에 앞뒤 맥락을 본다.
- 발·손 contact 프레임은 키를 너무 지우면 sliding이 생긴다. pop 제거와 contact 보존을 같이 본다.
- 소스 cleanup을 많이 했다면 take 이름이나 세션 로그에 `source_cleaned`, 프레임 범위, 처리 joint를 기록한다.

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
| **Source → Target** | Character Controls — 소스 캐릭터 | Live Retarget 프리뷰 |
| **Hand IK (Plot 전)** | **T/R 100 가능** | 손목 reach 확인·보정용. finger hold는 별도 pose layer로 확정 |

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

Control Rig 컨트롤이 활성화되면 **소스 제거 · Source Off** ([실무 #8](#실무-순서--animation-layer-파이프-권장)) 후 Phase 4.

---

## Phase 4 — Control Rig 클린업

**FBX 애니메이션 품질의 핵심 구간.** 발 sliding 1차 해결은 여기서.

### 4.1 Foot sliding

1. Foot IK 켜고 접지 프레임에서 ankle·ball 위치 고정.
2. 필요 시 **hip counter-translate** (발은 고정, 골반만 미세 이동).
3. 계단·경사면은 프레임별로 contact 키.

### 4.2 손 · 머리 (Animation Layer)

Control Rig **Animation Layer** + Weight — [layer-override-hands-head.md](layer-override-hands-head.md) (실무 #9).  
손목 reach는 IK pass로 맞추고, 주먹·펼침·검지 같은 **finger hold는 전용 Layer pose + Weight**로 먼저 확정 → [Layer 가이드](layer-override-hands-head.md#한눈-요약).

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

[실무 순서](#실무-순서--animation-layer-파이프-권장) 기준. Layer·Weight 상세: [layer-override-hands-head.md](layer-override-hands-head.md).

### MotionBuilder

- [ ] Source solo 재생 — 원본 pop / jitter / occlusion 프레임 확인
- [ ] 소스에서 튄 키는 Plot 전 보간/flat/smooth
- [ ] Hand IK T/R 100은 reach preview/pass 용도 · Match Source Off
- [ ] Plot to CR 후 **소스 캐릭터 제거**
- [ ] Animation Layer + Weight (손·목)
- [ ] Plot to Skeleton · export skeleton only

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
| Source QC / cleanup (프레임·joint·처리) | |
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
- [layer-override-hands-head.md](layer-override-hands-head.md) — Layer · Weight
- [unity-import.md](../unity-import.md) — Unity import
