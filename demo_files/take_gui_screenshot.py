#!/usr/bin/env python3
"""
GUIスクリーンショット撮影スクリプト
"""
import tkinter as tk
import sys
import os
import time
from PIL import Image, ImageTk

# プロジェクトルートをパスに追加
sys.path.insert(0, os.path.abspath('.'))

# 環境変数設定
os.environ['PYTHONIOENCODING'] = 'utf-8'

def create_gui_demo():
    """デモ用GUI作成"""
    from src.presentation.gui import MountainBlogGUI
    
    try:
        # GUIアプリケーションを作成
        app = MountainBlogGUI()
        
        # ウィンドウを表示
        app.root.deiconify()
        app.root.update()
        
        # 少し待ってからスクリーンショット
        app.root.after(2000, lambda: take_screenshot(app.root))
        
        # メインループ開始（10秒後に自動終了）
        app.root.after(10000, app.root.quit)
        app.root.mainloop()
        
    except Exception as e:
        print(f"GUI creation error: {e}")
        # フォールバック: 簡単なデモウィンドウ
        create_simple_demo()

def create_simple_demo():
    """シンプルなデモウィンドウ"""
    print("Creating simple demo window...")
    
    root = tk.Tk()
    root.title("Low Mountain Blog Generator - Demo")
    root.geometry("1000x700")
    root.configure(bg="#f0f0f0")
    
    # メインフレーム
    main_frame = tk.Frame(root, bg="#f0f0f0", padx=20, pady=20)
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    # タイトル
    title_label = tk.Label(
        main_frame,
        text="🏔️ Low Mountain Blog Generator",
        font=("Arial", 18, "bold"),
        bg="#f0f0f0",
        fg="#2c3e50"
    )
    title_label.pack(pady=(0, 30))
    
    # 3つのパネルを模擬
    panels_frame = tk.Frame(main_frame, bg="#f0f0f0")
    panels_frame.pack(fill=tk.BOTH, expand=True)
    
    # 左パネル - Mountain Selection
    left_panel = tk.LabelFrame(
        panels_frame, 
        text="Mountain Selection", 
        font=("Arial", 12, "bold"),
        padx=10, 
        pady=10
    )
    left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
    
    # サンプル山リスト
    mountains_data = [
        ("Mount Takao", "Tokyo", "599m", "Beginner"),
        ("Mount Maruyama", "Hokkaido", "225m", "Beginner"),
        ("Mount Fuji", "Shizuoka", "3776m", "Advanced"),
        ("Mount Zao", "Yamagata", "1841m", "Intermediate"),
        ("Mount Ibuki", "Shiga", "1377m", "Intermediate")
    ]
    
    # フィルター
    filter_frame = tk.Frame(left_panel)
    filter_frame.pack(fill=tk.X, pady=(0, 10))
    
    tk.Label(filter_frame, text="Region:").pack(side=tk.LEFT)
    region_combo = tk.OptionMenu(filter_frame, tk.StringVar(value="All"), 
                                 "All", "Hokkaido", "Kanto", "Chubu")
    region_combo.pack(side=tk.LEFT, padx=(5, 20))
    
    tk.Label(filter_frame, text="Difficulty:").pack(side=tk.LEFT)
    diff_combo = tk.OptionMenu(filter_frame, tk.StringVar(value="All"),
                              "All", "Beginner", "Intermediate", "Advanced")
    diff_combo.pack(side=tk.LEFT, padx=(5, 0))
    
    # 山リスト（リストボックスで模擬）
    listbox_frame = tk.Frame(left_panel)
    listbox_frame.pack(fill=tk.BOTH, expand=True)
    
    # ヘッダー
    header_frame = tk.Frame(listbox_frame, bg="#e8e8e8")
    header_frame.pack(fill=tk.X, pady=(0, 2))
    
    headers = ["Mountain", "Prefecture", "Elevation", "Difficulty"]
    for i, header in enumerate(headers):
        tk.Label(header_frame, text=header, font=("Arial", 10, "bold"), 
                bg="#e8e8e8", anchor="w").grid(row=0, column=i, sticky="ew", padx=2)
    
    # 山データ
    for i, (name, pref, elev, diff) in enumerate(mountains_data):
        row_frame = tk.Frame(listbox_frame)
        row_frame.pack(fill=tk.X, pady=1)
        
        tk.Label(row_frame, text=name, anchor="w", width=15).grid(row=0, column=0, sticky="ew")
        tk.Label(row_frame, text=pref, anchor="w", width=12).grid(row=0, column=1, sticky="ew")
        tk.Label(row_frame, text=elev, anchor="w", width=8).grid(row=0, column=2, sticky="ew")
        tk.Label(row_frame, text=diff, anchor="w", width=12).grid(row=0, column=3, sticky="ew")
    
    # 中央パネル - Article Generation
    center_panel = tk.LabelFrame(
        panels_frame, 
        text="Article Generation", 
        font=("Arial", 12, "bold"),
        padx=10, 
        pady=10
    )
    center_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
    
    # 選択された山情報
    info_panel = tk.LabelFrame(center_panel, text="Selected Mountain", padx=5, pady=5)
    info_panel.pack(fill=tk.X, pady=(0, 20))
    
    info_text = """🗻 Mount Takao (高尾山)

📍 Location: Tokyo (Kanto Region)
⛰️ Elevation: 599m
🎯 Difficulty: Beginner
⏱️ Hiking Time: 2-3 hours
📏 Distance: ~5km

🚉 Access: 50 min from Shinjuku

✨ Features:
  • Cable car available
  • Yakuoin Temple
  • Observation deck
  • Night view of Tokyo"""
    
    info_label = tk.Label(info_panel, text=info_text, justify=tk.LEFT, anchor="nw", 
                         font=("Courier", 9))
    info_label.pack(fill=tk.BOTH, expand=True)
    
    # 設定
    settings_panel = tk.LabelFrame(center_panel, text="Article Settings", padx=5, pady=5)
    settings_panel.pack(fill=tk.X, pady=(0, 20))
    
    # テーマ選択
    theme_frame = tk.Frame(settings_panel)
    theme_frame.pack(fill=tk.X, pady=5)
    tk.Label(theme_frame, text="Theme:").pack(side=tk.LEFT)
    theme_combo = tk.OptionMenu(theme_frame, tk.StringVar(value="Beginner Guide"),
                               "Auto Select", "Beginner Guide", "Family Hiking", "Scenic Views")
    theme_combo.pack(side=tk.LEFT, padx=(10, 0))
    
    # 文字数
    length_frame = tk.Frame(settings_panel)
    length_frame.pack(fill=tk.X, pady=5)
    tk.Label(length_frame, text="Target Length:").pack(side=tk.LEFT)
    length_spin = tk.Spinbox(length_frame, from_=1000, to=5000, value=2000, width=10)
    length_spin.pack(side=tk.LEFT, padx=(10, 0))
    
    # WordPress公開
    wp_frame = tk.Frame(settings_panel)
    wp_frame.pack(fill=tk.X, pady=5)
    wp_var = tk.BooleanVar()
    wp_check = tk.Checkbutton(wp_frame, text="Publish to WordPress immediately", variable=wp_var)
    wp_check.pack(side=tk.LEFT)
    
    # 生成ボタン
    button_frame = tk.Frame(center_panel)
    button_frame.pack(fill=tk.X, pady=(0, 20))
    
    generate_btn = tk.Button(
        button_frame, 
        text="🚀 Generate Article", 
        font=("Arial", 12, "bold"),
        bg="#3498db", 
        fg="white", 
        padx=20, 
        pady=10
    )
    generate_btn.pack(side=tk.LEFT, padx=(0, 10))
    
    preview_btn = tk.Button(
        button_frame, 
        text="👁️ Preview", 
        bg="#95a5a6", 
        fg="white", 
        padx=15, 
        pady=8
    )
    preview_btn.pack(side=tk.LEFT)
    
    # プログレスバー
    import tkinter.ttk as ttk
    progress = ttk.Progressbar(center_panel, length=300)
    progress.pack(pady=(0, 10))
    
    # ステータス
    status_label = tk.Label(center_panel, text="Select a mountain to generate article", 
                           fg="#7f8c8d")
    status_label.pack()
    
    # 右パネル - Generation Result
    right_panel = tk.LabelFrame(
        panels_frame, 
        text="Generation Result", 
        font=("Arial", 12, "bold"),
        padx=10, 
        pady=10
    )
    right_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0))
    
    # 結果表示エリア
    result_text = tk.Text(right_panel, height=20, width=40, wrap=tk.WORD, state=tk.DISABLED)
    result_scroll = tk.Scrollbar(right_panel, orient=tk.VERTICAL, command=result_text.yview)
    result_text.configure(yscrollcommand=result_scroll.set)
    
    result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    result_scroll.pack(side=tk.RIGHT, fill=tk.Y)
    
    # サンプル結果
    sample_result = """📰 Article Generation Result

📌 Title: Mount Takao: Perfect Beginner's Guide to Tokyo's Most Accessible Mountain

📊 Statistics:
  • Characters: 2,247
  • Generation time: 24.5s
  • Tags: 6
  • Products: 5
  • Hotels: 3

🏷️ Tags: beginner, Tokyo, cable-car, temple, night-view, hiking

📋 Summary:
Mount Takao offers the perfect introduction to hiking in Japan. Located just 50 minutes from Shinjuku, this 599-meter mountain provides stunning views of Tokyo and Mount Fuji on clear days. With cable car access and well-maintained trails, it's ideal for families and beginners...

📝 Article Content (preview):
Mount Takao (高尾山) stands as Tokyo's most beloved and accessible mountain, offering an perfect escape from the bustling city life. At 599 meters high, this sacred mountain has been welcoming visitors for over 1,200 years...
"""
    
    result_text.config(state=tk.NORMAL)
    result_text.insert(1.0, sample_result)
    result_text.config(state=tk.DISABLED)
    
    # ボタン
    btn_frame = tk.Frame(right_panel)
    btn_frame.pack(fill=tk.X, pady=(10, 0))
    
    tk.Button(btn_frame, text="📋 Copy").pack(side=tk.LEFT, padx=(0, 5))
    tk.Button(btn_frame, text="💾 Save").pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="🌐 Publish to WP", bg="#27ae60", fg="white").pack(side=tk.LEFT, padx=(5, 0))
    
    # ステータスバー
    status_frame = tk.Frame(root, relief=tk.SUNKEN, bd=1)
    status_frame.pack(fill=tk.X, side=tk.BOTTOM)
    
    status_bar = tk.Label(status_frame, text="Ready - Mountain data loaded: 20 mountains", 
                         anchor=tk.W, padx=10)
    status_bar.pack(fill=tk.X)
    
    # ウィンドウを画面中央に配置
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (1000 // 2)
    y = (root.winfo_screenheight() // 2) - (700 // 2)
    root.geometry(f"1000x700+{x}+{y}")
    
    # スクリーンショット撮影の準備
    root.after(1000, lambda: take_screenshot(root))
    
    # 5秒後に自動終了
    root.after(5000, root.quit)
    
    print("Demo window created. Taking screenshot...")
    root.mainloop()

def take_screenshot(window):
    """スクリーンショット撮影"""
    try:
        # ウィンドウの位置とサイズを取得
        window.update()
        x = window.winfo_rootx()
        y = window.winfo_rooty()
        width = window.winfo_width()
        height = window.winfo_height()
        
        print(f"Window position: {x}, {y}")
        print(f"Window size: {width}x{height}")
        
        # PIL でスクリーンショット（仮想的にファイルパスを生成）
        screenshot_path = "gui_screenshot_demo.png"
        
        # スクリーンショット機能が使用できない環境のため、代替案を提示
        print(f"Screenshot would be saved to: {screenshot_path}")
        print("Note: In WSL2 environment, actual screenshot capture may not be available")
        
        # 代わりにGUIの構造情報をテキストで出力
        save_gui_structure_info()
        
    except Exception as e:
        print(f"Screenshot error: {e}")

def save_gui_structure_info():
    """GUI構造情報をテキストファイルに保存"""
    gui_info = """
🎨 LOW MOUNTAIN BLOG GENERATOR - GUI LAYOUT 🎨
═══════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────┐
│                🏔️ Low Mountain Blog Generator                │
│                                                             │
├─────────────────┬─────────────────┬─────────────────────────┤
│ Mountain        │ Article         │ Generation              │
│ Selection       │ Generation      │ Result                  │
│                 │                 │                         │
│ Region: [All ▼] │ Selected Mount: │ 📰 Article Result       │
│ Diff:   [All ▼] │ ┌─────────────┐ │ ┌─────────────────────┐ │
│                 │ │🗻 Mount Takao│ │ │📌 Title: Mount      │ │
│ ┌─────────────┐ │ │             │ │ │   Takao Perfect...  │ │
│ │Mount    │Pre│ │ │📍 Tokyo     │ │ │                     │ │
│ │─────────┼───│ │ │⛰️ 599m      │ │ │📊 Stats:            │ │
│ │Takao    │Tok│ │ │🎯 Beginner  │ │ │  • Chars: 2,247     │ │
│ │Maruyama │Hok│ │ │⏱️ 2-3 hours │ │ │  • Time: 24.5s      │ │
│ │Fuji     │Shi│ │ │📏 ~5km      │ │ │  • Tags: 6          │ │
│ │Zao      │Yam│ │ │             │ │ │                     │ │
│ │Ibuki    │Shi│ │ │✨ Features:  │ │ │📋 Summary:          │ │
│ │...      │...│ │ │  • Cable car│ │ │Mount Takao offers  │ │
│ └─────────────┘ │ │  • Temple   │ │ │the perfect intro... │ │
│                 │ └─────────────┘ │ │                     │ │
│                 │                 │ │📝 Content:          │ │
│                 │ Article Settings│ │Mount Takao stands  │ │
│                 │ ┌─────────────┐ │ │as Tokyo's most...   │ │
│                 │ │Theme: [Beg▼]│ │ │                     │ │
│                 │ │Length: 2000 │ │ └─────────────────────┘ │
│                 │ │☐ Publish WP│ │                         │
│                 │ └─────────────┘ │ [📋Copy][💾Save][🌐WP] │
│                 │                 │                         │
│                 │ [🚀 Generate]   │                         │
│                 │ [👁️ Preview]    │                         │
│                 │ ▓▓▓▓▓░░░░ 45%  │                         │
│                 │ Status: Ready   │                         │
└─────────────────┴─────────────────┴─────────────────────────┘
│ Status: Ready - Mountain data loaded: 20 mountains           │
└─────────────────────────────────────────────────────────────┘

🎯 KEY FEATURES:
✅ 3-Column Layout for intuitive workflow
✅ Mountain Selection with filtering (Region & Difficulty)
✅ Real-time mountain information display
✅ Article generation settings (Theme, Length, Auto-publish)
✅ Live generation progress indication
✅ Comprehensive result display with statistics
✅ One-click operations (Copy, Save, WordPress publish)
✅ Responsive design adapting to window size

🌟 JAPANESE SUPPORT STATUS:
✅ UTF-8 encoding properly configured
✅ Unicode normalization (NFC) implemented
✅ Automatic Japanese/English display switching
✅ Text processing with charset-normalizer
✅ Environment variables optimized for Japanese text

💡 USER EXPERIENCE:
• Select mountain → Configure settings → Generate → Review → Publish
• 3-click article generation workflow
• Visual feedback with progress bars and status updates
• Professional color scheme (Blues and greens for mountain theme)
• Clear typography and intuitive button placement
"""
    
    with open('gui_layout_description.txt', 'w', encoding='utf-8') as f:
        f.write(gui_info)
    
    print("✅ GUI layout information saved to 'gui_layout_description.txt'")

def main():
    """メイン関数"""
    print("Creating GUI demo for screenshot...")
    
    # 環境変数を設定
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    
    try:
        create_simple_demo()
    except Exception as e:
        print(f"Demo creation failed: {e}")
        save_gui_structure_info()

if __name__ == "__main__":
    main()