from flask import Flask, render_template, request, send_file, jsonify
from music_emotion_agent import MusicEmotionAgent
import os

app = Flask(__name__)
agent = MusicEmotionAgent()

# 确保输出目录存在
UPLOAD_FOLDER = 'static/music'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_music():
    emotion = request.form.get('emotion')
    if not emotion:
        return jsonify({'error': '请选择情感类型'}), 400
    
    # 生成音乐文件名（WAV格式）
    output_file = os.path.join(UPLOAD_FOLDER, f"{emotion}_music.wav")
    
    try:
        # 生成音乐
        agent.generate_music(emotion, output_file)
        
        # 返回文件路径
        return jsonify({
            'success': True,
            'file_path': f"/static/music/{emotion}_music.wav",
            'message': f'已成功生成{emotion}情感的音乐'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 