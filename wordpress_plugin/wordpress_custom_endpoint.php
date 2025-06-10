
// functions.phpに追加するコード
add_action('rest_api_init', function () {
    register_rest_route('mountain-blog/v1', '/bulk-create', array(
        'methods' => 'POST',
        'callback' => 'mountain_blog_bulk_create',
        'permission_callback' => function() {
            return current_user_can('edit_posts');
        }
    ));
});

function mountain_blog_bulk_create($request) {
    $articles = $request->get_json_params();
    $created_posts = array();
    
    foreach ($articles as $article) {
        $post_data = array(
            'post_title' => wp_strip_all_tags($article['title']),
            'post_content' => $article['content'],
            'post_excerpt' => wp_strip_all_tags($article['excerpt']),
            'post_status' => 'draft',
            'post_type' => 'post',
            'tags_input' => $article['tags'],
            'post_category' => array(get_cat_ID('エリア別'))
        );
        
        $post_id = wp_insert_post($post_data);
        
        if ($post_id && !is_wp_error($post_id)) {
            $created_posts[] = array(
                'post_id' => $post_id,
                'title' => $article['title'],
                'status' => 'created'
            );
        }
    }
    
    return rest_ensure_response($created_posts);
}
