ifndef SOURCE_FILES
	export SOURCE_FILES:=annofab_3dpc
endif
ifndef TEST_FILES
	export TEST_FILES:=tests
endif

.PHONY: format lint test docs

format:
	poetry run ruff format ${SOURCE_FILES} ${TEST_FILES}
	poetry run ruff check ${SOURCE_FILES} ${TEST_FILES} --fix-only --exit-zero

lint:
	poetry run ruff check ${SOURCE_FILES}
	poetry run mypy ${SOURCE_FILES}
	poetry run pylint --jobs=0 ${SOURCE_FILES}


test:
	# 並列実行してレポートも出力する
	poetry run pytest -n auto tests

docs:
	cd docs && poetry run make html

