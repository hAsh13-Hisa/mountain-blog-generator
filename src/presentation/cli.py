#!/usr/bin/env python3
"""
CLI インターフェース
"""
import sys
import click
from typing import Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import track
import time

from config.settings import get_settings
from config.logging_config import initialize_logging
from src.application.services import MountainArticleService
from src.infrastructure.repositories import RepositoryFactory
from src.domain.entities import DifficultyLevel


# Rich console for beautiful output
console = Console()


@click.group()
@click.version_option(version="1.0.0")
def cli():
    """🏔️ 低山旅行自動記事作成アプリ
    
    日本全国の低山・中級山の登山記事を自動生成し、WordPressに投稿します。
    """
    # ログシステム初期化
    initialize_logging()


@cli.command()
def info():
    """アプリケーション情報を表示"""
    settings = get_settings()
    
    console.print(Panel.fit(
        "[bold blue]🏔️ 低山旅行自動記事作成アプリ[/bold blue]\n\n"
        f"WordPress URL: [green]{settings.WP_URL}[/green]\n"
        f"Claude Model: [yellow]{settings.CLAUDE_MODEL}[/yellow]\n"
        f"Log Level: [cyan]{settings.LOG_LEVEL}[/cyan]\n"
        f"Debug Mode: [magenta]{settings.DEBUG}[/magenta]",
        title="📋 Application Info"
    ))


@cli.command()
@click.option('--region', help='地域で絞り込み（例: 関東、関西）')
@click.option('--difficulty', type=click.Choice(['初級', '初級-中級', '中級', '上級']), help='難易度で絞り込み')
@click.option('--prefecture', help='都道府県で絞り込み（例: 東京都、神奈川県）')
@click.option('--keyword', help='キーワード検索')
def list_mountains(region: Optional[str], difficulty: Optional[str], prefecture: Optional[str], keyword: Optional[str]):
    """山一覧を表示"""
    try:
        mountain_repo = RepositoryFactory.get_mountain_repository()
        
        # フィルタリング
        mountains = mountain_repo.get_all()
        
        if region:
            mountains = [m for m in mountains if m.region == region]
        
        if difficulty:
            diff_level = DifficultyLevel(difficulty)
            mountains = [m for m in mountains if m.difficulty.level == diff_level]
        
        if prefecture:
            mountains = [m for m in mountains if prefecture in m.prefecture]
        
        if keyword:
            mountains = mountain_repo.search_by_keyword(keyword)
        
        if not mountains:
            console.print("[yellow]条件に一致する山が見つかりませんでした。[/yellow]")
            return
        
        # テーブル作成
        table = Table(title=f"🗻 山一覧 ({len(mountains)}件)")
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("山名", style="bold green")
        table.add_column("都道府県", style="blue")
        table.add_column("標高", style="yellow", justify="right")
        table.add_column("難易度", style="magenta")
        table.add_column("特徴", style="white")
        
        for mountain in mountains:
            features_str = ", ".join(mountain.features[:3])
            if len(mountain.features) > 3:
                features_str += "..."
            
            table.add_row(
                mountain.id,
                mountain.name,
                mountain.prefecture,
                f"{mountain.elevation}m",
                mountain.difficulty.level.value,
                features_str
            )
        
        console.print(table)
        
    except Exception as e:
        console.print(f"[red]エラー: {str(e)}[/red]")


@cli.command()
@click.argument('mountain_id')
def show_mountain(mountain_id: str):
    """山の詳細情報を表示"""
    try:
        mountain_repo = RepositoryFactory.get_mountain_repository()
        mountain = mountain_repo.get_by_id(mountain_id)
        
        if not mountain:
            console.print(f"[red]山が見つかりません: {mountain_id}[/red]")
            return
        
        # 詳細情報パネル
        info_text = f"""[bold green]{mountain.name}[/bold green] ({mountain.name_en})

📍 [blue]所在地:[/blue] {mountain.prefecture} ({mountain.region})
⛰️  [yellow]標高:[/yellow] {mountain.elevation}m
🎯 [magenta]難易度:[/magenta] {mountain.difficulty.level.value}
⏱️  [cyan]登山時間:[/cyan] {mountain.difficulty.hiking_time}
📏 [white]距離:[/white] {mountain.difficulty.distance}
📈 [green]標高差:[/green] {mountain.difficulty.elevation_gain}

🚉 [blue]アクセス:[/blue] {mountain.location.nearest_station}から{mountain.location.access_time}

✨ [yellow]特徴:[/yellow]
{chr(10).join(f"  • {feature}" for feature in mountain.features)}
"""
        
        if mountain.article_themes:
            info_text += f"""
📝 [cyan]記事テーマ案:[/cyan]
{chr(10).join(f"  • {theme}" for theme in mountain.article_themes)}
"""
        
        console.print(Panel(info_text, title=f"🗻 {mountain.name}", border_style="green"))
        
    except Exception as e:
        console.print(f"[red]エラー: {str(e)}[/red]")


