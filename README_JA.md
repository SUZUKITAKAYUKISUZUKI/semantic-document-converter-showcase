# Semantic Document Converter — 日本語ポートフォリオ

OCR・画像認識・ローカルAIを組み合わせた、原文忠実型の文書変換パイプライン

[English / Technical Engineering Showcase](README.md)

## 30秒で分かる概要

Semantic Document Converter（SDC）は、ページ画像から読みやすいMarkdownを生成するPythonベースの個人開発プロジェクトです。

一般的なOCRによる文字抽出だけでなく、文書のレイアウトや読み順、コード、数式、図表をそれぞれ扱い、AIによる不正確な補完を抑える検証処理も組み込んでいます。

本体のproduction implementationはPrivateで、このRepositoryでは設計・実装・検証能力を公開可能な範囲で紹介しています。

## このプロジェクトで実装したこと

- OCRを利用したページ画像からのテキスト抽出
- 見出し、本文、読み順などの文書構造の保持
- コード、数式、表、図、ダイアグラムの個別処理
- ローカルVisionモデルやLLMとの連携（Gemma 4 / FreeToken Kaiの明示的な検証経路を追加）
- Mermaid候補と、元画像だけから独立に抽出したノード・辺・ラベルを照合し、不確実な図は元画像として保持
- OCR結果やAI提案をそのまま採用しない決定論的な検証
- 元画像を根拠として局所的な修正だけを許可する設計
- Inspector、Corrector、Verifierによる役割分担型の確認処理
- 長時間処理を途中から再開するcheckpoint / resume
- 処理判断を後から追跡できるaudit設計
- Python CLIとしての処理フロー設計

単に「読める文章」を生成するのではなく、元資料に存在しない内容を加えず、確認できない箇所を推測で埋めないことを重視しています。

## この経験を活かせる案件

以下は過去の受注実績ではなく、本プロジェクトで培った技術を活用して対応可能と考えられる案件例です。

- Pythonによる文書処理・データ変換の自動化
- OCRツールの開発、精度改善、後処理設計
- PDFや画像からの情報抽出・構造化
- AI / LLMを組み込んだ社内向け業務ツール
- Ollamaを利用したローカルAI環境の構築
- Computer Visionを使った画像・文書データ処理
- LLM出力のJSON化、検証、誤出力抑制
- 長時間バッチ処理の中断・再開、障害復旧設計
- API / CLIベースの業務自動化

案件ごとに、入力形式、必要な精度、処理量、利用環境、確認方法を整理したうえで、実装範囲を提案できます。

## Semantic Processing Suite

SDCは、文書を段階的に処理する **Semantic Processing Suite** の上流コンポーネントです。

```text
Source Document
      ↓
SDC — Semantic Document Converter
      ↓
Source-faithful Reader Markdown
      ↓
SKC — Semantic Knowledge Crystallizer
      ↓
*_knowledge
      ↓
SLC — Semantic Logic Compiler
      ↓
*_logic
```

- **SDC:** 原資料をMarkdownとして忠実に再構成する層
- **SKC:** Markdownを再利用可能な知識資源へ整理する層
- **SLC:** 知識資源から明示的な論理資源を生成する層

SDCが要約や意味の再解釈を意図的に行わないのは、原資料の再構成と、後段の知識化・論理化を別の責務として扱うためです。

後段のSKC / SLCについては、[Semantic Knowledge Pipeline](https://github.com/SUZUKITAKAYUKISUZUKI/semantic-knowledge-pipeline-showcase)をご覧ください。

## 技術スタック

- Python
- OCR / 文書処理
- Computer Vision
- ローカルVLM / LLM
- Ollama / Gemma 4 / FreeToken Kai
- ローカルのOpenAI互換HTTP API
- Markdown / 構造化データ
- Structured Output
- 決定論的な検証
- CLI application design
- 中断・再開可能なバッチ処理

## 開発状況

**Status: Active Development / Release Qualification**

**状態確認日：2026-09-14。** 非公開側の最新READMEと実装（未コミットの開発変更を含む）に基づく開発状況であり、リリース済みビルドの説明ではありません。

SDC v0.2.0は引き続きRelease Qualification中で、release-lockedではありません。

| 検証段階 | 記録されている結果 |
| --- | --- |
| RQ-0〜RQ-3 | PASS：既存の統合・finishingの段階検証 |
| RQ-4 | HOLD：大規模文書でのリリース判定は未完了 |
| RQ5B | 検証モデルとして `nvidia/Gemma-4-26B-A4B-NVFP4` を選定 |
| RQ6b | HOLD：105ページの変換は完了。不正な視覚応答は元画像として保持したが、Kaiが出力予算を32トークンへ縮小し、最初のCorrector要求でFinishが停止 |

**RQ6bでは完成したReaderを生成できていません。** 変換の完了は、原文忠実性や一連の処理の合格を意味しません。単純グラフの実機smokeでも独立照合の応答が不正だったため画像保持となり、Mermaidの実機採用経路は未認定です。以前の見出し装飾の誤認識は既知リスクとしてクローズされており、修正済みとは扱っていません。

Gemmaは選定モデルとして維持していますが、検証合格までは既定のOllama構成を変更しません。Gemma経路では、Inspector・Corrector・Verifierを独立した逐次HTTP要求で実行します。JSONの欠落補完や別モデルへの自動切替は行わず、利用できない視覚応答は元画像を残し、原文照合や通信の失敗は明示的に停止します。

検証結果は非公開の開発記録からの要約です。実書籍の画像・内部テスト・生の検証データは公開していません。

完成済み製品やproduction-readyなシステムとして公開しているものではありません。

## 公開範囲

- 本体のproduction implementationはPrivateです
- このRepositoryは個人Engineering ProjectのPortfolio Showcaseです
- `demo/`の文章と画像はすべてsyntheticです
- `snippets/`はPortfolio用に新規作成した簡略例です
- 実書籍、著作物、顧客データ由来の内容は含みません
- Production code、内部prompt、qualification dataは公開していません
- OSS distributionではありません

## 詳細な技術情報

詳細なArchitecture、Engineering Case Study、Synthetic Demo、Representative Codeについては、[英語版README](README.md)をご覧ください。
