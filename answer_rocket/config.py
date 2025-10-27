import os
from typing import Optional, Dict, Any
from uuid import UUID

from answer_rocket.client_config import ClientConfig
from answer_rocket.graphql.sdk_operations import Operations
from sgqlc.types import Variable, Arg, non_null, String

from answer_rocket.graphql.client import GraphQlClient
from answer_rocket.graphql.schema import UUID as GQL_UUID, MaxCopilotSkill, MaxCopilot, \
    MaxMutationResponse, MaxCopilotQuestionInput, \
    MaxCreateCopilotQuestionResponse, MaxUser, MaxLLmPrompt, Boolean, HydratedReport


class Config:
    """
    Helper for accessing config, whether local or fetched from the configured server.
    """

    def __init__(self, config: ClientConfig, gql_client: GraphQlClient) -> None:
        """
        Initialize the Config helper.

        Parameters
        ----------
        config : ClientConfig
            The client configuration containing copilot and connection details.
        gql_client : GraphQlClient
            The GraphQL client for making server requests.
        """
        self._gql_client = gql_client
        self._config = config
        self.copilot_id = self._config.copilot_id
        self.copilot_skill_id = self._config.copilot_skill_id


    def get_copilots(self) -> list[MaxCopilot]:
        """
        Retrieve all copilots available to the user with their metadata.

        Returns
        -------
        list[MaxCopilot]
            A list of MaxCopilot objects.
        """
        try:
            op = Operations.query.get_copilots
            result = self._gql_client.submit(op, {})
            return result.get_copilots or []

        except Exception as e:
            print(f"Error retrieving copilots: {e}")
            return []
        
    def get_copilot(self, use_published_version: bool = True, copilot_id: str = None) -> MaxCopilot:
        """
        Retrieve information about a specific copilot.

        Parameters
        ----------
        use_published_version : bool, optional
            Whether to use the published version. Defaults to True.
        copilot_id : str, optional
            The ID of the copilot. If None, uses the configured copilot ID.

        Returns
        -------
        MaxCopilot | None
            The copilot information, or None if an error occurs.
        """
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
        """
        Retrieve information about a specific copilot skill.

        Parameters
        ----------
        use_published_version : bool, optional
            Whether to use the published version. Defaults to True.
        copilot_id : str, optional
            The ID of the copilot. If None, uses the configured copilot ID.
        copilot_skill_id : str, optional
            The ID of the copilot skill. If None, uses the configured skill ID.

        Returns
        -------
        MaxCopilotSkill | None
            The copilot skill information, or None if an error occurs.
        """
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

    def get_copilot_hydrated_reports(self, copilot_id: Optional[str] = None, override_dataset_id: Optional[str] = None, load_all_skills: bool = False) -> [HydratedReport]:
        """
        Get hydrated reports for a copilot.

        Parameters
        ----------
        copilot_id : str, optional
            The copilot ID. Defaults to the configured copilot_id.
        override_dataset_id : str, optional
            Optional dataset ID to override the copilot's default dataset.
        load_all_skills : bool, optional
            Whether to load all skills or just active ones. Defaults to False.

        Returns
        -------
        list[HydratedReport] | None
            List of hydrated report objects, or None if an error occurs.
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

    def create_copilot_question(self, nl: str, skill_id: UUID = None, hint: str = None, parameters = None) -> MaxCreateCopilotQuestionResponse:
        """
        Create a new copilot question.

        Parameters
        ----------
        nl : str
            The natural language question.
        skill_id : UUID, optional
            The ID of the skill to associate with the question.
        hint : str, optional
            A hint for the question.
        parameters : Any, optional
            Additional parameters for the question.

        Returns
        -------
        MaxCreateCopilotQuestionResponse | None
            The response containing the created question, or None if an error occurs.
        """
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
        """
        Update an existing copilot question.

        Parameters
        ----------
        copilot_question_id : UUID
            The ID of the question to update.
        nl : str, optional
            The updated natural language question.
        skill_id : UUID, optional
            The updated skill ID.
        hint : str, optional
            The updated hint.
        parameters : Any, optional
            The updated parameters.

        Returns
        -------
        MaxMutationResponse | None
            The mutation response, or None if an error occurs.
        """
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
        """
        Delete a copilot question.

        Parameters
        ----------
        copilot_question_id : UUID
            The ID of the question to delete.

        Returns
        -------
        MaxMutationResponse | None
            The mutation response, or None if an error occurs.
        """
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
        """
        Retrieve information about the current authenticated user.

        Returns
        -------
        MaxUser | None
            The current user information, or None if an error occurs.
        """
        try:
            query_args = {}

            op = Operations.query.current_user

            result = self._gql_client.submit(op, query_args)

            return result.current_user
        except Exception as e:
            return None

    def get_prompt(
            self,
            llm_prompt_id: UUID,
            template_vars: Dict[str, Any],
            k_shot_match: str,
        ) -> MaxLLmPrompt:
        """
        Retrieve an LLM prompt with template variables and k-shot matching.

        Parameters
        ----------
        llm_prompt_id : UUID
            The ID of the LLM prompt to retrieve.
        template_vars : Dict[str, Any]
            Template variables to substitute in the prompt.
        k_shot_match : str
            The k-shot matching criteria.

        Returns
        -------
        MaxLLmPrompt | None
            The LLM prompt with substitutions applied, or None if an error occurs.
        """
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

    def clear_copilot_cache(self, copilot_id: UUID = None) -> MaxMutationResponse:
        """
        Clear the cache for a copilot.

        Parameters
        ----------
        copilot_id : UUID, optional
            The ID of the copilot to clear cache for. If None, uses the configured copilot ID.

        Returns
        -------
        MaxMutationResponse
            The response from the clear cache operation, or None if an error occurs.
        """
        try:
            mutation_args = {
                'copilotId': str(copilot_id) if copilot_id else self.copilot_id,
            }

            mutation_vars = {
                'copilot_id': Arg(non_null(GQL_UUID)),
            }

            operation = self._gql_client.mutation(variables=mutation_vars)

            operation.clear_copilot_cache(
                copilot_id=Variable('copilot_id')
            )

            result = self._gql_client.submit(operation, mutation_args)

            return result.clear_copilot_cache
        except Exception as e:
            return None
