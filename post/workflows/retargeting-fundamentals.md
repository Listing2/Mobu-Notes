# 리타게팅 기초 — 알아야 할 개념

MotionBuilder에서 FBX 모션을 다룰 때 **반복해서 마주치는 개념**을 정리합니다.  
워크플로 절차는 [retargeting-cleanup.md](retargeting-cleanup.md)를 함께 보면 됩니다.

---

## 1. Mobu가 모션을 이해하는 방식

MotionBuilder는 FBX 본 계층만으로는 “사람/캐릭터”를 자동으로 알지 못한다.  
**Characterize**를 해야 HumanIK 기반 **Character Definition**이 생기고, Retarget·Control Rig·Plot이 동작한다.

| 용어 | 의미 |
|------|------|
| **Characterize** | 스켈레톤에 HumanIK 캐릭터 정의를 입히는 작업 |
| **Character Definition** | 어느 본이 Hips, Spine, LeftHand 등인지 Mobu가 아는 지도 |
| **Source (소스)** | 모캡·원본 모션이 붙은 characterize된 캐릭터 |
| **Target (타겟)** | 모션을 받을 게임/방송용 캐릭터 |
| **Control Rig** | IK/FK 컨트롤로 손·발·spine을 잡는 편집용 리그 |
| **Skeleton** | 실제 export되는 본 애니메이션 |
| **Retarget** | 소스 포즈를 타겟 비율·본 구조에 **실시간으로** 변환 |
| **Plot / Bake** | Retarget·Control Rig 결과를 **키프레임으로 굳히는** 작업 |

**핵심:** Retarget은 “미리보기·전달”, Plot/Bake는 “최종 데이터 확정”.

---

## 2. FBX import 시점에 확인할 것

merge/import 직후, Retarget 전에 아래를 확인한다. 여기서 틀어지면 이후 모든 단계가 고생한다.

### 2.1 축 (Up Axis) · 단위 (Unit)

| 항목 | 일반적 기대 | 문제 증상 |
|------|-------------|-----------|
| Up Axis | Y-up (Unity·많은 게임 파이프) | 캐릭터가 누워 있거나 90° 기울어짐 |
| Unit | cm (Mobu 기본) vs m (일부 DCC) | 스케일 100배 차이, 발이 땅 밑/위 |
| Root motion | Hips translation 포함 여부 | 제자리 애니인데 캐릭터가 slide |

**확인:** import 옵션, 캐릭터 발 위치, Hips Y 이동 궤적.

### 2.2 프레임레이트 (Take Rate)

- 모캡 원본 fps와 Mobu **Timeline / Take** fps가 다르면 재생 속도·키 간격이 어긋난다.
- merge 후 **Transport / Timecode**에서 take 길이·fps 확인.
- bake(plot) 시 **sample rate**는 보통 take fps와 맞춘다 (예: 60fps take → 60 sample).

### 2.3 본 이름 · 계층 · rest pose

- 모캡 프로그램·DCC·캐릭터 변환 툴마다 본 이름이 다르다.
- Characterize 시 **Auto Map**이 실패하면 수동으로 LeftArm → LeftArm 등 매핑.
- **Rest pose** (T-pose / A-pose)가 소스·타겟에서 다르면 Retarget 첫 프레임부터 팔·어깨가 꺾인다.

---

## 3. Reference Pose (Rest Pose) — Retarget 전 필수

정석 파이프라인에서 **가장 자주 빠지는 단계**이지만, 품질에 가장 크게 영향을 준다.

### 3.1 왜 중요한가

Retarget은 “소스 관절 회전 → 타겟 관절 회전” 변환이다.  
양쪽 **기준 자세(reference)** 가 다르면, 같은 회전값도 다른 visual pose가 된다.

### 3.2 확인 절차

1. 타겟 캐릭터 characterize 후 **Reference Pose** 상태 확인 (보통 T-pose).
2. 소스 모션 캐릭터 characterize 후, **0프레임 또는 bind pose** 확인.
3. 어깨·팔꿈치·손목·골반이 비정상이면:
   - import 옵션의 **Set Neutral Pose**
   - 또는 한 프레임에서 pose를 맞춘 뒤 **Define as Reference Pose** (파이프라인에 따라)

### 3.3 VRM → FBX 변환 시 주의

VRM(Humanoid)을 외부 툴로 FBX 뽑을 때 **A-pose / T-pose / bind pose** 가 툴마다 다르다.  
타겟 characterize 직후 Viewer에서 팔 각도를 꼭 본다.  
여기서 5~10° 어긋나도 Retarget 후 손·어깨 클린업 시간이 크게 늘어난다.

