## help - Display callable commands
## develop - Install dev dependencies and symlink the project in virtualenv

all: help

help:
	@echo "Usage: make COMMAND\n"
	@egrep "^##" [Mm]akefile | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'
	@echo "\n"

develop:
	flit install --symlink --deps develop

