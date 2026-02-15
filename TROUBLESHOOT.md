# AudioSlicer V-0.3 故障排除指南

## 问题清单

本指南覆盖以下常见问题及解决方案。

---

## 🔴 安装阶段问题

### 问题 1.1：Homebrew 找不到

**症状：** 运行 `brew` 时出现 `command not found: brew`

**原因：** Homebrew 未安装或未在 PATH 中

**解决方案：**

```bash
# 方法 1：安装 Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 方法 2：重新加载 shell（安装后）
exec zsh -l
which brew  # 验证
```

**检验成功的标志：** 输入 `brew --version` 能看到版本号

---

### 问题 1.2：ffmpeg 安装失败

**症状：** 运行 `brew install ffmpeg` 报错

**常见错误信息：**
- `Connection refused`
- `SSL certificate problem`
- `404 Not Found`

**解决方案：**

```bash
# 方法 1：更新 Homebrew 配置
brew update

# 方法 2：清除缓存后重试
brew cleanup
brew install ffmpeg

# 方法 3：用 arm64 特定版本（Apple Silicon Mac）
brew install ffmpeg --with-options=...
```

**验证安装：**
```bash
which ffmpeg
ffmpeg -version
```

**如果仍然失败：** 可能是网络问题，稍后重试或检查 Wi-Fi 连接。

---

### 问题 1.3：pydub 安装失败

**症状：** 运行 `pip3 install pydub` 出错

**常见错误：**
- `Connection error`
- `Permission denied`

**解决方案：**

```bash
# 方法 1：安装到用户目录（推荐）
pip3 install --user pydub

# 方法 2：升级 pip 后重试
pip3 install --upgrade pip
pip3 install pydub

# 方法 3：用清华源加速（中国用户）
pip3 install -i https://pypi.tsinghua.edu.cn/simple pydub
```

**验证安装：**
```bash
python3 -c "import pydub; print('pydub installed successfully')"
```

---

## 🟡 运行阶段问题

### 问题 2.1：GUI 无法启动（macOS 版本错误）

**症状：** 运行 `python3 AudioSlicer.py` 后窗口未出现，终端显示：
```
macOS 26 (2602) or later required, have instead 16 (1602) !
```

**原因：** Tkinter（Python GUI 库）要求更新的 macOS

**解决方案：**

```bash
# 方法 1：使用无 GUI 模式（测试功能）
python3 headless_test.py
python3 test_complete.py

# 方法 2：升级 macOS（系统设置 > 软件更新）
# macOS Big Sur (11) 及更新版本支持

# 方法 3：安装更新的 Python 版本
brew install python@3.11  # 或更新版本
/opt/homebrew/bin/python3.11 AudioSlicer.py
```

**临时解决方案：** 使用 `headless_test.py` 作为模板编写自动化脚本处理音频。

---

### 问题 2.2：ffmpeg not found（运行时错误）

**症状：** 启动 GUI 时弹出警告："ffmpeg not found in PATH"

**原因：** ffmpeg 已安装但路径不被识别

**解决方案：**

```bash
# 方法 1：检查 ffmpeg 位置
which ffmpeg
which avconv

# 方法 2：验证路径
python3 - <<'EOF'
from pydub import utils
print("ffmpeg:", utils.which('ffmpeg') or 'not found')
print("avconv:", utils.which('avconv') or 'not found')
EOF

# 方法 3：重新安装 ffmpeg（带完整选项）
brew uninstall ffmpeg
brew install ffmpeg --with-libopus  # 或其他需要的编解码器
```

**若仍未解决：** 手动检查 PATH：
```bash
echo $PATH
# 应该包含 /opt/homebrew/bin（M1/M2 Mac）或 /usr/local/bin（Intel Mac）
```

---

### 问题 2.3："No module named 'pydub'"

**症状：** 终端显示 `ModuleNotFoundError: No module named 'pydub'`

**原因：** pydub 未安装或安装在错误的 Python 版本

**解决方案：**

```bash
# 方法 1：确保用同一个 Python 版本
which python3
pip3 install pydub  # 要用 pip3 对应的 python3

# 方法 2：显式安装到当前 Python
python3 -m pip install pydub

# 方法 3：验证安装位置
python3 -m pip show pydub
# 检查 Location 是否在你的 Python 目录中
```

---

## 🔵 功能问题

### 问题 3.1：无法检测静音（没有分割点）

**症状：** 运行分割后，程序说"No silence detected"，或只生成 1 个文件

