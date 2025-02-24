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

start:  # start supervisord with project service and reverse-proxy tunnel to game-serve
	$(CMD) start
	tail -n 0 --retry --sleep-interval=0.5 --follow log/*.log

restart:  # stop-start supervisord cycle
	$(CMD) stop
	$(CMD) start
	tail -n 0  --retry --sleep-interval=0.5 --follow log/*.log

#

%: Makefile
	@$(CMD) $@


.DEFAULT_GOAL := restart
