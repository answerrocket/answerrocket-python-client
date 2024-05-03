import sgqlc.types
import sgqlc.operation
from . import schema

_schema = schema
_schema_root = _schema.schema

__all__ = ('Operations',)


def mutation_ask_chat_question():
    _op = sgqlc.operation.Operation(_schema_root.mutation_type, name='AskChatQuestion', variables=dict(copilotId=sgqlc.types.Arg(sgqlc.types.non_null(_schema.UUID)), question=sgqlc.types.Arg(sgqlc.types.non_null(_schema.String)), threadId=sgqlc.types.Arg(_schema.UUID), skipReportCache=sgqlc.types.Arg(_schema.Boolean), dryRunType=sgqlc.types.Arg(_schema.ChatDryRunType)))
    _op_ask_chat_question = _op.ask_chat_question(copilot_id=sgqlc.types.Variable('copilotId'), question=sgqlc.types.Variable('question'), thread_id=sgqlc.types.Variable('threadId'), skip_report_cache=sgqlc.types.Variable('skipReportCache'), dry_run_type=sgqlc.types.Variable('dryRunType'))
    _op_ask_chat_question.id()
    _op_ask_chat_question.thread_id()
    _op_ask_chat_question_answer = _op_ask_chat_question.answer()
    _op_ask_chat_question_answer.answer_id()
    _op_ask_chat_question_answer.answered_at()
    _op_ask_chat_question_answer.copilot_skill_id()
    _op_ask_chat_question_answer.has_finished()
    _op_ask_chat_question_answer.error()
    _op_ask_chat_question_answer.is_new_thread()
    _op_ask_chat_question_answer.message()
    _op_ask_chat_question_answer_report_results = _op_ask_chat_question_answer.report_results()
    _op_ask_chat_question_answer_report_results.id()
    _op_ask_chat_question_answer_report_results.title()
    _op_ask_chat_question_answer_report_results.report_name()
    _op_ask_chat_question_answer_report_results.run_id()
    _op_ask_chat_question_answer_report_results_parameters = _op_ask_chat_question_answer_report_results.parameters()
    _op_ask_chat_question_answer_report_results_parameters.key()
    _op_ask_chat_question_answer_report_results_parameters.values()
    _op_ask_chat_question_answer_report_results_parameters.label()
    _op_ask_chat_question_answer_report_results_content_blocks = _op_ask_chat_question_answer_report_results.content_blocks()
    _op_ask_chat_question_answer_report_results_content_blocks.id()
    _op_ask_chat_question_answer_report_results_content_blocks.title()
    _op_ask_chat_question_answer_report_results_content_blocks.payload()
    _op_ask_chat_question_answer.thread_id()
    _op_ask_chat_question_answer.user_id()
    return _op


class Mutation:
    ask_chat_question = mutation_ask_chat_question()


class Operations:
    mutation = Mutation