@cli.command()
@click.argument('mountain_id')
@click.option('--theme', help='記事テーマ（指定しない場合は自動選択）')
@click.option('--publish', is_flag=True, help='生成後すぐにWordPressに公開')
@click.option('--length', default=2000, help='目標文字数（デフォルト: 2000文字）')
def generate_article(mountain_id: str, theme: Optional[str], publish: bool, length: int):
    """山の記事を生成"""
    try:
        # 山の存在確認
        mountain_repo = RepositoryFactory.get_mountain_repository()
        mountain = mountain_repo.get_by_id(mountain_id)
        
        if not mountain:
            console.print(f"[red]山が見つかりません: {mountain_id}[/red]")
            return
        
        console.print(f"[bold green]🗻 {mountain.name}の記事を生成中...[/bold green]")
        
        if theme:
            console.print(f"📝 テーマ: {theme}")
        
        # プログレスバーで処理状況を表示
        service = MountainArticleService()
        
        with console.status("[bold green]記事を生成しています..."):
            result = service.create_and_publish_article(
                mountain_id=mountain_id,
                theme=theme,
                publish=publish
            )
        
        if result.success and result.article:
            article = result.article
            
            # 生成結果表示
            console.print("✅ [bold green]記事生成完了![/bold green]")
            
            result_panel = f"""📰 [bold blue]タイトル:[/bold blue] {article.content.title}

📊 [yellow]統計:[/yellow]
  • 文字数: {article.content.get_word_count():,}文字
  • 生成時間: {result.generation_time:.2f}秒
  • タグ数: {len(article.content.tags)}個
  • 商品数: {len(article.content.affiliate_products)}個
  • 宿泊施設数: {len(article.content.affiliate_hotels)}個

🏷️ [cyan]タグ:[/cyan] {', '.join(article.content.tags)}
"""
            
            if article.wordpress_id:
                result_panel += f"\n📝 [green]WordPress投稿ID:[/green] {article.wordpress_id}"
            
            console.print(Panel(result_panel, title="📊 生成結果", border_style="blue"))
            
            # 抜粋表示
            if article.content.excerpt:
                console.print(Panel(
                    article.content.excerpt,
                    title="📋 記事の要約",
                    border_style="yellow"
                ))
        
        else:
            console.print("[red]❌ 記事生成に失敗しました[/red]")
            if result.error_message:
                console.print(f"[red]エラー: {result.error_message}[/red]")
        
    except Exception as e:
        console.print(f"[red]エラー: {str(e)}[/red]")


@cli.command()
@click.option('--count', default=5, help='表示する山の数（デフォルト: 5）')
def suggestions(count: int):
    """記事作成におすすめの山を表示"""
    try:
        console.print("[bold blue]🎯 記事作成におすすめの山[/bold blue]")
        
        service = MountainArticleService()
        
        with console.status("[bold green]おすすめの山を検索中..."):
            mountains = service.get_mountain_suggestions(count)
        
        if not mountains:
            console.print("[yellow]おすすめの山が見つかりませんでした。[/yellow]")
            return
        
        table = Table(title=f"💡 おすすめの山 ({len(mountains)}件)")
        table.add_column("No", style="cyan", no_wrap=True)
        table.add_column("山名", style="bold green")
        table.add_column("都道府県", style="blue")
        table.add_column("難易度", style="magenta")
        table.add_column("おすすめ理由", style="yellow")
        
        for i, mountain in enumerate(mountains, 1):
            reason = []
            if mountain.is_beginner_friendly():
                reason.append("初心者向け")
            if mountain.has_cable_car():
                reason.append("ケーブルカーあり")
            if mountain.elevation < 1000:
                reason.append("低山")
            if not reason:
                reason.append("バランス良い")
            
            table.add_row(
                str(i),
                mountain.name,
                mountain.prefecture,
                mountain.difficulty.level.value,
                ", ".join(reason)
            )
        
        console.print(table)
        
        console.print("\n💡 [cyan]Tip:[/cyan] 記事を生成するには:")
        console.print("   [bold]mountain-blog generate-article [mountain_id][/bold]")
        
    except Exception as e:
        console.print(f"[red]エラー: {str(e)}[/red]")


