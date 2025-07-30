import os
from typing import Optional, Dict, Any
from uuid import UUID

from answer_rocket.client_config import ClientConfig
from answer_rocket.graphql.sdk_operations import Operations
from sgqlc.types import Variable, Arg, non_null, String

from answer_rocket.graphql.client import GraphQlClient
from answer_rocket.graphql.schema import UUID as GQL_UUID, MaxCopilotSkill, MaxCopilot, \
    MaxMutationResponse, CreateMaxCopilotSkillChatQuestionResponse, MaxCopilotQuestionInput, \
    MaxCreateCopilotQuestionResponse, MaxUser, MaxSkillComponent, MaxLLmPrompt, Boolean, HydratedReport


class Config:
    """
    Helper for accessing config, whether local or fetched from the configured server.
    """

    def __init__(self, config: ClientConfig, gql_client: GraphQlClient) -> None:
        self._gql_client = gql_client
        self._config = config
        self.copilot_id = self._config.copilot_id
        self.copilot_skill_id = self._config.copilot_skill_id

    def get_artifact(self, artifact_path: str) -> str:
        """
        artifact path: this is the filepath to your artifact relative to the root of your project.
        Server-side overrides are keyed on this path and will be fetched first when running inside AnswerRocket
        """
        if self._config.is_live_run:
            server_artifact = self._get_artifact_from_server(artifact_path)
            if server_artifact:
                return server_artifact

        # it is possible this could be put inside an else block if the above call were changed to get either the
        # override or the base artifact if one does not exist
        with open(_complete_artifact_path(artifact_path, self._config.resource_base_path)) as artifact_file:
            return artifact_file.read()

    def _get_artifact_from_server(self, artifact_path: str) -> Optional[dict]:
        if not self.copilot_id or not self.copilot_skill_id:
            return None
        artifact_query_args = {
            'copilotId': self.copilot_id,
            'copilotSkillId': self.copilot_skill_id,
            'artifactPath': artifact_path,
        }
        artifact_query_vars = {
            'copilot_id': Arg(non_null(GQL_UUID)),
            'copilot_skill_id': Arg(non_null(GQL_UUID)),
            'artifact_path': Arg(non_null(String)),
        }
        operation = self._gql_client.query(variables=artifact_query_vars)
        copilot_query = operation.get_copilot_skill_artifact_by_path(
            copilot_id=Variable('copilot_id'),
            copilot_skill_id=Variable('copilot_skill_id'),
            artifact_path=Variable('artifact_path'),
        )
        copilot_query.artifact()
        result = self._gql_client.submit(operation, artifact_query_args)
        if result.get_copilot_skill_artifact_by_path and result.get_copilot_skill_artifact_by_path.artifact:
            return result.get_copilot_skill_artifact_by_path.artifact

    def get_copilots(self) -> list[MaxCopilot]:
        """
        Retrieves all copilots available to the user with their metadata.

        Returns:
            list[MaxCopilot]: A list of MaxCopilot objects.
        """
        try:
            op = Operations.query.get_copilots
            result = self._gql_client.submit(op, {})
            return result.get_copilots or []

        except Exception as e:
            print(f"Error retrieving copilots: {e}")
            return []
        
    def get_copilot(self, use_published_version: bool = True, copilot_id: str = None) -> MaxCopilot:
        try:
            query_args = {
                'copilotId': copilot_id or self.copilot_id,
                'usePublishedVersion': use_published_version
            }

            query_vars = {
                'copilot_id': Arg(non_null(GQL_UUID)),
                'use_published_version': Arg(non_null(Boolean))
            }

            operation = self._gql_client.query(variables=query_vars)

            gql_query = operation.get_copilot_info(
                copilot_id=Variable('copilot_id'),
                use_published_version=Variable('use_published_version')
            )

            result = self._gql_client.submit(operation, query_args)

            max_copilot = result.get_copilot_info

            return max_copilot
        except Exception as e:
            print(e)
            return None

    def get_copilot_skill(self, use_published_version: bool = True, copilot_id: str = None, copilot_skill_id: str = None) -> MaxCopilotSkill:
        try:
            query_args = {
                'copilotId': copilot_id or self.copilot_id,
                'copilotSkillId': copilot_skill_id or self.copilot_skill_id,
                'usePublishedVersion': use_published_version
            }

            op = Operations.query.get_copilot_skill

            result = self._gql_client.submit(op, query_args)

            return result.get_copilot_skill
        except Exception as e:
            return None

    def get_skill_components(self) -> [MaxSkillComponent]:
        try:
            query_args = {
            }

            query_vars = {
            }

            operation = self._gql_client.query(variables=query_vars)

            gql_query = operation.get_skill_components(
            )

            result = self._gql_client.submit(operation, query_args)

            skill_components = result.get_skill_components

            return skill_components
        except Exception as e:
            return None

    def get_copilot_hydrated_reports(self, copilot_id: Optional[str] = None, override_dataset_id: Optional[str] = None, load_all_skills: bool = False) -> [HydratedReport]:
        """
        Get hydrated reports for a copilot.

        :param copilot_id: The copilot ID (defaults to the configured copilot_id)
        :param override_dataset_id: Optional dataset ID to override the copilot's default dataset
        :param load_all_skills: Whether to load all skills or just active ones (defaults to False)

        :returns List of hydrated report objects
        """
        try:
            effective_copilot_id = copilot_id or self.copilot_id
            if not effective_copilot_id:
                raise ValueError("copilot_id must be provided or configured")
                
            query_args = {
                'copilotId': effective_copilot_id,
            }
            
            if override_dataset_id:
                query_args['overrideDatasetId'] = override_dataset_id
                
            if load_all_skills:
                query_args['loadAllSkills'] = load_all_skills

            op = Operations.query.get_copilot_hydrated_reports

            result = self._gql_client.submit(op, query_args)

            return result.get_copilot_hydrated_reports
        except Exception as e:
            return None
        
    def create_copilot_skill_chat_question(self, question: str, expected_completion_response: str) -> CreateMaxCopilotSkillChatQuestionResponse:
        try:
            mutation_args = {
                'copilotId': self.copilot_id,
                'copilotSkillId': self.copilot_skill_id,
                'question': question,
                'expectedCompletionResponse': expected_completion_response,
            }

            mutation_vars = {
                'copilot_id': Arg(non_null(GQL_UUID)),
                'copilot_skill_id': Arg(non_null(GQL_UUID)),
                'question': Arg(non_null(String)),
                'expected_completion_response': Arg(non_null(String)),
            }

            operation = self._gql_client.mutation(variables=mutation_vars)

            operation.create_max_copilot_skill_chat_question(
                copilot_id=Variable('copilot_id'),
                copilot_skill_id=Variable('copilot_skill_id'),
                question=Variable('question'),
                expected_completion_response=Variable('expected_completion_response'),
            )

            result = self._gql_client.submit(operation, mutation_args)

            max_mutation_response = result.create_max_copilot_skill_chat_question

            return max_mutation_response
        except Exception as e:
            return None

    def update_copilot_skill_chat_question(self, copilot_skill_chat_question_id: UUID,
                                           question: str, expected_completion_response: str) -> MaxMutationResponse:
        try:
            mutation_args = {
                'copilotId': self.copilot_id,
                'copilotSkillId': self.copilot_skill_id,
                'copilotSkillChatQuestionId': str(copilot_skill_chat_question_id),
                'question': question,
                'expectedCompletionResponse': expected_completion_response,
            }

            mutation_vars = {
                'copilot_id': Arg(non_null(GQL_UUID)),
                'copilot_skill_id': Arg(non_null(GQL_UUID)),
                'copilot_skill_chat_question_id': Arg(non_null(GQL_UUID)),
                'question': Arg(non_null(String)),
                'expected_completion_response': Arg(non_null(String)),
            }

            operation = self._gql_client.mutation(variables=mutation_vars)

            operation.update_max_copilot_skill_chat_question(
                copilot_id=Variable('copilot_id'),
                copilot_skill_id=Variable('copilot_skill_id'),
                copilot_skill_chat_question_id=Variable('copilot_skill_chat_question_id'),
                question=Variable('question'),
                expected_completion_response=Variable('expected_completion_response'),
            )

            result = self._gql_client.submit(operation, mutation_args)

            max_mutation_response = result.update_max_copilot_skill_chat_question

            return max_mutation_response
        except Exception as e:
            return None

    def delete_copilot_skill_chat_question(self, copilot_skill_chat_question_id: UUID) -> MaxMutationResponse:
        try:
            mutation_args = {
                'copilotId': self.copilot_id,
                'copilotSkillId': self.copilot_skill_id,
                'copilotSkillChatQuestionId': str(copilot_skill_chat_question_id)
            }

            mutation_vars = {
                'copilot_id': Arg(non_null(GQL_UUID)),
                'copilot_skill_id': Arg(non_null(GQL_UUID)),
                'copilot_skill_chat_question_id': Arg(non_null(GQL_UUID))
            }

            operation = self._gql_client.mutation(variables=mutation_vars)

            operation.delete_max_copilot_skill_chat_question(
                copilot_id=Variable('copilot_id'),
                copilot_skill_id=Variable('copilot_skill_id'),
                copilot_skill_chat_question_id=Variable('copilot_skill_chat_question_id')
            )

            result = self._gql_client.submit(operation, mutation_args)

            max_mutation_response = result.delete_max_copilot_skill_chat_question

            return max_mutation_response
        except Exception as e:
            return None

    def create_copilot_question(self, nl: str, skill_id: UUID = None, hint: str = None, parameters = None) -> MaxCreateCopilotQuestionResponse:
        try:
            mutation_args = {
                'copilotId': self.copilot_id,
                'copilotQuestion': {
                    'nl': nl,
                    'skillId': skill_id,
                    'hint': hint,
                    'parameters': parameters
                }
            }

            mutation_vars = {
                'copilot_id': Arg(non_null(GQL_UUID)),
                'copilot_question': Arg(non_null(MaxCopilotQuestionInput)),
            }

            operation = self._gql_client.mutation(variables=mutation_vars)

            operation.create_max_copilot_question(
                copilot_id=Variable('copilot_id'),
                copilot_question=Variable('copilot_question')
            )

            result = self._gql_client.submit(operation, mutation_args)

            max_mutation_response = result.create_max_copilot_question

            return max_mutation_response
        except Exception as e:
            return None

    def update_copilot_question(self, copilot_question_id: UUID, nl: str = None, skill_id: UUID = None, hint: str = None, parameters = None) -> MaxMutationResponse:
        try:
            mutation_args = {
                'copilotId': self.copilot_id,
                'copilotQuestionId': str(copilot_question_id),
                'copilotQuestion': {
                    'nl': nl,
                    'skillId': skill_id,
                    'hint': hint,
                    'parameters': parameters
                }
            }

            mutation_vars = {
                'copilot_id': Arg(non_null(GQL_UUID)),
                'copilot_question_id': Arg(non_null(GQL_UUID)),
                'copilot_question': Arg(non_null(MaxCopilotQuestionInput))
            }

            operation = self._gql_client.mutation(variables=mutation_vars)

            operation.update_max_copilot_question(
                copilot_id=Variable('copilot_id'),
                copilot_question_id=Variable('copilot_question_id'),
                copilot_question=Variable('copilot_question')
            )

            result = self._gql_client.submit(operation, mutation_args)

            max_mutation_response = result.update_max_copilot_question

            return max_mutation_response
        except Exception as e:
            return None

    def delete_copilot_chat_question(self, copilot_question_id: UUID) -> MaxMutationResponse:
        try:
            mutation_args = {
                'copilotId': self.copilot_id,
                'copilotQuestionId': str(copilot_question_id)
            }

            mutation_vars = {
                'copilot_id': Arg(non_null(GQL_UUID)),
                'copilot_question_id': Arg(non_null(GQL_UUID))
            }

            operation = self._gql_client.mutation(variables=mutation_vars)

            operation.delete_max_copilot_question(
                copilot_id=Variable('copilot_id'),
                copilot_question_id=Variable('copilot_question_id')
            )

            result = self._gql_client.submit(operation, mutation_args)

            max_mutation_response = result.delete_max_copilot_question

            return max_mutation_response
        except Exception as e:
            return None

    def get_current_user(self) -> MaxUser:
        try:
            query_args = {
            }

            query_vars = {
            }

            operation = self._gql_client.query(variables=query_vars)

            operation.current_user()

            result = self._gql_client.submit(operation, query_args)

            max_user = result.current_user

            return max_user
        except Exception as e:
            return None

    def get_prompt(
            self,
            llm_prompt_id: UUID,
            template_vars: Dict[str, Any],
            k_shot_match: str,
        ) -> MaxLLmPrompt:
        try:
            query_args = {
                'llmPromptId': str(llm_prompt_id),
                'templateVariables': template_vars,
                'kShotMatch': k_shot_match
            }

            op = Operations.query.get_max_llm_prompt

            result = self._gql_client.submit(op, query_args)

            return result.get_max_llm_prompt
        except Exception as e:
            return None


def _complete_artifact_path(artifact_path: str, resource_base_path=None) -> str:
    """
    adjust the path according to the runtime env if needed.
    a noop when running locally, and possibly something we can remove entirely in the future
    """
    if resource_base_path:
        return os.path.join(resource_base_path, artifact_path)
    return artifact_path
