/**
 * 💰 アフィリエイト追跡システム
 * 収益最大化のための包括的なトラッキング
 */

class AffiliateTracker {
    constructor() {
        this.config = {
            apiEndpoint: '/api/analytics',
            batchSize: 10,
            flushInterval: 30000, // 30秒
            cookieDomain: '.omasse.com',
            sessionTimeout: 30 * 60 * 1000, // 30分
            enableDebug: false
        };
        
        this.eventQueue = [];
        this.sessionData = {};
        this.userProfile = {};
        
        this.init();
    }

    init() {
        this.initSession();
        this.loadUserProfile();
        this.startPeriodicFlush();
        this.trackPageView();
        this.initEventListeners();
    }

    /**
     * セッション初期化
     */
    initSession() {
        const sessionId = this.getSessionId();
        this.sessionData = {
            sessionId: sessionId,
            startTime: Date.now(),
            pageViews: 0,
            events: [],
            referrer: document.referrer,
            userAgent: navigator.userAgent,
            screenResolution: `${screen.width}x${screen.height}`,
            deviceType: this.getDeviceType()
        };
        
        this.debug('Session initialized:', this.sessionData);
    }

    /**
     * ユーザープロファイル読み込み
     */
    loadUserProfile() {
        try {
            const saved = localStorage.getItem('mountainMaster_profile');
            this.userProfile = saved ? JSON.parse(saved) : {
                userId: this.generateUserId(),
                visitCount: 0,
                totalSpent: 0,
                favoriteCategories: [],
                lastVisit: null,
                priceRange: 'unknown', // budget, mid, premium
                experience: 'beginner' // beginner, intermediate, advanced
            };
            
            this.userProfile.visitCount++;
            this.userProfile.lastVisit = Date.now();
            this.saveUserProfile();
        } catch (e) {
            this.debug('Failed to load user profile:', e);
        }
    }

    /**
     * ページビュー追跡
     */
    trackPageView() {
        this.sessionData.pageViews++;
        
        const pageData = {
            type: 'page_view',
            timestamp: Date.now(),
            url: window.location.href,
            title: document.title,
            path: window.location.pathname,
            referrer: document.referrer,
            sessionId: this.sessionData.sessionId,
            userId: this.userProfile.userId,
            visitCount: this.userProfile.visitCount,
            timeOnPreviousPage: this.getTimeOnPreviousPage()
        };
        
        this.queueEvent(pageData);
        this.updateLastPageTime();
    }

    /**
     * アフィリエイトクリック追跡
     */
    trackClick(affiliateId, productName, price, category = 'unknown') {
        const clickData = {
            type: 'affiliate_click',
            timestamp: Date.now(),
            affiliateId: affiliateId,
            productName: productName,
            price: price,
            category: category,
            sessionId: this.sessionData.sessionId,
            userId: this.userProfile.userId,
            pageUrl: window.location.href,
            position: this.getClickPosition(event),
            deviceType: this.sessionData.deviceType
        };
        
        this.queueEvent(clickData);
        this.updateUserProfileFromClick(category, price);
        
        this.debug('Affiliate click tracked:', clickData);
    }

    /**
     * 商品表示追跡
     */
    trackProductView(productId, productName, price = null) {
        const viewData = {
            type: 'product_view',
            timestamp: Date.now(),
            productId: productId,
            productName: productName,
            price: price,
            sessionId: this.sessionData.sessionId,
            userId: this.userProfile.userId,
            pageUrl: window.location.href,
            viewDuration: null // 後で更新
        };
        
        this.queueEvent(viewData);
        
        // 商品表示時間の追跡開始
        this.startProductViewTimer(productId);
    }

    /**
     * CTAボタンクリック追跡
     */
    trackCTAClick(ctaData) {
        const clickData = {
            type: 'cta_click',
            timestamp: Date.now(),
            buttonText: ctaData.buttonText,
            buttonType: ctaData.buttonType,
            section: ctaData.section,
            url: ctaData.url,
            sessionId: this.sessionData.sessionId,
            userId: this.userProfile.userId,
            pageUrl: window.location.href
        };
        
        this.queueEvent(clickData);
    }

    /**
     * A/Bテスト参加追跡
     */
    trackABTest(testName, variant) {
        const testData = {
            type: 'ab_test',
            timestamp: Date.now(),
            testName: testName,
            variant: variant,
            sessionId: this.sessionData.sessionId,
            userId: this.userProfile.userId,
            pageUrl: window.location.href
        };
        
        this.queueEvent(testData);
    }

