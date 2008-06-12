.PHONY: clean pylint

clean:
	rm -f *.pyc *.pyo
	rm -f builder/*.pyc builder/*.pyo
	rm -f spitter/*.pyc spitter/*.pyo
	rm -f comparator/*.pyc spitter/*.pyo

pylint:
	pylint --rcfile=.pylintrc --const-rgx='[a-z_][a-z0-9_]{2,30}$$' spitter/main.py --disable-msg=W0403
	pylint --rcfile=.pylintrc spitter/grammar.py
	pylint --rcfile=.pylintrc spitter/logger.py
	pylint --rcfile=.pylintrc spitter/generator.py
