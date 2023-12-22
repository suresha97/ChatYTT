build-code-uri:
	bash build_code_uri.sh

deploy-workflows-stack: build-code-uri
	cd chatytt-workflows && \
	sam build && \
	sam deploy

deploy-server-stack: build-code-uri
	cd chatytt-server && \
	sam build && \
	sam deploy

deploy-client-stack:
	cd chatytt-client && \
	sam build && \
	sam deploy
