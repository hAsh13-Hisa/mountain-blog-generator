// Article Generation Functions

// Generate article
async function generateArticle() {
    if (!selectedMountain) {
        showAlert('山を選択してください', 'warning');
        return;
    }

    const generateBtn = document.getElementById('generateBtn');
    const progressContainer = document.getElementById('progressContainer');
    const progressBar = document.getElementById('progressBar');
    const progressText = document.getElementById('progressText');
    const resultContainer = document.getElementById('resultContent');
    const resultActions = document.getElementById('resultActions');

    // Prepare request data
    const requestData = {
        mountain_id: selectedMountain.id,
        theme: document.getElementById('theme').value || null,
        target_length: parseInt(document.getElementById('targetLength').value),
        publish: document.getElementById('publishToWP').checked
    };

    try {
        // UI state: Start generation
        generateBtn.disabled = true;
        generateBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> 生成中...';
        progressContainer.style.display = 'block';
        resultActions.style.display = 'none';
        
        // Reset progress
        progressBar.style.width = '0%';
        progressText.textContent = '記事生成を開始しています...';

        // Start progress animation
        let progress = 0;
        let progressInterval = setInterval(() => {
            progress += Math.random() * 3;
            if (progress > 90) progress = 90;
            
            progressBar.style.width = `${progress}%`;
            
            // Update progress text based on progress
            if (progress < 30) {
                progressText.textContent = 'Claude AIで記事を生成中...';
            } else if (progress < 60) {
                progressText.textContent = '楽天商品を検索中...';
            } else if (progress < 80) {
                progressText.textContent = 'Unsplash画像を取得中...';
            } else {
                progressText.textContent = '記事を最終調整中...';
            }
        }, 1000);

        console.log('🚀 Starting article generation:', requestData);

        // Make API request
        const response = await fetch('/api/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestData)
        });

        const result = await response.json();

        // Clear progress animation
        if (typeof progressInterval !== 'undefined') {
            clearInterval(progressInterval);
        }
        progressBar.style.width = '100%';

        if (result.success) {
            generatedArticle = result.article;
            displayGenerationResult(result);
            showAlert('記事生成が完了しました！', 'success');
            console.log('✅ Article generated successfully');
        } else {
            throw new Error(result.error || '記事生成に失敗しました');
        }

    } catch (error) {
        console.error('❌ Generation error:', error);
        if (typeof progressInterval !== 'undefined') {
            clearInterval(progressInterval);
        }
        
        resultContainer.innerHTML = `
            <div class="text-center text-danger">
                <i class="fas fa-exclamation-triangle fa-2x mb-2"></i>
                <h6>記事生成に失敗しました</h6>
                <p class="small">${error.message}</p>
                <button class="btn btn-outline-primary btn-sm" onclick="location.reload()">
                    <i class="fas fa-refresh"></i> ページを再読み込み
                </button>
            </div>
        `;
        
        showAlert(`生成エラー: ${error.message}`, 'danger');
    } finally {
        // Reset UI state
        if (typeof progressInterval !== 'undefined') {
            clearInterval(progressInterval);
        }
        generateBtn.disabled = false;
        generateBtn.innerHTML = '<i class="fas fa-magic"></i> 記事を生成する';
        
        setTimeout(() => {
            progressContainer.style.display = 'none';
        }, 2000);
    }
}

// Display generation result
function displayGenerationResult(result) {
    const resultContainer = document.getElementById('resultContent');
    const resultActions = document.getElementById('resultActions');
    const publishBtn = document.getElementById('publishBtn');
    
    const article = result.article;
    const isPublished = result.published;

    resultContainer.innerHTML = `
        <div class="result-content">
            <!-- Stats -->
            <div class="result-stats">
                <div class="stat-item">
                    <span><i class="fas fa-clock"></i> 生成時間:</span>
                    <strong>${formatDuration(result.generation_time)}</strong>
                </div>
                <div class="stat-item">
                    <span><i class="fas fa-file-alt"></i> 文字数:</span>
                    <strong>${formatNumber(article.content.word_count)}文字</strong>
                </div>
                <div class="stat-item">
                    <span><i class="fas fa-tags"></i> タグ数:</span>
                    <strong>${article.content.tags.length}個</strong>
                </div>
                ${isPublished ? `
                <div class="stat-item">
                    <span><i class="fab fa-wordpress"></i> WordPress:</span>
                    <strong class="text-success">投稿済み</strong>
                </div>
                ` : ''}
            </div>

            <!-- Article Preview -->
            <div class="article-preview">
                <div class="article-title">${article.content.title}</div>
                <div class="article-excerpt">${article.content.excerpt}</div>
                <div class="article-tags">
                    ${article.content.tags.slice(0, 5).map(tag => 
                        `<span class="badge bg-primary">${tag}</span>`
                    ).join('')}
                    ${article.content.tags.length > 5 ? 
                        `<span class="badge bg-secondary">+${article.content.tags.length - 5}</span>` : ''
                    }
                </div>
            </div>

            <!-- Content Preview -->
            <div class="content-preview">
                <h6 class="text-muted">
                    <i class="fas fa-eye"></i> 内容プレビュー (最初の300文字)
                </h6>
                <div class="small text-muted bg-light p-2 rounded">
                    ${article.content.content.substring(0, 300)}...
                    ${article.content.content.includes('おすすめの登山用品') ? 
                        '<div class="mt-2 p-2 bg-success bg-opacity-10 border border-success rounded"><i class="fas fa-shopping-cart text-success"></i> <strong>楽天アフィリエイトリンクが含まれています</strong></div>' : 
                        ''
                    }
                </div>
            </div>
        </div>
    `;

    // Show action buttons
    resultActions.style.display = 'block';
    
    // Show publish button only if not already published
    if (!isPublished && article.wordpress_id !== 999) {
        publishBtn.style.display = 'inline-block';
    } else {
        publishBtn.style.display = 'none';
    }
}

