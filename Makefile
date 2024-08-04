# Make bash the shell
SHELL := /bin/bash
ONESHELL:

ROOT_DIR := $(shell pwd)
SRC_DIR := $(ROOT_DIR)/simple_python_template
C_SRC_DIR := $(ROOT_DIR)/sources
C_INCLUDE_DIR := $(ROOT_DIR)/include
C_VENDORS_DIR := $(ROOT_DIR)/vendors
TEST_DIR := $(ROOT_DIR)/tests
COMMAND := $(firstword $(MAKECMDGOALS))
ARGUMENTS := $(filter-out --,$(filter-out $(firstword $(MAKECMDGOALS)),$(MAKECMDGOALS)))
EXECUTABLE := $(firstword $(ARGUMENTS))
FIRST_ARGUMENT := $(word 1, $(ARGUMENTS))
SECOND_ARGUMENT := $(word 2, $(ARGUMENTS))
THIRD_ARGUMENT := $(word 3, $(ARGUMENTS))
EXTRA_ARGS_INDEX := $(shell echo $$(($(words $(filter-out --,$(filter $(ARGUMENTS),--))))))
EXTRA_ARGS := $(wordlist $(shell echo $$(($(EXTRA_ARGS_INDEX) + 2))), $(words $(ARGUMENTS)), $(ARGUMENTS))

TESTING_IN_DOCKER_IMAGE_NAME = testing_in_docker
C_SOURCE_FILES := $(wildcard $(C_SRC_DIR)/**.c)

# https://stackoverflow.com/questions/2214575/passing-arguments-to-make-run
define process_target
  ifeq ($$(firstword $$(MAKECMDGOALS)),$(1))
    # Use the rest as arguments for "run"
    RUN_ARGS := $$(wordlist 2,$$(words $$(MAKECMDGOALS)),$$(MAKECMDGOALS))
    # ... and turn them into do-nothing targets
    $$(eval $$(RUN_ARGS):;@:)
  endif
endef

# Define the cmake-format command
CLANG_FORMAT = clang-format -i

# Define specific targets to process
TARGETS := build test format test-in-docker list

$(foreach target,$(TARGETS),$(eval $(call process_target,$(target))))

list:
	echo "Here are the list of targets: [$(TARGETS)]";

test-in-docker:
	docker build -f Dockerfile_testing -t $(TESTING_IN_DOCKER_IMAGE_NAME) .
	docker run --rm -it --name $(TESTING_IN_DOCKER_IMAGE_NAME) $(TESTING_IN_DOCKER_IMAGE_NAME)

test:
	@if [ -d $(TEST_DIR)/$(FIRST_ARGUMENT) ]; then \
		python -m pytest $(TEST_DIR)/$(FIRST_ARGUMENT) --cov -s -vv; \
	elif [ "$(FIRST_ARGUMENT)" == "" ]; then \
		python -m pytest $(TEST_DIR) --cov -s -vv; \
	else \
		echo "Error: $(FIRST_ARGUMENT) is not a directory."; \
	fi;

format-test:
	@if [ -d $(TEST_DIR)/$(FIRST_ARGUMENT) ]; then \
		ruff format $(TEST_DIR)/$(FIRST_ARGUMENT); \
	elif [ "$(FIRST_ARGUMENT)" == "" ]; then \
		ruff format $(TEST_DIR); \
	else \
		echo "Error: $(FIRST_ARGUMENT) is not a directory."; \
	fi;

format:
	@if [ -d $(SRC_DIR)/$(FIRST_ARGUMENT) ]; then \
		ruff format $(SRC_DIR)/$(FIRST_ARGUMENT); \
	elif [ "$(FIRST_ARGUMENT)" == "" ]; then \
		ruff format $(SRC_DIR); \
	else \
		echo "Error: $(FIRST_ARGUMENT) is not a directory."; \
	fi; \
	echo "Formatting C source files now using $(CLANG_FORMAT)"; \
	for file in $(C_SOURCE_FILES); do \
		echo "Formatting $$file now..."; \
		$(CLANG_FORMAT) $$file; \
	done; \
	echo "Formatting is done!";

check:
	@if [ -d $(SRC_DIR)/$(FIRST_ARGUMENT) ]; then \
		ruff check $(SRC_DIR)/$(FIRST_ARGUMENT); \
	elif [ "$(FIRST_ARGUMENT)" == "" ]; then \
		ruff check $(SRC_DIR); \
	else \
		echo "Error: $(FIRST_ARGUMENT) is not a directory."; \
	fi;
