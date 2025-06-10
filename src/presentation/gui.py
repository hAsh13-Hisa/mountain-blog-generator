#!/usr/bin/env python3
"""
GUI アプリケーション - tkinter版
"""
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import queue
import locale
import sys
import os
from typing import Optional, List
from PIL import Image, ImageTk
import requests
from io import BytesIO
import charset_normalizer
import unicodedata

from config.settings import get_settings
from config.logging_config import initialize_logging, get_logger
from src.application.services import MountainArticleService
from src.infrastructure.repositories import RepositoryFactory
from src.domain.entities import Mountain, Article, GenerationRequest


class MountainBlogGUI:
    """低山旅行記事作成GUI"""
    
    def __init__(self):
        # UTF-8エンコーディングとロケールを設定
        self._setup_encoding()
        
        # 日本語フォント対応を初期化
        self._japanese_supported = self._check_japanese_support()
        
        self.settings = get_settings()
        self.logger = get_logger("gui")
        self.mountain_service = MountainArticleService()
        self.mountain_repo = RepositoryFactory.get_mountain_repository()
        
        # GUI状態管理
        self.selected_mountain: Optional[Mountain] = None
        self.generated_article: Optional[Article] = None
        self.result_queue = queue.Queue()
        
        # メインウィンドウ作成
        self.setup_main_window()
        self.setup_widgets()
        self.load_mountain_data()
    
    def _setup_encoding(self):
        """エンコーディング設定"""
        # 環境変数でPythonエンコーディングを強制
        os.environ['PYTHONIOENCODING'] = 'utf-8'
        
        # ロケール設定を試行
        locale_candidates = [
            'ja_JP.UTF-8',
            'en_US.UTF-8', 
            'C.UTF-8',
            ''  # システムデフォルト
        ]
        
        for loc in locale_candidates:
            try:
                locale.setlocale(locale.LC_ALL, loc)
                break
            except locale.Error:
                continue
    
    def _check_japanese_support(self):
        """日本語サポートをチェック"""
        try:
            # 日本語文字をエンコード/デコードできるかテスト
            test_text = "高尾山"
            test_text.encode('utf-8').decode('utf-8')
            return True
        except UnicodeError:
            return False
    
    def _normalize_japanese_text(self, text):
        """日本語テキストを正規化"""
        if not text:
            return text
        
        try:
            # Unicode正規化 (NFCで統一)
            normalized = unicodedata.normalize('NFC', text)
            
            # UTF-8エンコーディングを確認
            normalized.encode('utf-8')
            
            return normalized
        except (UnicodeError, UnicodeDecodeError):
            # 正規化に失敗した場合は元のテキストを返す
            return text
    
    def _get_display_text(self, japanese_text, english_text=None):
        """表示用テキストを取得（日本語サポートに応じて）"""
        if self._japanese_supported and japanese_text:
            return self._normalize_japanese_text(japanese_text)
        elif english_text:
            return english_text
        else:
            return self._normalize_japanese_text(japanese_text)  # フォールバック
    
    def setup_main_window(self):
        """メインウィンドウの設定"""
        self.root = tk.Tk()
        self.root.title("Low Mountain Blog Generator")  # 英語に変更
        self.root.geometry("1000x700")
        self.root.configure(bg="#f0f0f0")
        
        # 日本語フォント設定
        import platform
        if platform.system() == "Windows":
            self.default_font = ("Yu Gothic", 9)
            self.title_font = ("Yu Gothic", 16, "bold")
            self.button_font = ("Yu Gothic", 10, "bold")
        else:
            # Linux/Unix系 - 日本語対応フォントを試行
            try:
                # 利用可能なフォントを確認
                import tkinter.font as tkFont
                available_fonts = tkFont.families()
                
                # 日本語対応フォントの優先順位
                japanese_fonts = ["Noto Sans CJK JP", "Takao Gothic", "VL Gothic", "IPAGothic", "DejaVu Sans"]
                
                selected_font = "DejaVu Sans"  # デフォルト
                for font in japanese_fonts:
                    if font in available_fonts:
                        selected_font = font
                        break
                
                self.default_font = (selected_font, 9)
                self.title_font = (selected_font, 16, "bold")
                self.button_font = (selected_font, 10, "bold")
                
            except Exception:
                # フォント検出に失敗した場合のフォールバック
                self.default_font = ("TkDefaultFont", 9)
                self.title_font = ("TkDefaultFont", 16, "bold")
                self.button_font = ("TkDefaultFont", 10, "bold")
        
        # デフォルトフォントを設定
        self.root.option_add("*Font", self.default_font)
        
        # アイコン設定（任意）
        try:
            self.root.iconbitmap("icon.ico")  # アイコンファイルがあれば
        except:
            pass
    
    def setup_widgets(self):
        """ウィジェットの配置"""
        # メインフレーム
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # タイトル
        title_label = tk.Label(
            main_frame, 
            text="Low Mountain Blog Generator",
            font=self.title_font,
            bg="#f0f0f0",
            fg="#2c3e50"
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # 左パネル: 山選択
        self.setup_mountain_selection_panel(main_frame)
        
        # 中央パネル: 設定と生成
        self.setup_generation_panel(main_frame)
        
        # 右パネル: 結果表示
        self.setup_result_panel(main_frame)
        
        # 下部: ステータスバー
        self.setup_status_bar(main_frame)
        
        # グリッド設定
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
    
    def setup_mountain_selection_panel(self, parent):
        """山選択パネル"""
        # 山選択フレーム
        mountain_frame = ttk.LabelFrame(parent, text="Mountain Selection", padding="10")
        mountain_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # フィルタ
        filter_frame = ttk.Frame(mountain_frame)
        filter_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(filter_frame, text="Region:").grid(row=0, column=0, sticky=tk.W)
        self.region_var = tk.StringVar(value="All")
        self.region_combo = ttk.Combobox(
            filter_frame, 
            textvariable=self.region_var,
            values=["All", "Hokkaido", "Tohoku", "Kanto", "Chubu", "Kansai", "Chugoku", "Shikoku", "Kyushu", "Okinawa"],
            state="readonly",
            width=15
        )
        self.region_combo.grid(row=0, column=1, padx=(5, 0))
        self.region_combo.bind('<<ComboboxSelected>>', self.filter_mountains)
        
        ttk.Label(filter_frame, text="Difficulty:").grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        self.difficulty_var = tk.StringVar(value="All")
        self.difficulty_combo = ttk.Combobox(
            filter_frame,
            textvariable=self.difficulty_var,
            values=["All", "Beginner", "Beginner-Inter", "Intermediate", "Advanced"],
            state="readonly",
            width=15
        )
        self.difficulty_combo.grid(row=1, column=1, padx=(5, 0), pady=(5, 0))
        self.difficulty_combo.bind('<<ComboboxSelected>>', self.filter_mountains)
        
        # 山リスト
        list_frame = ttk.Frame(mountain_frame)
        list_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        
        # Treeview for mountain list
        columns = ("name", "prefecture", "elevation", "difficulty")
        self.mountain_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=15)
        
        # Treeviewにフォント設定
        style = ttk.Style()
        style.configure("Treeview", font=self.default_font)
        style.configure("Treeview.Heading", font=self.default_font)
        
        # 列設定
        self.mountain_tree.heading("name", text="Mountain")
        self.mountain_tree.heading("prefecture", text="Prefecture")
        self.mountain_tree.heading("elevation", text="Elevation")
        self.mountain_tree.heading("difficulty", text="Difficulty")
        
        self.mountain_tree.column("name", width=120)
        self.mountain_tree.column("prefecture", width=100)
        self.mountain_tree.column("elevation", width=60)
        self.mountain_tree.column("difficulty", width=80)
        
        # スクロールバー
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.mountain_tree.yview)
        self.mountain_tree.configure(yscrollcommand=scrollbar.set)
        
        self.mountain_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # 選択イベント
        self.mountain_tree.bind('<<TreeviewSelect>>', self.on_mountain_select)
        
        # グリッド設定
        mountain_frame.columnconfigure(0, weight=1)
        mountain_frame.rowconfigure(1, weight=1)
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
    
    def setup_generation_panel(self, parent):
        """記事生成パネル"""
        generation_frame = ttk.LabelFrame(parent, text="Article Generation", padding="10")
        generation_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10)
        
        # 選択された山の情報表示
        info_frame = ttk.LabelFrame(generation_frame, text="Selected Mountain", padding="10")
        info_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        
        self.mountain_info = tk.Text(info_frame, height=8, width=50, state=tk.DISABLED, wrap=tk.WORD)
        info_scroll = ttk.Scrollbar(info_frame, orient=tk.VERTICAL, command=self.mountain_info.yview)
        self.mountain_info.configure(yscrollcommand=info_scroll.set)
        
        self.mountain_info.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        info_scroll.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # 記事設定
        settings_frame = ttk.LabelFrame(generation_frame, text="Article Settings", padding="10")
        settings_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # テーマ選択
        ttk.Label(settings_frame, text="Theme:").grid(row=0, column=0, sticky=tk.W)
        self.theme_var = tk.StringVar(value="Auto Select")
        theme_values = [
            "Auto Select",
            "Beginner Guide", 
            "Family Hiking",
            "Autumn Leaves",
            "Scenic Views",
            "Power Spots",
            "Day Trip Plan"
        ]
        self.theme_combo = ttk.Combobox(
            settings_frame,
            textvariable=self.theme_var,
            values=theme_values,
            width=30
        )
        self.theme_combo.grid(row=0, column=1, padx=(10, 0), sticky=(tk.W, tk.E))
        
        # 目標文字数
        ttk.Label(settings_frame, text="Target Length:").grid(row=1, column=0, sticky=tk.W, pady=(10, 0))
        self.length_var = tk.StringVar(value="2000")
        length_spin = ttk.Spinbox(
            settings_frame,
            from_=1000,
            to=5000,
            increment=500,
            textvariable=self.length_var,
            width=10
        )
        length_spin.grid(row=1, column=1, padx=(10, 0), pady=(10, 0), sticky=tk.W)
        
        # WordPress公開オプション
        self.publish_var = tk.BooleanVar(value=False)
        publish_check = ttk.Checkbutton(
            settings_frame,
            text="Publish to WordPress immediately",
            variable=self.publish_var
        )
        publish_check.grid(row=2, column=0, columnspan=2, pady=(10, 0), sticky=tk.W)
        
        # 生成ボタン
        button_frame = ttk.Frame(generation_frame)
        button_frame.grid(row=2, column=0, pady=(0, 20))
        
        self.generate_button = tk.Button(
            button_frame,
            text="Generate Article",
            font=self.button_font,
            bg="#3498db",
            fg="white",
            padx=20,
            pady=10,
            command=self.generate_article
        )
        self.generate_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.preview_button = tk.Button(
            button_frame,
            text="Preview",
            font=self.default_font,
            bg="#95a5a6",
            fg="white",
            padx=15,
            pady=8,
            command=self.preview_article,
            state=tk.DISABLED
        )
        self.preview_button.pack(side=tk.LEFT)
        
        # プログレスバー
        self.progress = ttk.Progressbar(
            generation_frame,
            mode='indeterminate',
            length=300
        )
        self.progress.grid(row=3, column=0, pady=(0, 10))
        
        # ステータス表示
        self.status_label = tk.Label(
            generation_frame,
            text="Select a mountain to generate article",
            fg="#7f8c8d",
            bg="#f0f0f0",
            font=self.default_font
        )
        self.status_label.grid(row=4, column=0)
        
        # グリッド設定
        generation_frame.columnconfigure(0, weight=1)
        info_frame.columnconfigure(0, weight=1)
        info_frame.rowconfigure(0, weight=1)
        settings_frame.columnconfigure(1, weight=1)
    
    def setup_result_panel(self, parent):
        """結果表示パネル"""
        result_frame = ttk.LabelFrame(parent, text="Generation Result", padding="10")
        result_frame.grid(row=1, column=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(10, 0))
        
        # 記事情報表示
        self.result_text = scrolledtext.ScrolledText(
            result_frame,
            height=25,
            width=40,
            state=tk.DISABLED,
            wrap=tk.WORD
        )
        self.result_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 操作ボタン
        button_frame = ttk.Frame(result_frame)
        button_frame.grid(row=1, column=0, pady=(10, 0))
        
        self.copy_button = tk.Button(
            button_frame,
            text="Copy",
            command=self.copy_to_clipboard,
            state=tk.DISABLED,
            font=self.default_font
        )
        self.copy_button.pack(side=tk.LEFT, padx=(0, 5))
        
        self.save_button = tk.Button(
            button_frame,
            text="Save",
            command=self.save_article,
            state=tk.DISABLED,
            font=self.default_font
        )
        self.save_button.pack(side=tk.LEFT, padx=5)
        
        self.wordpress_button = tk.Button(
            button_frame,
            text="Publish to WP",
            command=self.publish_to_wordpress,
            state=tk.DISABLED,
            bg="#27ae60",
            fg="white",
            font=self.default_font
        )
        self.wordpress_button.pack(side=tk.LEFT, padx=(5, 0))
        
        # グリッド設定
        result_frame.columnconfigure(0, weight=1)
        result_frame.rowconfigure(0, weight=1)
    
    def setup_status_bar(self, parent):
        """ステータスバー"""
        status_frame = ttk.Frame(parent)
        status_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(20, 0))
        
        self.status_bar = tk.Label(
            status_frame,
            text="Ready",
            relief=tk.SUNKEN,
            anchor=tk.W,
            bg="#ecf0f1",
            padx=10,
            font=self.default_font
        )
        self.status_bar.pack(fill=tk.X)
    
    def load_mountain_data(self):
        """山データを読み込み"""
        try:
            mountains = self.mountain_repo.get_all()
            self.mountains = mountains
            self.populate_mountain_list(mountains)
            self.update_status(f"Mountain data loaded: {len(mountains)} mountains")
        except Exception as e:
            self.logger.error("Failed to load mountain data", e)
            messagebox.showerror("エラー", f"山データの読み込みに失敗しました: {str(e)}")
    
    def populate_mountain_list(self, mountains: List[Mountain]):
        """山リストを更新"""
        # 既存のアイテムをクリア
        for item in self.mountain_tree.get_children():
            self.mountain_tree.delete(item)
        
        # 新しいアイテムを追加（英語表記で統一）
        prefecture_en_map = {
            "北海道": "Hokkaido", "青森県": "Aomori", "岩手県": "Iwate", 
            "宮城県": "Miyagi", "山形県": "Yamagata", "福島県": "Fukushima",
            "東京都": "Tokyo", "神奈川県": "Kanagawa", "静岡県": "Shizuoka",
            "山梨県": "Yamanashi", "石川県": "Ishikawa", "岐阜県": "Gifu",
            "福井県": "Fukui", "滋賀県": "Shiga", "奈良県": "Nara",
            "大阪府": "Osaka", "兵庫県": "Hyogo", "鳥取県": "Tottori",
            "愛媛県": "Ehime", "熊本県": "Kumamoto", "大分県": "Oita",
            "鹿児島県": "Kagoshima", "沖縄県": "Okinawa"
        }
        
        difficulty_en_map = {
            "初級": "Beginner", "初級-中級": "Beginner-Inter",
            "中級": "Intermediate", "上級": "Advanced"
        }
        
        for mountain in mountains:
            # 日本語サポートに応じて表示テキストを選択
            if self._japanese_supported:
                # 日本語で表示
                name = mountain.name
                first_prefecture = mountain.prefecture.split("・")[0]
                prefecture = first_prefecture
                difficulty = mountain.difficulty.level.value
            else:
                # 英語で表示
                name = mountain.name_en if mountain.name_en else mountain.name
                first_prefecture = mountain.prefecture.split("・")[0]
                prefecture = prefecture_en_map.get(first_prefecture, first_prefecture)
                difficulty = difficulty_en_map.get(mountain.difficulty.level.value, mountain.difficulty.level.value)
            
            self.mountain_tree.insert(
                "",
                tk.END,
                values=(name, prefecture, f"{mountain.elevation}m", difficulty),
                tags=(mountain.id,)
            )
    
    def filter_mountains(self, event=None):
        """山をフィルタリング"""
        region = self.region_var.get()
        difficulty = self.difficulty_var.get()
        
        # 英語から日本語にマッピング
        region_map = {
            "All": "すべて", "Hokkaido": "北海道", "Tohoku": "東北", 
            "Kanto": "関東", "Chubu": "中部", "Kansai": "関西", 
            "Chugoku": "中国", "Shikoku": "四国", "Kyushu": "九州", "Okinawa": "沖縄"
        }
        
        difficulty_map = {
            "All": "すべて", "Beginner": "初級", "Beginner-Inter": "初級-中級", 
            "Intermediate": "中級", "Advanced": "上級"
        }
        
        mountains = self.mountains
        
        if region != "All":
            jp_region = region_map.get(region, region)
            mountains = [m for m in mountains if m.region == jp_region]
        
        if difficulty != "All":
            jp_difficulty = difficulty_map.get(difficulty, difficulty)
            mountains = [m for m in mountains if m.difficulty.level.value == jp_difficulty]
        
        self.populate_mountain_list(mountains)
        self.update_status(f"Filter result: {len(mountains)} mountains")
    
    def on_mountain_select(self, event):
        """山が選択された時の処理"""
        selection = self.mountain_tree.selection()
        if not selection:
            return
        
        item = self.mountain_tree.item(selection[0])
        mountain_id = item['tags'][0]
        
        # 山を取得
        self.selected_mountain = self.mountain_repo.get_by_id(mountain_id)
        
        if self.selected_mountain:
            self.display_mountain_info(self.selected_mountain)
            self.generate_button.config(state=tk.NORMAL)
            self.update_status(f"Selected: {self.selected_mountain.name}")
    
    def display_mountain_info(self, mountain: Mountain):
        """山の詳細情報を表示"""
        info_text = f"""🗻 {mountain.name} ({mountain.name_en})

📍 所在地: {mountain.prefecture} ({mountain.region})
⛰️ 標高: {mountain.elevation}m
🎯 難易度: {mountain.difficulty.level.value}
⏱️ 登山時間: {mountain.difficulty.hiking_time}
📏 距離: {mountain.difficulty.distance}
📈 標高差: {mountain.difficulty.elevation_gain}

🚉 アクセス: {mountain.location.nearest_station}から{mountain.location.access_time}

✨ 特徴:
{chr(10).join(f"  • {feature}" for feature in mountain.features[:5])}

📝 記事テーマ案:
{chr(10).join(f"  • {theme}" for theme in mountain.article_themes[:3])}
"""
        
        self.mountain_info.config(state=tk.NORMAL)
        self.mountain_info.delete(1.0, tk.END)
        self.mountain_info.insert(1.0, info_text)
        self.mountain_info.config(state=tk.DISABLED)
    
    def generate_article(self):
        """記事生成を開始"""
        if not self.selected_mountain:
            messagebox.showwarning("警告", "山を選択してください")
            return
        
        # UI状態更新
        self.generate_button.config(state=tk.DISABLED)
        self.progress.start()
        self.update_status("Generating article...")
        
        # バックグラウンドで記事生成
        threading.Thread(target=self._generate_article_thread, daemon=True).start()
        
        # 定期的に結果をチェック
        self.check_generation_result()
    
    def _generate_article_thread(self):
        """記事生成のバックグラウンド処理"""
        try:
            # テーマの英語から日本語マッピング
            theme_map = {
                "Auto Select": None,
                "Beginner Guide": "初心者向け登山ガイド",
                "Family Hiking": "家族でハイキング", 
                "Autumn Leaves": "秋の紅葉狩り",
                "Scenic Views": "絶景ハイキング",
                "Power Spots": "パワースポット巡り",
                "Day Trip Plan": "日帰り登山プラン"
            }
            
            theme_en = self.theme_var.get()
            theme = theme_map.get(theme_en, None)
            length = int(self.length_var.get())
            publish = self.publish_var.get()
            
            result = self.mountain_service.create_and_publish_article(
                mountain_id=self.selected_mountain.id,
                theme=theme,
                publish=publish
            )
            
            self.result_queue.put(("success", result))
            
        except Exception as e:
            self.result_queue.put(("error", str(e)))
    
    def check_generation_result(self):
        """生成結果をチェック"""
        try:
            result_type, result_data = self.result_queue.get_nowait()
            
            # UI状態リセット
            self.progress.stop()
            self.generate_button.config(state=tk.NORMAL)
            
            if result_type == "success":
                self.handle_generation_success(result_data)
            else:
                self.handle_generation_error(result_data)
                
        except queue.Empty:
            # まだ完了していない場合は100ms後に再チェック
            self.root.after(100, self.check_generation_result)
    
    def handle_generation_success(self, result):
        """生成成功時の処理"""
        if result.success and result.article:
            self.generated_article = result.article
            self.display_generation_result(result)
            self.enable_result_buttons()
            
            if self.generated_article.wordpress_id:
                self.update_status(f"記事生成・投稿完了! WordPress ID: {self.generated_article.wordpress_id}")
            else:
                self.update_status(f"記事生成完了! ({result.generation_time:.2f}秒)")
        else:
            self.handle_generation_error(result.error_message or "不明なエラー")
    
    def handle_generation_error(self, error_message):
        """生成エラー時の処理"""
        self.update_status("記事生成に失敗しました")
        messagebox.showerror("エラー", f"記事生成に失敗しました:\n{error_message}")
    
    def display_generation_result(self, result):
        """生成結果を表示"""
        article = result.article
        
        result_text = f"""📰 記事生成結果

📌 タイトル: {article.content.title}

📊 統計情報:
  • 文字数: {article.content.get_word_count():,}文字
  • 生成時間: {result.generation_time:.2f}秒
  • タグ数: {len(article.content.tags)}個
  • 商品数: {len(article.content.affiliate_products)}個
  • 宿泊施設数: {len(article.content.affiliate_hotels)}個

🏷️ タグ: {', '.join(article.content.tags)}

📋 要約:
{article.content.excerpt}

📝 記事内容 (抜粋):
{article.content.content[:500]}...

"""
        
        if article.wordpress_id:
            result_text += f"\n🌐 WordPress投稿ID: {article.wordpress_id}"
        
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(1.0, result_text)
        self.result_text.config(state=tk.DISABLED)
    
    def enable_result_buttons(self):
        """結果表示ボタンを有効化"""
        self.preview_button.config(state=tk.NORMAL)
        self.copy_button.config(state=tk.NORMAL)
        self.save_button.config(state=tk.NORMAL)
        
        if not self.generated_article.wordpress_id:
            self.wordpress_button.config(state=tk.NORMAL)
    
    def preview_article(self):
        """記事プレビューを表示"""
        if not self.generated_article:
            return
        
        preview_window = tk.Toplevel(self.root)
        preview_window.title(f"記事プレビュー - {self.generated_article.content.title}")
        preview_window.geometry("800x600")
        
        preview_text = scrolledtext.ScrolledText(
            preview_window,
            wrap=tk.WORD,
            padx=10,
            pady=10
        )
        preview_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 記事内容を表示
        full_content = f"""タイトル: {self.generated_article.content.title}

{self.generated_article.content.content}

タグ: {', '.join(self.generated_article.content.tags)}
"""
        
        preview_text.insert(1.0, full_content)
        preview_text.config(state=tk.DISABLED)
    
    def copy_to_clipboard(self):
        """記事をクリップボードにコピー"""
        if not self.generated_article:
            return
        
        content = f"{self.generated_article.content.title}\n\n{self.generated_article.content.content}"
        self.root.clipboard_clear()
        self.root.clipboard_append(content)
        self.update_status("記事をクリップボードにコピーしました")
    
    def save_article(self):
        """記事をファイルに保存"""
        if not self.generated_article:
            return
        
        from tkinter import filedialog
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("テキストファイル", "*.txt"), ("すべてのファイル", "*.*")],
            initialname=f"{self.generated_article.mountain.name}_記事.txt"
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(f"タイトル: {self.generated_article.content.title}\n\n")
                    f.write(self.generated_article.content.content)
                    f.write(f"\n\nタグ: {', '.join(self.generated_article.content.tags)}")
                
                self.update_status(f"記事を保存しました: {filename}")
                messagebox.showinfo("保存完了", f"記事を保存しました:\n{filename}")
                
            except Exception as e:
                messagebox.showerror("エラー", f"保存に失敗しました:\n{str(e)}")
    
    def publish_to_wordpress(self):
        """WordPressに投稿"""
        if not self.generated_article or self.generated_article.wordpress_id:
            return
        
        if messagebox.askyesno("確認", "WordPressに記事を投稿しますか？"):
            try:
                from src.application.services import PublishingService
                
                self.update_status("WordPressに投稿中...")
                publishing_service = PublishingService()
                
                wordpress_id = publishing_service.publish_to_wordpress(self.generated_article)
                
                self.update_status(f"WordPress投稿完了! ID: {wordpress_id}")
                self.wordpress_button.config(state=tk.DISABLED)
                messagebox.showinfo("投稿完了", f"WordPressに投稿しました!\n投稿ID: {wordpress_id}")
                
            except Exception as e:
                self.update_status("WordPress投稿に失敗しました")
                messagebox.showerror("エラー", f"WordPress投稿に失敗しました:\n{str(e)}")
    
    def update_status(self, message: str):
        """ステータスバーを更新"""
        self.status_bar.config(text=message)
        self.logger.info(f"Status: {message}")
    
    def run(self):
        """GUIアプリケーションを開始"""
        self.logger.info("Starting GUI application")
        self.root.mainloop()


def main():
    """メイン関数"""
    # ログシステム初期化
    initialize_logging()
    
    try:
        app = MountainBlogGUI()
        app.run()
    except Exception as e:
        print(f"アプリケーション起動エラー: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()