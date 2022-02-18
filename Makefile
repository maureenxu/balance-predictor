
venv: .venv/.venv_is_complete
.venv/.venv_is_complete:
	python3 -m venv .venv
	. .venv/bin/activate && pip install cython
	. .venv/bin/activate && pip install -e .
	. .venv/bin/activate && pip install -r requirements.txt
	. .venv/bin/activate && pip install -r requirements-dev.txt
	touch .venv/.venv_is_complete

clean:
	@if [ -d .venv ]; then\
		rm -r .venv;\
	fi

clean_setup: clean venv

setup: venv

lint:
	. .venv/bin/activate && pylint src
	. .venv/bin/activate && black -check src tests

test:
	. .venv/bin/activate && pytest --ignore=tests_old .

cov:
	. .venv/bin/activate && pytest --cov=src --cov-report xml --ignore=tests_old .

fix:
	. .venv/bin/activate && black .

run:
	bash ./run_services.sh