**原因：**
1. 音频连贯无停顿（如纯背景音乐）
2. 静音时长设置过高
3. 静音阈值不适配音频质量

**解决方案：**

```
方法 1：降低静音时长设置
  → 从 1000 ms 改为 500 ms
  → 再改为 300 ms（最小值）
  
方法 2：检查音频本身
  → 用媒体播放器播放
  → 听是否有明显停顿
  → 如无停顿，分割可能不适合此音频
  
方法 3：修改代码中的静音阈值（高级）
  → 打开 AudioSlicer.py
  → 找到 thresh_db = -50
  → 改为 -40 或 -35（更敏感）
  → 保存并重启
```

**判断标准：** 好的分割应该在说话人明显的停顿处切割。

---

### 问题 3.2：分割过度（生成太多文件）

**症状：** 生成的文件数过多（如 50+ 个），某些片段只有几秒钟

**原因：** 静音时长设置太低，检测到了过多停顿

**解决方案：**

```
方法 1：提高静音时长
  → 从 300 ms 改为 500 ms
  → 再改为 800 ms
  → 测试结果
  
方法 2：提高静音阈值（代码修改）
  → 打开 AudioSlicer.py
  → thresh_db = -50 改为 -55（更不敏感）
  → 保存重启
```

---

### 问题 3.3：分割不足（文件太大）

**症状：** 只生成 2-3 个大文件，没有在合适的位置分割

**原因：** 静音时长设置过高，漏掉了短停顿

**解决方案：**

```
方法 1：降低静音时长
  → 从 800 ms 改为 500 ms
  → 再改为 300 ms
  
方法 2：降低静音阈值（代码修改）
  → thresh_db = -50 改为 -40（更敏感）
```

---

### 问题 3.4：导出失败

**症状：** 进度条卡住，或看到错误消息："Export failed"

**常见原因：**
1. 输出文件夹无写入权限
2. 磁盘满
3. 文件名冲突

**解决方案：**

```bash
# 方法 1：检查文件夹权限
ls -ld /path/to/output/folder
# 应该看到 drwx... 开头

# 方法 2：改变文件夹权限
chmod 755 /path/to/output/folder

# 方法 3：选择不同的输出文件夹
# GUI 中重新选择一个新的文件夹

# 方法 4：检查磁盘空间
df -h
# 检查 /Volumes 中是否有足够空间
```

---

### 问题 3.5：导出特别慢

**症状：** 即使是小文件也花费很长时间（> 5 分钟）

**原因：** 
1. 文件太大
2. ffmpeg 编码设置默认参数高
3. 系统资源占用

**解决方案：**

```bash
# 方法 1：等待（完全正常）
# 大文件处理需要时间，可以接受 5-15 分钟

# 方法 2：检查系统资源
# 按 Command + Space，输入 Activity Monitor
# 检查 CPU 和内存是否被其他程序占用

# 方法 3：关闭其他应用
# 关闭浏览器、邮件等，释放 CPU
```

---

## 🟢 验证测试

### 如何知道一切正常？

运行完整测试：

```bash
python3 test_complete.py
```

**预期结果：**
```
============================================================
TEST SUMMARY
============================================================
  ✓ PASS: ffmpeg availability
  ✓ PASS: pydub import
  ✓ PASS: audio generation
  ✓ PASS: silence detection
  ✓ PASS: audio slicing
  ✓ PASS: audio export
  ✓ PASS: AudioSlicer.py syntax

Total: 7/7 passed

🎉 ALL TESTS PASSED!
```

**如果任何一项失败：** 按照上面的对应问题查找解决方案。

---

## 🆘 终极解决方案

如果以上都不管用，尝试：

### 完整重装

```bash
# 1. 卸载并清理
pip3 uninstall pydub
brew uninstall ffmpeg

# 2. 清除缓存
brew cleanup
pip3 cache purge

# 3. 重新安装
brew install ffmpeg
pip3 install pydub

# 4. 验证
python3 test_complete.py
```

### 检查系统完整性（macOS）

```bash
# 运行系统检查（可能需要管理员密码）
softwareupdate -a
diskutil verifyVolume /

# 重启 Mac
sudo reboot
```

---

## 📞 获取更多帮助

1. **查看详细指南** → `GUIDE.md`
2. **快速参考** → `QUICK_START.md`
3. **查看 README** → `README.md`
4. **运行诊断** → `python3 test_complete.py`

---

**记住：** 大多数问题都是安装或路径问题，系统重启往往能解决很多神秘的错误！🔄
