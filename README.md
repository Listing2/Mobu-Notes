# Mobu-Notes

MotionBuilder 및 모션캡처 파이프라인 정리 저장소.

MolistBase6 / Lilnity 스튜디오에서 쓰는 **Mobu → Unity → 방송** 흐름의 설정, 트러블슈팅, 운영 노트를 모읍니다.

## 목적

- MotionBuilder 송출/수신 설정을 한곳에 기록
- 프레임레이트, 지터, 포트, VMC 등 반복 이슈의 **원인·검증·해결**을 축적
- 신규 합류자·미래의 나를 위한 체크리스트 제공

## 문서 구조

| 경로 | 내용 |
|------|------|
| [docs/pipeline/overview.md](docs/pipeline/overview.md) | 전체 파이프라인 개요 |
| [docs/motionbuilder/](docs/motionbuilder/) | Mobu 쪽 설정·플러그인·송출 |
| [docs/unity/](docs/unity/) | Unity 수신·동기화·네트워크 |
| [docs/troubleshooting/](docs/troubleshooting/) | 증상별 트러블슈팅 |
| [docs/checklists/](docs/checklists/) | 방송 전·장애 시 점검표 |
| [docs/templates/](docs/templates/) | 이슈/세션 기록 템플릿 |

## 빠른 링크 (작성 예정)

- [지터 발생 시 1차 점검](docs/troubleshooting/jitter.md)
- [프레임레이트 정책 (60 / 120 / 240)](docs/motionbuilder/framerate-policy.md)
- [방송 전 모캡 체크리스트](docs/checklists/pre-broadcast-mocap.md)

## 작성 규칙

- 문서·주석·커밋 메시지는 **한국어** 우선
- 파일명·코드 식별자는 **ASCII** 유지
- 내부 IP, 포트, 계정 등 민감 정보는 `docs/private/`에 두거나 placeholder로 마스킹
- 재현 가능한 항목은 **환경(Mobu 버전, Unity 버전, 인원 수, fps)** 을 함께 기록

## 관련 프로젝트

- [Listing2 / Repositories](https://github.com/Listing2?tab=repositories)
- MolistBase6 (사내 Unity 스튜디오 — 본 저장소와 별도)

## 라이선스

MIT — 상세는 [LICENSE](LICENSE).
