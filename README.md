# Mobu-Notes

모션캡처 스튜디오 **MotionBuilder → Unity → 방송** 파이프라인을 정리한 지식 저장소.  
실무 절차·도구·스크립트·체크리스트를 **post(후처리)** 와 **live(라이브)** 로 나눠 둔다.

**로컬 환경:** MotionBuilder **2025** · Unity (타임라인·시네마 / 라이브 수신)

---

## 저장소 구조

```text
Mobu-Notes/
├── post/          녹화 FBX → Mobu 리타게팅·클린업 → FBX export
├── live/          Mobu 실시간 송출 → Unity → 방송·지터·체크리스트
├── shared/        이슈·세션 기록 템플릿
└── .vscode/       post/scripts venv · motionbuilder-stubs
```

| 폴더 | 언제 쓰나 | 끝 결과물 |
|------|-----------|-----------|
| **[post/](post/)** | 모캡 **녹화 FBX**를 게임/VTuber 캐릭터에 옮길 때 | 클린업된 **skeleton anim FBX** → Unity |
| **[live/](live/)** | **방송·실시간** mocap 송출할 때 | Unity 실시간 캐릭터 · OBS |
| **[shared/](shared/)** | 세션·버그 기록 | issue-log 템플릿 |

```text
[post]  모캡 FBX → Mobu Retarget → CR Layer 클린업 → Skeleton plot → FBX → Unity
[live]  모캡 → Mobu stream → Unity sync → OBS / 방송
```

---

## post — 표준 후처리 (요약)

상세 12단계: **[post/workflows/retargeting-cleanup.md#실무-순서--animation-layer-파이프-권장](post/workflows/retargeting-cleanup.md#실무-순서--animation-layer-파이프-권장)**

| 구간 | 하는 일 | 핵심 주의 |
|------|---------|-----------|
| 준비 | 모션-only FBX · 타겟 characterize · Source 연결 · 스케일 맞춤 | VRM Reference pose · **Plot 전 Hand IK 100 X** |
| 굳히기 | Plot to Control Rig · **소스 캐릭터 제거** | 전신+손가락 · Reducer Off |
| 수정 | CR **Animation Layer** + Weight · Foot IK | 포즈=레이어 · 타이밍=Weight |
| 마무리 | Plot to Skeleton · FBX export | skeleton anim만 · CR·소스 제외 |

**손목·손가락 drift** 대부분: Plot 전 Hand IK 100 · 소스 미제거 · Layer Weight 없이 pose만 키 — [layer 가이드](post/workflows/layer-override-hands-head.md)

---

## 문서 맵

### post — 읽는 순서 (처음)

1. [retargeting-fundamentals.md](post/workflows/retargeting-fundamentals.md) — Characterize, Match Source, plot, foot sliding **왜**
2. [retargeting-cleanup.md](post/workflows/retargeting-cleanup.md) — Phase 0~6 · **실무 12단계**
3. [layer-override-hands-head.md](post/workflows/layer-override-hands-head.md) — 손·목 Layer + Weight
4. [unity-import.md](post/unity-import.md) — Unity FBX import

### post — 참고·도구

| 문서 | 내용 |
|------|------|
| [post/workflows/README.md](post/workflows/README.md) | 워크플로 목록 · 학습 순서 |
| [post/installation.md](post/installation.md) | Mobu 경로 · PythonStartup/Scripts · Cursor 스텁 |
| [post/external-tools.md](post/external-tools.md) | Retargeter, OpenMoBu, awesome-mobu 큐레이션 |
| [post/scripts/vendor/README.md](post/scripts/vendor/README.md) | GitHub 스크립트 vendor · Retargeter 실행 |
| [post/ai-motion-cleanup.md](post/ai-motion-cleanup.md) | ML·실험 클린업 (본 파이프는 Mobu CR 정석) |
| [post/scripts/](post/scripts/) | Python · `vendor/retargeter/retargeter.py` (Mobu 2025 패치) |

### live

| 문서 | 내용 |
|------|------|
| [live/README.md](live/README.md) | live 진입점 |
| [pipeline/overview.md](live/pipeline/overview.md) | 전체 파이프 (post/live 구분) |
| [motionbuilder/framerate-policy.md](live/motionbuilder/framerate-policy.md) | 송출 fps |
| [unity/sync.md](live/unity/sync.md) | Unity 라이브 sync |
| [troubleshooting/jitter.md](live/troubleshooting/jitter.md) | 지터 1차 점검 |
| [checklists/pre-broadcast-mocap.md](live/checklists/pre-broadcast-mocap.md) | 방송 전 체크 |

### shared

| 문서 | 내용 |
|------|------|
| [shared/templates/issue-log.md](shared/templates/issue-log.md) | 이슈·세션 기록 |

---

## 설치된·권장 외부 도구

| 도구 | 용도 | 주의 |
|------|------|------|
| [eksod/Retargeter](https://github.com/eksod/Retargeter) | FBX 폴더 **일괄** merge·retarget | **Python Editor**에서 vendor copy 실행 — upstream `main()` 그대로 Scripts에 두면 **Mobu 시작 실패** |
| [OpenMoBu](https://github.com/Neill3d/OpenMoBu) | HIK 템플릿 · ReCreateRig · StayOnFloor 등 | **Mobu 2025** Release와 버전 일치 |
| motionbuilder-stubs | Cursor `pyfbsdk` 자동완성 | [installation.md](post/installation.md) · `post/scripts/setup-dev.ps1` |

---

## 빠른 시작

```powershell
# Cursor에서 Mobu Python 편집 (1회)
cd post/scripts
.\setup-dev.ps1
```

| 목적 | 열 문서 |
|------|---------|
| 오늘 take 클린업 | [실무 12단계](post/workflows/retargeting-cleanup.md#실무-순서--animation-layer-파이프-권장) |
| Mobu 경로·Retargeter | [installation.md](post/installation.md) |
| 방송 전 점검 | [pre-broadcast-mocap.md](live/checklists/pre-broadcast-mocap.md) |
| 버그·세션 기록 | [issue-log.md](shared/templates/issue-log.md) |

---

## 작성 규칙

- 문서·주석·커밋 메시지: **한국어** 우선
- 파일명·코드 식별자: **ASCII**
- 민감 정보: `live/private/` 또는 placeholder
- 재현 항목 기록: Mobu/Unity 버전, fps, take 출처, Match Source, plot reducer, export 옵션

---

## 관련

- [Listing2 / Repositories](https://github.com/Listing2?tab=repositories)

## 라이선스

MIT — [LICENSE](LICENSE).
