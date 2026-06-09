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

## 시작하기

| 업무 | 진입점 |
|------|--------|
| FBX 후처리 | [post/workflows/](post/workflows/) |
| 라이브·방송 | [live/](live/) |
| Mobu 설치·스크립트 | [post/installation.md](post/installation.md) |

## 작성 규칙

- 문서·주석·커밋 메시지는 **한국어** 우선
- 파일명·코드 식별자는 **ASCII** 유지
- 민감 정보는 `live/private/`에 두거나 placeholder로 마스킹
- 재현 가능한 항목은 **환경(Mobu 버전, Unity 버전, 인원 수, fps)** 기록

## 관련

- [Listing2 / Repositories](https://github.com/Listing2?tab=repositories)

## 라이선스

MIT — [LICENSE](LICENSE).
