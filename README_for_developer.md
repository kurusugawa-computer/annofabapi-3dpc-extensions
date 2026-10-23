# Usage for Developer
開発者用のドキュメントです。

# Release
GitHubのReleasesからリリースしてください。バージョンはSemantic Versioningに従います。
リリースすると、以下の状態になります。

* パッケージのバージョンは、[uv-dynamic-versioning](https://github.com/ninoseki/uv-dynamic-versioning) でGitHubのバージョンタグから生成されます。`__version__` はインストール済みパッケージのメタデータを参照します。
* 自動でPyPIに公開されます。


# 開発環境

uv 0.13.4 以上と Python 3.12+を利用してください。

```sh
uv sync --locked --python 3.12
make lint
```

lint・整形には Ruff、型検査には mypy を利用します。`make format` で整形し、`make lint` でチェックしてください。

## シークレット検査

`make gitleaks` で現在のブランチの Git 履歴を検査します。gitleaks をインストール済みならそのコマンドを使い、未インストールなら Docker で v8.30.1 を実行します。検出値はログでマスクします。CI でも同じ検査を実行します。

コミット前の差分検査には pre-commit フックを利用できます。

```sh
uv sync --locked
uv run pre-commit install
```
