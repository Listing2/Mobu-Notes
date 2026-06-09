# Animation Layer — 손 · 머리 Override

Plot to CR **이후** 손가락·Neck/Head만 Animation Layer + Weight로 덮어쓰기.

| 문서 | 역할 |
|------|------|
| [retargeting-cleanup.md](retargeting-cleanup.md) | 전체 Phase · [실무 12단계](retargeting-cleanup.md#실무-순서--animation-layer-파이프-권장) |
| **이 문서** | Layer · Weight · drift 트러블슈팅 |

---

## 언제 쓰는가

| 증상 | 대응 |
|------|------|
| 손가락 drift, 주먹·그립 고정 | 손 레이어 + Weight |
| Neck/Head 과꺾임 (A~B) | 머리 레이어 + Weight |
| 발 sliding | Layer X → [cleanup §4.1](retargeting-cleanup.md#phase-4--control-rig-클린업) Foot IK |

merge 입력: **모션-only FBX** (예: `Kapu_001.fbx`). RT 풀 export 재merge는 drift 유발.

---

## 레이어 구조

```text
Base (Weight 100%)     ← Plot to CR (전신+손가락)
Hands_Grip_Fist         ← Weight 키
Hands_Grip_Open
Head_Neck_Fix_01
```

**원칙:** 포즈 = 레이어 · **타이밍 = Layer Weight** · 키 = **Control Rig** (Skeleton 직접 키 X)

**전제:** [cleanup Phase 3](retargeting-cleanup.md#phase-3--plot-to-control-rig) Plot to CR · 소스 제거 · Base untouched — [실무 #7~8](retargeting-cleanup.md#실무-순서--animation-layer-파이프-권장)

---

## 손 — 포즈 + Weight

1. 레퍼런스 프레임 → 레이어 `Hands_Grip_Fist` 등 추가.
2. **Finger FK multi-select** → 주먹·펼침·그립 pose.
3. **Weight 키:**

| 프레임 | Fist Weight | Open Weight |
|--------|-------------|-------------|
| A | 0→100 | 0 |
| A~B | 100 | 0 |
| C | 100→0 | 0→100 |

- Hold: A·B 동일 pose · tangent **Flat / Constant**.
- Hold 구간: **Hand IK Off** · **FK finger only** (IK + mocap finger = drift).

그립 2~4종 반복 → 레이어 분리 + Weight. 1~2번만 → 레이어 1개 + 구간 키도 OK.

---

## Neck / Head

1. `Head_Neck_Fix_01` 레이어 · **CR Neck + Head FK**만.
2. A~B Weight 100 · 밖 0 · Hold Flat.

---

## Plot · Export

Layer·Weight loop 확인 후 → [cleanup Phase 5~6](retargeting-cleanup.md#phase-5--plot-to-skeleton) Plot to Skeleton · export.

---

## drift / 포즈가 풀릴 때

| 증상 | 확인 |
|------|------|
| 손가락 서서히 벌어짐 | Plot to CR **손가락 포함** · **소스 캐릭터** 잔존 |
| 레이어 켰는데도 변함 | Skeleton finger curve → **CR만** 키 |
| Hold 중 튐 | Hand IK + finger 동시 → **FK only** |
| Weight 100인데 섞임 | Override에 **손/목 CR만** 키 |

Plot 전 **Hand IK 100** → Base에 bake되어 Layer와 싸움 → [Hand IK × Layer](retargeting-cleanup.md#hand-ik--animation-layer-타이밍).

---

## Kapu / Cappu 메모

| 파일 | 용도 |
|------|------|
| `Kapu_001.fbx` (~4MB) | merge 소스 (30fps, 손가락 본 포함) |
| `Kapu_RT_001.fbx` (~364MB) | 풀 export — **재merge 비추** |

레이어 키: **CR(HumanIK)** — `cappu_Ctrl`, Finger FK (Skeleton `Cappu_Char:…` X).

---

## 관련

- [retargeting-fundamentals.md](retargeting-fundamentals.md) §10 Foot Sliding
- [../scripts/vendor/README.md](../scripts/vendor/README.md)
