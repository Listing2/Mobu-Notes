# live — Real-time & Broadcast

**실시간** mocap stream, Unity sync, 방송 전 checklist.

FBX retarget·Control Rig cleanup은 **[post/](../post/)** — 여기서 다루지 않습니다.

---

## Docs

| Path | What |
|------|------|
| [pipeline/overview.md](pipeline/overview.md) | post + live 전체 pipeline |
| [motionbuilder/](motionbuilder/) | Mobu **stream** fps · plugins |
| [unity/](unity/) | Unity **live** sync · ports |
| [troubleshooting/](troubleshooting/) | jitter 등 |
| [checklists/](checklists/) | 방송 전 점검 |

---

## Quick links

- [Framerate policy](motionbuilder/framerate-policy.md)
- [Unity sync](unity/sync.md)
- [Jitter check](troubleshooting/jitter.md)
- [Pre-broadcast checklist](checklists/pre-broadcast-mocap.md)

---

## post vs live

| live | post |
|------|------|
| Mobu → Unity **real-time** | recorded **FBX** retarget |
| fps · jitter · ports | Control Rig · Layer · export |
| broadcast checklist | [Unity FBX import](../post/unity-import.md) |
