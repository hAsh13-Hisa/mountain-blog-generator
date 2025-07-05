/**
 * 🏔️ 低山マスター - フレッシュサイトJavaScript
 * アフィリエイト収益最大化に特化した機能実装
 */

class FreshSite {
    constructor() {
        this.init();
    }

    init() {
        document.addEventListener('DOMContentLoaded', () => {
            this.initMobileMenu();
            this.initSmoothScroll();
            this.initLazyLoading();
            this.initAnimations();
            this.initCTATracking();
            this.initPerformanceOptimization();
        });
    }

    /**
     * モバイルメニューの制御
     */
    initMobileMenu() {
        const mobileToggle = document.querySelector('.mobile-menu-toggle');
        const mobileNav = document.querySelector('.mobile-nav');
        
        if (!mobileToggle || !mobileNav) return;

        mobileToggle.addEventListener('click', () => {
            const isActive = mobileToggle.classList.contains('active');
            
            // トグル状態を切り替え
            mobileToggle.classList.toggle('active');
            mobileNav.classList.toggle('active');
            
            // aria属性を更新
            mobileToggle.setAttribute('aria-expanded', !isActive);
            
            // ボディのスクロールを制御
            document.body.style.overflow = isActive ? 'auto' : 'hidden';
        });

        // モバイルメニューリンククリック時の処理
        const mobileLinks = mobileNav.querySelectorAll('a');
        mobileLinks.forEach(link => {
            link.addEventListener('click', () => {
                // メニューを閉じる
                mobileToggle.classList.remove('active');
                mobileNav.classList.remove('active');
                mobileToggle.setAttribute('aria-expanded', false);
                document.body.style.overflow = 'auto';
            });
        });

        // 画面サイズ変更時の処理
        window.addEventListener('resize', () => {
            if (window.innerWidth >= 768) {
                mobileToggle.classList.remove('active');
                mobileNav.classList.remove('active');
                mobileToggle.setAttribute('aria-expanded', false);
                document.body.style.overflow = 'auto';
            }
        });
    }

    /**
     * スムーススクロール機能
     */
    initSmoothScroll() {
        // ページ内リンクのスムーススクロール
        const internalLinks = document.querySelectorAll('a[href^="#"]');
        
        internalLinks.forEach(link => {
            link.addEventListener('click', (e) => {
                const targetId = link.getAttribute('href').substring(1);
                const targetElement = document.getElementById(targetId);
                
                if (targetElement) {
                    e.preventDefault();
                    
                    // ヘッダーの高さを考慮したオフセット
                    const headerHeight = document.querySelector('.site-header').offsetHeight;
                    const targetPosition = targetElement.offsetTop - headerHeight - 20;
                    
                    window.scrollTo({
                        top: targetPosition,
                        behavior: 'smooth'
                    });
                }
            });
        });
    }

