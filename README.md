# Spelling-Game
一个基于 **Python + HTML 前后端分离架构** 的英语单词听音拼写小游戏。

项目使用 **Flask** 提供后端 API，使用原生 **HTML / CSS / JavaScript** 构建前端页面，并基于 [tts](https://github.com/wangwangit/tts) 项目生成英语语音。

用户可以听单词发音、听字母拼读，然后输入单词进行拼写测试。项目还支持手动录入新单词，首次录入后会自动生成 `words.json` 词库文件。

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/Flask-3.0+-green.svg" alt="Flask Version">
 <img src="https://img.shields.io/badge/TTS-Microsoft%20Edge-orange.svg" alt="TTS Provider">
 <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License">
</p>



## 功能特性

- 听单词发音
- 听字母逐个拼读
- 输入单词进行拼写测试
- 答案由后端保存，防止前端作弊
- 支持手动录入新单词
- 首次录入后自动生成 `words.json`
- 支持查看当前词库
- 前后端分离架构，便于二次开发
- 页面简洁美观，支持移动端访问

---

## 项目结构

```text
spelling-game/
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   └── words.json
└── frontend/
    └── index.html
```

说明：

- `backend/app.py`：后端服务，提供词库管理、游戏逻辑、语音代理等 API。
- `backend/requirements.txt`：Python 依赖。
- `backend/words.json`：词库文件，首次录入单词后自动生成。
- `frontend/index.html`：前端页面。

---

## 快速开始

### 1. 进入后端目录

```bash
cd backend
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

`requirements.txt` 内容：

```text
Flask
Flask-Cors
requests
```

### 3. 启动后端服务

```bash
python app.py
```

启动成功后访问：

```text
http://127.0.0.1:5000
```

> 注意：请不要直接双击打开 `frontend/index.html`。  
> 本项目通过后端服务托管前端页面，请直接访问 `http://127.0.0.1:5000`。

---

## 使用说明

1. 点击「抽取新单词」开始游戏。
2. 点击「读单词」听完整单词发音。
3. 点击「拼字母」听字母逐个拼读。
4. 在输入框中输入你听到的单词。
5. 点击「提交答案」查看是否正确。
6. 在下方「词库管理」中输入新单词并回车，即可录入词库。

首次录入新单词后，后端目录会自动生成：

```text
backend/words.json
```

之后程序会优先读取该文件作为词库。

---

## API 说明

### 获取词库

```http
GET /api/words
```

返回当前词库列表和单词数量。

---

### 添加单词

```http
POST /api/words
```

请求示例：

```json
{
  "word": "apple"
}
```

成功返回：

```json
{
  "success": true,
  "message": "录入成功",
  "count": 31
}
```

---

### 开始游戏

```http
POST /api/game/start
```

后端会随机抽取一个单词，并将答案保存在 Session 中。

返回示例：

```json
{
  "length": 5,
  "total_words": 30
}
```

---

### 获取语音

```http
POST /api/game/audio
```

请求示例：

```json
{
  "mode": "word"
}
```

`mode` 支持：

- `word`：朗读完整单词
- `spell`：逐个字母拼读

返回：

```text
audio/mpeg
```

---

### 检查答案

```http
POST /api/game/check
```

请求示例：

```json
{
  "guess": "apple"
}
```

成功返回：

```json
{
  "success": true,
  "message": "回答正确"
}
```

失败返回：

```json
{
  "success": false,
  "message": "回答错误，正确答案是 apple"
}
```

---

## 自定义 TTS 服务

本项目默认使用：

```text
https://tts.wangwangit.com/v1/audio/speech
```

如果你希望自己部署 TTS 服务，可以参考：

```text
https://github.com/wangwangit/tts
```

部署完成后，修改 `backend/app.py` 中的：

```python
TTS_API_URL = "https://tts.wangwangit.com/v1/audio/speech"
```

替换为你自己的服务地址即可。

---

## 技术栈

- Python
- Flask
- Flask-Cors
- requests
- HTML
- CSS
- JavaScript
- Fetch API
- Microsoft Edge TTS

---

## License

MIT
