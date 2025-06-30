<?php
/**
 * ロリポップサーバー用 PHP動的サイト
 * 分類・タグ・検索機能付き
 */

// データファイル読み込み
$mountains_json = file_get_contents('data/mountains.json');
$articles_json = file_get_contents('data/articles.json');
$mountains = json_decode($mountains_json, true);
$articles = json_decode($articles_json, true);

// URLパラメータ取得
$page_type = $_GET['page'] ?? 'home';
$search_query = $_GET['q'] ?? '';
$tag = $_GET['tag'] ?? '';
$region = $_GET['region'] ?? '';
$difficulty = $_GET['difficulty'] ?? '';

// 検索・フィルタリング関数
function filterArticles($articles, $query = '', $tag = '', $region = '', $difficulty = '') {
    return array_filter($articles, function($article) use ($query, $tag, $region, $difficulty) {
        // キーワード検索
        if ($query && !stripos($article['title'] . $article['content'], $query)) {
            return false;
        }
        // タグフィルタ
        if ($tag && !in_array($tag, $article['tags'])) {
            return false;
        }
        // 地域フィルタ
        if ($region && $article['region'] !== $region) {
            return false;
        }
        // 難易度フィルタ
        if ($difficulty && $article['difficulty'] !== $difficulty) {
            return false;
        }
        return true;
    });
}

// フィルタリング実行
$filtered_articles = filterArticles($articles, $search_query, $tag, $region, $difficulty);

?>
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>日本の低山ガイド - 標高400m以下の登山情報</title>
    <link rel="stylesheet" href="/css/style.css">
    <script src="https://unpkg.com/htmx.org@1.9.10"></script>