@cli.command()
def stats():
    """山データの統計情報を表示"""
    try:
        mountain_repo = RepositoryFactory.get_mountain_repository()
        
        with console.status("[bold green]統計情報を計算中..."):
            stats_data = mountain_repo.get_statistics()
        
        if not stats_data:
            console.print("[yellow]統計データが取得できませんでした。[/yellow]")
            return
        
        # 基本統計
        console.print(Panel.fit(
            f"[bold green]総山数:[/bold green] {stats_data['total_mountains']}山\n"
            f"[bold yellow]標高範囲:[/bold yellow] {stats_data['elevation_stats']['min']}m - {stats_data['elevation_stats']['max']}m\n"
            f"[bold cyan]平均標高:[/bold cyan] {stats_data['elevation_stats']['average']}m\n"
            f"[bold magenta]初心者向け:[/bold magenta] {stats_data['beginner_friendly_count']}山\n"
            f"[bold blue]ケーブルカーあり:[/bold blue] {stats_data['cable_car_count']}山",
            title="📊 基本統計"
        ))
        
        # 地域別統計
        region_table = Table(title="🗾 地域別統計")
        region_table.add_column("地域", style="cyan")
        region_table.add_column("山数", style="yellow", justify="right")
        region_table.add_column("割合", style="green", justify="right")
        
        total = stats_data['total_mountains']
        for region, count in stats_data['regions'].items():
            percentage = (count / total) * 100 if total > 0 else 0
            region_table.add_row(region, str(count), f"{percentage:.1f}%")
        
        console.print(region_table)
        
        # 難易度別統計
        difficulty_table = Table(title="🎯 難易度別統計")
        difficulty_table.add_column("難易度", style="magenta")
        difficulty_table.add_column("山数", style="yellow", justify="right")
        difficulty_table.add_column("割合", style="green", justify="right")
        
        for difficulty, count in stats_data['difficulties'].items():
            percentage = (count / total) * 100 if total > 0 else 0
            difficulty_table.add_row(difficulty, str(count), f"{percentage:.1f}%")
        
        console.print(difficulty_table)
        
    except Exception as e:
        console.print(f"[red]エラー: {str(e)}[/red]")


@cli.command()
@click.option('--tag', multiple=True, help='検索タグ（複数指定可能）')
def search_by_tags(tag):
    """タグで山を検索"""
    try:
        if not tag:
            console.print("[yellow]検索タグを指定してください。[/yellow]")
            console.print("例: --tag 初心者向け --tag ケーブルカー")
            return
        
        mountain_repo = RepositoryFactory.get_mountain_repository()
        
        with console.status(f"[bold green]タグで検索中: {', '.join(tag)}"):
            mountains = mountain_repo.search_by_tags(list(tag))
        
        if not mountains:
            console.print(f"[yellow]タグ '{', '.join(tag)}' に一致する山が見つかりませんでした。[/yellow]")
            return
        
        console.print(f"[bold green]🔍 タグ検索結果: {', '.join(tag)}[/bold green]")
        
        table = Table(title=f"検索結果 ({len(mountains)}件)")
        table.add_column("山名", style="bold green")
        table.add_column("都道府県", style="blue")
        table.add_column("標高", style="yellow", justify="right")
        table.add_column("難易度", style="magenta")
        
        for mountain in mountains:
            table.add_row(
                mountain.name,
                mountain.prefecture,
                f"{mountain.elevation}m",
                mountain.difficulty.level.value
            )
        
        console.print(table)
        
    except Exception as e:
        console.print(f"[red]エラー: {str(e)}[/red]")


def main():
    """メイン関数"""
    try:
        cli()
    except KeyboardInterrupt:
        console.print("\n[yellow]処理が中断されました。[/yellow]")
        sys.exit(1)
    except Exception as e:
        console.print(f"\n[red]予期しないエラーが発生しました: {str(e)}[/red]")
        sys.exit(1)


if __name__ == "__main__":
    main()