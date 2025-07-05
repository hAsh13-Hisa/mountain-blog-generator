/**
 * 低山旅行 - ミニマルデザイン JavaScript
 * ユーザー体験最優先・軽量・高性能
 */

class MinimalSite {
    constructor() {
        this.init();
    }

    init() {
        this.setupMobileMenu();
        this.setupSmoothScroll();
        this.setupIntersectionObserver();
        this.setupAccessibility();
        this.setupAnalytics();
    }

    // モバイルメニューの制御
    setupMobileMenu() {
        const mobileToggle = document.querySelector('.mobile-menu-toggle');
        const mobileNav = document.querySelector('.mobile-nav');
        
        if (!mobileToggle || !mobileNav) return;
        
        mobileToggle.addEventListener('click', () => {
            const isOpen = mobileNav.classList.contains('active');
            
            // 状態切り替え
            mobileNav.classList.toggle('active');
            mobileToggle.classList.toggle('active');
            
            // アクセシビリティ属性
            mobileToggle.setAttribute('aria-expanded', !isOpen);
            mobileToggle.setAttribute('aria-label', isOpen ? 'メニューを開く' : 'メニューを閉じる');
            
            // ボディスクロール制御
            document.body.style.overflow = isOpen ? 'auto' : 'hidden';
        });
        
        // 外側クリックでメニューを閉じる
        document.addEventListener('click', (e) => {
            if (!mobileToggle.contains(e.target) && !mobileNav.contains(e.target)) {
                mobileNav.classList.remove('active');
                mobileToggle.classList.remove('active');
                mobileToggle.setAttribute('aria-expanded', 'false');
                mobileToggle.setAttribute('aria-label', 'メニューを開く');
                document.body.style.overflow = 'auto';
            }
        });
        
        // ESCキーでメニューを閉じる
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && mobileNav.classList.contains('active')) {
                mobileNav.classList.remove('active');
                mobileToggle.classList.remove('active');
                mobileToggle.setAttribute('aria-expanded', 'false');
                mobileToggle.setAttribute('aria-label', 'メニューを開く');
                document.body.style.overflow = 'auto';
                mobileToggle.focus();
            }
        });
    }

    // スムーススクロール
    setupSmoothScroll() {
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', (e) => {
                e.preventDefault();
                const target = document.querySelector(anchor.getAttribute('href'));
                
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

    // Intersection Observer でアニメーション
    setupIntersectionObserver() {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('fade-in');
                    observer.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        });

        // 対象要素を監視
        document.querySelectorAll('.card, .section-header').forEach(el => {
            observer.observe(el);
        });
    }

    // アクセシビリティ強化
    setupAccessibility() {
        // フォーカス管理
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Tab') {
                document.body.classList.add('keyboard-navigation');
            }
        });

        document.addEventListener('mousedown', () => {
            document.body.classList.remove('keyboard-navigation');
        });

        // スキップリンク
        const skipLink = document.querySelector('.sr-only');
        if (skipLink) {
            skipLink.addEventListener('focus', () => {
                skipLink.classList.remove('sr-only');
            });
            
            skipLink.addEventListener('blur', () => {
                skipLink.classList.add('sr-only');
            });
        }
    }

    // アナリティクス（シンプル）
    setupAnalytics() {
        // アフィリエイトリンククリック追跡
        document.querySelectorAll('a[href*="amazon"], a[href*="rakuten"], a[data-affiliate]').forEach(link => {
            link.addEventListener('click', (e) => {
                const affiliate = link.dataset.affiliate || 'unknown';
                const product = link.closest('.card')?.querySelector('.card-title')?.textContent || 'unknown';
                
                // 簡単なログ記録（実際の分析ツールに送信）
                console.log(`Affiliate Click: ${affiliate} - ${product}`);
                
                // 実際の実装では Google Analytics や他の分析ツールに送信
                if (typeof gtag !== 'undefined') {
                    gtag('event', 'click', {
                        'event_category': 'affiliate',
                        'event_label': `${affiliate} - ${product}`,
                        'value': 1
                    });
                }
            });
        });

        // ページビュー追跡
        if (typeof gtag !== 'undefined') {
            gtag('config', 'GA_MEASUREMENT_ID', {
                'page_title': document.title,
                'page_location': window.location.href
            });
        }
    }
}

// DOM読み込み完了時に初期化
document.addEventListener('DOMContentLoaded', () => {
    new MinimalSite();
});

// パフォーマンス監視
window.addEventListener('load', () => {
    // First Contentful Paint
    const observer = new PerformanceObserver((list) => {
        list.getEntries().forEach((entry) => {
            if (entry.name === 'first-contentful-paint') {
                console.log('FCP:', entry.startTime);
            }
        });
    });
    
    observer.observe({entryTypes: ['paint']});
    
    // 画像遅延読み込み
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    if (img.dataset.src) {
                        img.src = img.dataset.src;
                        img.classList.remove('lazy');
                        imageObserver.unobserve(img);
                    }
                }
            });
        });

        document.querySelectorAll('img[data-src]').forEach(img => {
            imageObserver.observe(img);
        });
    }
});

// エラーハンドリング
window.addEventListener('error', (e) => {
    console.error('JavaScript Error:', e.error);
    // エラーレポートシステムに送信（実際の実装で）
});

// サービスワーカー登録（PWA対応）
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/sw.js')
            .then(registration => {
                console.log('Service Worker registered:', registration);
            })
            .catch(error => {
                console.log('Service Worker registration failed:', error);
            });
    });
}