</head>
<body>
    <header>
        <h1>日本の低山ガイド</h1>
        <nav>
            <a href="/">ホーム</a>
            <a href="/?page=regions">地域別</a>
            <a href="/?page=difficulty">難易度別</a>
            <a href="/?page=tags">タグ一覧</a>
        </nav>
        
        <!-- 検索フォーム -->
        <form method="get" action="/" class="search-form">
            <input type="text" name="q" placeholder="山名・キーワードで検索" value="<?= htmlspecialchars($search_query) ?>">
            <button type="submit">検索</button>
        </form>
    </header>
    
    <main>
        <?php if ($page_type === 'home'): ?>
            <!-- トップページ -->
            <section class="hero">
                <h2>初心者・家族向けの低山情報サイト</h2>
                <p>標高400m以下、登山道が整備された安全な山々をご紹介</p>
            </section>
            
            <!-- フィルタ -->
            <aside class="filters">
                <h3>絞り込み</h3>
                
                <!-- 地域別 -->
                <div class="filter-group">
                    <h4>地域</h4>
                    <select name="region" onchange="window.location.href='/?region=' + this.value">
                        <option value="">すべて</option>
                        <option value="北海道" <?= $region === '北海道' ? 'selected' : '' ?>>北海道</option>
                        <option value="東北" <?= $region === '東北' ? 'selected' : '' ?>>東北</option>
                        <option value="関東" <?= $region === '関東' ? 'selected' : '' ?>>関東</option>
                        <option value="中部" <?= $region === '中部' ? 'selected' : '' ?>>中部</option>
                        <option value="関西" <?= $region === '関西' ? 'selected' : '' ?>>関西</option>
                        <option value="四国" <?= $region === '四国' ? 'selected' : '' ?>>四国</option>
                        <option value="九州" <?= $region === '九州' ? 'selected' : '' ?>>九州</option>
                    </select>
                </div>
                
                <!-- 難易度別 -->
                <div class="filter-group">
                    <h4>難易度</h4>
                    <select name="difficulty" onchange="window.location.href='/?difficulty=' + this.value">
                        <option value="">すべて</option>
                        <option value="初級" <?= $difficulty === '初級' ? 'selected' : '' ?>>初級</option>
                        <option value="初級-中級" <?= $difficulty === '初級-中級' ? 'selected' : '' ?>>初級-中級</option>
                    </select>
                </div>
                
                <!-- タグクラウド -->
                <div class="filter-group">
                    <h4>人気のタグ</h4>
                    <div class="tag-cloud">
                        <a href="/?tag=夜景" class="tag">夜景</a>
                        <a href="/?tag=神社・寺" class="tag">神社・寺</a>
                        <a href="/?tag=桜の名所" class="tag">桜の名所</a>
                        <a href="/?tag=ロープウェイ" class="tag">ロープウェイ</a>
                        <a href="/?tag=家族向け" class="tag">家族向け</a>
                        <a href="/?tag=富士山展望" class="tag">富士山展望</a>
                    </div>
                </div>
            </aside>
            
            <!-- 記事一覧 -->
            <section class="articles">
                <h3>
                    <?php
                    if ($search_query) echo "「{$search_query}」の検索結果";
                    elseif ($tag) echo "タグ「{$tag}」の記事";
                    elseif ($region) echo "地域「{$region}」の山";
                    elseif ($difficulty) echo "難易度「{$difficulty}」の山";
                    else echo "最新の記事";
                    ?>
                </h3>
                
                <div class="article-grid">
                    <?php foreach ($filtered_articles as $article): ?>
                    <article class="article-card">
                        <img src="<?= $article['featured_image'] ?>" alt="<?= $article['title'] ?>">
                        <h4><a href="/article.php?id=<?= $article['id'] ?>"><?= $article['title'] ?></a></h4>
                        <div class="article-meta">
                            <span class="region"><?= $article['region'] ?></span>
                            <span class="elevation"><?= $article['elevation'] ?>m</span>
                            <span class="difficulty"><?= $article['difficulty'] ?></span>
                        </div>
                        <div class="tags">
                            <?php foreach ($article['tags'] as $tag): ?>
                            <a href="/?tag=<?= urlencode($tag) ?>" class="tag-link">#<?= $tag ?></a>
                            <?php endforeach; ?>
                        </div>
                    </article>
                    <?php endforeach; ?>
                </div>
            </section>
            
        <?php elseif ($page_type === 'regions'): ?>
            <!-- 地域別ページ -->
            <h2>地域から探す</h2>
            <div class="region-grid">
                <?php
                $regions = ['北海道', '東北', '関東', '中部', '関西', '四国', '九州'];
                foreach ($regions as $r):
                    $count = count(array_filter($articles, fn($a) => $a['region'] === $r));
                ?>
                <div class="region-card">
                    <h3><a href="/?region=<?= $r ?>"><?= $r ?></a></h3>
                    <p><?= $count ?>件の山</p>
                </div>
                <?php endforeach; ?>
            </div>
            
        <?php elseif ($page_type === 'tags'): ?>
            <!-- タグ一覧ページ -->
            <h2>タグから探す</h2>
            <?php
            // すべてのタグを集計
            $all_tags = [];
            foreach ($articles as $article) {
                foreach ($article['tags'] as $tag) {
                    $all_tags[$tag] = ($all_tags[$tag] ?? 0) + 1;
                }
            }
            arsort($all_tags);
            ?>
            <div class="tag-list">
                <?php foreach ($all_tags as $tag => $count): ?>
                <div class="tag-item">
                    <a href="/?tag=<?= urlencode($tag) ?>"><?= $tag ?> (<?= $count ?>)</a>
                </div>
                <?php endforeach; ?>
            </div>
        <?php endif; ?>
    </main>
    
    <footer>
        <p>&copy; 2025 日本の低山ガイド</p>
    </footer>
    
    <script>
    // 検索のライブプレビュー（オプション）
    document.querySelector('input[name="q"]').addEventListener('input', function(e) {
        if (e.target.value.length > 2) {
            // AJAX検索実装可能
        }
    });
    </script>
</body>
</html>