    /**
     * 遅延読み込み（Lazy Loading）
     */
    initLazyLoading() {
        // Intersection Observer対応チェック
        if ('IntersectionObserver' in window) {
            const imageObserver = new IntersectionObserver((entries, observer) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        
                        // data-src から src に移動
                        if (img.dataset.src) {
                            img.src = img.dataset.src;
                            img.removeAttribute('data-src');
                        }
                        
                        // lazy-image クラスを削除
                        img.classList.remove('lazy-image');
                        img.classList.add('loaded');
                        
                        observer.unobserve(img);
                    }
                });
            }, {
                rootMargin: '50px 0px',
                threshold: 0.01
            });

            // 遅延読み込み対象の画像を監視
            const lazyImages = document.querySelectorAll('img.lazy-image');
            lazyImages.forEach(img => imageObserver.observe(img));
        }
    }

    /**
     * アニメーション効果
     */
    initAnimations() {
        // スクロール時のフェードインアニメーション
        if ('IntersectionObserver' in window) {
            const animationObserver = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('animate-in');
                    }
                });
            }, {
                threshold: 0.1,
                rootMargin: '0px 0px -50px 0px'
            });

            // アニメーション対象要素を監視
            const animateElements = document.querySelectorAll('.equipment-card, .mountain-gear-card, .region-card');
            animateElements.forEach(el => {
                el.style.opacity = '0';
                el.style.transform = 'translateY(30px)';
                el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
                animationObserver.observe(el);
            });
        }

        // CSSアニメーションクラス
        const style = document.createElement('style');
        style.textContent = `
            .animate-in {
                opacity: 1 !important;
                transform: translateY(0) !important;
            }
            
            .pulse-effect {
                animation: pulse-effect 2s ease-in-out infinite;
            }
            
            @keyframes pulse-effect {
                0%, 100% { transform: scale(1); }
                50% { transform: scale(1.05); }
            }
        `;
        document.head.appendChild(style);
    }

    /**
     * CTAボタンクリック追跡
     */
    initCTATracking() {
        const ctaButtons = document.querySelectorAll('.cta-button');
        
        ctaButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                const buttonText = button.textContent.trim();
                const buttonType = button.classList.contains('primary') ? 'primary' : 'secondary';
                const section = this.getParentSection(button);
                
                // アフィリエイト追跡（AffiliateTracker.jsで処理）
                if (typeof AffiliateTracker !== 'undefined') {
                    AffiliateTracker.trackCTAClick({
                        buttonText,
                        buttonType,
                        section,
                        url: button.href
                    });
                }
                
                // コンソールログ（開発用）
                console.log('CTA Clicked:', {
                    text: buttonText,
                    type: buttonType,
                    section: section,
                    timestamp: new Date().toISOString()
                });
            });
        });
    }

    /**
     * パフォーマンス最適化
     */
    initPerformanceOptimization() {
        // Critical CSSの後に非Critical CSSを読み込み
        this.loadNonCriticalCSS();
        
        // Service Worker登録（将来実装用）
        this.registerServiceWorker();
        
        // プリフェッチ設定
        this.initPrefetch();
    }

    /**
     * 非Critical CSS の遅延読み込み
     */
    loadNonCriticalCSS() {
        const nonCriticalCSS = [
            '/static_fresh/css/print.css'
        ];

        nonCriticalCSS.forEach(href => {
            const link = document.createElement('link');
            link.rel = 'stylesheet';
            link.href = href;
            link.media = 'print';
            link.onload = function() {
                this.media = 'all';
            };
            document.head.appendChild(link);
        });
    }

    /**
     * Service Worker登録（PWA対応準備）
     */
    registerServiceWorker() {
        if ('serviceWorker' in navigator) {
            window.addEventListener('load', () => {
                navigator.serviceWorker.register('/sw.js')
                    .then(registration => {
                        console.log('SW registered: ', registration);
                    })
                    .catch(registrationError => {
                        console.log('SW registration failed: ', registrationError);
                    });
            });
        }
    }

    /**
     * プリフェッチ機能
     */
    initPrefetch() {
        // ホバー時に次ページをプリフェッチ
        const prefetchLinks = document.querySelectorAll('a[href^="/"]');
        const prefetched = new Set();

        prefetchLinks.forEach(link => {
            link.addEventListener('mouseenter', () => {
                const href = link.href;
                
                if (!prefetched.has(href) && href !== window.location.href) {
                    const prefetchLink = document.createElement('link');
                    prefetchLink.rel = 'prefetch';
                    prefetchLink.href = href;
                    document.head.appendChild(prefetchLink);
                    prefetched.add(href);
                }
            });
        });
    }

    /**
     * ユーティリティ: 親セクションを取得
     */
    getParentSection(element) {
        const section = element.closest('section');
        if (section) {
            // セクションのクラス名から特定
            const sectionClasses = Array.from(section.classList);
            const sectionClass = sectionClasses.find(cls => 
                ['hero', 'featured-equipment', 'mountain-with-gear', 'regional-guide', 'beginner-guide'].includes(cls)
            );
            return sectionClass || 'unknown';
        }
        return 'unknown';
    }

    /**
     * ユーティリティ: デバウンス関数
     */
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    /**
     * ユーティリティ: スロットル関数
     */
    throttle(func, limit) {
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
    }
}

/**
 * 装備推奨システム
 */
class EquipmentRecommendation {
    constructor() {
        this.userPreferences = this.loadUserPreferences();
        this.init();
    }

    init() {
        this.trackUserInteraction();
        this.personalizeRecommendations();
    }

    /**
     * ユーザーの操作を追跡して嗜好を学習
     */
    trackUserInteraction() {
        // 装備カードのクリック追跡
        document.addEventListener('click', (e) => {
            const equipmentCard = e.target.closest('.equipment-card');
            if (equipmentCard) {
                const category = this.getEquipmentCategory(equipmentCard);
                const priceRange = this.getPriceRange(equipmentCard);
                
                this.updateUserPreferences(category, priceRange);
            }
        });
    }

    /**
     * ユーザー嗜好に基づく推奨表示
     */
    personalizeRecommendations() {
        const recommendationElements = document.querySelectorAll('.equipment-grid .equipment-card');
        
        recommendationElements.forEach(card => {
            const category = this.getEquipmentCategory(card);
            const score = this.calculateRecommendationScore(category);
            
            // スコアに基づいて表示順序を調整
            card.style.order = Math.round(score * -100); // 高スコアほど前に
        });
    }

    /**
     * 装備カテゴリを取得
     */
    getEquipmentCategory(card) {
        const title = card.querySelector('.card-title')?.textContent || '';
        
        if (title.includes('ザック') || title.includes('バックパック')) return 'backpack';
        if (title.includes('シューズ') || title.includes('靴')) return 'shoes';
        if (title.includes('ジャケット') || title.includes('ウェア')) return 'clothing';
        
        return 'other';
    }

    /**
     * 価格帯を取得
     */
    getPriceRange(card) {
        const priceElement = card.querySelector('.price-current');
        if (!priceElement) return 'unknown';
        
        const price = parseInt(priceElement.textContent.replace(/[^0-9]/g, ''));
        
        if (price < 5000) return 'budget';
        if (price < 15000) return 'mid';
        return 'premium';
    }

