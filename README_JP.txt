# **Collatz Jacobsthal Topology Visualizer**

Hiroshi Harada — May 23, 2026

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Document: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

## **概要 (Overview)**
本プロジェクトは、$3n+1$ コラッツ写像（Collatz conjecture）における自然数の振る舞いを幾何学的に可視化する Python ツールキットおよび研究レポートです。
自然数を 2 進対数螺旋空間へ写像し、Voronoi 分割を適用することで、任意の奇数ノードの周囲に 7 系統の Jacobsthal（$J$）型数列による「ステンドグラス状」の美しいトポロジー（RGB カラー幾何学構造）が形成されていることを示します。

## **ギャラリー (Gallery)**
![collatz_J-mandala_M1](collatz_J-mandala_M1.png)

> **The Stained-Glass Topology of the Collatz Map:**
> 最終アトラクター $1 \cdot 2^b$ 軸周辺の自然数空間の可視化。2進対数螺旋上への写像と Voronoi 分割により、7 系統の Jacobsthal 型数列に支配された高度に秩序立った幾何学構造が浮かび上がる。シアン色の軌道は奇数コラッツ軌道の最後の遷移（$5 \to 1$）を示しており、$1 \cdot 2^b$ 軸へとシームレスに着地している。

## **リポジトリ構成 (Repository Structure)**
- `code_01_collatz_voronoi.py` : 任意の初期値からの奇数コラッツ軌道と、Voronoi 空間上の直線軌跡を描画する導入用スクリプト。
- `code_02_collatz_jacobsthal.py` : 任意の奇数ルート $M$ を中心とした、7 系統の Jacobsthal トポロジー（RGB カラー構造）を描画するメインスクリプト。
- `REPORT_JP.md` / `REPORT_EN.md` : 本手法の数学的背景、および初期値 7 における軌道遷移の検証をまとめた研究レポート。

## **動作環境 (Requirements)**
- Python 3.x
- `numpy`
- `matplotlib`
- `scipy`
- `adjustText` （ラベルのオーバーラップを防ぐためのライブラリ。強く推奨）

依存ライブラリのインストール：
```bash
pip install numpy matplotlib scipy adjustText
```

## **使用方法 (Usage)**

スクリプトを実行すると、可視化された高解像度の画像データ（PNG）がカレントディレクトリに生成されます。
各スクリプト内の `CONFIGURATION` セクションの変数を変更することで、描画対象を自由にカスタマイズできます。

```python
# code_02_collatz_jacobsthal.py の設定例
TARGET_M = 1       # 背景となる奇数ルート M (1, 5, 11, 13, 17...)
N_DRAW = 2000      # 描画する自然数の範囲
```

### ⚠️ **奇数ルート $M$ の指定に関する注意点**

Collatz 予想の逆算構造において、3 の倍数（$M \equiv 0 \pmod 3$）は逆 Collatz 木の「葉（終端）」であり、それ以上奇数の親ノードを持ちません。
そのため、$M$ に 3 の倍数を指定すると真の $J$ 数列はすべて分数となり、コード上では丸め誤差による不正確な幾何学構造が描画されてしまいます。
`TARGET_M` には必ず **$M \equiv 1, 2 \pmod 3$** を満たす奇数を指定してください。

## **ライセンス (License)**

* **Research Documents (`REPORT_JP.md`, `REPORT_EN.md`):** [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
* **Python Source Code:** [MIT License](https://opensource.org/licenses/MIT)

Copyright (c) 2026 Hiroshi Harada
