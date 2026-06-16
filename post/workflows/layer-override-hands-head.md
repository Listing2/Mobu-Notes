# Animation Layer — 손 · 머리 Override

손가락·Neck/Head를 **Animation Layer + Weight**로 구간별 고정/완화하는 메모.  
큰 손가락 pose hold는 Plot to CR 이후 solver로 버티게 하지 말고, **전용 layer에서 먼저 포즈를 소유**하게 한 뒤 CR/스켈레톤으로 굳힌다.

| 문서 | 역할 |
|------|------|
| [retargeting-cleanup.md](retargeting-cleanup.md) | 전체 Phase · [실무 순서](retargeting-cleanup.md#실무-순서--animation-layer-파이프-권장) |
| **이 문서** | Layer · Weight · drift 트러블슈팅 |

---

## 언제 쓰는가

| 증상 | 대응 |
|------|------|
| 손가락 drift, 주먹·그립 고정 | 손 레이어 + Weight |
| Neck/Head 과꺾임 (A~B) | 머리 레이어 + Weight |
| 발 sliding | Layer X → [cleanup §4.1](retargeting-cleanup.md#phase-4--control-rig-클린업) Foot IK |

merge 입력: **모션-only FBX** (예: `Kapu_001.fbx`). RT 풀 export 재merge는 drift 유발.

## 한눈 요약

| 목적 | 담당 |
|------|------|
| 손목 위치 맞추기 | Hand IK / wrist effector |
| 손가락 모양 고정 | Finger FK pose layer |
| 포즈가 들어오는 타이밍 | Layer Weight |
| Base 손가락이 계속 흔들릴 때 | 문제 구간 finger curve flat / reference-only 옵션 |

---

## 레이어 구조

```text
Base (Weight 100%)     ← Plot to CR (전신+손가락)
Hands_Grip_Fist         ← Weight 키
Hands_Grip_Open
Hands_Index_Point
Head_Neck_Fix_01
```

**원칙:** 포즈 = 레이어 · **타이밍 = Layer Weight** · 키 = **Control Rig / pose layer** (Skeleton 직접 키 X)

**전제:** [cleanup 실무 순서](retargeting-cleanup.md#실무-순서--animation-layer-파이프-권장). 손목 reach는 IK pass로 맞춰도 되지만, finger hold는 CR solver가 아니라 **전용 layer pose**가 맡는 쪽이 안정적이다.

---

## 어디서 해야 하나

| 작업 | 추천 단계 | 이유 |
|------|-----------|------|
| 손목 reach 맞추기 | Plot 전 IK pass / 필요 시 CR effector 키 | IK 100이 실제로 도움 되는 구간 |
| 주먹·다 편 손·검지 pointing 같은 **정해진 손가락 pose** | **전용 hand layer**에서 pose + Weight | CR에서 IK/FK가 섞이면 “합성된 결과”처럼 보여 hard hold가 안 됨 |
| Plot 후 CR 손가락 수정 | 미세 보정만 | 큰 pose hold는 이미 bake된 Base와 싸우기 쉬움 |

CR Animation Layer는 강한 constraint가 아니라 **Base 위에 섞이는 layer**에 가깝다. 손가락 hold를 고정하려면 손가락 전체 pose를 한 layer가 소유하고, Weight로 들어오고 나가는 시간을 제어한다.

### Base finger reference-only 아이디어

기존 모션의 finger curve를 **최종 데이터**로 끝까지 살리는 대신, “어떤 포즈가 필요했는지 보는 레퍼런스”로만 쓰는 방법도 고려할 만하다.

```text
BaseAnimation
├── body / arm / wrist  유지
└── finger              문제 구간만 flat 또는 제거

Hands_Fist / Hands_Open / Hands_Index_Point
└── Finger FK pose + Weight
```

이건 기본 단계가 아니라 **hard hold가 필요할 때의 옵션**이다. 손가락 mocap 디테일을 버리는 대신, 주먹·펼침·검지 pointing 같은 포즈가 확실히 고정된다. 처음에는 전체 take 삭제보다 **문제 구간만 flat**을 먼저 테스트한다.

---

## 손 — 포즈 + Weight

1. 레퍼런스 프레임 → 레이어 `Hands_Grip_Fist` 등 추가.
2. **Finger FK multi-select** → 주먹·펼침·검지 pointing·그립 pose.
3. **Weight 키:**

| 프레임 | Fist Weight | Open Weight | Index Point Weight |
|--------|-------------|-------------|--------------------|
| A | 0→100 | 0 | 0 |
| A~B | 100 | 0 | 0 |
| C | 100→0 | 0→100 | 0 |
| D | 0 | 100→0 | 0→100 |

- Hold: A·B 동일 pose · tangent **Flat / Constant**.
- Hold 구간: **Finger FK pose가 소유**. Hand IK는 손목 reach용이지 finger hold 고정용이 아님.

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
| Hold 중 튐 | 손목 IK와 finger pose가 같이 소유 → finger pose layer가 손가락 전체를 소유하게 정리 |
| Weight 100인데 섞임 | Layer mute/lock, Weight key, 또는 Base에 남은 finger curve 확인 |

손목은 IK 100으로 맞춰도 된다. 단, 주먹·펼침·검지 pointing처럼 “정해진 손 모양을 오래 유지”하는 작업은 IK가 아니라 **pose preset layer + Weight**가 맡는다 → [cleanup 판단 기준](retargeting-cleanup.md#판단-기준--어디서-고칠까).

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
