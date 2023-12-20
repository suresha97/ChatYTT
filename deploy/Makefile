build-code-uri:
	bash build_code_uri.sh

deploy-workflows-stack: build-code-uri
	cd chatytt-workflows && \
	sam build && \
	sam deploy

deploy-api-stack: build-code-uri
	cd chatytt-api && \
	sam build && \
	sam deploy

deploy-webapp-stack:
	cd chatytt-webapp && \
	sam build && \
	sam deploy
