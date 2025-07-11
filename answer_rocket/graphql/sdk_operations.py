import sgqlc.types
import sgqlc.operation
from . import schema

_schema = schema
_schema_root = _schema.schema

__all__ = ('Operations',)


def fragment_chat_result_fragment():
    _frag = sgqlc.operation.Fragment(_schema.MaxChatResult, 'ChatResultFragment')
    _frag.answer_id()
    _frag.thread_id()
    _frag.chat_pipeline_profile()
    _frag.general_diagnostics()
    _frag.answered_at()
    _frag.copilot_skill_id()
    _frag.has_finished()
    _frag.error()
    _frag.is_new_thread()
    _frag.message()
    _frag_report_results = _frag.report_results()
    _frag_report_results.title()
    _frag_report_results.report_name()
    _frag_report_results_parameters = _frag_report_results.parameters()
    _frag_report_results_parameters.key()
    _frag_report_results_parameters.values()
    _frag_report_results_parameters.label()
    _frag_report_results.custom_payload()
    _frag_report_results_content_blocks = _frag_report_results.content_blocks()
    _frag_report_results_content_blocks.id()
    _frag_report_results_content_blocks.title()
    _frag_report_results_content_blocks.layout_json()
    _frag.thread_id()
    _frag.user_id()
    return _frag


class Fragment:
    chat_result_fragment = fragment_chat_result_fragment()


def mutation_ask_chat_question():
    _op = sgqlc.operation.Operation(_schema_root.mutation_type, name='AskChatQuestion', variables=dict(copilotId=sgqlc.types.Arg(sgqlc.types.non_null(_schema.UUID)), question=sgqlc.types.Arg(sgqlc.types.non_null(_schema.String)), threadId=sgqlc.types.Arg(_schema.UUID), skipReportCache=sgqlc.types.Arg(_schema.Boolean), dryRunType=sgqlc.types.Arg(_schema.ChatDryRunType), modelOverrides=sgqlc.types.Arg(sgqlc.types.list_of(_schema.ModelOverride)), indicatedSkills=sgqlc.types.Arg(sgqlc.types.list_of(_schema.String)), history=sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(_schema.MessageHistoryInput))), questionType=sgqlc.types.Arg(_schema.QuestionType), threadType=sgqlc.types.Arg(_schema.ThreadType)))
    _op_ask_chat_question = _op.ask_chat_question(copilot_id=sgqlc.types.Variable('copilotId'), question=sgqlc.types.Variable('question'), thread_id=sgqlc.types.Variable('threadId'), skip_report_cache=sgqlc.types.Variable('skipReportCache'), dry_run_type=sgqlc.types.Variable('dryRunType'), model_overrides=sgqlc.types.Variable('modelOverrides'), indicated_skills=sgqlc.types.Variable('indicatedSkills'), history=sgqlc.types.Variable('history'), question_type=sgqlc.types.Variable('questionType'), thread_type=sgqlc.types.Variable('threadType'))
    _op_ask_chat_question.id()
    _op_ask_chat_question.thread_id()
    _op_ask_chat_question_answer = _op_ask_chat_question.answer()
    _op_ask_chat_question_answer.__fragment__(fragment_chat_result_fragment())
    return _op


def mutation_queue_chat_question():
    _op = sgqlc.operation.Operation(_schema_root.mutation_type, name='QueueChatQuestion', variables=dict(threadId=sgqlc.types.Arg(sgqlc.types.non_null(_schema.UUID)), question=sgqlc.types.Arg(sgqlc.types.non_null(_schema.String)), skipCache=sgqlc.types.Arg(_schema.Boolean), modelOverrides=sgqlc.types.Arg(sgqlc.types.list_of(_schema.ModelOverride)), indicatedSkills=sgqlc.types.Arg(sgqlc.types.list_of(_schema.String)), history=sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(_schema.MessageHistoryInput)))))
    _op_queue_chat_question = _op.queue_chat_question(thread_id=sgqlc.types.Variable('threadId'), question=sgqlc.types.Variable('question'), skip_cache=sgqlc.types.Variable('skipCache'), model_overrides=sgqlc.types.Variable('modelOverrides'), indicated_skills=sgqlc.types.Variable('indicatedSkills'), history=sgqlc.types.Variable('history'))
    _op_queue_chat_question.thread_id()
    _op_queue_chat_question.id()
    return _op


