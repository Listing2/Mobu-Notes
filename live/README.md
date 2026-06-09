# live — 라이브 · 방송

**실시간** 모캡 송출, Unity 수신·동기화, 방송 운영 노트.

FBX 리타게팅·클린업(후처리)은 **[post/](../post/)** 와 분리.

## 문서

| 경로 | 내용 |
|------|------|
| [pipeline/overview.md](pipeline/overview.md) | 전체 파이프라인 (live + post 구분) |
| [motionbuilder/](motionbuilder/) | Mobu **송출** fps, 플러그인 |
| [unity/](unity/) | Unity **라이브** sync, 포트 |
| [troubleshooting/](troubleshooting/) | 지터 등 |
| [checklists/](checklists/) | 방송 전 점검 |

## 빠른 링크

- [프레임레이트 정책](motionbuilder/framerate-policy.md)
- [Unity sync](unity/sync.md)
- [지터](troubleshooting/jitter.md)
- [방송 전 체크리스트](checklists/pre-broadcast-mocap.md)

## post와의 관계

| live | post |
|------|------|
| Mobu → Unity **실시간** 스트림 | 녹화 **FBX** merge·retarget |
| fps·지터·포트 | Control Rig·plot·export |
| 방송 체크리스트 | Unity FBX import — [post/unity-import.md](../post/unity-import.md) |
