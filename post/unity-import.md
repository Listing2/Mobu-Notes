# Unity — FBX 애니메이션 Import

Mobu에서 plot·export한 FBX를 Unity에 넣을 때의 설정.  
**발 sliding 등 모션 품질 1차 해결은 Mobu Control Rig**에서 하는 것이 정석이다.  
Unity 쪽은 import·압축·Humanoid 매핑 이슈를 다룬다.

Mobu 작업 절차: [workflows/retargeting-cleanup.md](workflows/retargeting-cleanup.md)

---

## Foot Sliding (import 후)

Mobu에서 정리했는데 Unity에서 **발이 미끄러지는** 경우.

### 원인 구분

| 계층 | 확인 |
|------|------|
| Mobu | 스케일·Control Rig foot IK·plot reducer — [fundamentals §10](workflows/retargeting-fundamentals.md#10-foot-sliding--원인-계층) |
| Unity | Anim compression / error tolerance로 **키가 줄거나 보간이 달라짐** |

### FBX Import — Animation 탭

| 옵션 | 권장 | 설명 |
|------|------|------|
| **Position Error** | `0.03` | 허용 오차 초과 position 키 제거 |
| **Rotation Error** | `0.03` | rotation 키 제거 |
| **Scale Error** | `0.03` | scale 키 제거 |
| **Anim. Compression** | **Off** (또는 Keyframe Reduction 최소) | 접지 프레임 키 보존 |

Error 값을 키우면 파일은 작아지지만 **발 접지 키**가 merge·삭제되어 sliding처럼 보일 수 있다.

### 권장 순서

1. **Compression Off** 또는 Error `0.03`으로 import
2. Scene에서 재생해 sliding 여부 확인
3. 여전히 sliding → **Mobu 쪽** foot IK·plot 재검토 (Unity만으로 해결 안 됨)
4. Mobu OK인데만 Error·Compression을 조금씩 조정해 용량 최적화

---

## Humanoid vs Generic

| Rig | 용도 |
|-----|------|
| **Humanoid** | 리타겟·Avatar Mask·다른 Humanoid 클립 재사용 |
| **Generic** | 비인형·커스텀 본 — Mapping 직접 관리 |

VRM·게임 캐릭터는 보통 Humanoid. Import 후 **Configure**에서 bone mapping 한 번 확인.

---

## Root Motion

- Mobu에서 **Plot Translation on Root** 로 bake했으면 Unity clip에 root motion 포함.
- Animator **Apply Root Motion** / Timeline offset 정책을 프로젝트에 맞게 통일.

---

## 기록할 항목 (Mobu 설정과 세트)

| 항목 | 값 |
|------|-----|
| Mobu export fps | |
| Match Source / scale | |
| Plot Translation on Root | |
| Unity Position/Rotation/Scale Error | |
| Anim. Compression | |

재현·디버깅 시 Mobu export 설정과 Unity import 설정을 **한 세트**로 남긴다.
