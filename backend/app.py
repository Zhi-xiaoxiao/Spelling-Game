import os
import json
import random
import requests
from flask import Flask, request, jsonify, session, send_from_directory
from flask_cors import CORS

# ==========================================
# 1. Flask 应用初始化与配置
# ==========================================
# static_folder 指向同级目录的 frontend，实现本地静态文件托管
app = Flask(__name__, static_folder='../frontend', static_url_path='')
app.secret_key = os.urandom(24).hex() # 用于 Session 防作弊

# 开启 CORS 跨域支持，并允许携带 Cookie (Session)
CORS(app, supports_credentials=True)

# 基于 wangwangit/tts 的公开 API
TTS_API_URL = "https://tts.wangwangit.com/v1/audio/speech"

# 词库持久化配置
WORDS_FILE = 'words.json'
DEFAULT_WORDS = [
    "apple", "banana", "cat", "dog", "elephant", "flower", "guitar", "happiness",
    "island", "jungle", "kitchen", "lemon", "music", "night", "ocean", "python",
    "queen", "rabbit", "school", "tiger", "umbrella", "violin", "window", "yellow",
    "zebra", "computer", "keyboard", "monitor", "programming", "developer"
]

# ==========================================
# 2. 词库管理引擎 (JSON 持久化)
# ==========================================
def load_words():
    if os.path.exists(WORDS_FILE):
        try:
            with open(WORDS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return DEFAULT_WORDS[:]
    return DEFAULT_WORDS[:]

def save_words(word_list):
    """第一次录入新单词时，会自动在当前目录生成 words.json"""
    with open(WORDS_FILE, 'w', encoding='utf-8') as f:
        json.dump(word_list, f, ensure_ascii=False, indent=2)

# ==========================================
# 3. 前端静态文件路由
# ==========================================
@app.route('/')
def index():
    # 将前端 index.html 映射为根目录
    return send_from_directory(app.static_folder, 'index.html')

# ==========================================
# 4. RESTful API 路由
# ==========================================
@app.route('/api/words', methods=['GET'])
def get_words():
    """获取当前词库状态"""
    words = load_words()
    return jsonify({
        "count": len(words),
        "words": words,
        "is_custom": os.path.exists(WORDS_FILE)
    })

@app.route('/api/words', methods=['POST'])
def add_word():
    """录入新单词并触发 JSON 生成"""
    data = request.get_json()
    new_word = data.get('word', '').strip().lower()
    
    if not new_word or not new_word.isalpha():
        return jsonify({"success": False, "message": "只能包含英文字母!"}), 400
        
    words = load_words()
    if new_word in words:
        return jsonify({"success": False, "message": f"'{new_word}' 已在词库中!"}), 400
        
    words.append(new_word)
    save_words(words) 
    
    return jsonify({
        "success": True, 
        "message": f"✅ 录入成功！已保存至 words.json",
        "count": len(words)
    })

@app.route('/api/game/start', methods=['POST'])
def start_game():
    """开始新一轮游戏，将答案存入后端 Session (防作弊)"""
    words = load_words()
    if not words:
        return jsonify({"error": "词库为空"}), 400
        
    word = random.choice(words)
    session['current_answer'] = word
    
    return jsonify({
        "length": len(word),
        "total_words": len(words)
    })

@app.route('/api/game/audio', methods=['POST'])
def get_audio():
    """代理请求 TTS API，避免前端跨域和接口暴露"""
    data = request.get_json()
    mode = data.get('mode', 'word') 
    word = session.get('current_answer', '')
    
    if not word:
        return jsonify({"error": "请先开始游戏"}), 400
        
    text = word if mode == 'word' else '. '.join(list(word)) + '.'
        
    payload = {
        "input": text,
        "voice": "en-US-JennyNeural", 
        "speed": 0.8 if mode == 'spell' else 1.0,
        "pitch": "0",
        "style": "general"
    }
    
    try:
        # 调用 wangwangit/tts 接口
        response = requests.post(TTS_API_URL, json=payload, headers={"Content-Type": "application/json"}, timeout=10)
        if response.status_code == 200:
            # 将音频流直接透传给前端
            return app.response_class(response.content, mimetype='audio/mpeg')
        return jsonify({"error": "TTS 服务响应异常"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/game/check', methods=['POST'])
def check_answer():
    """校验用户提交的答案"""
    data = request.get_json()
    guess = data.get('guess', '').strip().lower()
    correct = session.get('current_answer', '').lower()
    
    if not correct:
        return jsonify({"success": False, "message": "游戏未开始"}), 400
        
    if guess == correct:
        # 答对后清除 Session，防止重复提交
        session.pop('current_answer', None)
        return jsonify({"success": True, "message": "🎉 太棒了，完全正确!"})
    else:
        return jsonify({"success": False, "message": f"❌ 拼写错误! 正确答案是: {correct}"})

if __name__ == '__main__':
    print("🚀 后端 API 服务已启动: http://127.0.0.1:5000")
    print("💡 请在浏览器访问上述地址体验拼拼乐！")
    app.run(debug=True, port=5000)