    /**
     * スクロール深度追跡
     */
    trackScrollDepth() {
        let maxScroll = 0;
        const trackPoints = [25, 50, 75, 90, 100];
        const tracked = new Set();
        
        const throttledScroll = this.throttle(() => {
            const scrollPercent = Math.round(
                ((window.scrollY + window.innerHeight) / document.documentElement.scrollHeight) * 100
            );
            
            maxScroll = Math.max(maxScroll, scrollPercent);
            
            trackPoints.forEach(point => {
                if (scrollPercent >= point && !tracked.has(point)) {
                    tracked.add(point);
                    
                    this.queueEvent({
                        type: 'scroll_depth',
                        timestamp: Date.now(),
                        depth: point,
                        sessionId: this.sessionData.sessionId,
                        userId: this.userProfile.userId,
                        pageUrl: window.location.href
                    });
                }
            });
        }, 1000);
        
        window.addEventListener('scroll', throttledScroll);
        
        // ページ離脱時に最大スクロール深度を記録
        window.addEventListener('beforeunload', () => {
            this.queueEvent({
                type: 'max_scroll_depth',
                timestamp: Date.now(),
                maxDepth: maxScroll,
                sessionId: this.sessionData.sessionId,
                userId: this.userProfile.userId,
                pageUrl: window.location.href
            });
            this.flush();
        });
    }

    /**
     * 検索追跡
     */
    trackSearch(query, results = null) {
        const searchData = {
            type: 'search',
            timestamp: Date.now(),
            query: query,
            results: results,
            sessionId: this.sessionData.sessionId,
            userId: this.userProfile.userId,
            pageUrl: window.location.href
        };
        
        this.queueEvent(searchData);
    }

    /**
     * フォーム送信追跡
     */
    trackFormSubmit(formName, formData = {}) {
        const submitData = {
            type: 'form_submit',
            timestamp: Date.now(),
            formName: formName,
            formData: formData,
            sessionId: this.sessionData.sessionId,
            userId: this.userProfile.userId,
            pageUrl: window.location.href
        };
        
        this.queueEvent(submitData);
    }

    /**
     * エラー追跡
     */
    trackError(error, context = '') {
        const errorData = {
            type: 'error',
            timestamp: Date.now(),
            message: error.message,
            stack: error.stack,
            context: context,
            sessionId: this.sessionData.sessionId,
            userId: this.userProfile.userId,
            pageUrl: window.location.href,
            userAgent: navigator.userAgent
        };
        
        this.queueEvent(errorData);
    }

    /**
     * コンバージョン追跡
     */
    trackConversion(conversionData) {
        const conversion = {
            type: 'conversion',
            timestamp: Date.now(),
            affiliateId: conversionData.affiliateId,
            productName: conversionData.productName,
            price: conversionData.price,
            category: conversionData.category,
            sessionId: this.sessionData.sessionId,
            userId: this.userProfile.userId,
            conversionValue: conversionData.value || conversionData.price,
            currency: conversionData.currency || 'JPY'
        };
        
        this.queueEvent(conversion);
        this.userProfile.totalSpent += conversionData.price || 0;
        this.saveUserProfile();
    }

    /**
     * イベントリスナー初期化
     */
    initEventListeners() {
        // スクロール深度追跡
        this.trackScrollDepth();
        
        // 外部リンククリック追跡
        document.addEventListener('click', (e) => {
            const link = e.target.closest('a');
            if (link && this.isExternalLink(link.href)) {
                this.queueEvent({
                    type: 'external_link_click',
                    timestamp: Date.now(),
                    url: link.href,
                    text: link.textContent.trim(),
                    sessionId: this.sessionData.sessionId,
                    userId: this.userProfile.userId,
                    pageUrl: window.location.href
                });
            }
        });
        
        // エラー追跡
        window.addEventListener('error', (e) => {
            this.trackError(e.error || new Error(e.message), 'window_error');
        });
        
        // Promise拒否追跡
        window.addEventListener('unhandledrejection', (e) => {
            this.trackError(new Error(e.reason), 'unhandled_promise_rejection');
        });
        
        // ページ離脱時の処理
        window.addEventListener('beforeunload', () => {
            this.queueEvent({
                type: 'page_unload',
                timestamp: Date.now(),
                timeOnPage: Date.now() - this.getLastPageTime(),
                sessionId: this.sessionData.sessionId,
                userId: this.userProfile.userId,
                pageUrl: window.location.href
            });
            this.flush();
        });
        
        // ビジビリティ変更追跡
        document.addEventListener('visibilitychange', () => {
            this.queueEvent({
                type: 'visibility_change',
                timestamp: Date.now(),
                visible: !document.hidden,
                sessionId: this.sessionData.sessionId,
                userId: this.userProfile.userId,
                pageUrl: window.location.href
            });
        });
    }

    /**
     * イベントをキューに追加
     */
    queueEvent(eventData) {
        this.eventQueue.push(eventData);
        this.sessionData.events.push(eventData);
        
        // バッチサイズに達したら送信
        if (this.eventQueue.length >= this.config.batchSize) {
            this.flush();
        }
        
        this.debug('Event queued:', eventData);
    }

