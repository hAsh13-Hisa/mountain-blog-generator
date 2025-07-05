/**
 * Site JavaScript - 低山マスター
 * アフィリエイトサイト専用機能
 */

document.addEventListener('DOMContentLoaded', function() {
    initializeAffiliateSite();
});

function initializeAffiliateSite() {
    initMobileMenu();
    initSmoothScrolling();
    initLazyLoading();
    initCTAButtons();
    initAffiliateTracking();
}

/**
 * モバイルメニューの初期化
 */
function initMobileMenu() {
    const mobileToggle = document.querySelector('.mobile-menu-toggle');
    const mainNav = document.querySelector('.main-nav');
    
    if (mobileToggle && mainNav) {
        mobileToggle.addEventListener('click', function() {
            mainNav.classList.toggle('mobile-open');
            this.classList.toggle('active');
        });
        
        // メニュー外クリックで閉じる
        document.addEventListener('click', function(e) {
            if (!mobileToggle.contains(e.target) && !mainNav.contains(e.target)) {
                mainNav.classList.remove('mobile-open');
                mobileToggle.classList.remove('active');
            }
        });
    }
}

/**
 * スムーススクロールの初期化
 */
function initSmoothScrolling() {
    // アンカーリンクのスムーススクロール
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                const headerHeight = document.querySelector('.site-header').offsetHeight;
                const targetPosition = target.offsetTop - headerHeight - 20;
                
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
}

/**
 * 遅延読み込みの初期化
 */
function initLazyLoading() {
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver(function(entries, observer) {
            entries.forEach(function(entry) {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src || img.src;
                    img.classList.remove('lazy');
                    observer.unobserve(img);
                }
            });
        });
        
        document.querySelectorAll('img[loading="lazy"]').forEach(function(img) {
            imageObserver.observe(img);
        });
    }
}

/**
 * CTAボタンの強化
 */
function initCTAButtons() {
    document.querySelectorAll('.cta-button').forEach(button => {
        // ホバー効果の強化
        button.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px)';
        });
        
        button.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
        
        // クリック効果
        button.addEventListener('click', function(e) {
            // リップル効果を追加
            const ripple = document.createElement('span');
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;
            
            ripple.style.width = ripple.style.height = size + 'px';
            ripple.style.left = x + 'px';
            ripple.style.top = y + 'px';
            ripple.classList.add('ripple');
            
            this.appendChild(ripple);
            
            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    });
}

/**
 * アフィリエイトトラッキングの初期化
 */
function initAffiliateTracking() {
    // アフィリエイトリンクのクリック追跡
    document.querySelectorAll('.affiliate-link').forEach(link => {
        link.addEventListener('click', function() {
            const productId = this.dataset.product;
            const setId = this.dataset.set;
            const eventType = this.dataset.event || 'click';
            
            // Google Analytics 4イベント送信（仮）
            if (typeof gtag !== 'undefined') {
                gtag('event', 'affiliate_click', {
                    'product_id': productId,
                    'set_id': setId,
                    'link_url': this.href
                });
            }
            
            // コンソールログ（開発用）
            console.log('Affiliate Link Clicked:', {
                productId: productId,
                setId: setId,
                url: this.href,
                timestamp: new Date().toISOString()
            });
        });
    });
    
    // 商品表示の追跡
    if ('IntersectionObserver' in window) {
        const productObserver = new IntersectionObserver(function(entries) {
            entries.forEach(function(entry) {
                if (entry.isIntersecting) {
                    const productBox = entry.target;
                    const productId = productBox.dataset.productId;
                    
                    if (typeof gtag !== 'undefined') {
                        gtag('event', 'product_view', {
                            'product_id': productId
                        });
                    }
                    
                    console.log('Product Viewed:', productId);
                }
            });
        }, {
            threshold: 0.5
        });
        
        document.querySelectorAll('.affiliate-product-box').forEach(function(box) {
            productObserver.observe(box);
        });
    }
}

