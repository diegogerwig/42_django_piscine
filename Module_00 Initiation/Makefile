SHELL := /bin/bash

# Define una macro para el encabezado
HEADER = \
	print_header() { \
		echo "============================================="; \
		echo "============================================="; \
		echo "   🧪 Running tests -> $$1"; \
		echo "============================================="; \
		echo "============================================="; \
	}; \
	print_header

all: test_0

test_0:
	@$(HEADER) "DJANGO MOD_00 EX_00"
	@cd ./ex00 && bash test.sh

clean:
	@echo "Cleaning up..."

fclean: stop clean
	@echo "Full clean..."

re: fclean all

.PHONY: all test_0 test_1 clean fclean re
