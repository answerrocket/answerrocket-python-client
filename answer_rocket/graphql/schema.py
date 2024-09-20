import sgqlc.types
import sgqlc.types.datetime


schema = sgqlc.types.Schema()



########################################################################
# Scalars and Enumerations
########################################################################
Boolean = sgqlc.types.Boolean

class ChatDryRunType(sgqlc.types.Enum):
    __schema__ = schema
    __choices__ = ('SKIP_SKILL_EXEC', 'SKIP_SKILL_NLG')


DateTime = sgqlc.types.datetime.DateTime

class DpsAggMethod(sgqlc.types.Enum):
    __schema__ = schema
    __choices__ = ('AVG', 'COUNT', 'CUSTOM', 'MAX', 'MIN', 'NONE', 'SUM')


Float = sgqlc.types.Float

Int = sgqlc.types.Int

class JSON(sgqlc.types.Scalar):
    __schema__ = schema


class MetricType(sgqlc.types.Enum):
    __schema__ = schema
    __choices__ = ('BASIC', 'RATIO', 'SHARE')


class ModelTypes(sgqlc.types.Enum):
    __schema__ = schema
    __choices__ = ('CHAT', 'EMBEDDINGS', 'NARRATIVE')


class SimplifiedDataType(sgqlc.types.Enum):
    __schema__ = schema
    __choices__ = ('BOOLEAN', 'DATE', 'NUMBER', 'STRING')


String = sgqlc.types.String

class UUID(sgqlc.types.Scalar):
    __schema__ = schema



########################################################################
# Input Objects
########################################################################
class FunctionCallMessageInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('name', 'arguments')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    arguments = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='arguments')


class MaxCopilotQuestionInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('skill_id', 'nl', 'hint', 'parameters')
    skill_id = sgqlc.types.Field(UUID, graphql_name='skillId')
    nl = sgqlc.types.Field(String, graphql_name='nl')
    hint = sgqlc.types.Field(String, graphql_name='hint')
    parameters = sgqlc.types.Field(JSON, graphql_name='parameters')


class MessageHistoryInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('role', 'content', 'name', 'function_call')
    role = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='role')
    content = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='content')
    name = sgqlc.types.Field(String, graphql_name='name')
    function_call = sgqlc.types.Field(FunctionCallMessageInput, graphql_name='functionCall')


class ModelOverride(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('model_type', 'model_name')
    model_type = sgqlc.types.Field(sgqlc.types.non_null(ModelTypes), graphql_name='modelType')
    model_name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='modelName')



########################################################################
# Output Objects and Interfaces
########################################################################
class LLMApiConfig(sgqlc.types.Interface):
    __schema__ = schema
    __field_names__ = ('id', 'api_type', 'model_type', 'model_name')
    id = sgqlc.types.Field(sgqlc.types.non_null(UUID), graphql_name='id')
    api_type = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='apiType')
    model_type = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='modelType')
    model_name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='modelName')


class MaxDomainObject(sgqlc.types.Interface):
    __schema__ = schema
    __field_names__ = ('type', 'id', 'name', 'description', 'output_label', 'synonyms', 'output_label_plural', 'hide_from_user', 'misc_info')
    type = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='type')
    id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='id')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    description = sgqlc.types.Field(String, graphql_name='description')
    output_label = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='outputLabel')
    synonyms = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))), graphql_name='synonyms')
    output_label_plural = sgqlc.types.Field(String, graphql_name='outputLabelPlural')
    hide_from_user = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='hideFromUser')
    misc_info = sgqlc.types.Field(String, graphql_name='miscInfo')


class MaxDomainAttribute(sgqlc.types.Interface):
    __schema__ = schema
    __field_names__ = ('type', 'id', 'name', 'description', 'output_label', 'synonyms', 'output_label_plural', 'hide_from_user', 'misc_info', 'display_format', 'headline_name', 'is_favorite', 'simplified_data_type', 'sql', 'domain_entity')
    type = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='type')
    id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='id')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    description = sgqlc.types.Field(String, graphql_name='description')
    output_label = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='outputLabel')
    synonyms = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))), graphql_name='synonyms')
    output_label_plural = sgqlc.types.Field(String, graphql_name='outputLabelPlural')
    hide_from_user = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='hideFromUser')
    misc_info = sgqlc.types.Field(String, graphql_name='miscInfo')
    display_format = sgqlc.types.Field(String, graphql_name='displayFormat')
    headline_name = sgqlc.types.Field(String, graphql_name='headlineName')
    is_favorite = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='isFavorite')
    simplified_data_type = sgqlc.types.Field(SimplifiedDataType, graphql_name='simplifiedDataType')
    sql = sgqlc.types.Field(String, graphql_name='sql')
    domain_entity = sgqlc.types.Field('MaxDomainEntity', graphql_name='domainEntity')


class MaxDimensionAttribute(sgqlc.types.Interface):
    __schema__ = schema
    __field_names__ = ('type', 'id', 'name', 'description', 'output_label', 'synonyms', 'output_label_plural', 'hide_from_user', 'misc_info', 'display_format', 'headline_name', 'is_favorite', 'simplified_data_type', 'sql', 'domain_entity', 'dimension_value_mapping_list', 'default_filter_value', 'is_required_in_query')
    type = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='type')
    id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='id')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    description = sgqlc.types.Field(String, graphql_name='description')
    output_label = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='outputLabel')
    synonyms = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))), graphql_name='synonyms')
    output_label_plural = sgqlc.types.Field(String, graphql_name='outputLabelPlural')
    hide_from_user = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='hideFromUser')
    misc_info = sgqlc.types.Field(String, graphql_name='miscInfo')
    display_format = sgqlc.types.Field(String, graphql_name='displayFormat')
    headline_name = sgqlc.types.Field(String, graphql_name='headlineName')
    is_favorite = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='isFavorite')
    simplified_data_type = sgqlc.types.Field(SimplifiedDataType, graphql_name='simplifiedDataType')
    sql = sgqlc.types.Field(String, graphql_name='sql')
    domain_entity = sgqlc.types.Field('MaxDomainEntity', graphql_name='domainEntity')
    dimension_value_mapping_list = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('DimensionValueMapping'))), graphql_name='dimensionValueMappingList')
    default_filter_value = sgqlc.types.Field(String, graphql_name='defaultFilterValue')
    is_required_in_query = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='isRequiredInQuery')


