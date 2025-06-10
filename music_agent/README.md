# 情感音乐生成器

这是一个基于情感生成音乐的 Python 程序。它可以根据指定的情感类型生成相应的音乐旋律。

## 功能特点

- 支持多种情感类型：
  - 快乐 (happy)
  - 悲伤 (sad)
  - 兴奋 (excited)
  - 平静 (calm)
- 自动生成符合情感特征的旋律
- 输出标准 MIDI 文件格式

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

```python
from music_emotion_agent import MusicEmotionAgent

# 创建 agent 实例
agent = MusicEmotionAgent()

# 生成快乐的音乐
agent.generate_music("happy", "happy_music.mid")

# 生成悲伤的音乐
agent.generate_music("sad", "sad_music.mid")

# 生成兴奋的音乐
agent.generate_music("excited", "excited_music.mid")

# 生成平静的音乐
agent.generate_music("calm", "calm_music.mid")
```

## 技术说明

该程序使用以下参数来定义不同情感的音乐特征：

- 音阶（Scale）：决定可用音符的范围和调式
- 速度（Tempo）：控制音乐的快慢
- 力度（Dynamics）：控制音量的大小
- 节奏模式（Rhythm Patterns）：定义音符的时值组合
- 八度范围（Octave Range）：确定音高范围

## 依赖库

- music21：用于音乐理论和 MIDI 文件处理
- numpy：用于数学计算
- python-sonic：用于音频处理
- pygame：用于音频播放
- python-dotenv：用于环境变量管理 