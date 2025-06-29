<?php
/**
 * Plugin Name: Auto Featured Image Activation
 * Description: インポート後に自動的にFeatured Image from URLを有効化
 * Version: 1.0
 * Author: Mountain Blog Generator
 */

// セキュリティチェック
if (!defined('ABSPATH')) {
    exit;
}

class AutoFeaturedImageActivation {
    
    public function __construct() {
        add_action('wp_insert_post', array($this, 'activate_featured_image'), 10, 3);
        add_action('post_updated', array($this, 'activate_featured_image_update'), 10, 3);
    }
    
    /**
     * 新しい投稿が追加された時に実行
     */
    public function activate_featured_image($post_id, $post, $update) {
        // インポート時のみ実行（手動投稿は除く）
        if (wp_is_post_revision($post_id) || wp_is_post_autosave($post_id)) {
            return;
        }
        
        $this->process_featured_image($post_id);
    }
    
    /**
     * 投稿が更新された時に実行
     */
    public function activate_featured_image_update($post_id, $post_after, $post_before) {
        $this->process_featured_image($post_id);
    }
    
    /**
     * Featured Image from URLの処理
     */
    private function process_featured_image($post_id) {
        // fifu_image_urlメタフィールドを確認
        $image_url = get_post_meta($post_id, 'fifu_image_url', true);
        
        if (!empty($image_url)) {
            // _thumbnail_idを設定してアイキャッチ画像として認識させる
            update_post_meta($post_id, '_thumbnail_id', 'fifu');
            
            // Featured Image from URLプラグインが有効な場合の追加処理
            if (function_exists('fifu_activate')) {
                // プラグイン固有の処理を実行
                update_post_meta($post_id, 'fifu_image_url', $image_url);
                
                // alt属性があれば設定
                $image_alt = get_post_meta($post_id, 'fifu_image_alt', true);
                if (!empty($image_alt)) {
                    update_post_meta($post_id, 'fifu_image_alt', $image_alt);
                }
                
                // ログ記録
                error_log("Auto Featured Image: Activated for post {$post_id} with URL: {$image_url}");
            }
        }
    }
}

// プラグインを初期化
new AutoFeaturedImageActivation();

/**
 * 一括処理用の関数（必要に応じて使用）
 */
function batch_activate_featured_images() {
    $posts = get_posts(array(
        'post_type' => 'post',
        'numberposts' => -1,
        'meta_query' => array(
            array(
                'key' => 'fifu_image_url',
                'compare' => 'EXISTS'
            ),
            array(
                'key' => '_thumbnail_id',
                'compare' => 'NOT EXISTS'
            )
        )
    ));
    
    foreach ($posts as $post) {
        $image_url = get_post_meta($post->ID, 'fifu_image_url', true);
        if (!empty($image_url)) {
            update_post_meta($post->ID, '_thumbnail_id', 'fifu');
            error_log("Batch process: Activated featured image for post {$post->ID}");
        }
    }
    
    return count($posts);
}

// 管理画面でのテスト実行（開発用）
if (isset($_GET['batch_activate_images']) && current_user_can('manage_options')) {
    $count = batch_activate_featured_images();
    wp_die("処理完了: {$count}件の投稿を処理しました。");
}
?>