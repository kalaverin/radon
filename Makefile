# it's just wrapper around xc, but with some additional features
#
# home site  https://xcfile.dev
# source     https://github.com/joerdav/xc

CONFIG := $(or $(EXECUTE_FILE), TASKS.md)
CMD := xc -file $(CONFIG)
export XC := $(CMD)


execute:  # deploy eXeCute tool (xc)
	go install golang.org/dl/go1.22.6@latest && \
	go install github.com/joerdav/xc/cmd/xc@latest

#

%: Makefile
	@$(CMD) $@


.DEFAULT_GOAL := lint
