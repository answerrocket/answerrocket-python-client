dev-install: generate-requirements
	python -m piptools sync requirements.txt

generate-requirements: setup-pip-tools
	pip-compile -o requirements.txt pyproject.toml

setup-pip-tools:
	python -m pip install pip-tools
	
# to run this target you must be able to run an introspection query against a local AnswerRocket server
# pass the id of the tenant you have running when you invoke the target: make generate-gql-schema tenant=yourtenant
generate-gql-schema:
	bash gql-schema-gen.sh $(tenant)