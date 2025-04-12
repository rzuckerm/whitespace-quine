INTERACTIVE := $(shell test -t 0 && echo t)
DOCKER_IMAGE := esolang/whitespace:latest
DOCKER_RUN := docker run -i$(INTERACTIVE) -v $(PWD):/local -w /local $(DOCKER_IMAGE)
SRC := src/whitespace_quine/__init__.py
META_GENERATE := .meta-generate
QUINE_FILES := quine.ws*
BLACK := poetry run black -l 100 .

.PHONY: help
help:
	@echo "clean    - Clean generated files"
	@echo "check	- Check formatting"
	@echo "format   - Format code and tests"
	@echo "generate - Generate quine assembly code and assembled program"
	@echo "run      - Run the quine"
	@echo "shell    - Shell into the Whitespace docker image"
	@echo "test     - Test generated code"

.PHONY: format
format:
	$(BLACK)

.PHONY: check
check:
	$(BLACK) --check

.PHONY: generate
generate: $(META_GENERATE)
$(META_GENERATE): $(SRC)
	poetry run python src/whitespace_quine/__init__.py
	touch $@

.PHONY: test
test:
	poetry run pytest -vvl tests

.PHONY: run
run: $(META_GENERATE)
	$(DOCKER_RUN) sh -c 'echo "" | whitespace quine.ws'

.PHONY: shell
shell: $(META_GENERATE)
	$(DOCKER_RUN) sh

.PHONY: clean
clean:
	rm $(META_GENERATE) $(QUINE_FILES)
