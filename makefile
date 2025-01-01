# Variables
DEB_BUILD_DIR = build
SKEL_DIR = root.skel

# Targets
all: build-deb

prepare:
	@echo "Preparing staging area..."
	# Ensure the build directory exists
	mkdir -p $(DEB_BUILD_DIR)
	# Move the contents of the skel directory to the build directory
	cp -r $(SKEL_DIR)/* $(DEB_BUILD_DIR)/

build-deb: prepare
	@echo "Building the .deb package..."
	# Use dpkg-deb or your build tool of choice to build the package
	dpkg-deb --build $(DEB_BUILD_DIR)

clean:
	@echo "Cleaning up..."
	rm -rf $(DEB_BUILD_DIR)

.PHONY: all prepare build-deb clean
