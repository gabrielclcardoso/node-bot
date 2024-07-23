VPATH = .venv/bin/

.venv:
	python -m venv .venv

setup: .venv
	$(VPATH)pip install -r requirements.txt

run: .venv
	@$(VPATH)python srcs/bot.py


install: .venv
	$(VPATH)pip install $(pkg) && $(VPATH)pip freeze > requirements.txt;


.PHONY: install setup