class MaxDomainEntity(sgqlc.types.Interface):
    __schema__ = schema
    __field_names__ = ('type', 'id', 'name', 'description', 'output_label', 'synonyms', 'output_label_plural', 'hide_from_user', 'misc_info', 'db_table', 'derived_table_sql', 'attributes')
    type = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='type')
    id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='id')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    description = sgqlc.types.Field(String, graphql_name='description')
    output_label = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='outputLabel')
    synonyms = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))), graphql_name='synonyms')
    output_label_plural = sgqlc.types.Field(String, graphql_name='outputLabelPlural')
    hide_from_user = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='hideFromUser')
    misc_info = sgqlc.types.Field(String, graphql_name='miscInfo')
    db_table = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='dbTable')
    derived_table_sql = sgqlc.types.Field(String, graphql_name='derivedTableSql')
    attributes = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(MaxDomainAttribute))), graphql_name='attributes')


class ChatFeedback(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('type', 'feedback', 'user_id')
    type = sgqlc.types.Field(String, graphql_name='type')
    feedback = sgqlc.types.Field(JSON, graphql_name='feedback')
    user_id = sgqlc.types.Field(UUID, graphql_name='userId')


class CopilotSkillArtifact(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('copilot_skill_artifact_id', 'copilot_id', 'copilot_skill_id', 'artifact_path', 'artifact', 'description', 'created_user_id', 'created_utc', 'last_modified_user_id', 'last_modified_utc', 'version', 'is_active', 'is_deleted')
    copilot_skill_artifact_id = sgqlc.types.Field(sgqlc.types.non_null(UUID), graphql_name='copilotSkillArtifactId')
    copilot_id = sgqlc.types.Field(sgqlc.types.non_null(UUID), graphql_name='copilotId')
    copilot_skill_id = sgqlc.types.Field(sgqlc.types.non_null(UUID), graphql_name='copilotSkillId')
    artifact_path = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='artifactPath')
    artifact = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='artifact')
    description = sgqlc.types.Field(String, graphql_name='description')
    created_user_id = sgqlc.types.Field(sgqlc.types.non_null(UUID), graphql_name='createdUserId')
    created_utc = sgqlc.types.Field(sgqlc.types.non_null(DateTime), graphql_name='createdUtc')
    last_modified_user_id = sgqlc.types.Field(sgqlc.types.non_null(UUID), graphql_name='lastModifiedUserId')
    last_modified_utc = sgqlc.types.Field(sgqlc.types.non_null(DateTime), graphql_name='lastModifiedUtc')
    version = sgqlc.types.Field(sgqlc.types.non_null(UUID), graphql_name='version')
    is_active = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='isActive')
    is_deleted = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='isDeleted')


class CopilotSkillRunResponse(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('success', 'code', 'errors', 'data')
    success = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='success')
    code = sgqlc.types.Field(String, graphql_name='code')
    errors = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='errors')
    data = sgqlc.types.Field(JSON, graphql_name='data')


class CostInfo(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('completion_tokens', 'prompt_tokens', 'total_tokens', 'cost_estimate_usd', 'model')
    completion_tokens = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='completionTokens')
    prompt_tokens = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='promptTokens')
    total_tokens = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='totalTokens')
    cost_estimate_usd = sgqlc.types.Field(Float, graphql_name='costEstimateUsd')
    model = sgqlc.types.Field(String, graphql_name='model')


class CreateMaxCopilotSkillChatQuestionResponse(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('copilot_skill_chat_question_id', 'success', 'code', 'error')
    copilot_skill_chat_question_id = sgqlc.types.Field(UUID, graphql_name='copilotSkillChatQuestionId')
    success = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='success')
    code = sgqlc.types.Field(String, graphql_name='code')
    error = sgqlc.types.Field(String, graphql_name='error')


class DimensionValueMapping(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('value', 'mapped_values')
    value = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='value')
    mapped_values = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))), graphql_name='mappedValues')


class DomainObjectResponse(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('success', 'code', 'error', 'domain_object')
    success = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='success')
    code = sgqlc.types.Field(String, graphql_name='code')
    error = sgqlc.types.Field(String, graphql_name='error')
    domain_object = sgqlc.types.Field(MaxDomainObject, graphql_name='domainObject')


class EvaluateChatQuestionResponse(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('success', 'eval_results')
    success = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='success')
    eval_results = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('EvaluateChatQuestionResult'))), graphql_name='evalResults')


class EvaluateChatQuestionResult(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('eval_type', 'pass_', 'explanation', 'correct_function', 'is_loading', 'cost')
    eval_type = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='evalType')
    pass_ = sgqlc.types.Field(Boolean, graphql_name='pass')
    explanation = sgqlc.types.Field(String, graphql_name='explanation')
    correct_function = sgqlc.types.Field(String, graphql_name='correctFunction')
    is_loading = sgqlc.types.Field(Boolean, graphql_name='isLoading')
    cost = sgqlc.types.Field(CostInfo, graphql_name='cost')


class ExecuteRqlQueryResponse(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('success', 'code', 'error', 'process_rql_script_response', 'sql', 'data')
    success = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='success')
    code = sgqlc.types.Field(String, graphql_name='code')
    error = sgqlc.types.Field(String, graphql_name='error')
    process_rql_script_response = sgqlc.types.Field(JSON, graphql_name='processRqlScriptResponse')
    sql = sgqlc.types.Field(String, graphql_name='sql')
    data = sgqlc.types.Field(JSON, graphql_name='data')


class ExecuteSqlQueryResponse(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('success', 'code', 'error', 'data')
    success = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='success')
    code = sgqlc.types.Field(String, graphql_name='code')
    error = sgqlc.types.Field(String, graphql_name='error')
    data = sgqlc.types.Field(JSON, graphql_name='data')


