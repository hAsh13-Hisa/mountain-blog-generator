// 11ty (Eleventy) 設定ファイル
module.exports = function(eleventyConfig) {
  // アフィリエイトリンク処理
  eleventyConfig.addShortcode("rakutenProduct", function(product) {
    return `
      <div class="product-card">
        <a href="${product.affiliateUrl}" target="_blank" rel="noopener">
          <img src="${product.imageUrl}" alt="${product.name}" loading="lazy">
          <h3>${product.name}</h3>
        </a>
      </div>
    `;
  });

  // 記事レイアウト
  eleventyConfig.addLayoutAlias('article', 'layouts/article.njk');
  
  // 静的ファイルコピー
  eleventyConfig.addPassthroughCopy("images");
  eleventyConfig.addPassthroughCopy("css");
  
  return {
    dir: {
      input: "src",
      output: "dist"
    }
  };
};