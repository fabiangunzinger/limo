SHELL := /bin/bash

ROOTDIR := $(shell pwd)

DATADIR := data
CODEDIR := code

RAWDATA := $(DATADIR)/raw.csv
CLEANDATA := $(DATADIR)/clean.parquet


# =============================================================================

.PHONY: data
.DELETE_ON_ERROR: $(CLEANDATA)

data:
	@echo 'Preparing data.'
	@python3 $(CODEDIR)/finances/read_monzo.py


# ----------------------------------------------------------------------------

.PHONY: app
app:
	open http://127.0.0.1:8050/
	python3 $(CODEDIR)/app.py


# ------------------------------------------------------------------------------

.PHONY: run

run:
	open http://127.0.0.1:8050/
