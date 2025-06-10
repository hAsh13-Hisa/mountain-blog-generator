<?php
/**
 * Plugin Name: Mountain Blog Bulk Poster
 * Description: 大量記事投稿用のカスタムエンドポイント
 * Version: 1.0
 * Author: Mountain Blog Generator
 */

// セキュリティチェック
if (!defined('ABSPATH')) {
    exit;
}

class MountainBlogBulkPoster {
    
    public function __construct() {
        add_action('rest_api_init', array($this, 'register_endpoints'));
    }
    
    public function register_endpoints() {
        // 大量投稿エンドポイント
        register_rest_route('mountain-blog/v1', '/bulk-create', array(
            'methods' => 'POST',
            'callback' => array($this, 'bulk_create_posts'),
            'permission_callback' => array($this, 'check_permissions'),
            'args' => array(
                'articles' => array(
                    'required' => false,
                    'type' => 'array',
                ),
            ),
        ));
        
        // テストエンドポイント
        register_rest_route('mountain-blog/v1', '/test', array(
            'methods' => 'GET',
            'callback' => array($this, 'test_endpoint'),
            'permission_callback' => array($this, 'check_permissions'),
        ));
    }
    
    public function check_permissions() {
        return current_user_can('edit_posts');
    }
    
    public function test_endpoint($request) {
        return rest_ensure_response(array(
            'status' => 'success',
            'message' => 'Mountain Blog Bulk Poster エンドポイントが正常に動作しています',
            'user' => wp_get_current_user()->user_login,
            'timestamp' => current_time('mysql')
        ));
    }
    
    public function bulk_create_posts($request) {
        $articles = $request->get_json_params();
        
        if (empty($articles)) {
            return new WP_Error('no_articles', '記事データが提供されていません', array('status' => 400));
        }
        
        $created_posts = array();
        $errors = array();
        
        foreach ($articles as $index => $article) {
            try {
                // 必須フィールドのチェック
                if (empty($article['title']) || empty($article['content'])) {
                    $errors[] = array(
                        'index' => $index,
                        'error' => 'タイトルまたはコンテンツが空です'
                    );
                    continue;
                }
                
                // 投稿データを準備
                $post_data = array(
                    'post_title' => sanitize_text_field($article['title']),
                    'post_content' => wp_kses_post($article['content']),
                    'post_excerpt' => sanitize_textarea_field($article['excerpt'] ?? ''),
                    'post_status' => 'draft',
                    'post_type' => 'post',
                    'post_author' => get_current_user_id(),
                    'meta_input' => array(
                        'mountain_blog_generated' => true,
                        'mountain_blog_timestamp' => current_time('mysql')
                    )
                );
                
                // 投稿を作成
                $post_id = wp_insert_post($post_data);
                
                if (is_wp_error($post_id)) {
                    $errors[] = array(
                        'index' => $index,
                        'error' => $post_id->get_error_message()
                    );
                    continue;
                }
                
                // タグを設定
                if (!empty($article['tags']) && is_array($article['tags'])) {
                    wp_set_post_tags($post_id, $article['tags']);
                }
                
                // カテゴリを設定
                $category_id = get_cat_ID('エリア別');
                if ($category_id > 0) {
                    wp_set_post_categories($post_id, array($category_id));
                }
                
                $created_posts[] = array(
                    'post_id' => $post_id,
                    'title' => $article['title'],
                    'status' => 'created',
                    'edit_url' => admin_url("post.php?post={$post_id}&action=edit")
                );
                
            } catch (Exception $e) {
                $errors[] = array(
                    'index' => $index,
                    'error' => $e->getMessage()
                );
            }
        }
        
        $response = array(
            'success' => true,
            'created_count' => count($created_posts),
            'error_count' => count($errors),
            'created_posts' => $created_posts
        );
        
        if (!empty($errors)) {
            $response['errors'] = $errors;
        }
        
        return rest_ensure_response($response);
    }
}

// プラグインを初期化
new MountainBlogBulkPoster();

// 管理画面にメニューを追加
add_action('admin_menu', function() {
    add_options_page(
        'Mountain Blog Bulk Poster',
        'Mountain Blog',
        'manage_options',
        'mountain-blog-bulk-poster',
        function() {
            echo '<div class="wrap">';
            echo '<h1>Mountain Blog Bulk Poster</h1>';
            echo '<p>大量記事投稿用のREST APIエンドポイントが有効になりました。</p>';
            echo '<h3>利用可能なエンドポイント:</h3>';
            echo '<ul>';
            echo '<li><strong>テスト:</strong> <code>GET /wp-json/mountain-blog/v1/test</code></li>';
            echo '<li><strong>大量投稿:</strong> <code>POST /wp-json/mountain-blog/v1/bulk-create</code></li>';
            echo '</ul>';
            echo '<p>認証にはApplication Passwordsを使用してください。</p>';
            echo '</div>';
        }
    );
});
?>