def mutation_cancel_chat_question():
    _op = sgqlc.operation.Operation(_schema_root.mutation_type, name='CancelChatQuestion', variables=dict(entryId=sgqlc.types.Arg(sgqlc.types.non_null(_schema.UUID))))
    _op_cancel_chat_question = _op.cancel_chat_question(entry_id=sgqlc.types.Variable('entryId'))
    _op_cancel_chat_question.thread_id()
    _op_cancel_chat_question.id()
    return _op


def mutation_create_chat_thread():
    _op = sgqlc.operation.Operation(_schema_root.mutation_type, name='CreateChatThread', variables=dict(copilotId=sgqlc.types.Arg(sgqlc.types.non_null(_schema.UUID))))
    _op_create_chat_thread = _op.create_chat_thread(copilot_id=sgqlc.types.Variable('copilotId'))
    _op_create_chat_thread.id()
    _op_create_chat_thread.copilot_id()
    return _op


def mutation_add_feedback():
    _op = sgqlc.operation.Operation(_schema_root.mutation_type, name='AddFeedback', variables=dict(entryId=sgqlc.types.Arg(sgqlc.types.non_null(_schema.UUID)), feedbackType=sgqlc.types.Arg(sgqlc.types.non_null(_schema.FeedbackType)), message=sgqlc.types.Arg(_schema.String)))
    _op.add_feedback(entry_id=sgqlc.types.Variable('entryId'), feedback_type=sgqlc.types.Variable('feedbackType'), message=sgqlc.types.Variable('message'))
    return _op


def mutation_set_skill_memory():
    _op = sgqlc.operation.Operation(_schema_root.mutation_type, name='SetSkillMemory', variables=dict(entryId=sgqlc.types.Arg(sgqlc.types.non_null(_schema.UUID)), skillMemoryPayload=sgqlc.types.Arg(sgqlc.types.non_null(_schema.JSON))))
    _op.set_skill_memory(entry_id=sgqlc.types.Variable('entryId'), skill_memory_payload=sgqlc.types.Variable('skillMemoryPayload'))
    return _op


def mutation_create_dimension():
    _op = sgqlc.operation.Operation(_schema_root.mutation_type, name='CreateDimension', variables=dict(datasetId=sgqlc.types.Arg(sgqlc.types.non_null(_schema.UUID)), dimension=sgqlc.types.Arg(sgqlc.types.non_null(_schema.JSON))))
    _op_create_dimension = _op.create_dimension(dataset_id=sgqlc.types.Variable('datasetId'), dimension=sgqlc.types.Variable('dimension'))
    _op_create_dimension.success()
    _op_create_dimension.code()
    _op_create_dimension.error()
    return _op


def mutation_update_dimension():
    _op = sgqlc.operation.Operation(_schema_root.mutation_type, name='UpdateDimension', variables=dict(datasetId=sgqlc.types.Arg(sgqlc.types.non_null(_schema.UUID)), dimension=sgqlc.types.Arg(sgqlc.types.non_null(_schema.JSON))))
    _op_update_dimension = _op.update_dimension(dataset_id=sgqlc.types.Variable('datasetId'), dimension=sgqlc.types.Variable('dimension'))
    _op_update_dimension.success()
    _op_update_dimension.code()
    _op_update_dimension.error()
    return _op


def mutation_delete_dimension():
    _op = sgqlc.operation.Operation(_schema_root.mutation_type, name='DeleteDimension', variables=dict(datasetId=sgqlc.types.Arg(sgqlc.types.non_null(_schema.UUID)), dimensionId=sgqlc.types.Arg(sgqlc.types.non_null(_schema.String))))
    _op_delete_dimension = _op.delete_dimension(dataset_id=sgqlc.types.Variable('datasetId'), dimension_id=sgqlc.types.Variable('dimensionId'))
    _op_delete_dimension.success()
    _op_delete_dimension.code()
    _op_delete_dimension.error()
    return _op


def mutation_create_metric():
    _op = sgqlc.operation.Operation(_schema_root.mutation_type, name='CreateMetric', variables=dict(datasetId=sgqlc.types.Arg(sgqlc.types.non_null(_schema.UUID)), metric=sgqlc.types.Arg(sgqlc.types.non_null(_schema.JSON))))
    _op_create_metric = _op.create_metric(dataset_id=sgqlc.types.Variable('datasetId'), metric=sgqlc.types.Variable('metric'))
    _op_create_metric.success()
    _op_create_metric.code()
    _op_create_metric.error()
    return _op


