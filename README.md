# utilizers
色々なところで使えそうなツールを作成.

## 概要
日常生活やPythonでの開発に役立ちそうなちょっとしたツールをモジュール化する.

## ローカル環境のセットアップ
仮想環境を構築する.

```
source setup.sh
```

`PYTHONPATH` を通して追加する.

```
echo "export PYTHONPATH=../../.." >> ~/.bashrc
source ~/.bashrc
```

## Commit ルール
Commit の際は以下のルールに合わせて種類ごとにする.  

🎉  初めてのコミット (Initial Commit)  
🔖  バージョンタグ (Version Tag)  
✨  新機能 (New Feature)  
🐛  バグ修正 (Bugfix)  
♻️  リファクタリング (Refactoring)  
📚  ドキュメント (Documentation)  
🎨  デザインUI/UX (Accessibility)  
🐎  パフォーマンス (Performance)  
🔧  ツール (Tooling)  
🚨  テスト (Tests)  
💩  非推奨追加 (Deprecation)  
🗑️  削除 (Removal)  
🚧  WIP (Work In Progress)