class MaxChatEntry(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('id', 'thread_id', 'question', 'answer', 'feedback')
    id = sgqlc.types.Field(sgqlc.types.non_null(UUID), graphql_name='id')
    thread_id = sgqlc.types.Field(UUID, graphql_name='threadId')
    question = sgqlc.types.Field('MaxChatQuestion', graphql_name='question')
    answer = sgqlc.types.Field('MaxChatResult', graphql_name='answer')
    feedback = sgqlc.types.Field(ChatFeedback, graphql_name='feedback')


class MaxChatQuestion(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('asked_at', 'nl')
    asked_at = sgqlc.types.Field(DateTime, graphql_name='askedAt')
    nl = sgqlc.types.Field(String, graphql_name='nl')


class MaxChatResult(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('answer_id', 'answered_at', 'copilot_skill_id', 'has_finished', 'error', 'is_new_thread', 'message', 'report_results', 'thread_id', 'user_id')
    answer_id = sgqlc.types.Field(UUID, graphql_name='answerId')
    answered_at = sgqlc.types.Field(DateTime, graphql_name='answeredAt')
    copilot_skill_id = sgqlc.types.Field(UUID, graphql_name='copilotSkillId')
    has_finished = sgqlc.types.Field(Boolean, graphql_name='hasFinished')
    error = sgqlc.types.Field(String, graphql_name='error')
    is_new_thread = sgqlc.types.Field(Boolean, graphql_name='isNewThread')
    message = sgqlc.types.Field(String, graphql_name='message')
    report_results = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('MaxReportResult')), graphql_name='reportResults')
    thread_id = sgqlc.types.Field(UUID, graphql_name='threadId')
    user_id = sgqlc.types.Field(UUID, graphql_name='userId')


class MaxChatThread(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('id', 'entry_count', 'title', 'copilot_id', 'entries')
    id = sgqlc.types.Field(sgqlc.types.non_null(UUID), graphql_name='id')
    entry_count = sgqlc.types.Field(Int, graphql_name='entryCount')
    title = sgqlc.types.Field(String, graphql_name='title')
    copilot_id = sgqlc.types.Field(sgqlc.types.non_null(UUID), graphql_name='copilotId')
    entries = sgqlc.types.Field(sgqlc.types.list_of(MaxChatEntry), graphql_name='entries')


class MaxColumn(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('name', 'jdbc_type', 'length', 'precision', 'scale')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    jdbc_type = sgqlc.types.Field(String, graphql_name='jdbcType')
    length = sgqlc.types.Field(Int, graphql_name='length')
    precision = sgqlc.types.Field(Int, graphql_name='precision')
    scale = sgqlc.types.Field(Int, graphql_name='scale')


class MaxCopilot(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('copilot_id', 'name', 'description', 'system_prompt', 'beta_yaml', 'global_python_code', 'copilot_questions', 'connection_datasets')
    copilot_id = sgqlc.types.Field(sgqlc.types.non_null(UUID), graphql_name='copilotId')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    description = sgqlc.types.Field(String, graphql_name='description')
    system_prompt = sgqlc.types.Field(String, graphql_name='systemPrompt')
    beta_yaml = sgqlc.types.Field(String, graphql_name='betaYaml')
    global_python_code = sgqlc.types.Field(String, graphql_name='globalPythonCode')
    copilot_questions = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('MaxCopilotQuestion'))), graphql_name='copilotQuestions')
    connection_datasets = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('MaxCopilotConnectionDataset'))), graphql_name='connectionDatasets')


class MaxCopilotConnectionDataset(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('dataset_id', 'name')
    dataset_id = sgqlc.types.Field(sgqlc.types.non_null(UUID), graphql_name='datasetId')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')


class MaxCopilotQuestion(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('copilot_question_id', 'nl', 'skill_id', 'parameters', 'is_starter', 'hint', 'created_user_id', 'created_utc', 'last_modified_user_id', 'last_modified_utc', 'version', 'is_deleted')
    copilot_question_id = sgqlc.types.Field(sgqlc.types.non_null(UUID), graphql_name='copilotQuestionId')
    nl = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='nl')
    skill_id = sgqlc.types.Field(UUID, graphql_name='skillId')
    parameters = sgqlc.types.Field(JSON, graphql_name='parameters')
    is_starter = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='isStarter')
    hint = sgqlc.types.Field(String, graphql_name='hint')
    created_user_id = sgqlc.types.Field(sgqlc.types.non_null(UUID), graphql_name='createdUserId')
    created_utc = sgqlc.types.Field(sgqlc.types.non_null(DateTime), graphql_name='createdUtc')
    last_modified_user_id = sgqlc.types.Field(sgqlc.types.non_null(UUID), graphql_name='lastModifiedUserId')
    last_modified_utc = sgqlc.types.Field(sgqlc.types.non_null(DateTime), graphql_name='lastModifiedUtc')
    version = sgqlc.types.Field(sgqlc.types.non_null(UUID), graphql_name='version')
    is_deleted = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='isDeleted')


class MaxCopilotSkill(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('copilot_skill_id', 'name', 'copilot_skill_type', 'detailed_name', 'description', 'detailed_description', 'dataset_id', 'skill_chat_questions', 'yaml_code', 'skill_code', 'misc_info', 'scheduling_only', 'copilot_skill_nodes')
    copilot_skill_id = sgqlc.types.Field(sgqlc.types.non_null(UUID), graphql_name='copilotSkillId')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    copilot_skill_type = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='copilotSkillType')
    detailed_name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='detailedName')
    description = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='description')
    detailed_description = sgqlc.types.Field(String, graphql_name='detailedDescription')
    dataset_id = sgqlc.types.Field(UUID, graphql_name='datasetId')
    skill_chat_questions = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of('MaxCopilotSkillChatQuestion')), graphql_name='skillChatQuestions')
    yaml_code = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='yamlCode')
    skill_code = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='skillCode')
    misc_info = sgqlc.types.Field(JSON, graphql_name='miscInfo')
    scheduling_only = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='schedulingOnly')
    copilot_skill_nodes = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('MaxCopilotSkillNode'))), graphql_name='copilotSkillNodes')


class MaxCopilotSkillChatQuestion(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('copilot_skill_chat_question_id', 'question', 'expected_completion_response')
    copilot_skill_chat_question_id = sgqlc.types.Field(sgqlc.types.non_null(UUID), graphql_name='copilotSkillChatQuestionId')
    question = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='question')
    expected_completion_response = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='expectedCompletionResponse')