def mutation_update_metric():
    _op = sgqlc.operation.Operation(_schema_root.mutation_type, name='UpdateMetric', variables=dict(datasetId=sgqlc.types.Arg(sgqlc.types.non_null(_schema.UUID)), metric=sgqlc.types.Arg(sgqlc.types.non_null(_schema.JSON))))
    _op_update_metric = _op.update_metric(dataset_id=sgqlc.types.Variable('datasetId'), metric=sgqlc.types.Variable('metric'))
    _op_update_metric.success()
    _op_update_metric.code()
    _op_update_metric.error()
    return _op


def mutation_delete_metric():
    _op = sgqlc.operation.Operation(_schema_root.mutation_type, name='DeleteMetric', variables=dict(datasetId=sgqlc.types.Arg(sgqlc.types.non_null(_schema.UUID)), metricId=sgqlc.types.Arg(sgqlc.types.non_null(_schema.String))))
    _op_delete_metric = _op.delete_metric(dataset_id=sgqlc.types.Variable('datasetId'), metric_id=sgqlc.types.Variable('metricId'))
    _op_delete_metric.success()
    _op_delete_metric.code()
    _op_delete_metric.error()
    return _op


def mutation_update_loading_message():
    _op = sgqlc.operation.Operation(_schema_root.mutation_type, name='UpdateLoadingMessage', variables=dict(answerId=sgqlc.types.Arg(sgqlc.types.non_null(_schema.UUID)), message=sgqlc.types.Arg(sgqlc.types.non_null(_schema.String))))
    _op.update_loading_message(answer_id=sgqlc.types.Variable('answerId'), message=sgqlc.types.Variable('message'))
    return _op


class Mutation:
    add_feedback = mutation_add_feedback()
    ask_chat_question = mutation_ask_chat_question()
    cancel_chat_question = mutation_cancel_chat_question()
    create_chat_thread = mutation_create_chat_thread()
    create_dimension = mutation_create_dimension()
    create_metric = mutation_create_metric()
    delete_dimension = mutation_delete_dimension()
    delete_metric = mutation_delete_metric()
    queue_chat_question = mutation_queue_chat_question()
    set_skill_memory = mutation_set_skill_memory()
    update_dimension = mutation_update_dimension()
    update_loading_message = mutation_update_loading_message()
    update_metric = mutation_update_metric()


def query_chat_entry():
    _op = sgqlc.operation.Operation(_schema_root.query_type, name='ChatEntry', variables=dict(id=sgqlc.types.Arg(sgqlc.types.non_null(_schema.UUID))))
    _op_chat_entry = _op.chat_entry(id=sgqlc.types.Variable('id'))
    _op_chat_entry.id()
    _op_chat_entry.thread_id()
    _op_chat_entry_question = _op_chat_entry.question()
    _op_chat_entry_question.asked_at()
    _op_chat_entry_question.nl()
    _op_chat_entry_answer = _op_chat_entry.answer()
    _op_chat_entry_answer.__fragment__(fragment_chat_result_fragment())
    _op_chat_entry.feedback()
    _op_chat_entry.user()
    _op_chat_entry.skill_memory_payload()
    return _op


def query_dataframes_for_entry():
    _op = sgqlc.operation.Operation(_schema_root.query_type, name='DataframesForEntry', variables=dict(entryId=sgqlc.types.Arg(sgqlc.types.non_null(_schema.UUID))))
    _op_chat_entry = _op.chat_entry(id=sgqlc.types.Variable('entryId'))
    _op_chat_entry.id()
    _op_chat_entry_answer = _op_chat_entry.answer()
    _op_chat_entry_answer_report_results = _op_chat_entry_answer.report_results()
    _op_chat_entry_answer_report_results.gzipped_dataframes_and_metadata()
    return _op


def query_chat_thread():
    _op = sgqlc.operation.Operation(_schema_root.query_type, name='ChatThread', variables=dict(id=sgqlc.types.Arg(sgqlc.types.non_null(_schema.UUID))))
    _op_chat_thread = _op.chat_thread(id=sgqlc.types.Variable('id'))
    _op_chat_thread.id()
    _op_chat_thread.entry_count()
    _op_chat_thread.title()
    _op_chat_thread.copilot_id()
    _op_chat_thread_entries = _op_chat_thread.entries()
    _op_chat_thread_entries.id()
    _op_chat_thread_entries.thread_id()
    _op_chat_thread_entries_answer = _op_chat_thread_entries.answer()
    _op_chat_thread_entries_answer.__fragment__(fragment_chat_result_fragment())
    _op_chat_thread_entries.skill_memory_payload()
    return _op


