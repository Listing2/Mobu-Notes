# live — Real-time & Broadcast

**Real-time** mocap stream, Unity sync, and pre-broadcast checklists.

For FBX retarget / Control Rig cleanup, use **[post/](../post/)**.

---

## Docs

| Path | What |
|------|------|
| [pipeline/overview.md](pipeline/overview.md) | post + live overview |
| [motionbuilder/](motionbuilder/) | Mobu **stream** fps · plugins |
| [unity/](unity/) | Unity **live** sync · ports |
| [troubleshooting/](troubleshooting/) | jitter and live issues |
| [checklists/](checklists/) | pre-broadcast checks |

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
