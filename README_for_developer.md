# Usage for Developer
開発者用のドキュメントです。

# Release
GitHubのReleasesからリリースしてください。バージョンはSemantic Versioningに従います。
リリースすると、以下の状態になります。

* パッケージのバージョンは、[uv-dynamic-versioning](https://github.com/ninoseki/uv-dynamic-versioning) でGitHubのバージョンタグから生成されます。`__version__` はインストール済みパッケージのメタデータを参照します。
* 自動でPyPIに公開されます。


# 開発環境

uv 0.13.4 以上と Python 3.11 以上を利用してください。

```sh
uv sync --locked --python 3.11
make lint
```
