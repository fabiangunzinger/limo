SHELL := /bin/bash

ROOTDIR := $(shell pwd)

DATADIR := data
SRCDIR := src

RAWDATA := $(DATADIR)/raw.csv
CLEANDATA := $(DATADIR)/clean.parquet


# =============================================================================

.PHONY: data
.DELETE_ON_ERROR: $(CLEANDATA)

data:
	@echo 'Preparing data.'
	@python3 $(SRCDIR)/read_data.py


# ----------------------------------------------------------------------------

.PHONY: app
app: $(CLEANDATA)
	open http://127.0.0.1:8050/
	python3 $(SRCDIR)/app.py


# ------------------------------------------------------------------------------

.PHONY: run

run:
	open http://127.0.0.1:8050/
