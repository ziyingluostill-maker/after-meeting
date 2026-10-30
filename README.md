# after-meeting

Cursor Agent Skill：会议录音 → 行动导向会议纪要（事项 / 负责人 / DDL / 计划）。

## 安装

复制到个人 skills 目录：

```bash
cp -R after-meeting ~/.cursor/skills/after-meeting
```

或在本机 clone 后软链：

```bash
git clone <repo-url> ~/.cursor/skills/after-meeting
```

## 用法

在 Cursor 对话中发送会议录音（m4a/mp3/wav/aac），并说明「出纪要」即可。Agent 会读取本 skill，转写音频并生成 Excel（行动项 / 计划与里程碑 / 结论与待拍板）。

## 依赖

- macOS `afconvert`（系统自带）
- Python 3 + `openai-whisper`、`numpy`、`openpyxl`
