# 파이프라인 개요

## 기본 흐름

```text
모션캡처 프로그램에서 녹화한 원본
    ↓
MotionBuilder (리타겟·정리·송출)
    ↓
Unity (라이브 sync / VMC / OSC)
    ↓
방송 카메라·캐릭터·UI
    ↓
OBS / 캡처보드 / Spout·NDI
```

## 역할 분리

| 구간 | 담당 | 기록 위치 |
|------|------|-----------|
| 원본 캡처 fps | 모캡 PC / 볼륨 | [framerate-policy.md](../motionbuilder/framerate-policy.md) |
| Mobu 송출 fps | MotionBuilder | [motionbuilder/](..) |
| Unity 수신·보간 | Unity PC / 수신 앱 | [unity/sync.md](../unity/sync.md) |
| 네트워크 포트 | 아바타별 OSC/VMC | [unity/ports.md](../unity/ports.md) |

## 원칙

1. **원본 캡처 fps가 실제 정보량의 상한**이다. Mobu/Unity에서 120으로 올려도 원본이 60이면 중간 프레임은 보간·복제일 수 있다.
2. 지터는 코드·입력·네트워크 중 하나만 보지 말고 **동일 씬·동일 빌드**에서 입력 fps부터 분리 검증한다.
3. 설정 변경은 “무엇을 바꿨는지 + 기대 결과 + 실제 결과” 세트로 남긴다.

## TODO

- [ ] 스튜디오 실제 장비 목록 (PC 역할, NIC, 캡처보드)
- [ ] MotionBuilder 버전 및 사용 플러그인 목록
- [ ] 인원 수별 권장 fps 표
