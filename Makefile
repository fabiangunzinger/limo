SHELL := /bin/bash

ROOTDIR := $(shell pwd)

DATADIR := data
SRCDIR := src

RAWDATA := $(DATADIR)/raw/raw.csv


data: $(RAWDATA)
	python3 $(SRCDIR)/read_data.py $(RAWDATA)
