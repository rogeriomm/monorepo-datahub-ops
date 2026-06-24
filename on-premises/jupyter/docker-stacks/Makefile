.PHONY: test

SHELL:=bash
REGISTRY?=quay.io
OWNER?=jupyter
TAG?=latest

# Enable BuildKit for Docker build
export DOCKER_BUILDKIT:=1

# All the images listed in the build dependency order
ALL_IMAGES:= \
	docker-stacks-foundation \
	base-notebook \
	minimal-notebook \
	scipy-notebook \
	r-notebook \
	julia-notebook \
	tensorflow-notebook \
	pytorch-notebook \
	datascience-notebook \
	pyspark-notebook \
	all-spark-notebook

# Note that `ROOT_IMAGE` and `PYTHON_VERSION` arguments are only applicable to the `docker-stacks-foundation` image
build/%: DOCKER_BUILD_ARGS?=
build/%: ROOT_IMAGE?=ubuntu:24.04
build/%: PYTHON_VERSION?=3.12
build/%: ## build the latest image for a stack using the system's architecture
	docker build $(DOCKER_BUILD_ARGS) --rm --force-rm \
	  --tag "$(REGISTRY)/$(OWNER)/$(notdir $@):$(TAG)" \
	  "./images/$(notdir $@)" \
	  --build-arg REGISTRY="$(REGISTRY)" \
	  --build-arg OWNER="$(OWNER)" \
	  --build-arg ROOT_IMAGE="$(ROOT_IMAGE)" \
	  --build-arg PYTHON_VERSION="$(PYTHON_VERSION)"
	@echo -n "Built image size: "
	@docker images "$(REGISTRY)/$(OWNER)/$(notdir $@):latest" --format "{{.Size}}"
	docker save "$(REGISTRY)/$(OWNER)/$(notdir $@):$(TAG)" -o "$(notdir $@)_$(TAG).tar"
build-all: $(foreach I, $(ALL_IMAGES), build/$(I)) ## build all stacks



check-outdated/%: ## check the outdated mamba/conda packages in a stack and produce a report
	@TEST_IMAGE="$(REGISTRY)/$(OWNER)/$(notdir $@)" pytest tests/by_image/docker-stacks-foundation/test_outdated.py
check-outdated-all: $(foreach I, $(ALL_IMAGES), check-outdated/$(I)) ## check all the stacks for outdated packages



cont-stop-all: ## stop all containers
	@echo "Stopping all containers ..."
	-docker stop --time 0 $(shell docker ps --all --quiet) 2> /dev/null
cont-rm-all: ## remove all containers
	@echo "Removing all containers ..."
	-docker rm --force $(shell docker ps --all --quiet) 2> /dev/null
cont-clean-all: cont-stop-all cont-rm-all ## clean all containers (stop + rm)


img-list: ## list jupyter images
	@echo "Listing $(OWNER) images ..."
	docker images "$(OWNER)/*"
	docker images "*/$(OWNER)/*"
img-rm-dang: ## remove dangling images (tagged None)
	@echo "Removing dangling images ..."
	-docker rmi --force $(shell docker images -f "dangling=true" --quiet) 2> /dev/null
img-rm-jupyter: ## remove jupyter images
	@echo "Removing $(OWNER) images ..."
	-docker rmi --force $(shell docker images --quiet "$(OWNER)/*") 2> /dev/null
	-docker rmi --force $(shell docker images --quiet "*/$(OWNER)/*") 2> /dev/null
img-rm: img-rm-dang img-rm-jupyter ## remove dangling and jupyter images



pull/%: ## pull a jupyter image
	docker pull "$(REGISTRY)/$(OWNER)/$(notdir $@)"
pull-all: $(foreach I, $(ALL_IMAGES), pull/$(I)) ## pull all images
push/%: ## push all tags for a jupyter image
	docker push --all-tags "$(REGISTRY)/$(OWNER)/$(notdir $@)"
push-all: $(foreach I, $(ALL_IMAGES), push/$(I)) ## push all tagged images



run-shell/%: ## run a bash in interactive mode in a stack
	docker run -it --rm "$(REGISTRY)/$(OWNER)/$(notdir $@)" $(SHELL)
run-sudo-shell/%: ## run bash in interactive mode as root in a stack
	docker run -it --rm --user root "$(REGISTRY)/$(OWNER)/$(notdir $@)" $(SHELL)



test/%: ## run tests against a stack
	python3 -m tests.run_tests \
	  --registry "$(REGISTRY)" \
	  --owner "$(OWNER)" \
	  --image "$(notdir $@)"
test-all: $(foreach I, $(ALL_IMAGES), test/$(I)) ## test all stacks