def query_all_chat_entries():
    _op = sgqlc.operation.Operation(_schema_root.query_type, name='AllChatEntries', variables=dict(offset=sgqlc.types.Arg(_schema.Int), limit=sgqlc.types.Arg(_schema.Int), filters=sgqlc.types.Arg(_schema.JSON)))
    _op_all_chat_entries = _op.all_chat_entries(offset=sgqlc.types.Variable('offset'), limit=sgqlc.types.Variable('limit'), filters=sgqlc.types.Variable('filters'))
    _op_all_chat_entries.id()
    _op_all_chat_entries.thread_id()
    _op_all_chat_entries_question = _op_all_chat_entries.question()
    _op_all_chat_entries_question.asked_at()
    _op_all_chat_entries_question.nl()
    _op_all_chat_entries_answer = _op_all_chat_entries.answer()
    _op_all_chat_entries_answer.__fragment__(fragment_chat_result_fragment())
    _op_all_chat_entries.feedback()
    _op_all_chat_entries.user()
    return _op


def query_skill_memory():
    _op = sgqlc.operation.Operation(_schema_root.query_type, name='SkillMemory', variables=dict(entryId=sgqlc.types.Arg(sgqlc.types.non_null(_schema.UUID))))
    _op.skill_memory(entry_id=sgqlc.types.Variable('entryId'))
    return _op


def query_get_max_llm_prompt():
    _op = sgqlc.operation.Operation(_schema_root.query_type, name='GetMaxLlmPrompt', variables=dict(llmPromptId=sgqlc.types.Arg(sgqlc.types.non_null(_schema.UUID)), templateVariables=sgqlc.types.Arg(_schema.JSON), kShotMatch=sgqlc.types.Arg(_schema.String)))
    _op_get_max_llm_prompt = _op.get_max_llm_prompt(llm_prompt_id=sgqlc.types.Variable('llmPromptId'), template_variables=sgqlc.types.Variable('templateVariables'), k_shot_match=sgqlc.types.Variable('kShotMatch'))
    _op_get_max_llm_prompt.llm_prompt_id()
    _op_get_max_llm_prompt.name()
    _op_get_max_llm_prompt.prompt_response()
    return _op


def query_get_copilot_skill():
    _op = sgqlc.operation.Operation(_schema_root.query_type, name='GetCopilotSkill', variables=dict(copilotId=sgqlc.types.Arg(sgqlc.types.non_null(_schema.UUID)), copilotSkillId=sgqlc.types.Arg(sgqlc.types.non_null(_schema.UUID)), usePublishedVersion=sgqlc.types.Arg(_schema.Boolean)))
    _op_get_copilot_skill = _op.get_copilot_skill(copilot_id=sgqlc.types.Variable('copilotId'), copilot_skill_id=sgqlc.types.Variable('copilotSkillId'), use_published_version=sgqlc.types.Variable('usePublishedVersion'))
    _op_get_copilot_skill.copilot_skill_id()
    _op_get_copilot_skill.name()
    _op_get_copilot_skill.copilot_skill_type()
    _op_get_copilot_skill.detailed_name()
    _op_get_copilot_skill.description()
    _op_get_copilot_skill.detailed_description()
    _op_get_copilot_skill.dataset_id()
    _op_get_copilot_skill_skill_chat_questions = _op_get_copilot_skill.skill_chat_questions()
    _op_get_copilot_skill_skill_chat_questions.copilot_skill_chat_question_id()
    _op_get_copilot_skill_skill_chat_questions.question()
    _op_get_copilot_skill_skill_chat_questions.expected_completion_response()
    _op_get_copilot_skill.yaml_code()
    _op_get_copilot_skill.skill_code()
    _op_get_copilot_skill.misc_info()
    _op_get_copilot_skill.scheduling_only()
    _op_get_copilot_skill_copilot_skill_nodes = _op_get_copilot_skill.copilot_skill_nodes()
    _op_get_copilot_skill_copilot_skill_nodes.copilot_skill_node_id()
    _op_get_copilot_skill_copilot_skill_nodes.skill_component_id()
    _op_get_copilot_skill_copilot_skill_nodes.name()
    _op_get_copilot_skill_copilot_skill_nodes.description()
    _op_get_copilot_skill_copilot_skill_nodes.user_data()
    _op_get_copilot_skill_copilot_skill_nodes_node_connections = _op_get_copilot_skill_copilot_skill_nodes.node_connections()
    _op_get_copilot_skill_copilot_skill_nodes_node_connections.input_property()
    _op_get_copilot_skill_copilot_skill_nodes_node_connections.source_node_id()
    _op_get_copilot_skill_copilot_skill_nodes_node_connections.output_property()
    _op_get_copilot_skill_parameters = _op_get_copilot_skill.parameters()
    _op_get_copilot_skill_parameters.copilot_skill_parameter_id()
    _op_get_copilot_skill_parameters.name()
    _op_get_copilot_skill_parameters.copilot_parameter_type()
    _op_get_copilot_skill_parameters.parameter_source_key()
    _op_get_copilot_skill_parameters.is_multi()
    _op_get_copilot_skill_parameters.metadata_field()
    _op_get_copilot_skill_parameters.llm_description()
    _op_get_copilot_skill_parameters.constrained_values()
    _op_get_copilot_skill_parameters.value()
    _op_get_copilot_skill_parameters.description()
    _op_get_copilot_skill_parameters.is_active()
    _op_get_copilot_skill_parameters.created_user_id()
    _op_get_copilot_skill_parameters.created_utc()
    _op_get_copilot_skill_parameters.last_modified_user_id()
    _op_get_copilot_skill_parameters.last_modified_utc()
    _op_get_copilot_skill_parameters.version()
    return _op


