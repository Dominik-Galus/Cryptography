format:
	black --line-length 88 src --exclude="src/data/aes_constants" && isort --profile black src 