class MaxCopilotSkillNode(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('copilot_skill_node_id', 'skill_component_id', 'name', 'description', 'user_data', 'node_connections')
    copilot_skill_node_id = sgqlc.types.Field(sgqlc.types.non_null(UUID), graphql_name='copilotSkillNodeId')
    skill_component_id = sgqlc.types.Field(sgqlc.types.non_null(UUID), graphql_name='skillComponentId')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    description = sgqlc.types.Field(String, graphql_name='description')
    user_data = sgqlc.types.Field(JSON, graphql_name='userData')
    node_connections = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('MaxCopilotSkillNodeConnection'))), graphql_name='nodeConnections')


class MaxCopilotSkillNodeConnection(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('input_property', 'source_node_id', 'output_property')
    input_property = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='inputProperty')
    source_node_id = sgqlc.types.Field(sgqlc.types.non_null(UUID), graphql_name='sourceNodeId')
    output_property = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='outputProperty')


class MaxCreateCopilotQuestionResponse(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('copilot_question_id', 'success', 'code', 'errors')
    copilot_question_id = sgqlc.types.Field(UUID, graphql_name='copilotQuestionId')
    success = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='success')
    code = sgqlc.types.Field(String, graphql_name='code')
    errors = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))), graphql_name='errors')


class MaxDatabase(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('database_id', 'name', 'dbms', 'schema')
    database_id = sgqlc.types.Field(sgqlc.types.non_null(UUID), graphql_name='databaseId')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    dbms = sgqlc.types.Field(String, graphql_name='dbms')
    schema = sgqlc.types.Field(String, graphql_name='schema')


class MaxDataset(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('dataset_id', 'name', 'description', 'domain_objects', 'misc_info', 'database', 'tables', 'dimension_value_distribution_map', 'date_range_boundary_attribute_id', 'dimension_hierarchies', 'metric_hierarchies', 'domain_attribute_statistics', 'default_performance_metric_id', 'dataset_min_date', 'dataset_max_date', 'query_row_limit', 'use_database_casing')
    dataset_id = sgqlc.types.Field(sgqlc.types.non_null(UUID), graphql_name='datasetId')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    description = sgqlc.types.Field(String, graphql_name='description')
    domain_objects = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(MaxDomainObject))), graphql_name='domainObjects')
    misc_info = sgqlc.types.Field(String, graphql_name='miscInfo')
    database = sgqlc.types.Field(MaxDatabase, graphql_name='database')
    tables = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('MaxTable'))), graphql_name='tables')
    dimension_value_distribution_map = sgqlc.types.Field(JSON, graphql_name='dimensionValueDistributionMap')
    date_range_boundary_attribute_id = sgqlc.types.Field(String, graphql_name='dateRangeBoundaryAttributeId')
    dimension_hierarchies = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of('MaxDimensionHierarchyNode')), graphql_name='dimensionHierarchies')
    metric_hierarchies = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of('MaxMetricHierarchyNode')), graphql_name='metricHierarchies')
    domain_attribute_statistics = sgqlc.types.Field(JSON, graphql_name='domainAttributeStatistics')
    default_performance_metric_id = sgqlc.types.Field(String, graphql_name='defaultPerformanceMetricId')
    dataset_min_date = sgqlc.types.Field(DateTime, graphql_name='datasetMinDate')
    dataset_max_date = sgqlc.types.Field(DateTime, graphql_name='datasetMaxDate')
    query_row_limit = sgqlc.types.Field(Int, graphql_name='queryRowLimit')
    use_database_casing = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='useDatabaseCasing')


class MaxDimensionHierarchyNode(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('dimension_hierarchy_node_id', 'dimension_attribute_id', 'description', 'children')
    dimension_hierarchy_node_id = sgqlc.types.Field(sgqlc.types.non_null(UUID), graphql_name='dimensionHierarchyNodeId')
    dimension_attribute_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='dimensionAttributeId')
    description = sgqlc.types.Field(String, graphql_name='description')
    children = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('MaxDimensionHierarchyNode'))), graphql_name='children')


class MaxDomainAttributeStatisticInfo(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('null_count', 'min_value', 'max_value', 'distinct_count')
    null_count = sgqlc.types.Field(Int, graphql_name='nullCount')
    min_value = sgqlc.types.Field(String, graphql_name='minValue')
    max_value = sgqlc.types.Field(String, graphql_name='maxValue')
    distinct_count = sgqlc.types.Field(Int, graphql_name='distinctCount')


class MaxLLmPrompt(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('llm_prompt_id', 'name', 'prompt_response')
    llm_prompt_id = sgqlc.types.Field(sgqlc.types.non_null(UUID), graphql_name='llmPromptId')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    prompt_response = sgqlc.types.Field(JSON, graphql_name='promptResponse')


class MaxMetricHierarchyNode(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('metric_hierarchy_node_id', 'metric_id', 'description', 'children')
    metric_hierarchy_node_id = sgqlc.types.Field(sgqlc.types.non_null(UUID), graphql_name='metricHierarchyNodeId')
    metric_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='metricId')
    description = sgqlc.types.Field(String, graphql_name='description')
    children = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('MaxMetricHierarchyNode'))), graphql_name='children')


class MaxMutationResponse(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('success', 'code', 'error')
    success = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='success')
    code = sgqlc.types.Field(String, graphql_name='code')
    error = sgqlc.types.Field(String, graphql_name='error')


class MaxReportParamsAndValues(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('key', 'values', 'label', 'color')
    key = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='key')
    values = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))), graphql_name='values')
    label = sgqlc.types.Field(String, graphql_name='label')
    color = sgqlc.types.Field(String, graphql_name='color')


class MaxReportResult(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('title', 'report_name', 'parameters', 'custom_payload')
    title = sgqlc.types.Field(String, graphql_name='title')
    report_name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='reportName')
    parameters = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(MaxReportParamsAndValues)), graphql_name='parameters')
    custom_payload = sgqlc.types.Field(JSON, graphql_name='customPayload')


class MaxSkillComponent(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('skill_component_id', 'node_type', 'organization', 'name', 'description', 'input_properties', 'output_properties', 'component_data')
    skill_component_id = sgqlc.types.Field(sgqlc.types.non_null(UUID), graphql_name='skillComponentId')
    node_type = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='nodeType')
    organization = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='organization')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    description = sgqlc.types.Field(String, graphql_name='description')
    input_properties = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('MaxSkillComponentInputProperty'))), graphql_name='inputProperties')
    output_properties = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('MaxSkillComponentOutputProperty'))), graphql_name='outputProperties')
    component_data = sgqlc.types.Field(sgqlc.types.non_null(JSON), graphql_name='componentData')


