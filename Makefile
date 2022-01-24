
venv: .venv/.venv_is_complete
.venv/.venv_is_complete:
	python3 -m venv .venv
	. .venv/bin/activate && pip install -r requirements.txt
	. .venv/bin/activate && pip install -r requirements-dev.txt
	touch .venv/.venv_is_complete

clean:
	@if [ -d .venv ]; then\
		rm -r .venv;\
	fi

clean_setup: clean venv

setup: venv

test:
	. .venv/bin/activate && pytest . 