import numpy as np
from music21 import *
import random
import os
from typing import Dict, List, Tuple
import tempfile

class MusicEmotionAgent:
    def __init__(self):
        # 定义不同情感对应的音乐参数
        self.emotion_params = {
            "happy": {
                "notes": ["C4", "D4", "E4", "F4", "G4", "A4", "B4", "C5", "D5", "E5"],
                "tempo": 120,
                "rhythm_patterns": [1.0, 0.5, 0.5, 1.0],
            },
            "sad": {
                "notes": ["A3", "B3", "C4", "D4", "E4", "F4", "G4", "A4", "B4", "C5"],
                "tempo": 75,
                "rhythm_patterns": [2.0, 1.0, 1.0, 2.0],
            },
            "excited": {
                "notes": ["G4", "A4", "B4", "C5", "D5", "E5", "F#5", "G5", "A5", "B5"],
                "tempo": 140,
                "rhythm_patterns": [0.25, 0.25, 0.5, 0.25, 0.25, 0.5],
            },
            "calm": {
                "notes": ["F4", "G4", "A4", "Bb4", "C5", "D5", "E5", "F5"],
                "tempo": 85,
                "rhythm_patterns": [2.0, 1.0, 1.0, 2.0],
            }
        }

    def note_to_frequency(self, note_name):
        """将音符名称转换为频率"""
        # 音符到半音数的映射（相对于C4）
        note_map = {
            'C': 0, 'C#': 1, 'Db': 1, 'D': 2, 'D#': 3, 'Eb': 3,
            'E': 4, 'F': 5, 'F#': 6, 'Gb': 6, 'G': 7, 'G#': 8,
            'Ab': 8, 'A': 9, 'A#': 10, 'Bb': 10, 'B': 11
        }
        
        # 解析音符名称
        if len(note_name) == 2:
            note, octave = note_name[0], int(note_name[1])
        elif len(note_name) == 3:
            note, octave = note_name[:2], int(note_name[2])
        else:
            return 440.0  # 默认A4
        
        # 计算频率
        semitones = note_map.get(note, 9) + (octave - 4) * 12
        frequency = 440.0 * (2 ** (semitones / 12.0))
        return frequency

    def generate_tone(self, frequency, duration, sample_rate=44100):
        """生成指定频率和时长的音调"""
        frames = int(duration * sample_rate)
        arr = np.zeros(frames)
        
        for i in range(frames):
            # 生成正弦波
            arr[i] = np.sin(2 * np.pi * frequency * i / sample_rate)
            # 添加包络以避免爆音
            if i < frames * 0.1:  # 淡入
                arr[i] *= i / (frames * 0.1)
            elif i > frames * 0.9:  # 淡出
                arr[i] *= (frames - i) / (frames * 0.1)
        
        return arr

    def generate_melody(self, emotion: str, length: int = 16) -> np.ndarray:
        """
        根据指定的情感生成旋律音频数据
        """
        if emotion not in self.emotion_params:
            raise ValueError(f"不支持的情感类型: {emotion}")
            
        params = self.emotion_params[emotion]
        sample_rate = 44100
        
        # 计算每个四分音符的时长（秒）
        quarter_note_duration = 60.0 / params["tempo"]
        
        audio_data = np.array([])
        
        # 生成音符
        for i in range(length):
            # 随机选择音符
            note_name = random.choice(params["notes"])
            
            # 随机选择时值
            duration_beats = random.choice(params["rhythm_patterns"])
            duration_seconds = duration_beats * quarter_note_duration
            
            # 生成音调
            frequency = self.note_to_frequency(note_name)
            tone = self.generate_tone(frequency, duration_seconds, sample_rate)
            
            # 添加到音频数据
            audio_data = np.concatenate([audio_data, tone])
            
            # 添加短暂的间隔
            silence = np.zeros(int(0.05 * sample_rate))
            audio_data = np.concatenate([audio_data, silence])
        
        return audio_data

    def save_wav(self, audio_data, filename: str, sample_rate=44100):
        """
        将音频数据保存为 WAV 文件
        """
        try:
            # 确保目录存在
            dir_path = os.path.dirname(filename)
            if dir_path:
                os.makedirs(dir_path, exist_ok=True)
            
            # 归一化音频数据
            audio_data = audio_data / np.max(np.abs(audio_data))
            
            # 转换为16位整数
            audio_data = (audio_data * 32767).astype(np.int16)
            
            # 使用 music21 保存 WAV 文件
            import wave
            with wave.open(filename, 'w') as wav_file:
                wav_file.setnchannels(1)  # 单声道
                wav_file.setsampwidth(2)  # 16位
                wav_file.setframerate(sample_rate)
                wav_file.writeframes(audio_data.tobytes())
            
            print(f"WAV 文件已保存到: {filename}")
        except Exception as e:
            print(f"保存 WAV 文件时出错: {str(e)}")
            raise

    def generate_music(self, emotion: str, output_file: str):
        """
        生成音乐并保存为 WAV 文件
        """
        try:
            print(f"开始生成 {emotion} 情感的音乐...")
            audio_data = self.generate_melody(emotion)
            
            # 确保输出文件是 .wav 格式
            if not output_file.endswith('.wav'):
                output_file = output_file.rsplit('.', 1)[0] + '.wav'
            
            self.save_wav(audio_data, output_file)
            print(f"已生成 {emotion} 情感的音乐，保存为 {output_file}")
        except Exception as e:
            print(f"生成音乐时出错: {str(e)}")
            raise

if __name__ == "__main__":
    # 使用示例
    agent = MusicEmotionAgent()
    agent.generate_music("happy", "happy_music.wav") 