class MaxSkillComponentInputProperty(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('name', 'label', 'description', 'type', 'is_required', 'is_list', 'can_wire_from_output')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    label = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='label')
    description = sgqlc.types.Field(String, graphql_name='description')
    type = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='type')
    is_required = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='isRequired')
    is_list = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='isList')
    can_wire_from_output = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='canWireFromOutput')


class MaxSkillComponentOutputProperty(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('name', 'label', 'description', 'type', 'is_required', 'is_list', 'can_wire_to_input')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    label = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='label')
    description = sgqlc.types.Field(String, graphql_name='description')
    type = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='type')
    is_required = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='isRequired')
    is_list = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='isList')
    can_wire_to_input = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='canWireToInput')


class MaxTable(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('name', 'columns')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    columns = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(MaxColumn))), graphql_name='columns')


class MaxUser(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('first_name', 'last_name', 'email_address')
    first_name = sgqlc.types.Field(String, graphql_name='firstName')
    last_name = sgqlc.types.Field(String, graphql_name='lastName')
    email_address = sgqlc.types.Field(String, graphql_name='emailAddress')


class Mutation(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('create_max_copilot_skill_chat_question', 'update_max_copilot_skill_chat_question', 'delete_max_copilot_skill_chat_question', 'create_max_copilot_question', 'update_max_copilot_question', 'delete_max_copilot_question', 'reload_dataset', 'update_chat_answer_payload', 'ask_chat_question', 'evaluate_chat_question', 'queue_chat_question', 'cancel_chat_question', 'create_chat_thread', 'share_thread')
    create_max_copilot_skill_chat_question = sgqlc.types.Field(sgqlc.types.non_null(CreateMaxCopilotSkillChatQuestionResponse), graphql_name='createMaxCopilotSkillChatQuestion', args=sgqlc.types.ArgDict((
        ('copilot_id', sgqlc.types.Arg(sgqlc.types.non_null(UUID), graphql_name='copilotId', default=None)),
        ('copilot_skill_id', sgqlc.types.Arg(sgqlc.types.non_null(UUID), graphql_name='copilotSkillId', default=None)),
        ('question', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='question', default=None)),
        ('expected_completion_response', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='expectedCompletionResponse', default=None)),
))
    )
    update_max_copilot_skill_chat_question = sgqlc.types.Field(sgqlc.types.non_null(MaxMutationResponse), graphql_name='updateMaxCopilotSkillChatQuestion', args=sgqlc.types.ArgDict((
        ('copilot_id', sgqlc.types.Arg(sgqlc.types.non_null(UUID), graphql_name='copilotId', default=None)),
        ('copilot_skill_id', sgqlc.types.Arg(sgqlc.types.non_null(UUID), graphql_name='copilotSkillId', default=None)),
        ('copilot_skill_chat_question_id', sgqlc.types.Arg(sgqlc.types.non_null(UUID), graphql_name='copilotSkillChatQuestionId', default=None)),
        ('question', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='question', default=None)),
        ('expected_completion_response', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='expectedCompletionResponse', default=None)),
))
    )
    delete_max_copilot_skill_chat_question = sgqlc.types.Field(sgqlc.types.non_null(MaxMutationResponse), graphql_name='deleteMaxCopilotSkillChatQuestion', args=sgqlc.types.ArgDict((
        ('copilot_id', sgqlc.types.Arg(sgqlc.types.non_null(UUID), graphql_name='copilotId', default=None)),
        ('copilot_skill_id', sgqlc.types.Arg(sgqlc.types.non_null(UUID), graphql_name='copilotSkillId', default=None)),
        ('copilot_skill_chat_question_id', sgqlc.types.Arg(sgqlc.types.non_null(UUID), graphql_name='copilotSkillChatQuestionId', default=None)),
))
    )
    create_max_copilot_question = sgqlc.types.Field(sgqlc.types.non_null(MaxCreateCopilotQuestionResponse), graphql_name='createMaxCopilotQuestion', args=sgqlc.types.ArgDict((
        ('copilot_id', sgqlc.types.Arg(sgqlc.types.non_null(UUID), graphql_name='copilotId', default=None)),
        ('copilot_question', sgqlc.types.Arg(sgqlc.types.non_null(MaxCopilotQuestionInput), graphql_name='copilotQuestion', default=None)),
))
    )
    update_max_copilot_question = sgqlc.types.Field(sgqlc.types.non_null(MaxMutationResponse), graphql_name='updateMaxCopilotQuestion', args=sgqlc.types.ArgDict((
        ('copilot_id', sgqlc.types.Arg(sgqlc.types.non_null(UUID), graphql_name='copilotId', default=None)),
        ('copilot_question_id', sgqlc.types.Arg(sgqlc.types.non_null(UUID), graphql_name='copilotQuestionId', default=None)),
        ('copilot_question', sgqlc.types.Arg(sgqlc.types.non_null(MaxCopilotQuestionInput), graphql_name='copilotQuestion', default=None)),
))
    )
    delete_max_copilot_question = sgqlc.types.Field(sgqlc.types.non_null(MaxMutationResponse), graphql_name='deleteMaxCopilotQuestion', args=sgqlc.types.ArgDict((
        ('copilot_id', sgqlc.types.Arg(sgqlc.types.non_null(UUID), graphql_name='copilotId', default=None)),
        ('copilot_question_id', sgqlc.types.Arg(sgqlc.types.non_null(UUID), graphql_name='copilotQuestionId', default=None)),
))
    )
    reload_dataset = sgqlc.types.Field(sgqlc.types.non_null(MaxMutationResponse), graphql_name='reloadDataset', args=sgqlc.types.ArgDict((
        ('dataset_id', sgqlc.types.Arg(UUID, graphql_name='datasetId', default=None)),
        ('database_id', sgqlc.types.Arg(UUID, graphql_name='databaseId', default=None)),
        ('table_names', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='tableNames', default=None)),
))
    )
    update_chat_answer_payload = sgqlc.types.Field(JSON, graphql_name='updateChatAnswerPayload', args=sgqlc.types.ArgDict((
        ('answer_id', sgqlc.types.Arg(sgqlc.types.non_null(UUID), graphql_name='answerId', default=None)),
        ('payload', sgqlc.types.Arg(sgqlc.types.non_null(JSON), graphql_name='payload', default=None)),
))
    )
    ask_chat_question = sgqlc.types.Field(MaxChatEntry, graphql_name='askChatQuestion', args=sgqlc.types.ArgDict((
        ('copilot_id', sgqlc.types.Arg(sgqlc.types.non_null(UUID), graphql_name='copilotId', default=None)),
        ('question', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='question', default=None)),
        ('thread_id', sgqlc.types.Arg(UUID, graphql_name='threadId', default=None)),
        ('skip_report_cache', sgqlc.types.Arg(Boolean, graphql_name='skipReportCache', default=None)),
        ('dry_run_type', sgqlc.types.Arg(ChatDryRunType, graphql_name='dryRunType', default=None)),
        ('model_overrides', sgqlc.types.Arg(sgqlc.types.list_of(ModelOverride), graphql_name='modelOverrides', default=None)),
        ('indicated_skills', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='indicatedSkills', default=None)),
        ('history', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(MessageHistoryInput)), graphql_name='history', default=None)),
))
    )
    evaluate_chat_question = sgqlc.types.Field(sgqlc.types.non_null(EvaluateChatQuestionResponse), graphql_name='evaluateChatQuestion', args=sgqlc.types.ArgDict((
        ('entry_id', sgqlc.types.Arg(sgqlc.types.non_null(UUID), graphql_name='entryId', default=None)),
        ('evals', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))), graphql_name='evals', default=None)),
))
    )
    queue_chat_question = sgqlc.types.Field(MaxChatEntry, graphql_name='queueChatQuestion', args=sgqlc.types.ArgDict((
        ('thread_id', sgqlc.types.Arg(sgqlc.types.non_null(UUID), graphql_name='threadId', default=None)),
        ('question', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='question', default=None)),
        ('skip_cache', sgqlc.types.Arg(Boolean, graphql_name='skipCache', default=None)),
        ('model_overrides', sgqlc.types.Arg(sgqlc.types.list_of(ModelOverride), graphql_name='modelOverrides', default=None)),
        ('indicated_skills', sgqlc.types.Arg(sgqlc.types.list_of(String), graphql_name='indicatedSkills', default=None)),
        ('history', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(MessageHistoryInput)), graphql_name='history', default=None)),
))
    )
    cancel_chat_question = sgqlc.types.Field(MaxChatEntry, graphql_name='cancelChatQuestion', args=sgqlc.types.ArgDict((
        ('entry_id', sgqlc.types.Arg(sgqlc.types.non_null(UUID), graphql_name='entryId', default=None)),
))
    )
    create_chat_thread = sgqlc.types.Field(MaxChatThread, graphql_name='createChatThread', args=sgqlc.types.ArgDict((
        ('copilot_id', sgqlc.types.Arg(sgqlc.types.non_null(UUID), graphql_name='copilotId', default=None)),
))
    )
    share_thread = sgqlc.types.Field(sgqlc.types.non_null('SharedThread'), graphql_name='shareThread', args=sgqlc.types.ArgDict((
        ('original_thread_id', sgqlc.types.Arg(UUID, graphql_name='originalThreadId', default=None)),
))
    )


