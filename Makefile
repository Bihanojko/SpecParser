.PHONY: test

run:
ifdef SPEC
	python abstract_model.py -i ${SPEC}
endif
ifndef SPEC
	python abstract_model.py
endif

test:
	python tests.py
