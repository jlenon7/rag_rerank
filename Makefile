# Setup the project environment by:
# - Run pipenv shell to start the virtual env.
env:
	pipenv --python=${conda run which python} --site-packages
	pipenv shell 

# Install all libraries of package.
install-all:
	pipenv install --system --dev

# Clone code repositories that will be analyzed.
clone:
	python -m bin.clone

# Ask something to GPT and use the VectorDB information using base RAG architecture.
ask:
	python -m bin.ask

# Insert data in the VectorDB using base RAG architecture.
insert:
	python -m bin.insert