class Query(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('ping', 'current_user', 'get_copilot_skill_artifact_by_path', 'get_copilot_info', 'get_copilot_skill', 'run_copilot_skill', 'get_skill_components', 'execute_sql_query', 'execute_rql_query', 'get_dataset_id', 'get_dataset', 'get_domain_object', 'get_domain_object_by_name', 'llmapi_config_for_sdk', 'get_max_llm_prompt', 'user_chat_threads', 'user_chat_entries', 'chat_thread', 'chat_entry')
    ping = sgqlc.types.Field(String, graphql_name='ping')
    current_user = sgqlc.types.Field(MaxUser, graphql_name='currentUser')
    get_copilot_skill_artifact_by_path = sgqlc.types.Field(CopilotSkillArtifact, graphql_name='getCopilotSkillArtifactByPath', args=sgqlc.types.ArgDict((
        ('copilot_id', sgqlc.types.Arg(sgqlc.types.non_null(UUID), graphql_name='copilotId', default=None)),
        ('copilot_skill_id', sgqlc.types.Arg(sgqlc.types.non_null(UUID), graphql_name='copilotSkillId', default=None)),
        ('artifact_path', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='artifactPath', default=None)),
))
    )
    get_copilot_info = sgqlc.types.Field(MaxCopilot, graphql_name='getCopilotInfo', args=sgqlc.types.ArgDict((
        ('copilot_id', sgqlc.types.Arg(sgqlc.types.non_null(UUID), graphql_name='copilotId', default=None)),
        ('use_published_version', sgqlc.types.Arg(Boolean, graphql_name='usePublishedVersion', default=None)),
))
    )
    get_copilot_skill = sgqlc.types.Field(MaxCopilotSkill, graphql_name='getCopilotSkill', args=sgqlc.types.ArgDict((
        ('copilot_id', sgqlc.types.Arg(sgqlc.types.non_null(UUID), graphql_name='copilotId', default=None)),
        ('copilot_skill_id', sgqlc.types.Arg(sgqlc.types.non_null(UUID), graphql_name='copilotSkillId', default=None)),
        ('use_published_version', sgqlc.types.Arg(Boolean, graphql_name='usePublishedVersion', default=None)),
))
    )
    run_copilot_skill = sgqlc.types.Field(CopilotSkillRunResponse, graphql_name='runCopilotSkill', args=sgqlc.types.ArgDict((
        ('copilot_id', sgqlc.types.Arg(sgqlc.types.non_null(UUID), graphql_name='copilotId', default=None)),
        ('skill_name', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='skillName', default=None)),
        ('parameters', sgqlc.types.Arg(JSON, graphql_name='parameters', default=None)),
        ('use_published_version', sgqlc.types.Arg(Boolean, graphql_name='usePublishedVersion', default=None)),
))
    )
    get_skill_components = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(MaxSkillComponent))), graphql_name='getSkillComponents')
    execute_sql_query = sgqlc.types.Field(ExecuteSqlQueryResponse, graphql_name='executeSqlQuery', args=sgqlc.types.ArgDict((
        ('database_id', sgqlc.types.Arg(sgqlc.types.non_null(UUID), graphql_name='databaseId', default=None)),
        ('sql_query', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='sqlQuery', default=None)),
        ('row_limit', sgqlc.types.Arg(Int, graphql_name='rowLimit', default=None)),
        ('copilot_id', sgqlc.types.Arg(UUID, graphql_name='copilotId', default=None)),
        ('copilot_skill_id', sgqlc.types.Arg(UUID, graphql_name='copilotSkillId', default=None)),
))
    )
    execute_rql_query = sgqlc.types.Field(ExecuteRqlQueryResponse, graphql_name='executeRqlQuery', args=sgqlc.types.ArgDict((
        ('dataset_id', sgqlc.types.Arg(sgqlc.types.non_null(UUID), graphql_name='datasetId', default=None)),
        ('rql_query', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='rqlQuery', default=None)),
        ('row_limit', sgqlc.types.Arg(Int, graphql_name='rowLimit', default=None)),
        ('copilot_id', sgqlc.types.Arg(UUID, graphql_name='copilotId', default=None)),
        ('copilot_skill_id', sgqlc.types.Arg(UUID, graphql_name='copilotSkillId', default=None)),
))
    )
    get_dataset_id = sgqlc.types.Field(UUID, graphql_name='getDatasetId', args=sgqlc.types.ArgDict((
        ('dataset_name', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='datasetName', default=None)),
))
    )
    get_dataset = sgqlc.types.Field(MaxDataset, graphql_name='getDataset', args=sgqlc.types.ArgDict((
        ('dataset_id', sgqlc.types.Arg(sgqlc.types.non_null(UUID), graphql_name='datasetId', default=None)),
        ('copilot_id', sgqlc.types.Arg(UUID, graphql_name='copilotId', default=None)),
))
    )
    get_domain_object = sgqlc.types.Field(DomainObjectResponse, graphql_name='getDomainObject', args=sgqlc.types.ArgDict((
        ('dataset_id', sgqlc.types.Arg(sgqlc.types.non_null(UUID), graphql_name='datasetId', default=None)),
        ('domain_object_id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='domainObjectId', default=None)),
))
    )
    get_domain_object_by_name = sgqlc.types.Field(DomainObjectResponse, graphql_name='getDomainObjectByName', args=sgqlc.types.ArgDict((
        ('dataset_id', sgqlc.types.Arg(sgqlc.types.non_null(UUID), graphql_name='datasetId', default=None)),
        ('rql_name', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='rqlName', default=None)),
))
    )
    llmapi_config_for_sdk = sgqlc.types.Field(LLMApiConfig, graphql_name='LLMApiConfigForSdk', args=sgqlc.types.ArgDict((
        ('model_type', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='modelType', default=None)),
))
    )
    get_max_llm_prompt = sgqlc.types.Field(MaxLLmPrompt, graphql_name='getMaxLlmPrompt', args=sgqlc.types.ArgDict((
        ('llm_prompt_id', sgqlc.types.Arg(sgqlc.types.non_null(UUID), graphql_name='llmPromptId', default=None)),
        ('template_variables', sgqlc.types.Arg(JSON, graphql_name='templateVariables', default=None)),
        ('k_shot_match', sgqlc.types.Arg(String, graphql_name='kShotMatch', default=None)),
))
    )
    user_chat_threads = sgqlc.types.Field(sgqlc.types.list_of(JSON), graphql_name='userChatThreads', args=sgqlc.types.ArgDict((
        ('copilot_id', sgqlc.types.Arg(sgqlc.types.non_null(UUID), graphql_name='copilotId', default=None)),
        ('start_date', sgqlc.types.Arg(DateTime, graphql_name='startDate', default=None)),
        ('end_date', sgqlc.types.Arg(DateTime, graphql_name='endDate', default=None)),
))
    )
    user_chat_entries = sgqlc.types.Field(sgqlc.types.list_of(JSON), graphql_name='userChatEntries', args=sgqlc.types.ArgDict((
        ('thread_id', sgqlc.types.Arg(sgqlc.types.non_null(UUID), graphql_name='threadId', default=None)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
))
    )
    chat_thread = sgqlc.types.Field(MaxChatThread, graphql_name='chatThread', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(UUID), graphql_name='id', default=None)),
))
    )
    chat_entry = sgqlc.types.Field(MaxChatEntry, graphql_name='chatEntry', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(UUID), graphql_name='id', default=None)),
))
    )


