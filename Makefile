export MODULE:=annofab_3dpc
ifndef FORMAT_FILES
	export FORMAT_FILES:=${MODULE} tests
endif
ifndef LINT_FILES
	export LINT_FILES:=${MODULE}
endif

.PHONY: format lint test docs publish

format:
	poetry run autoflake  --in-place --remove-all-unused-imports  --ignore-init-module-imports --recursive ${FORMAT_FILES}
	poetry run isort ${FORMAT_FILES}
	poetry run black ${FORMAT_FILES}

lint:
	poetry run mypy ${LINT_FILES}
	poetry run flake8 ${LINT_FILES}
	poetry run pylint --jobs=0 ${LINT_FILES}

test:
	# 並列実行してレポートも出力する
	poetry run pytest -n auto  --cov=${MODULE} --cov-report=html tests

docs:
	cd docs && poetry run make html

publish:
	poetry publish --build
