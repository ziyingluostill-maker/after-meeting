# after-meeting

Cursor Plugin：会议录音 → 行动导向会议纪要（事项 / 负责人 / DDL / 计划）。

仓库已按 Cursor **marketplace / plugin** 结构打包，同事可从 GitHub 一键导入。

## 一键导入（Cursor）

1. 打开 Cursor → **Customize**（或 Settings 里的 Plugins / Marketplace）
2. 选择 **From GitHub Repository**
3. 填入：

```text
https://github.com/ziyingluostill-maker/after-meeting
```

4. 安装插件 `after-meeting`
5. 对话里发送会议录音，或输入 `/after-meeting`

## 手动安装（备用）

```bash
git clone https://github.com/ziyingluostill-maker/after-meeting.git ~/.cursor/skills/after-meeting
```

Cursor 会递归发现其中的 `skills/after-meeting/SKILL.md`。

## 用法

发送会议录音（m4a / mp3 / wav / aac），说明「出纪要」。Agent 会转写并生成 Excel：

- **行动项**：事项、负责人、DDL、优先级、状态
- **计划与里程碑**
- **结论与待拍板**

## 依赖

- macOS：`afconvert`（系统自带）
- Python 3：`openai-whisper`、`numpy`、`openpyxl`

```bash
pip3 install openai-whisper numpy openpyxl
```

## 仓库结构

```text
.cursor-plugin/marketplace.json          # GitHub 一键导入所需
after-meeting/
  .cursor-plugin/plugin.json
  skills/after-meeting/
    SKILL.md
    scripts/transcribe_audio.py
```
