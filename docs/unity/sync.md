# Unity 동기화 (Mobu 라이브 수신)

Unity 런타임 기준 메모. 프로젝트별 수신 컴포넌트·설정은 각 Unity 프로젝트 저장소 참고.

## 핵심 개념

- 수신 측은 snapshot 보간으로 부드럽게 표시
- 송신 측(`isSender`)은 보간을 우회하고 로컬 데이터를 직접 적용
- VMC 손가락만 active여도 Humanoid 전체가 sender로 취급될 수 있음 → 보간 우회·지터 후보

## 60fps 입력 시 컨피그 1차 조정

| 항목 | 120 기준 참고 | 60 기준 테스트 |
|------|---------------|----------------|
| `MOTION_SYNC_INTERVAL` | ~0.0083 | ~0.016–0.017 |
| snapshot delay | 0.10–0.14 | 0.14–0.20 |

컨피그만으로 부족한 경우: 원본 timestamp 불안정, 동일 포즈 반복, 멀티 PC 시계 차이 등 → 코드 측 adaptive delay 검토.

## 관련 이슈 로그

- [jitter.md](../troubleshooting/jitter.md)
