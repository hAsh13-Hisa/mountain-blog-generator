// Mountain Blog Generator - Main JavaScript

// Global variables
let selectedMountain = null;
let generatedArticle = null;
let mountains = [];

// Initialize application
document.addEventListener('DOMContentLoaded', function() {
    console.log('🏔️ Mountain Blog Generator initialized');
    loadMountains();
    setupEventListeners();
});

// Load mountains data
async function loadMountains() {
    try {
        const response = await fetch('/api/mountains');
        const data = await response.json();
        
        if (data.success) {
            mountains = data.mountains;
            console.log(`✅ Loaded ${mountains.length} mountains`);
        } else {
            console.error('❌ Failed to load mountains:', data.error);
            showAlert('山データの読み込みに失敗しました', 'danger');
        }
    } catch (error) {
        console.error('❌ Error loading mountains:', error);
        showAlert('山データの読み込み中にエラーが発生しました', 'danger');
    }
}

// Setup event listeners
function setupEventListeners() {
    // Mountain card selection
    document.addEventListener('click', function(e) {
        const mountainCard = e.target.closest('.mountain-card');
        if (mountainCard) {
            selectMountain(mountainCard);
        }
    });

    // Filters
    document.getElementById('regionFilter').addEventListener('change', filterMountains);
    document.getElementById('difficultyFilter').addEventListener('change', filterMountains);
    document.getElementById('mountainSearch').addEventListener('input', filterMountains);

    // Form validation
    document.getElementById('theme').addEventListener('change', updateGenerateButton);
    document.getElementById('targetLength').addEventListener('change', updateGenerateButton);
    document.getElementById('publishToWP').addEventListener('change', updateGenerateButton);
}

// Select mountain
function selectMountain(mountainCard) {
    // Remove previous selection
    document.querySelectorAll('.mountain-card').forEach(card => {
        card.classList.remove('selected');
    });

    // Add selection
    mountainCard.classList.add('selected');
    
    const mountainId = mountainCard.dataset.mountainId;
    selectedMountain = mountains.find(m => m.id === mountainId);
    
    if (selectedMountain) {
        displayMountainInfo(selectedMountain);
        updateGenerateButton();
        console.log('✅ Selected mountain:', selectedMountain.name);
    }
}

// Display mountain information
async function displayMountainInfo(mountain) {
    const infoContainer = document.getElementById('mountainInfo');
    
    try {
        // Get detailed mountain data
        const response = await fetch(`/api/mountain/${mountain.id}`);
        const data = await response.json();
        
        if (data.success) {
            const detailedMountain = data.mountain;
            
            infoContainer.innerHTML = `
                <div class="mountain-info">
                    <h5 class="text-primary">
                        <i class="fas fa-mountain"></i> ${detailedMountain.name}
                        ${detailedMountain.name_en ? `<small class="text-muted">(${detailedMountain.name_en})</small>` : ''}
                    </h5>
                    
                    <div class="row g-2 mb-3">
                        <div class="col-6">
                            <small class="text-muted">標高</small>
                            <div class="fw-bold text-primary">${detailedMountain.elevation}m</div>
                        </div>
                        <div class="col-6">
                            <small class="text-muted">難易度</small>
                            <div class="fw-bold">${detailedMountain.difficulty.level}</div>
                        </div>
                        <div class="col-6">
                            <small class="text-muted">登山時間</small>
                            <div>${detailedMountain.difficulty.hiking_time}</div>
                        </div>
                        <div class="col-6">
                            <small class="text-muted">距離</small>
                            <div>${detailedMountain.difficulty.distance}</div>
                        </div>
                    </div>
                    
                    <div class="mb-3">
                        <small class="text-muted">アクセス</small>
                        <div>${detailedMountain.location.nearest_station}から${detailedMountain.location.access_time}</div>
                    </div>
                    
                    <div class="mb-3">
                        <small class="text-muted">特徴</small>
                        <div class="mt-1">
                            ${detailedMountain.features.slice(0, 3).map(feature => 
                                `<span class="badge bg-light text-dark feature-tag">${feature}</span>`
                            ).join('')}
                        </div>
                    </div>
                    
                    ${detailedMountain.description ? `
                        <div class="mb-2">
                            <small class="text-muted">説明</small>
                            <div class="small">${detailedMountain.description.substring(0, 150)}...</div>
                        </div>
                    ` : ''}
                </div>
            `;
        } else {
            infoContainer.innerHTML = `
                <div class="text-danger">
                    <i class="fas fa-exclamation-triangle"></i>
                    山の詳細情報を取得できませんでした
                </div>
            `;
        }
    } catch (error) {
        console.error('Error loading mountain details:', error);
        infoContainer.innerHTML = `
            <div class="text-warning">
                <i class="fas fa-exclamation-triangle"></i>
                山の情報を読み込み中にエラーが発生しました
            </div>
        `;
    }
}

// Filter mountains
function filterMountains() {
    const regionFilter = document.getElementById('regionFilter').value;
    const difficultyFilter = document.getElementById('difficultyFilter').value;
    const searchQuery = document.getElementById('mountainSearch').value.toLowerCase();
    
    const mountainCards = document.querySelectorAll('.mountain-card');
    let visibleCount = 0;
    
    mountainCards.forEach(card => {
        const region = card.dataset.region;
        const difficulty = card.dataset.difficulty;
        const name = card.dataset.name.toLowerCase();
        
        const regionMatch = !regionFilter || region === regionFilter;
        const difficultyMatch = !difficultyFilter || difficulty === difficultyFilter;
        const nameMatch = !searchQuery || name.includes(searchQuery);
        
        if (regionMatch && difficultyMatch && nameMatch) {
            card.style.display = 'block';
            visibleCount++;
        } else {
            card.style.display = 'none';
        }
    });
    
    document.getElementById('mountainCount').textContent = visibleCount;
}

// Update generate button state
function updateGenerateButton() {
    const generateBtn = document.getElementById('generateBtn');
    generateBtn.disabled = !selectedMountain;
}

// Show alert message
function showAlert(message, type = 'info') {
    // Create alert element
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    alertDiv.style.cssText = 'top: 80px; right: 20px; z-index: 1050; min-width: 300px;';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(alertDiv);
    
    // Auto dismiss after 5 seconds
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.remove();
        }
    }, 5000);
}

// Copy to clipboard utility
async function copyToClipboard(text) {
    try {
        await navigator.clipboard.writeText(text);
        showAlert('クリップボードにコピーしました', 'success');
    } catch (error) {
        console.error('Copy failed:', error);
        showAlert('コピーに失敗しました', 'danger');
    }
}

// Download text file utility
function downloadTextFile(content, filename) {
    const blob = new Blob([content], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

// Format numbers
function formatNumber(num) {
    return new Intl.NumberFormat('ja-JP').format(num);
}

// Format time duration
function formatDuration(seconds) {
    if (seconds < 60) {
        return `${seconds.toFixed(1)}秒`;
    } else {
        const minutes = Math.floor(seconds / 60);
        const remainingSeconds = seconds % 60;
        return `${minutes}分${remainingSeconds.toFixed(0)}秒`;
    }
}