// Copy article to clipboard
async function copyArticle() {
    if (!generatedArticle) {
        showAlert('生成された記事がありません', 'warning');
        return;
    }

    const content = `${generatedArticle.content.title}\n\n${generatedArticle.content.content}\n\nタグ: ${generatedArticle.content.tags.join(', ')}`;
    await copyToClipboard(content);
}

// Download article
function downloadArticle() {
    if (!generatedArticle) {
        showAlert('生成された記事がありません', 'warning');
        return;
    }

    const content = `${generatedArticle.content.title}\n\n${generatedArticle.content.content}\n\nタグ: ${generatedArticle.content.tags.join(', ')}\n\n生成日時: ${new Date().toLocaleString('ja-JP')}`;
    const filename = `${generatedArticle.mountain.name}_記事_${new Date().toISOString().split('T')[0]}.txt`;
    
    downloadTextFile(content, filename);
    showAlert('記事をダウンロードしました', 'success');
}

// Preview article in modal
function previewArticle() {
    if (!generatedArticle) {
        showAlert('生成された記事がありません', 'warning');
        return;
    }

    const previewContent = document.getElementById('previewContent');
    
    // Format content for preview
    let formattedContent = generatedArticle.content.content;
    
    // Simple markdown-style formatting
    formattedContent = formattedContent
        .replace(/\n\n/g, '</p><p>')
        .replace(/\n/g, '<br>')
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>');

    previewContent.innerHTML = `
        <div class="article-preview-full">
            <h1 class="mb-3">${generatedArticle.content.title}</h1>
            
            <div class="mb-3">
                <span class="badge bg-info me-2">
                    <i class="fas fa-mountain"></i> ${generatedArticle.mountain.name}
                </span>
                <span class="badge bg-success me-2">
                    <i class="fas fa-file-alt"></i> ${formatNumber(generatedArticle.content.word_count)}文字
                </span>
                <span class="badge bg-warning">
                    <i class="fas fa-tags"></i> ${generatedArticle.content.tags.length}タグ
                </span>
            </div>

            <div class="mb-4 p-3 bg-light rounded">
                <h6 class="text-muted">要約</h6>
                <p class="mb-0 fst-italic">${generatedArticle.content.excerpt}</p>
            </div>

            <div class="article-body">
                <p>${formattedContent}</p>
            </div>

            <div class="mt-4 pt-3 border-top">
                <h6 class="text-muted mb-2">タグ</h6>
                ${generatedArticle.content.tags.map(tag => 
                    `<span class="badge bg-outline-primary me-1 mb-1">#${tag}</span>`
                ).join('')}
            </div>
        </div>
    `;

    // Show modal
    const modal = new bootstrap.Modal(document.getElementById('previewModal'));
    modal.show();
}

// Publish to WordPress
async function publishToWordPress() {
    if (!generatedArticle || generatedArticle.wordpress_id) {
        showAlert('投稿できる記事がありません', 'warning');
        return;
    }

    if (!confirm('WordPressに記事を投稿しますか？')) {
        return;
    }

    const publishBtn = document.getElementById('publishBtn');
    const originalText = publishBtn.innerHTML;

    try {
        publishBtn.disabled = true;
        publishBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> 投稿中...';

        // In a real implementation, this would make an API call to publish
        // For now, we'll simulate the process
        await new Promise(resolve => setTimeout(resolve, 2000));
        
        showAlert('WordPress投稿機能は現在開発中です', 'info');
        
    } catch (error) {
        console.error('Publish error:', error);
        showAlert(`投稿エラー: ${error.message}`, 'danger');
    } finally {
        publishBtn.disabled = false;
        publishBtn.innerHTML = originalText;
    }
}