def query_get_copilot_info():
    _op = sgqlc.operation.Operation(_schema_root.query_type, name='GetCopilotInfo', variables=dict(copilotId=sgqlc.types.Arg(sgqlc.types.non_null(_schema.UUID)), usePublishedVersion=sgqlc.types.Arg(_schema.Boolean)))
    _op_get_copilot_info = _op.get_copilot_info(copilot_id=sgqlc.types.Variable('copilotId'), use_published_version=sgqlc.types.Variable('usePublishedVersion'))
    _op_get_copilot_info.copilot_id()
    _op_get_copilot_info.name()
    _op_get_copilot_info.description()
    _op_get_copilot_info.system_prompt()
    _op_get_copilot_info.beta_yaml()
    _op_get_copilot_info.global_python_code()
    _op_get_copilot_info.copilot_questions()
    _op_get_copilot_info.connection_datasets()
    _op_get_copilot_info.copilot_skill_ids()
    _op_get_copilot_info.copilot_topics()
    return _op


def query_get_copilots():
    _op = sgqlc.operation.Operation(_schema_root.query_type, name='GetCopilots')
    _op_get_copilots = _op.get_copilots()
    _op_get_copilots.copilot_id()
    _op_get_copilots.name()
    _op_get_copilots.description()
    _op_get_copilots.system_prompt()
    _op_get_copilots.beta_yaml()
    _op_get_copilots.global_python_code()
    _op_get_copilots_copilot_questions = _op_get_copilots.copilot_questions()
    _op_get_copilots_copilot_questions.copilot_question_id()
    _op_get_copilots_copilot_questions.nl()
    _op_get_copilots_copilot_questions.skill_id()
    _op_get_copilots_copilot_questions.parameters()
    _op_get_copilots_copilot_questions.is_starter()
    _op_get_copilots_copilot_questions.hint()
    _op_get_copilots_copilot_questions.created_user_id()
    _op_get_copilots_copilot_questions.created_utc()
    _op_get_copilots_copilot_questions.last_modified_user_id()
    _op_get_copilots_copilot_questions.last_modified_utc()
    _op_get_copilots_copilot_questions.version()
    _op_get_copilots_copilot_questions.is_deleted()
    _op_get_copilots_connection_datasets = _op_get_copilots.connection_datasets()
    _op_get_copilots_connection_datasets.dataset_id()
    _op_get_copilots_connection_datasets.name()
    _op_get_copilots.copilot_skill_ids()
    _op_get_copilots_copilot_topics = _op_get_copilots.copilot_topics()
    _op_get_copilots_copilot_topics.copilot_topic_id()
    _op_get_copilots_copilot_topics.name()
    _op_get_copilots_copilot_topics.description()
    _op_get_copilots_copilot_topics.research_outline()
    _op_get_copilots_copilot_topics.presentation_outline()
    _op_get_copilots_copilot_topics.created_user_id()
    _op_get_copilots_copilot_topics.created_user_name()
    _op_get_copilots_copilot_topics.created_utc()
    _op_get_copilots_copilot_topics.last_modified_user_id()
    _op_get_copilots_copilot_topics.last_modified_user_name()
    _op_get_copilots_copilot_topics.last_modified_utc()
    _op_get_copilots_copilot_topics.is_active()
    _op_get_copilots.database_id()
    _op_get_copilots.dataset_id()
    return _op