    /**
     * キューのイベントを送信
     */
    async flush() {
        if (this.eventQueue.length === 0) return;
        
        const events = [...this.eventQueue];
        this.eventQueue = [];
        
        try {
            const response = await fetch(this.config.apiEndpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    events: events,
                    session: this.sessionData,
                    user: this.userProfile
                }),
                keepalive: true
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            this.debug('Events sent successfully:', events.length);
        } catch (error) {
            this.debug('Failed to send events:', error);
            // 失敗したイベントを再キューに追加
            this.eventQueue.unshift(...events);
        }
    }

    /**
     * 定期的なフラッシュ開始
     */
    startPeriodicFlush() {
        setInterval(() => {
            this.flush();
        }, this.config.flushInterval);
    }

    /**
     * ユーティリティメソッド
     */
    
    getSessionId() {
        let sessionId = sessionStorage.getItem('mountainMaster_sessionId');
        if (!sessionId) {
            sessionId = 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
            sessionStorage.setItem('mountainMaster_sessionId', sessionId);
        }
        return sessionId;
    }

    generateUserId() {
        return 'user_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }

    getDeviceType() {
        const width = window.screen.width;
        if (width < 768) return 'mobile';
        if (width < 1024) return 'tablet';
        return 'desktop';
    }

    isExternalLink(url) {
        try {
            const urlObj = new URL(url, window.location.origin);
            return urlObj.hostname !== window.location.hostname;
        } catch {
            return false;
        }
    }

    getClickPosition(event) {
        if (!event) return null;
        return {
            x: event.clientX,
            y: event.clientY,
            pageX: event.pageX,
            pageY: event.pageY
        };
    }

    updateUserProfileFromClick(category, price) {
        // カテゴリ嗜好を更新
        if (!this.userProfile.favoriteCategories.includes(category)) {
            this.userProfile.favoriteCategories.push(category);
        }
        
        // 価格帯を更新
        if (price) {
            if (price < 5000) this.userProfile.priceRange = 'budget';
            else if (price < 15000) this.userProfile.priceRange = 'mid';
            else this.userProfile.priceRange = 'premium';
        }
        
        this.saveUserProfile();
    }

    saveUserProfile() {
        try {
            localStorage.setItem('mountainMaster_profile', JSON.stringify(this.userProfile));
        } catch (e) {
            this.debug('Failed to save user profile:', e);
        }
    }

    startProductViewTimer(productId) {
        const startTime = Date.now();
        
        // 商品要素の可視性を監視
        const productElement = document.querySelector(`[data-product-id="${productId}"]`);
        if (!productElement) return;
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (!entry.isIntersecting) {
                    const viewDuration = Date.now() - startTime;
                    
                    this.queueEvent({
                        type: 'product_view_end',
                        timestamp: Date.now(),
                        productId: productId,
                        viewDuration: viewDuration,
                        sessionId: this.sessionData.sessionId,
                        userId: this.userProfile.userId,
                        pageUrl: window.location.href
                    });
                    
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.1 });
        
        observer.observe(productElement);
    }

    getTimeOnPreviousPage() {
        const lastPageTime = this.getLastPageTime();
        return lastPageTime ? Date.now() - lastPageTime : 0;
    }

    getLastPageTime() {
        return parseInt(sessionStorage.getItem('mountainMaster_lastPageTime') || '0');
    }

    updateLastPageTime() {
        sessionStorage.setItem('mountainMaster_lastPageTime', Date.now().toString());
    }

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

    debug(...args) {
        if (this.config.enableDebug) {
            console.log('[AffiliateTracker]', ...args);
        }
    }

    /**
     * 公開API
     */
    
    // 設定を更新
    updateConfig(newConfig) {
        this.config = { ...this.config, ...newConfig };
    }
    
    // デバッグモードを切り替え
    setDebugMode(enabled) {
        this.config.enableDebug = enabled;
    }
    
    // 現在のセッションデータを取得
    getSessionData() {
        return { ...this.sessionData };
    }
    
    // 現在のユーザープロファイルを取得
    getUserProfile() {
        return { ...this.userProfile };
    }
    
    // 手動でイベントを送信
    sendEvent(eventData) {
        this.queueEvent(eventData);
    }
    
    // 統計情報を取得
    getStats() {
        return {
            sessionId: this.sessionData.sessionId,
            pageViews: this.sessionData.pageViews,
            eventsCount: this.sessionData.events.length,
            queueLength: this.eventQueue.length,
            visitCount: this.userProfile.visitCount,
            totalSpent: this.userProfile.totalSpent
        };
    }
}

// グローバルインスタンス作成
const affiliateTracker = new AffiliateTracker();

// グローバルオブジェクトとして公開
window.AffiliateTracker = affiliateTracker;

// デバッグ用: 開発環境でのみデバッグモードを有効化
if (window.location.hostname === 'localhost' || window.location.hostname.includes('dev')) {
    affiliateTracker.setDebugMode(true);
}

export default AffiliateTracker;