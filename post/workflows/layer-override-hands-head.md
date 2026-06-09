# Animation Layer — 손 · 머리 Override

Control Rig 클린업(Phase 4)에서 **손가락·Neck/Head만** 구간별로 덮어쓰는 방법.  
전신 파이프: [retargeting-cleanup.md](retargeting-cleanup.md) Phase 0~6.

---

## 언제 쓰는가

| 증상 | 레이어 Override |
|------|-----------------|
| 손가락 mocap drift, 주먹·그립 고정 | 손 레이어 + Weight |
| Neck/Head 과꺾임 (A~B 구간) | 머리 레이어 + Weight |
| 발 sliding | **레이어 비추천** → Foot IK ([retargeting-cleanup.md](retargeting-cleanup.md) §4.1) |

입력 merge는 **모션-only FBX** (예: `Kapu_001.fbx`). RT 풀 씬(소스+캐+리그) 재import는 drift 원인.

---

## 레이어 구조 (권장)

```text
Base (Weight 100%, 항상)
  ← Plot to Control Rig 전신 (손가락 포함)

Hands_Grip_Fist   (Weight 키)   ← 미리 잡아둔 포즈
Hands_Grip_Open   (Weight 키)
Hands_Grip_Prop   (Weight 키)

Head_Neck_Fix_01  (Weight 키)   ← A~B 목/머리 보정
```

**원칙:** 포즈는 레이어에, **타이밍은 Layer Weight** 키.

---

## Phase A — 레이어 만들기 전 (필수)

[retargeting-cleanup.md](retargeting-cleanup.md) **Phase 0~3 완료 후** — Plot to Control Rig **이후**, Override 레이어 **이전**.

| 확인 | 내용 |
|------|------|
| 전제 | merge·Retarget·**Plot to CR**(전신+손가락, reducer Off)·**소스 캐릭터 제거** — cleanup Phase 1~3 |
| Base | Plot 결과 **그대로** (손·목 먼저 손대지 않기) |
| 키 대상 | **Control Rig** (`cappu_Ctrl`, Finger FK, Neck/Head FK). **Skeleton** (`Cappu_Char:…`) 직접 키 X |

---

## Phase B — 손: 미리 포징 + Weight

### 1. 포즈 프리셋 (레퍼런스 프레임)

1. 레퍼런스 프레임(0 또는 작업용 1프레임)으로 이동.
2. 레이어 `Hands_Grip_Fist` 등 **새 레이어** 추가.
3. **Finger FK multi-select** → 주먹·펼침·그립 pose.
4. **Hand IK hold 구간**에서는 **FK finger** 사용 (IK + mocap finger = drift).

같은 rotation 숫자를 모든 본에 paste하지 말고, **여러 FK를 같이 rotate**하거나 **Pose paste**.

### 2. Weight 키 (타임라인)

| 프레임 | Fist Weight | Open Weight | 보이는 손 |
|--------|-------------|-------------|-----------|
| A | 0→100 | 0 | mocap → 주먹 |
| A~B | 100 | 0 | 주먹 hold |
| C | 100→0 | 0→100 | 주먹 → 펼침 |

- Hold: A·B **동일 pose**, tangent **Flat / Constant**.
- 전환: Weight 1~3프레임 블렌드 (또는 Constant 0/100).

### 3. 그립 종류별

| 그립 수 | 방식 |
|---------|------|
| 2~4종 반복 | **레이어 분리 + Weight** (권장) |
| 1~2번만 | 레이어 1개 + 구간별 키도 OK |

---

## Phase C — Neck / Head

1. 레이어 `Head_Neck_Fix_01` 추가.
2. **CR Neck + Head FK**만 선택 → 과꺾임 덜한 pose.
3. A~B **Weight 100**, 밖에서는 **0**.
4. Hold: A·B 동일 + Flat tangent.

머리는 본 수가 적어 손보다 관리가 쉽다. 구간마다 레이어를 늘리거나, 한 레이어에 구간별 pose 키.

---

## Phase D — Plot to Skeleton · Export

1. 모든 레이어 Weight·pose 확인 (loop 재생).
2. **Bake to Control Rig** 이미 끝난 상태 → 레이어 merge 평가.
3. **Bake to Skeleton** (CR → skeleton), Reducer **Off**.
4. Export: **skeleton anim만** — 소스·CR·mesh 제외.

---

## drift / 포즈가 풀릴 때

| 증상 | 확인 |
|------|------|
| 손가락이 서서히 벌어짐 | Plot to CR에 **손가락 포함**했는지 · **소스 캐릭터** 남았는지 |
| 레이어 켰는데도 변함 | Skeleton finger curve 살아 있음 → CR만 키했는지 |
| Hold 중 튐 | **Hand IK** + mocap finger 동시 → Hold 구간 **FK only** |
| Weight 100인데 섞임 | Override 레이어에 **손/목 CR만** 키했는지 |

---

## Kapu / Cappu 메모

| 파일 | 용도 |
|------|------|
| `Kapu_001.fbx` (~4MB) | merge **소스 모션** (30fps, ~1489f, 손가락 본 포함) |
| `Kapu_RT_001.fbx` (~364MB) | Mobu 풀 export — **재merge 비추** (소스+`Cappu_Char`+`cappu_Ctrl`+Layer) |

본 이름: 소스 `LeftHandIndex1` … / 타겟 `Cappu_Char:Thumb_Proximal_L` … → 레이어 키는 **CR(HumanIK)** 쪽.

---

## 체크리스트

- [ ] Plot to CR (전신+손가락, reducer Off)
- [ ] 소스 캐릭터 / Relation 제거
- [ ] Base = Plot 결과
- [ ] 손 포즈 프리셋 레이어 (레퍼런스 프레임)
- [ ] 손·머리 **Weight** 키 (A~B hold)
- [ ] Hold 구간 FK finger / Flat tangent
- [ ] Plot to Skeleton → export skeleton only

---

## 관련

- [retargeting-cleanup.md](retargeting-cleanup.md) — 전체 Phase
- [retargeting-fundamentals.md](retargeting-fundamentals.md) §10 Foot Sliding
- [../scripts/vendor/README.md](../scripts/vendor/README.md) — GitHub 스크립트 추가