---

## 4. Character Mapping (Relation Mapping)

Characterize = “이 본이 LeftUpLeg다”를 정의.  
**Mapping** = 소스 LeftUpLeg 회전을 타겟 LeftUpLeg에 **어떻게 연결할지** 지정.

### 4.1 Auto vs Manual

| 상황 | 대응 |
|------|------|
| 본 이름·구조가 표준에 가깝다 | Auto mapping으로 충분한 경우 많음 |
| 게임 리그 커스텀 본 이름 | Manual mapping 필수 |
| 소스에 Extra 본 (Prop, Camera) | Retarget 대상에서 제외 |

### 4.2 매핑 오류 증상

| 증상 | 흔한 원인 |
|------|-----------|
| 다리가 뒤로 꺾임 | Left/Right Leg 스왑 |
| 팔이 몸통을 관통 | Clavicle / Shoulder 매핑 오류 |
| 머리만 따로 돌아감 | Neck vs Head vs HeadEnd |
| 손가락 뭉개짐 | Finger chain 누락 (게임 캐릭터는 손가락 생략하기도 함) |

**팁:** Retarget 프리뷰에서 **한 관절씩** isolate해 보고, 어느 본부터 틀어지는지 역추적.

---

## 5. 스케일 · 비율 (Proportion)

리타게팅 품질 1순위 변수. “정설”에서 가장 강조되는 부분.

### 5.1 무엇을 맞추는가

- **키 본 길이 비율:** Hips–Knee–Ankle, Shoulder–Elbow–Wrist
- **전체 캐릭터 scale:** 모캡 배우 대비 게임 캐릭터 체형
- **Root height:** 발이 지면에 닿는지

### 5.2 맞추는 방법 (실무)

1. 타겟 캐릭터 **Scale** 조정 (모션/소스 스켈에 맞춤 — 본인 워크플로 핵심).
2. Retarget 옵션의 **Scale Active / Scale Passive** (버전·UI에 따라 이름 상이).
3. 필요 시 **Character Settings → Definition** 에서 reference scale 확인.

### 5.3 스케일이 틀리면

- 발이 땅을 **미끄러짐** (foot IK로도 한계)
- 손이 무릎·허벅지에 **파묻힘**
- 어깨 shrug / 팔 over-extension

**원칙:** Unity에서 foot sliding을 돌려도, Mobu에서 비율이 크게 틀리면 근본 해결이 안 된다.

---

## 6. Match Source — On / Off

“항상 Off”가 아니라 **무엇을 root에 맡길지** 선택하는 옵션.

| | Match Source **On** | Match Source **Off** |
|---|---------------------|----------------------|
| Root 위치·회전 | 소스 Hips/root를 타겟이 **더 따름** | 타겟 root를 **독립** 유지 |
| 적합한 경우 | 비율 비슷, 소스 이동을 그대로 살리는 라이브 프리뷰 | 스케일 수동 맞춤 후 Control Rig에서 root·접지 직접 잡기 |
| 클린업 파이프 | Plot 전 root drift 주의 | Control Rig에서 hip/root 키 잡기 편함 |

**본인 워크플로 (Match Source Off)가 맞는 이유:**  
스케일을 모션에 맞춘 뒤, **Bake to Control Rig → hip/foot IK로 접지·root를 손으로 확정**할 것이기 때문.

라이브 송출·프리뷰만 할 때는 On이 편할 수 있다. 문서에는 **용도별**로 기록해 두면 좋다.

---

## 7. Retarget vs Live Retarget

| 모드 | 설명 |
|------|------|
| **Live Retarget** | 타임라인 재생 중 실시간 변환. 프리뷰·송출용 |
| **Bake / Plot to Control Rig** | 구간·전체를 키로 저장. 클린업·export용 |

클린업 파이프라인: Live로 대략 확인 → **반드시 Plot으로 굳힌 뒤** Control Rig 편집.

---

## 8. Control Rig — 왜 거치는가

스켈레톤 본에 직접 키를 찍으면:

- FK/IK 전환 시 키가 꼬임
- constraint·retarget 잔여 영향
- export 시 불필요한 본·키 포함

**정석:** Retarget → **Control Rig에 Plot** → IK foot / reach hand / spine → **Skeleton에 Plot**.

### 8.1 Control Rig에서 자주 하는 작업

| 작업 | 방법 |
|------|------|
| Foot sliding | Foot IK, Ankle/Floor contact, 필요 시 hip counter-translate |
| 손 위치 | Reach / Hand IK, constraint |
| 상체 각도 | Spine FK, Chest offset |
| 머리 | Neck/Head FK, look-at은 보통 후단(엔진) |