/**
 * 価格アニメーション
 */
function animatePrice(element) {
    const finalPrice = parseInt(element.textContent.replace(/[^\d]/g, ''));
    const duration = 1000;
    const steps = 30;
    const increment = finalPrice / steps;
    let current = 0;
    let step = 0;
    
    const timer = setInterval(function() {
        current += increment;
        step++;
        
        element.textContent = '¥' + Math.floor(current).toLocaleString();
        
        if (step >= steps) {
            clearInterval(timer);
            element.textContent = '¥' + finalPrice.toLocaleString();
        }
    }, duration / steps);
}

/**
 * 検索機能（将来実装用）
 */
function initSearch() {
    const searchInput = document.querySelector('.search-input');
    const searchResults = document.querySelector('.search-results');
    
    if (searchInput) {
        let debounceTimer;
        
        searchInput.addEventListener('input', function() {
            clearTimeout(debounceTimer);
            debounceTimer = setTimeout(() => {
                performSearch(this.value);
            }, 300);
        });
    }
}

function performSearch(query) {
    // 検索機能の実装（将来対応）
    console.log('Search query:', query);
}

/**
 * フォーム送信の処理
 */
function initForms() {
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function(e) {
            // フォームバリデーション
            const requiredFields = this.querySelectorAll('[required]');
            let isValid = true;
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    field.classList.add('error');
                } else {
                    field.classList.remove('error');
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                alert('必須項目を入力してください。');
            }
        });
    });
}

/**
 * スクロール連動エフェクト
 */
function initScrollEffects() {
    let ticking = false;
    
    function updateScrollEffects() {
        const scrolled = window.pageYOffset;
        const rate = scrolled * -0.5;
        
        // パララックス効果
        const parallaxElements = document.querySelectorAll('.parallax');
        parallaxElements.forEach(element => {
            element.style.transform = `translateY(${rate}px)`;
        });
        
        ticking = false;
    }
    
    function requestTick() {
        if (!ticking) {
            requestAnimationFrame(updateScrollEffects);
            ticking = true;
        }
    }
    
    window.addEventListener('scroll', requestTick);
}

/**
 * ユーティリティ関数
 */
const Utils = {
    // デバウンス関数
    debounce: function(func, wait, immediate) {
        let timeout;
        return function executedFunction() {
            const context = this;
            const args = arguments;
            const later = function() {
                timeout = null;
                if (!immediate) func.apply(context, args);
            };
            const callNow = immediate && !timeout;
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
            if (callNow) func.apply(context, args);
        };
    },
    
    // スロットル関数
    throttle: function(func, limit) {
        let inThrottle;
        return function() {
            const args = arguments;
            const context = this;
            if (!inThrottle) {
                func.apply(context, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    },
    
    // 要素の表示判定
    isElementInViewport: function(el) {
        const rect = el.getBoundingClientRect();
        return (
            rect.top >= 0 &&
            rect.left >= 0 &&
            rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
            rect.right <= (window.innerWidth || document.documentElement.clientWidth)
        );
    }
};

// CSSアニメーション用クラス
const style = document.createElement('style');
style.textContent = `
    .ripple {
        position: absolute;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.6);
        transform: scale(0);
        animation: ripple-animation 0.6s linear;
        pointer-events: none;
    }
    
    @keyframes ripple-animation {
        to {
            transform: scale(2);
            opacity: 0;
        }
    }
    
    .fade-in {
        opacity: 0;
        animation: fadeIn 0.6s ease-in-out forwards;
    }
    
    @keyframes fadeIn {
        to {
            opacity: 1;
        }
    }
    
    .slide-up {
        transform: translateY(30px);
        opacity: 0;
        animation: slideUp 0.6s ease-out forwards;
    }
    
    @keyframes slideUp {
        to {
            transform: translateY(0);
            opacity: 1;
        }
    }
`;
document.head.appendChild(style);

// エクスポート（モジュール対応）
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { Utils };
}