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
    _op = sgqlc.operation.Operation(_schema_root.mutation_type, name='AskChatQuestion', variables=dict(copilotId=sgqlc.types.Arg(sgqlc.types.non_null(_schema.UUID)), question=sgqlc.types.Arg(sgqlc.types.non_null(_schema.String)), threadId=sgqlc.types.Arg(_schema.UUID), skipReportCache=sgqlc.types.Arg(_schema.Boolean), dryRunType=sgqlc.types.Arg(_schema.ChatDryRunType), modelOverrides=sgqlc.types.Arg(sgqlc.types.list_of(_schema.ModelOverride)), indicatedSkills=sgqlc.types.Arg(sgqlc.types.list_of(_schema.String)), history=sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(_schema.MessageHistoryInput)))))
    _op_ask_chat_question = _op.ask_chat_question(copilot_id=sgqlc.types.Variable('copilotId'), question=sgqlc.types.Variable('question'), thread_id=sgqlc.types.Variable('threadId'), skip_report_cache=sgqlc.types.Variable('skipReportCache'), dry_run_type=sgqlc.types.Variable('dryRunType'), model_overrides=sgqlc.types.Variable('modelOverrides'), indicated_skills=sgqlc.types.Variable('indicatedSkills'), history=sgqlc.types.Variable('history'))
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


def mutation_update_loading_message():
    _op = sgqlc.operation.Operation(_schema_root.mutation_type, name='UpdateLoadingMessage', variables=dict(answerId=sgqlc.types.Arg(sgqlc.types.non_null(_schema.UUID)), message=sgqlc.types.Arg(sgqlc.types.non_null(_schema.String))))
    _op.update_loading_message(answer_id=sgqlc.types.Variable('answerId'), message=sgqlc.types.Variable('message'))
    return _op


class Mutation:
    add_feedback = mutation_add_feedback()
    ask_chat_question = mutation_ask_chat_question()
    cancel_chat_question = mutation_cancel_chat_question()
    create_chat_thread = mutation_create_chat_thread()
    queue_chat_question = mutation_queue_chat_question()
    set_skill_memory = mutation_set_skill_memory()
    update_loading_message = mutation_update_loading_message()


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
    return _op


def query_chat_completion():
    _op = sgqlc.operation.Operation(_schema_root.query_type, name='ChatCompletion', variables=dict(messages=sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(_schema.LlmChatMessage)))), modelSelection=sgqlc.types.Arg(_schema.LlmModelSelection)))
    _op.chat_completion(messages=sgqlc.types.Variable('messages'), model_selection=sgqlc.types.Variable('modelSelection'))
    return _op


def query_narrative_completion():
    _op = sgqlc.operation.Operation(_schema_root.query_type, name='NarrativeCompletion', variables=dict(prompt=sgqlc.types.Arg(sgqlc.types.non_null(_schema.String)), modelSelection=sgqlc.types.Arg(_schema.LlmModelSelection)))
    _op.narrative_completion(prompt=sgqlc.types.Variable('prompt'), model_selection=sgqlc.types.Variable('modelSelection'))
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
    get_copilot_skill = query_get_copilot_skill()
    get_max_llm_prompt = query_get_max_llm_prompt()
    narrative_completion = query_narrative_completion()
    research_completion = query_research_completion()
    skill_memory = query_skill_memory()
    sql_completion = query_sql_completion()


class Operations:
    fragment = Fragment
    mutation = Mutation
    query = Query
