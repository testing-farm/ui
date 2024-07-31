.DEFAULT_GOAL := help

IMAGE_NAME ?= quay.io/testing-farm/ui
# default image tag set to current user name
IMAGE_TAG ?= ${USER}

##@ Containers

container/build:  ## Build container
	poetry build
	poetry export -f requirements.txt --output requirements.txt
	buildah bud -t $(IMAGE_NAME):$(IMAGE_TAG) -f container/Containerfile .

container/push:  ## Push containers
	buildah push $(IMAGE_NAME):$(IMAGE_TAG)

# See https://www.thapaliya.com/en/writings/well-documented-makefiles/ for details.
reverse = $(if $(1),$(call reverse,$(wordlist 2,$(words $(1)),$(1)))) $(firstword $(1))

help:  ## Show this help
	@awk 'BEGIN {FS = ":.*##"; printf "$(info $(PRELUDE))"} /^[a-zA-Z_/-]+:.*?##/ { printf "  \033[36m%-35s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(call reverse, $(MAKEFILE_LIST))
