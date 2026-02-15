# AudioSlicer V-0.3 快速参考卡

## 🚀 30 秒快速启动

### 第一次使用（5分钟安装）

```bash
# 1. 安装 ffmpeg
brew install ffmpeg

# 2. 安装 Python 3.11（解决 Tkinter 兼容性问题）
brew install python@3.11

# 3. 安装 Tkinter GUI 支持
brew install python-tk@3.11

# 4. 安装 Python 库
pip3.11 install pydub

# 5. 验证
python3.11 AudioSlicer.py
```

### 日常使用（运行应用）

```bash
cd "/Users/你的用户名/AI TEST/Audio Test"
python3.11 AudioSlicer.py
```

---

## 📖 3 步分割音频

| 步骤 | 操作 |
|------|------|
| 1️⃣ **选择文件** | 点击 "Choose Audio File"，选择 `.mp3` 或 `.m4a` |
| 2️⃣ **选择输出** | 点击 "Choose Output Dir"，选择一个空文件夹 |
| 3️⃣ **调整 & 开始** | 设置静音时长（默认 500 ms），点击 "Start Slicing" |

**结果** → 输出文件夹里会出现 `001.mp3`, `002.mp3` ...

---

## 🎚️ 静音时长如何选？

| 场景 | 建议值 |
|------|-------|
| 播客 / 讲座 | 500–800 ms |
| 有声书 | 600–900 ms |
| 音乐 | 800–1000 ms |
| 短句子多 | 300–500 ms |

**原则：** 试试 500 ms，不满意就调整。

---

## ❌ 出错了？

| 错误信息 | 解决方案 |
|---------|--------|
| `command not found: ffmpeg` | 运行 `brew install ffmpeg` |
| `No module named 'pydub'` | 运行 `pip3.11 install pydub` |
| `command not found: brew` | 需要先安装 Homebrew |
| Tkinter 崩溃（Python 3.9） | 运行 `brew install python@3.11`，然后用 `python3.11 AudioSlicer.py` |
| 无法检测到静音 | 音频可能没有停顿，试试降低时长设置 |

---

## 💡 小贴士

- ✅ 用小文件（< 10 MB）先测试
- ✅ 导出前检查输出文件夹是否为空
- ✅ 原文件不会被删除，放心使用
- ✅ MP3 在所有设备都能播放

---

## 📞 需要帮助？

详细指南见：`GUIDE.md`（完整说明）

---

**Happy Slicing!** 🎵
