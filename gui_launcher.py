#!/usr/bin/env python3
"""
GUI版低山旅行記事作成アプリの起動スクリプト
"""
import sys
import os

# プロジェクトルートをパスに追加
sys.path.insert(0, os.path.abspath('.'))

from src.presentation.gui import main

if __name__ == "__main__":
    main()