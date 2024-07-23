ROOT_DIR := $(shell pwd)
SRC_DIR := $(ROOT_DIR)/freqtrade
TEST_DIR := $(ROOT_DIR)/tests
COMMAND := $(firstword $(MAKECMDGOALS))
ARGUMENTS := $(filter-out --,$(filter-out $(firstword $(MAKECMDGOALS)),$(MAKECMDGOALS)))
EXECUTABLE := $(firstword $(ARGUMENTS))
FIRST_ARGUMENT := $(word 1, $(ARGUMENTS))
SECOND_ARGUMENT := $(word 2, $(ARGUMENTS))
THIRD_ARGUMENT := $(word 3, $(ARGUMENTS))
EXTRA_ARGS_INDEX := $(shell echo $$(($(words $(filter-out --,$(filter $(ARGUMENTS),--))))))
EXTRA_ARGS := $(wordlist $(shell echo $$(($(EXTRA_ARGS_INDEX) + 2))), $(words $(ARGUMENTS)), $(ARGUMENTS))

# https://stackoverflow.com/questions/2214575/passing-arguments-to-make-run
define process_target
  ifeq ($$(firstword $$(MAKECMDGOALS)),$(1))
    # use the rest as arguments for "run"
    RUN_ARGS := $$(wordlist 2,$$(words $$(MAKECMDGOALS)),$$(MAKECMDGOALS))
    # ...and turn them into do-nothing targets
    $$(eval $$(RUN_ARGS):;@:)
  endif
endef

# Define specific targets to process
$(eval $(call process_target,build))
$(eval $(call process_target,test))
$(eval $(call process_target,format))

test:
	@if [ -d ${TEST_DIR}/${FIRST_ARGUMENT} ]; then \
		python -m pytest ${TEST_DIR}/${FIRST_ARGUMENT}; \
	elif [ ${FIRST_ARGUMENT} == "" ]; then \
		python -m pytest ${TEST_DIR}; \
	else \
		echo "Error: ${FIRST_ARGUMENT} is not a directory."; \
	fi;

format:
	@if [ -d ${TEST_DIR}/${FIRST_ARGUMENT} ]; then \
		ruff format ${TEST_DIR}/${FIRST_ARGUMENT}; \
	elif [ ${FIRST_ARGUMENT} == "" ]; then \
		ruff format ${TEST_DIR}; \
	else \
		echo "Error: ${FIRST_ARGUMENT} is not a directory."; \
	fi;