### 8.2 Plot to Skeleton 시 확인할 옵션

Plot / Bake 대화상자(버전마다 **Plot Options**, **Bake to Skeleton** 등):

| 옵션 | 설명 | 권장 |
|------|------|------|
| **Plot on Frame** | take fps마다 키 | 클린업 export는 보통 On |
| **Plot Translation on Root** | Hips/root 이동을 키에 포함 | root motion 필요 시 On |
| **Constant Key Reducer** | 비슷한 키 제거·압축 | **Off** 또는 보수적 — 발 접지 키가 지워지면 sliding |
| **Rotation / Translation** | 무엇을 bake할지 | 전신 bake 시 둘 다 |
| **Frame range** | 전체 take vs 구간 | merge된 take 전체 확인 |

**기록할 것:** 사용한 옵션 스크린샷 또는 체크 상태. 재현에 필수.

---

## 9. Export (FBX) — 무엇을 내보내는가

Mobu 작업의 **최종 산출물** 정의. Unity는 그 다음 단계.

### 9.1 Export 대상

| 포함 | 제외 |
|------|------|
| 타겟 **Skeleton** 본 애니메이션 | Control Rig 컨트롤러 |
| Skinned mesh (필요 시) | 소스 모캡 캐릭터 |
| Take / Animation stack | Constraint, auxiliary |

**확인:** export 전 Control Rig가 아닌 **Character skeleton**이 선택되어 있는지.

### 9.2 FBX export 옵션 (Mobu 측)

| 항목 | 메모 |
|------|------|
| **ASCII vs Binary** | Binary가 일반적 (용량·호환) |
| **Embed media** | 텍스처 포함 여부 — 애니만이면 Off |
| **Bake animation** | Plot된 take가 stack에 있는지 |
| **Input / Output rate** | fps 일치 |
| **Units** | Unity와 맞출 scale |

### 9.3 Export 전 Self-check

- [ ] 소스 캐릭터 숨김/제외
- [ ] Control Rig → Skeleton plot 완료
- [ ] Constraint 해제 또는 plot으로 bake됨
- [ ] 0프레임·마지막 프레임 pose 이상 없음
- [ ] 발 접지 구간 visual check

---

## 10. Foot Sliding — 원인 계층

발 미끄러짐은 **한 곳**에서 생기지 않는다. 아래 순서로 원인을 좁힌다.

```text
1. Mobu — 스케일/비율 불일치
2. Mobu — Retarget/Match Source/root
3. Mobu — Control Rig 클린업 부족 (1차 해결 구간)
4. Export — 잘못된 본/plot range
5. Unity — Anim Compression / Error tolerance (downstream)
```

**FBX 애니메이션 정설:** 3번까지 Mobu에서 해결하는 것이 맞다.  
5번은 import 설정 이슈 — [unity-import.md](../unity-import.md).  
ML·스크립트 보조 옵션 — [ai-motion-cleanup.md](../ai-motion-cleanup.md).

---

## 11. 자주 하는 실수

| 실수 | 결과 |
|------|------|
| 소스만 characterize | Retarget 연결 불가 또는 불안정 |
| Reference pose 무시 | 어깨·팔 1프레임부터 틀어짐 |
| 스케일 안 맞춤 | foot slide, penetration |
| Skeleton에 직접 키 | IK/FK 꼬임, export 지옥 |
| Constant Key Reducer 과 aggressive | 접지 키 삭제 → sliding |
| 소스+리그까지 export | Unity Humanoid 매핑 혼란 |
| fps mismatch | 재생 속도·보간 이상 |

---

## 12. 학습·참고 순서 (추천)

1. Characterize (타겟·소스 각각)
2. Reference pose / mapping
3. Retarget 프리뷰 + 스케일
4. Plot to Control Rig
5. Foot/hand 클린업
6. Plot to Skeleton
7. FBX export + DCC/Unity에서 검증

튜토리얼을 봤다면 3~6이 “본인 워크플로”와 일치하는 구간이다.  
1~2, 7~8(Plot/Export 옵션)을 문서·습관으로 보강하면 **정설 파이프**에 거의 근접한다.

---

## 관련 문서

- [retargeting-cleanup.md](retargeting-cleanup.md) — 단계별 실무 절차·체크리스트
- [unity-import.md](../unity-import.md) — Unity FBX import (Foot Sliding 등)
- [ai-motion-cleanup.md](../ai-motion-cleanup.md) — AI · ML · 코딩 클린업
