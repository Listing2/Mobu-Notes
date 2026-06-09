# Mobu-Notes

모션캡처 스튜디오 **Mobu → Unity → 방송** 파이프라인 정리 저장소.

## 두 가지 업무

| 폴더 | 언제 | 내용 |
|------|------|------|
| **[post/](post/)** | 녹화 FBX **후처리** | 리타게팅·Control Rig 클린업·Skeleton bake·export |
| **[live/](live/)** | **라이브 송출·방송** | Mobu 송출 fps, Unity sync, 지터, 방송 체크리스트 |
| **[shared/](shared/)** | 공통 | 이슈·세션 기록 템플릿 |

```text
[post]  모캡 FBX → Mobu 리타겟·클린업 → FBX → Unity (타임라인·시네마)
[live]  모캡 → Mobu 송출 → Unity 실시간 → OBS / 방송
```

## 빠른 링크

### post — 후처리

- [리타게팅 개념](post/workflows/retargeting-fundamentals.md)
- [클린업 실무 절차](post/workflows/retargeting-cleanup.md)
- [Mobu 설치 경로 · Scripts](post/installation.md)
- [외부 Python 도구](post/external-tools.md)
- [AI · 코딩 클린업](post/ai-motion-cleanup.md)

### live — 라이브·방송

- [파이프라인 개요](live/pipeline/overview.md)
- [프레임레이트 정책](live/motionbuilder/framerate-policy.md)
- [지터 1차 점검](live/troubleshooting/jitter.md)
- [방송 전 체크리스트](live/checklists/pre-broadcast-mocap.md)

## 작성 규칙

- 문서·주석·커밋 메시지는 **한국어** 우선
- 파일명·코드 식별자는 **ASCII** 유지
- 민감 정보는 `live/private/`에 두거나 placeholder로 마스킹
- 재현 가능한 항목은 **환경(Mobu 버전, Unity 버전, 인원 수, fps)** 기록

## 관련

- [Listing2 / Repositories](https://github.com/Listing2?tab=repositories)

## 라이선스

MIT — [LICENSE](LICENSE).
