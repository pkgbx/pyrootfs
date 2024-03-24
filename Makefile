PY_CMD := poetry run python
PYTEST_CMD := ${PY_CMD} -m pytest
TEST_DIR := ./tests

.PHONY: test
test:
	${PYTEST_CMD} ${TEST_DIR}
