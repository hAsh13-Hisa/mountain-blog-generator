/**
 * Affiliate Tracking JavaScript
 * アフィリエイト収益最大化のための追跡・分析機能
 */

class AffiliateTracker {
    constructor() {
        this.sessionId = this.generateSessionId();
        this.userId = this.getUserId();
        this.events = [];
        this.init();
    }
    
    init() {
        this.trackPageView();
        this.initClickTracking();
        this.initScrollTracking();
        this.initTimeTracking();
        this.initConversionTracking();
        
        // ページ離脱時にデータを送信
        window.addEventListener('beforeunload', () => {
            this.sendEvents();
        });
        
        // 定期的にデータを送信
        setInterval(() => {
            this.sendEvents();
        }, 30000); // 30秒ごと
    }
    
    /**
     * セッションIDを生成
     */
    generateSessionId() {
        return 'sess_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }
    
    /**
     * ユーザーIDを取得（ローカルストレージから、なければ生成）
     */
    getUserId() {
        let userId = localStorage.getItem('affiliate_user_id');
        if (!userId) {
            userId = 'user_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
            localStorage.setItem('affiliate_user_id', userId);
        }
        return userId;
    }
    
    /**
     * ページビューを追跡
     */
    trackPageView() {
        this.addEvent('page_view', {
            url: window.location.href,
            title: document.title,
            referrer: document.referrer,
            timestamp: new Date().toISOString(),
            viewport: {
                width: window.innerWidth,
                height: window.innerHeight
            },
            device: this.getDeviceInfo()
        });
    }
    
    /**
     * クリック追跡を初期化
     */
    initClickTracking() {
        // アフィリエイトリンクのクリック
        document.addEventListener('click', (e) => {
            const target = e.target.closest('.affiliate-link');
            if (target) {
                this.trackAffiliateClick(target, e);
            }
            
            // CTAボタンのクリック
            const ctaButton = e.target.closest('.cta-button');
            if (ctaButton) {
                this.trackCTAClick(ctaButton, e);
            }
            
            // 商品画像のクリック
            const productImage = e.target.closest('.product-image, .card-image');
            if (productImage) {
                this.trackProductImageClick(productImage, e);
            }
        });
    }
    
    /**
     * アフィリエイトリンククリックの追跡
     */
    trackAffiliateClick(element, event) {
        const productId = element.dataset.product;
        const setId = element.dataset.set;
        const category = element.dataset.category;
        const position = this.getElementPosition(element);
        
        this.addEvent('affiliate_click', {
            product_id: productId,
            set_id: setId,
            category: category,
            url: element.href,
            text: element.textContent.trim(),
            position: position,
            timestamp: new Date().toISOString()
        });
        
        // Google Analytics 4への送信
        if (typeof gtag !== 'undefined') {
            gtag('event', 'select_content', {
                content_type: 'affiliate_product',
                content_id: productId,
                custom_parameters: {
                    affiliate_category: category,
                    page_position: position
                }
            });
        }
        
        console.log('🔗 Affiliate Click Tracked:', {
            productId,
            setId,
            url: element.href
        });
    }
    
    /**
     * CTAボタンクリックの追跡
     */
    trackCTAClick(element, event) {
        const buttonText = element.textContent.trim();
        const buttonType = element.className.includes('primary') ? 'primary' : 'secondary';
        const section = this.getParentSection(element);
        
        this.addEvent('cta_click', {
            button_text: buttonText,
            button_type: buttonType,
            section: section,
            position: this.getElementPosition(element),
            timestamp: new Date().toISOString()
        });
    }
    
    /**
     * 商品画像クリックの追跡
     */
    trackProductImageClick(element, event) {
        const productBox = element.closest('.affiliate-product-box, .equipment-card');
        const productId = productBox ? productBox.dataset.productId : null;
        
        this.addEvent('product_image_click', {
            product_id: productId,
            image_src: element.querySelector('img')?.src,
            timestamp: new Date().toISOString()
        });
    }
    
    /**
     * スクロール追跡を初期化
     */
    initScrollTracking() {
        let maxScroll = 0;
        const scrollThresholds = [25, 50, 75, 90, 100];
        const trackedThresholds = new Set();
        
        const trackScroll = this.throttle(() => {
            const scrollPercent = Math.round(
                (window.scrollY / (document.body.scrollHeight - window.innerHeight)) * 100
            );
            
            maxScroll = Math.max(maxScroll, scrollPercent);
            
            // 閾値を超えた時の追跡
            scrollThresholds.forEach(threshold => {
                if (scrollPercent >= threshold && !trackedThresholds.has(threshold)) {
                    trackedThresholds.add(threshold);
                    this.addEvent('scroll_depth', {
                        depth_percent: threshold,
                        timestamp: new Date().toISOString()
                    });
                }
            });
        }, 500);
        
        window.addEventListener('scroll', trackScroll);
        
        // ページ離脱時に最大スクロール値を記録
        window.addEventListener('beforeunload', () => {
            this.addEvent('max_scroll', {
                max_scroll_percent: maxScroll,
                timestamp: new Date().toISOString()
            });
        });
    }
    
    /**
     * 滞在時間の追跡
     */
    initTimeTracking() {
        this.startTime = Date.now();
        this.isActive = true;
        this.totalActiveTime = 0;
        this.lastActiveTime = this.startTime;
        
        // ページがアクティブかどうかの監視
        document.addEventListener('visibilitychange', () => {
            if (document.hidden) {
                this.totalActiveTime += Date.now() - this.lastActiveTime;
                this.isActive = false;
            } else {
                this.lastActiveTime = Date.now();
                this.isActive = true;
            }
        });
        
        // マウス移動やキーボード操作でアクティブ状態を更新
        ['mousemove', 'keydown', 'scroll', 'click'].forEach(event => {
            document.addEventListener(event, this.throttle(() => {
                if (!this.isActive) {
                    this.lastActiveTime = Date.now();
                    this.isActive = true;
                }
            }, 1000));
        });
        
        // 定期的に滞在時間を記録
        setInterval(() => {
            const currentTime = Date.now();
            const sessionTime = currentTime - this.startTime;
            const activeTime = this.isActive 
                ? this.totalActiveTime + (currentTime - this.lastActiveTime)
                : this.totalActiveTime;
            
            this.addEvent('time_tracking', {
                session_time_seconds: Math.round(sessionTime / 1000),
                active_time_seconds: Math.round(activeTime / 1000),
                timestamp: new Date().toISOString()
            });
        }, 60000); // 1分ごと
    }
    
    /**
     * コンバージョン追跡を初期化
     */
    initConversionTracking() {
        // 商品表示の追跡（Intersection Observer）
        if ('IntersectionObserver' in window) {
            const productObserver = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const productBox = entry.target;
                        const productId = productBox.dataset.productId;
                        
                        this.addEvent('product_impression', {
                            product_id: productId,
                            viewport_percent: Math.round(entry.intersectionRatio * 100),
                            timestamp: new Date().toISOString()
                        });
                        
                        // Google Analytics 4への送信
                        if (typeof gtag !== 'undefined') {
                            gtag('event', 'view_item', {
                                currency: 'JPY',
                                value: productBox.dataset.price || 0,
                                items: [{
                                    item_id: productId,
                                    item_name: productBox.querySelector('.product-name, .card-content h3')?.textContent,
                                    item_category: productBox.dataset.category || 'equipment'
                                }]
                            });
                        }
                        
                        // 一度表示されたら監視を停止
                        productObserver.unobserve(productBox);
                    }
                });
            }, {
                threshold: [0.5, 0.75, 1.0]
            });
            
            // 商品ボックスを監視
            document.querySelectorAll('.affiliate-product-box, .equipment-card').forEach(box => {
                productObserver.observe(box);
            });
        }
        
        // フォーム送信の追跡
        document.addEventListener('submit', (e) => {
            const form = e.target;
            const formType = form.dataset.formType || 'unknown';
            
            this.addEvent('form_submit', {
                form_type: formType,
                form_action: form.action,
                timestamp: new Date().toISOString()
            });
        });
    }
    
    /**
     * イベントを追加
     */
    addEvent(eventType, data) {
        this.events.push({
            event_type: eventType,
            session_id: this.sessionId,
            user_id: this.userId,
            url: window.location.href,
            user_agent: navigator.userAgent,
            ...data
        });
        
        // イベントが100個を超えたら送信
        if (this.events.length >= 100) {
            this.sendEvents();
        }
    }
    
    /**
     * イベントデータを送信
     */
    sendEvents() {
        if (this.events.length === 0) return;
        
        const eventsToSend = [...this.events];
        this.events = [];
        
        // 送信処理（実際の実装では適切なエンドポイントに送信）
        if (navigator.sendBeacon) {
            // ページ離脱時も確実に送信
            navigator.sendBeacon('/api/analytics', JSON.stringify({
                events: eventsToSend,
                timestamp: new Date().toISOString()
            }));
        } else {
            // フォールバック
            fetch('/api/analytics', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    events: eventsToSend,
                    timestamp: new Date().toISOString()
                })
            }).catch(err => {
                console.warn('Analytics sending failed:', err);
                // 失敗したイベントを元に戻す
                this.events.unshift(...eventsToSend);
            });
        }
        
        console.log('📊 Analytics Events Sent:', eventsToSend.length);
    }
    
    /**
     * デバイス情報を取得
     */
    getDeviceInfo() {
        return {
            is_mobile: /Mobile|Android|iPhone|iPad/.test(navigator.userAgent),
            is_tablet: /iPad|Android.*Mobile/.test(navigator.userAgent),
            platform: navigator.platform,
            language: navigator.language
        };
    }
    
    /**
     * 要素の位置を取得（ページ内での順序）
     */
    getElementPosition(element) {
        const allSimilarElements = document.querySelectorAll(element.tagName + '.' + element.className.split(' ')[0]);
        return Array.from(allSimilarElements).indexOf(element) + 1;
    }
    
    /**
     * 親セクションを取得
     */
    getParentSection(element) {
        const section = element.closest('section');
        return section ? section.className.split(' ')[0] : 'unknown';
    }
    
    /**
     * スロットル関数
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
    
    /**
     * A/Bテスト用の機能
     */
    getABTestVariant(testName) {
        const stored = localStorage.getItem(`ab_test_${testName}`);
        if (stored) return stored;
        
        const variants = ['A', 'B'];
        const variant = variants[Math.floor(Math.random() * variants.length)];
        localStorage.setItem(`ab_test_${testName}`, variant);
        
        this.addEvent('ab_test_assignment', {
            test_name: testName,
            variant: variant,
            timestamp: new Date().toISOString()
        });
        
        return variant;
    }
    
    /**
     * コンバージョンを手動追跡
     */
    trackConversion(conversionType, value = 0, productId = null) {
        this.addEvent('conversion', {
            conversion_type: conversionType,
            value: value,
            product_id: productId,
            timestamp: new Date().toISOString()
        });
        
        // Google Analytics 4への送信
        if (typeof gtag !== 'undefined') {
            gtag('event', 'purchase', {
                transaction_id: this.sessionId + '_' + Date.now(),
                value: value,
                currency: 'JPY',
                items: productId ? [{
                    item_id: productId,
                    item_name: conversionType,
                    quantity: 1,
                    price: value
                }] : []
            });
        }
    }
}

// グローバルインスタンスを作成
window.affiliateTracker = new AffiliateTracker();

// 手動追跡用のヘルパー関数をグローバルに公開
window.trackConversion = function(type, value, productId) {
    window.affiliateTracker.trackConversion(type, value, productId);
};

window.getABTestVariant = function(testName) {
    return window.affiliateTracker.getABTestVariant(testName);
};

// デバッグ用
if (window.location.search.includes('debug=true')) {
    window.affiliateTracker.debug = true;
    console.log('🔍 Affiliate Tracking Debug Mode Enabled');
}