    /**
     * ユーザー嗜好を更新
     */
    updateUserPreferences(category, priceRange) {
        if (!this.userPreferences[category]) {
            this.userPreferences[category] = {};
        }
        
        this.userPreferences[category][priceRange] = 
            (this.userPreferences[category][priceRange] || 0) + 1;
        
        this.saveUserPreferences();
    }

    /**
     * 推奨スコアを計算
     */
    calculateRecommendationScore(category) {
        const categoryPrefs = this.userPreferences[category] || {};
        const totalInteractions = Object.values(categoryPrefs).reduce((sum, count) => sum + count, 0);
        
        return totalInteractions > 0 ? totalInteractions / 10 : 0.5; // デフォルトスコア
    }

    /**
     * ユーザー嗜好を保存
     */
    saveUserPreferences() {
        try {
            localStorage.setItem('mountainMaster_preferences', JSON.stringify(this.userPreferences));
        } catch (e) {
            console.warn('Failed to save user preferences:', e);
        }
    }

    /**
     * ユーザー嗜好を読み込み
     */
    loadUserPreferences() {
        try {
            const saved = localStorage.getItem('mountainMaster_preferences');
            return saved ? JSON.parse(saved) : {};
        } catch (e) {
            console.warn('Failed to load user preferences:', e);
            return {};
        }
    }
}

/**
 * A/Bテストシステム（収益最適化）
 */
class ABTestManager {
    constructor() {
        this.tests = {};
        this.init();
    }

    init() {
        this.loadActiveTests();
        this.applyTests();
    }

    /**
     * アクティブなテストを読み込み
     */
    loadActiveTests() {
        // 実際の実装では外部APIまたは設定ファイルから読み込み
        this.tests = {
            'cta_button_color': {
                variants: ['orange', 'red', 'green'],
                allocation: [0.4, 0.4, 0.2],
                metric: 'click_through_rate'
            },
            'price_display_format': {
                variants: ['with_discount', 'without_discount'],
                allocation: [0.5, 0.5],
                metric: 'conversion_rate'
            }
        };
    }

    /**
     * テストを適用
     */
    applyTests() {
        Object.entries(this.tests).forEach(([testName, config]) => {
            const variant = this.getVariant(testName, config.variants, config.allocation);
            this.applyVariant(testName, variant);
            
            // テスト参加を記録
            this.trackTestParticipation(testName, variant);
        });
    }

    /**
     * バリアントを決定
     */
    getVariant(testName, variants, allocation) {
        // ユーザーIDに基づく決定的な割り当て
        const userId = this.getUserId();
        const hash = this.simpleHash(`${testName}_${userId}`);
        const random = (hash % 1000) / 1000;
        
        let cumulative = 0;
        for (let i = 0; i < variants.length; i++) {
            cumulative += allocation[i];
            if (random < cumulative) {
                return variants[i];
            }
        }
        
        return variants[0]; // フォールバック
    }

    /**
     * バリアントを適用
     */
    applyVariant(testName, variant) {
        switch (testName) {
            case 'cta_button_color':
                this.applyCTAColorVariant(variant);
                break;
            case 'price_display_format':
                this.applyPriceDisplayVariant(variant);
                break;
        }
    }

    /**
     * CTAボタン色のバリアント適用
     */
    applyCTAColorVariant(variant) {
        const ctaButtons = document.querySelectorAll('.cta-button.primary');
        const colorMap = {
            'orange': '#ff6b35',
            'red': '#d73035',
            'green': '#27ae60'
        };
        
        ctaButtons.forEach(button => {
            button.style.background = colorMap[variant];
        });
    }

    /**
     * 価格表示のバリアント適用
     */
    applyPriceDisplayVariant(variant) {
        const priceDisplays = document.querySelectorAll('.price-display');
        
        priceDisplays.forEach(display => {
            const discountElement = display.querySelector('.price-discount');
            if (variant === 'without_discount' && discountElement) {
                discountElement.style.display = 'none';
            }
        });
    }

    /**
     * テスト参加を記録
     */
    trackTestParticipation(testName, variant) {
        if (typeof AffiliateTracker !== 'undefined') {
            AffiliateTracker.trackABTest(testName, variant);
        }
    }

    /**
     * ユーザーIDを取得（またはセッションIDを生成）
     */
    getUserId() {
        let userId = localStorage.getItem('mountainMaster_userId');
        if (!userId) {
            userId = 'user_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
            localStorage.setItem('mountainMaster_userId', userId);
        }
        return userId;
    }

    /**
     * 簡単なハッシュ関数
     */
    simpleHash(str) {
        let hash = 0;
        for (let i = 0; i < str.length; i++) {
            const char = str.charCodeAt(i);
            hash = ((hash << 5) - hash) + char;
            hash = hash & hash; // 32bit整数に変換
        }
        return Math.abs(hash);
    }
}

// インスタンス化
const freshSite = new FreshSite();
const equipmentRecommendation = new EquipmentRecommendation();
const abTestManager = new ABTestManager();

// グローバル関数として公開（他のスクリプトから利用可能）
window.FreshSite = {
    instance: freshSite,
    EquipmentRecommendation: equipmentRecommendation,
    ABTestManager: abTestManager
};