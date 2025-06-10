#!/usr/bin/env python3
"""
Web UI デモ - Flask版
既存のビジネスロジックをそのまま活用
"""
import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from flask import Flask, render_template_string, request, jsonify
from src.application.services import MountainArticleService
from src.infrastructure.repositories import RepositoryFactory

app = Flask(__name__)

# 既存のサービスを再利用
mountain_service = MountainArticleService()
mountain_repo = RepositoryFactory.get_mountain_repository()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🏔️ Low Mountain Blog Generator</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }
        .card { border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); }
        .btn-primary { background: linear-gradient(45deg, #667eea, #764ba2); border: none; }
        #loading { display: none; }
    </style>
</head>
<body>
    <div class="container my-5">
        <div class="row justify-content-center">
            <div class="col-lg-10">
                <div class="card">
                    <div class="card-header text-center bg-primary text-white">
                        <h1>🏔️ Low Mountain Blog Generator</h1>
                        <p class="mb-0">AIで日本の低山記事を自動生成</p>
                    </div>
                    <div class="card-body">
                        
                        <!-- 山選択セクション -->
                        <div class="row">
                            <div class="col-md-4">
                                <h5>🗻 山の選択</h5>
                                <select id="mountainSelect" class="form-select mb-3">
                                    <option value="">山を選択してください</option>
                                    {% for mountain in mountains %}
                                    <option value="{{ mountain.id }}" 
                                            data-name="{{ mountain.name }}"
                                            data-elevation="{{ mountain.elevation }}"
                                            data-difficulty="{{ mountain.difficulty.level.value }}">
                                        {{ mountain.name }} ({{ mountain.elevation }}m)
                                    </option>
                                    {% endfor %}
                                </select>
                                
                                <div id="mountainInfo" class="alert alert-info" style="display: none;">
                                    <h6 id="infoTitle"></h6>
                                    <p id="infoDetails"></p>
                                </div>
                            </div>
                            
                            <!-- 設定セクション -->
                            <div class="col-md-4">
                                <h5>⚙️ 記事設定</h5>
                                
                                <label class="form-label">テーマ:</label>
                                <select id="theme" class="form-select mb-3">
                                    <option value="">自動選択</option>
                                    <option value="初心者向け登山ガイド">初心者向けガイド</option>
                                    <option value="家族でハイキング">家族ハイキング</option>
                                    <option value="秋の紅葉狩り">秋の紅葉狩り</option>
                                    <option value="絶景ハイキング">絶景ハイキング</option>
                                </select>
                                
                                <label class="form-label">目標文字数:</label>
                                <select id="length" class="form-select mb-3">
                                    <option value="1500">1,500文字 (短文)</option>
                                    <option value="2000" selected>2,000文字 (標準)</option>
                                    <option value="3000">3,000文字 (長文)</option>
                                </select>
                                
                                <div class="form-check">
                                    <input class="form-check-input" type="checkbox" id="publishWP">
                                    <label class="form-check-label" for="publishWP">
                                        WordPressに自動投稿
                                    </label>
                                </div>
                            </div>
                            
                            <!-- 生成ボタン・進捗 -->
                            <div class="col-md-4">
                                <h5>🚀 記事生成</h5>
                                <button id="generateBtn" class="btn btn-primary btn-lg w-100 mb-3" onclick="generateArticle()">
                                    記事を生成する
                                </button>
                                
                                <div id="loading" class="text-center">
                                    <div class="spinner-border text-primary" role="status">
                                        <span class="visually-hidden">生成中...</span>
                                    </div>
                                    <p class="mt-2">記事を生成中です...<br><small>通常20-30秒かかります</small></p>
                                </div>
                                
                                <div id="progress" class="progress mb-3" style="display: none;">
                                    <div class="progress-bar progress-bar-striped progress-bar-animated" 
                                         role="progressbar" style="width: 0%"></div>
                                </div>
                            </div>
                        </div>
                        
                        <!-- 結果表示セクション -->
                        <div id="result" class="mt-4" style="display: none;">
                            <hr>
                            <h5>📰 生成結果</h5>
                            <div class="row">
                                <div class="col-md-8">
                                    <div class="card">
                                        <div class="card-body">
                                            <h6 id="articleTitle" class="card-title"></h6>
                                            <div id="articleStats" class="small text-muted mb-2"></div>
                                            <div id="articlePreview" class="card-text"></div>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <button class="btn btn-outline-primary btn-sm w-100 mb-2" onclick="copyArticle()">
                                        📋 記事をコピー
                                    </button>
                                    <button class="btn btn-outline-success btn-sm w-100 mb-2" onclick="downloadArticle()">
                                        💾 ファイル保存
                                    </button>
                                    <button class="btn btn-success btn-sm w-100" onclick="publishToWP()">
                                        🌐 WordPressに投稿
                                    </button>
                                </div>
                            </div>
                        </div>
                        
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        let generatedArticle = null;
        
        // 山選択時の情報表示
        document.getElementById('mountainSelect').addEventListener('change', function() {
            const option = this.selectedOptions[0];
            const infoDiv = document.getElementById('mountainInfo');
            
            if (option.value) {
                document.getElementById('infoTitle').textContent = option.dataset.name;
                document.getElementById('infoDetails').textContent = 
                    `標高: ${option.dataset.elevation}m | 難易度: ${option.dataset.difficulty}`;
                infoDiv.style.display = 'block';
            } else {
                infoDiv.style.display = 'none';
            }
        });
        
        // 記事生成
        async function generateArticle() {
            const mountainId = document.getElementById('mountainSelect').value;
            if (!mountainId) {
                alert('山を選択してください');
                return;
            }
            
            const generateBtn = document.getElementById('generateBtn');
            const loading = document.getElementById('loading');
            const progress = document.getElementById('progress');
            
            // UI更新
            generateBtn.disabled = true;
            loading.style.display = 'block';
            progress.style.display = 'block';
            
            // 進捗バーアニメーション
            let progressValue = 0;
            const progressInterval = setInterval(() => {
                progressValue += Math.random() * 10;
                if (progressValue > 90) progressValue = 90;
                document.querySelector('.progress-bar').style.width = progressValue + '%';
            }, 1000);
            
            try {
                const response = await fetch('/api/generate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        mountain_id: mountainId,
                        theme: document.getElementById('theme').value,
                        publish: document.getElementById('publishWP').checked
                    })
                });
                
                const result = await response.json();
                
                if (result.success) {
                    showResult(result);
                } else {
                    alert('エラー: ' + result.error);
                }
                
            } catch (error) {
                alert('生成に失敗しました: ' + error.message);
            } finally {
                clearInterval(progressInterval);
                generateBtn.disabled = false;
                loading.style.display = 'none';
                progress.style.display = 'none';
                document.querySelector('.progress-bar').style.width = '100%';
                setTimeout(() => {
                    progress.style.display = 'none';
                }, 1000);
            }
        }
        
        // 結果表示
        function showResult(result) {
            generatedArticle = result.article;
            
            document.getElementById('articleTitle').textContent = result.article.content.title;
            document.getElementById('articleStats').textContent = 
                `文字数: ${result.article.content.get_word_count()}文字 | 生成時間: ${result.generation_time}秒`;
            document.getElementById('articlePreview').innerHTML = 
                result.article.content.excerpt + '<br><br><small class="text-muted">記事の一部を表示</small>';
            
            document.getElementById('result').style.display = 'block';
        }
        
        // 記事操作
        function copyArticle() {
            if (generatedArticle) {
                navigator.clipboard.writeText(generatedArticle.content.content);
                alert('記事をクリップボードにコピーしました');
            }
        }
        
        function downloadArticle() {
            if (generatedArticle) {
                const content = `${generatedArticle.content.title}\n\n${generatedArticle.content.content}`;
                const blob = new Blob([content], { type: 'text/plain' });
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `${generatedArticle.mountain.name}_記事.txt`;
                a.click();
                URL.revokeObjectURL(url);
            }
        }
        
        function publishToWP() {
            if (generatedArticle && !generatedArticle.wordpress_id) {
                // WordPress投稿処理
                alert('WordPress投稿機能は開発中です');
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """メインページ"""
    mountains = mountain_repo.get_all()
    return render_template_string(HTML_TEMPLATE, mountains=mountains)

@app.route('/api/generate', methods=['POST'])
def generate_article_api():
    """記事生成API"""
    try:
        data = request.json
        
        result = mountain_service.create_and_publish_article(
            mountain_id=data['mountain_id'],
            theme=data.get('theme'),
            publish=data.get('publish', False)
        )
        
        if result.success:
            return jsonify({
                'success': True,
                'article': {
                    'content': {
                        'title': result.article.content.title,
                        'content': result.article.content.content,
                        'excerpt': result.article.content.excerpt,
                        'get_word_count': result.article.content.get_word_count()
                    },
                    'mountain': {
                        'name': result.article.mountain.name
                    },
                    'wordpress_id': result.article.wordpress_id
                },
                'generation_time': f"{result.generation_time:.2f}"
            })
        else:
            return jsonify({
                'success': False,
                'error': result.error_message
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    print("🌐 Web UI Demo starting at http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)