def query_get_grounded_value():
    _op = sgqlc.operation.Operation(_schema_root.query_type, name='GetGroundedValue', variables=dict(datasetId=sgqlc.types.Arg(sgqlc.types.non_null(_schema.UUID)), value=sgqlc.types.Arg(sgqlc.types.non_null(_schema.String)), domainEntity=sgqlc.types.Arg(_schema.String), copilotId=sgqlc.types.Arg(_schema.UUID)))
    _op_get_grounded_value = _op.get_grounded_value(dataset_id=sgqlc.types.Variable('datasetId'), value=sgqlc.types.Variable('value'), domain_entity=sgqlc.types.Variable('domainEntity'), copilot_id=sgqlc.types.Variable('copilotId'))
    _op_get_grounded_value.matched_value()
    _op_get_grounded_value.match_quality()
    _op_get_grounded_value.match_type()
    _op_get_grounded_value.mapped_indicator()
    _op_get_grounded_value.mapped_value()
    _op_get_grounded_value.preferred()
    _op_get_grounded_value.domain_entity()
    _op_get_grounded_value.other_matches()
    return _op


def query_chat_completion():
    _op = sgqlc.operation.Operation(_schema_root.query_type, name='ChatCompletion', variables=dict(messages=sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(_schema.LlmChatMessage)))), modelSelection=sgqlc.types.Arg(_schema.LlmModelSelection)))
    _op.chat_completion(messages=sgqlc.types.Variable('messages'), model_selection=sgqlc.types.Variable('modelSelection'))
    return _op


def query_narrative_completion():
    _op = sgqlc.operation.Operation(_schema_root.query_type, name='NarrativeCompletion', variables=dict(prompt=sgqlc.types.Arg(sgqlc.types.non_null(_schema.String)), modelSelection=sgqlc.types.Arg(_schema.LlmModelSelection)))
    _op.narrative_completion(prompt=sgqlc.types.Variable('prompt'), model_selection=sgqlc.types.Variable('modelSelection'))
    return _op


def query_narrative_completion_with_prompt():
    _op = sgqlc.operation.Operation(_schema_root.query_type, name='NarrativeCompletionWithPrompt', variables=dict(promptName=sgqlc.types.Arg(sgqlc.types.non_null(_schema.String)), promptVariables=sgqlc.types.Arg(_schema.JSON), modelSelection=sgqlc.types.Arg(_schema.LlmModelSelection)))
    _op.narrative_completion_with_prompt(prompt_name=sgqlc.types.Variable('promptName'), prompt_variables=sgqlc.types.Variable('promptVariables'), model_selection=sgqlc.types.Variable('modelSelection'))
    return _op


def query_sql_completion():
    _op = sgqlc.operation.Operation(_schema_root.query_type, name='SqlCompletion', variables=dict(messages=sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(_schema.LlmChatMessage)))), modelSelection=sgqlc.types.Arg(_schema.LlmModelSelection)))
    _op.sql_completion(messages=sgqlc.types.Variable('messages'), model_selection=sgqlc.types.Variable('modelSelection'))
    return _op


def query_research_completion():
    _op = sgqlc.operation.Operation(_schema_root.query_type, name='ResearchCompletion', variables=dict(messages=sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(_schema.LlmChatMessage)))), modelSelection=sgqlc.types.Arg(_schema.LlmModelSelection)))
    _op.research_completion(messages=sgqlc.types.Variable('messages'), model_selection=sgqlc.types.Variable('modelSelection'))
    return _op


class Query:
    all_chat_entries = query_all_chat_entries()
    chat_completion = query_chat_completion()
    chat_entry = query_chat_entry()
    chat_thread = query_chat_thread()
    dataframes_for_entry = query_dataframes_for_entry()
    get_copilot_info = query_get_copilot_info()
    get_copilot_skill = query_get_copilot_skill()
    get_copilots = query_get_copilots()
    get_grounded_value = query_get_grounded_value()
    get_max_llm_prompt = query_get_max_llm_prompt()
    narrative_completion = query_narrative_completion()
    narrative_completion_with_prompt = query_narrative_completion_with_prompt()
    research_completion = query_research_completion()
    skill_memory = query_skill_memory()
    sql_completion = query_sql_completion()


class Operations:
    fragment = Fragment
    mutation = Mutation
    query = Query