class SharedThread(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('id', 'user_id', 'original_thread_id', 'copilot_id', 'shared_by', 'last_updated_utc', 'created_utc', 'is_deleted', 'link_to_shared_thread')
    id = sgqlc.types.Field(sgqlc.types.non_null(UUID), graphql_name='id')
    user_id = sgqlc.types.Field(sgqlc.types.non_null(UUID), graphql_name='userId')
    original_thread_id = sgqlc.types.Field(sgqlc.types.non_null(UUID), graphql_name='originalThreadId')
    copilot_id = sgqlc.types.Field(sgqlc.types.non_null(UUID), graphql_name='copilotId')
    shared_by = sgqlc.types.Field(String, graphql_name='sharedBy')
    last_updated_utc = sgqlc.types.Field(sgqlc.types.non_null(DateTime), graphql_name='lastUpdatedUTC')
    created_utc = sgqlc.types.Field(sgqlc.types.non_null(DateTime), graphql_name='createdUTC')
    is_deleted = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='isDeleted')
    link_to_shared_thread = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='linkToSharedThread')


class AzureOpenaiCompletionLLMApiConfig(sgqlc.types.Type, LLMApiConfig):
    __schema__ = schema
    __field_names__ = ('api_base_url', 'api_version', 'openai_model_name', 'max_tokens_input', 'max_tokens_content_generation', 'temperature', 'top_p', 'presence_penalty', 'frequency_penalty', 'cost_per_model_input_unit', 'cost_per_model_output_unit')
    api_base_url = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='apiBaseUrl')
    api_version = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='apiVersion')
    openai_model_name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='openaiModelName')
    max_tokens_input = sgqlc.types.Field(Int, graphql_name='maxTokensInput')
    max_tokens_content_generation = sgqlc.types.Field(Int, graphql_name='maxTokensContentGeneration')
    temperature = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='temperature')
    top_p = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='topP')
    presence_penalty = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='presencePenalty')
    frequency_penalty = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='frequencyPenalty')
    cost_per_model_input_unit = sgqlc.types.Field(Float, graphql_name='costPerModelInputUnit')
    cost_per_model_output_unit = sgqlc.types.Field(Float, graphql_name='costPerModelOutputUnit')


class AzureOpenaiEmbeddingLLMApiConfig(sgqlc.types.Type, LLMApiConfig):
    __schema__ = schema
    __field_names__ = ('api_base_url', 'api_version')
    api_base_url = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='apiBaseUrl')
    api_version = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='apiVersion')


class MaxCalculatedAttribute(sgqlc.types.Type, MaxDomainObject, MaxDomainAttribute, MaxDimensionAttribute):
    __schema__ = schema
    __field_names__ = ('rql',)
    rql = sgqlc.types.Field(String, graphql_name='rql')


class MaxCalculatedMetric(sgqlc.types.Type, MaxDomainObject):
    __schema__ = schema
    __field_names__ = ('display_format', 'rql', 'sql', 'agg_method', 'is_positive_direction_up', 'can_be_averaged', 'is_not_additive', 'growth_output_format', 'hide_percentage_change', 'simplified_data_type', 'metric_type')
    display_format = sgqlc.types.Field(String, graphql_name='displayFormat')
    rql = sgqlc.types.Field(String, graphql_name='rql')
    sql = sgqlc.types.Field(String, graphql_name='sql')
    agg_method = sgqlc.types.Field(sgqlc.types.non_null(DpsAggMethod), graphql_name='aggMethod')
    is_positive_direction_up = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='isPositiveDirectionUp')
    can_be_averaged = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='canBeAveraged')
    is_not_additive = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='isNotAdditive')
    growth_output_format = sgqlc.types.Field(String, graphql_name='growthOutputFormat')
    hide_percentage_change = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='hidePercentageChange')
    simplified_data_type = sgqlc.types.Field(SimplifiedDataType, graphql_name='simplifiedDataType')
    metric_type = sgqlc.types.Field(MetricType, graphql_name='metricType')


class MaxDimensionEntity(sgqlc.types.Type, MaxDomainObject, MaxDomainEntity):
    __schema__ = schema
    __field_names__ = ('primary_attribute', 'archetype')
    primary_attribute = sgqlc.types.Field('MaxPrimaryAttribute', graphql_name='primaryAttribute')
    archetype = sgqlc.types.Field(String, graphql_name='archetype')


class MaxFactEntity(sgqlc.types.Type, MaxDomainObject, MaxDomainEntity):
    __schema__ = schema
    __field_names__ = ()


class MaxMetricAttribute(sgqlc.types.Type, MaxDomainObject, MaxDomainAttribute):
    __schema__ = schema
    __field_names__ = ('db_metric_column', 'agg_method', 'is_row_level_filter', 'is_positive_direction_up', 'can_be_averaged', 'is_not_additive', 'growth_output_format', 'hide_percentage_change', 'sql_agg_expression', 'metric_type')
    db_metric_column = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='dbMetricColumn')
    agg_method = sgqlc.types.Field(sgqlc.types.non_null(DpsAggMethod), graphql_name='aggMethod')
    is_row_level_filter = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='isRowLevelFilter')
    is_positive_direction_up = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='isPositiveDirectionUp')
    can_be_averaged = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='canBeAveraged')
    is_not_additive = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='isNotAdditive')
    growth_output_format = sgqlc.types.Field(String, graphql_name='growthOutputFormat')
    hide_percentage_change = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='hidePercentageChange')
    sql_agg_expression = sgqlc.types.Field(String, graphql_name='sqlAggExpression')
    metric_type = sgqlc.types.Field(MetricType, graphql_name='metricType')


class MaxNormalAttribute(sgqlc.types.Type, MaxDomainObject, MaxDomainAttribute, MaxDimensionAttribute):
    __schema__ = schema
    __field_names__ = ('db_column', 'db_secondary_column')
    db_column = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='dbColumn')
    db_secondary_column = sgqlc.types.Field(String, graphql_name='dbSecondaryColumn')


class MaxPrimaryAttribute(sgqlc.types.Type, MaxDomainObject, MaxDomainAttribute, MaxDimensionAttribute):
    __schema__ = schema
    __field_names__ = ('db_primary_key_columns', 'db_secondary_column')
    db_primary_key_columns = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))), graphql_name='dbPrimaryKeyColumns')
    db_secondary_column = sgqlc.types.Field(String, graphql_name='dbSecondaryColumn')


class MaxReferenceAttribute(sgqlc.types.Type, MaxDomainObject, MaxDomainAttribute, MaxDimensionAttribute):
    __schema__ = schema
    __field_names__ = ('db_foreign_key_columns', 'referenced_dimension_entity_id')
    db_foreign_key_columns = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(String)), graphql_name='dbForeignKeyColumns')
    referenced_dimension_entity_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='referencedDimensionEntityId')


class OpenaiCompletionLLMApiConfig(sgqlc.types.Type, LLMApiConfig):
    __schema__ = schema
    __field_names__ = ('organization', 'max_tokens_content_generation', 'temperature', 'top_p', 'presence_penalty', 'frequency_penalty', 'cost_per_model_input_unit', 'cost_per_model_output_unit')
    organization = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='organization')
    max_tokens_content_generation = sgqlc.types.Field(Int, graphql_name='maxTokensContentGeneration')
    temperature = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='temperature')
    top_p = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='topP')
    presence_penalty = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='presencePenalty')
    frequency_penalty = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='frequencyPenalty')
    cost_per_model_input_unit = sgqlc.types.Field(Float, graphql_name='costPerModelInputUnit')
    cost_per_model_output_unit = sgqlc.types.Field(Float, graphql_name='costPerModelOutputUnit')


class OpenaiEmbeddingLLMApiConfig(sgqlc.types.Type, LLMApiConfig):
    __schema__ = schema
    __field_names__ = ('organization',)
    organization = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='organization')



########################################################################
# Unions
########################################################################

########################################################################
# Schema Entry Points
########################################################################
schema.query_type = Query
schema.mutation_type = Mutation
schema.subscription_type = None

