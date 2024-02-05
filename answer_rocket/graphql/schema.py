import sgqlc.types
import sgqlc.types.datetime


schema = sgqlc.types.Schema()



########################################################################
# Scalars and Enumerations
########################################################################
Boolean = sgqlc.types.Boolean

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


class SimplifiedDataType(sgqlc.types.Enum):
    __schema__ = schema
    __choices__ = ('BOOLEAN', 'DATE', 'NUMBER', 'STRING')


String = sgqlc.types.String

class UUID(sgqlc.types.Scalar):
    __schema__ = schema



########################################################################
# Input Objects
########################################################################

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
    __field_names__ = ('type', 'id', 'name', 'description', 'output_label', 'synonyms', 'output_label_plural', 'hide_from_user', 'misc_info', 'db_table', 'attributes')
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
    attributes = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(MaxDomainAttribute))), graphql_name='attributes')


class ChatThread(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('id', 'entry_count', 'title', 'pinned_dataset')
    id = sgqlc.types.Field(sgqlc.types.non_null(UUID), graphql_name='id')
    entry_count = sgqlc.types.Field(Int, graphql_name='entryCount', args=sgqlc.types.ArgDict((
        ('most_recent_entry_inclusive', sgqlc.types.Arg(UUID, graphql_name='mostRecentEntryInclusive', default=None)),
))
    )
    title = sgqlc.types.Field(String, graphql_name='title')
    pinned_dataset = sgqlc.types.Field(UUID, graphql_name='pinnedDataset')


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
    __field_names__ = ('copilot_id', 'name', 'description', 'system_prompt', 'beta_yaml', 'global_python_code')
    copilot_id = sgqlc.types.Field(sgqlc.types.non_null(UUID), graphql_name='copilotId')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    description = sgqlc.types.Field(String, graphql_name='description')
    system_prompt = sgqlc.types.Field(String, graphql_name='systemPrompt')
    beta_yaml = sgqlc.types.Field(String, graphql_name='betaYaml')
    global_python_code = sgqlc.types.Field(String, graphql_name='globalPythonCode')


class MaxCopilotSkill(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('copilot_skill_id', 'name', 'detailed_name', 'description', 'detailed_description', 'dataset_id', 'skill_chat_questions', 'yaml_code', 'skill_code', 'misc_info', 'scheduling_only')
    copilot_skill_id = sgqlc.types.Field(sgqlc.types.non_null(UUID), graphql_name='copilotSkillId')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    detailed_name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='detailedName')
    description = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='description')
    detailed_description = sgqlc.types.Field(String, graphql_name='detailedDescription')
    dataset_id = sgqlc.types.Field(UUID, graphql_name='datasetId')
    skill_chat_questions = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of('MaxCopilotSkillChatQuestion')), graphql_name='skillChatQuestions')
    yaml_code = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='yamlCode')
    skill_code = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='skillCode')
    misc_info = sgqlc.types.Field(JSON, graphql_name='miscInfo')
    scheduling_only = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='schedulingOnly')


class MaxCopilotSkillChatQuestion(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('copilot_skill_chat_question_id', 'question', 'expected_completion_response')
    copilot_skill_chat_question_id = sgqlc.types.Field(sgqlc.types.non_null(UUID), graphql_name='copilotSkillChatQuestionId')
    question = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='question')
    expected_completion_response = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='expectedCompletionResponse')


class MaxDatabase(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('database_id', 'name', 'dbms', 'schema')
    database_id = sgqlc.types.Field(sgqlc.types.non_null(UUID), graphql_name='databaseId')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    dbms = sgqlc.types.Field(String, graphql_name='dbms')
    schema = sgqlc.types.Field(String, graphql_name='schema')


class MaxDataset(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('dataset_id', 'name', 'domain_objects', 'misc_info', 'database', 'tables', 'dimension_value_distribution_map', 'date_range_boundary_attribute_id')
    dataset_id = sgqlc.types.Field(sgqlc.types.non_null(UUID), graphql_name='datasetId')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    domain_objects = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(MaxDomainObject))), graphql_name='domainObjects')
    misc_info = sgqlc.types.Field(String, graphql_name='miscInfo')
    database = sgqlc.types.Field(MaxDatabase, graphql_name='database')
    tables = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('MaxTable'))), graphql_name='tables')
    dimension_value_distribution_map = sgqlc.types.Field(JSON, graphql_name='dimensionValueDistributionMap')
    date_range_boundary_attribute_id = sgqlc.types.Field(String, graphql_name='dateRangeBoundaryAttributeId')


class MaxMutationResponse(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('success', 'code', 'error')
    success = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='success')
    code = sgqlc.types.Field(String, graphql_name='code')
    error = sgqlc.types.Field(String, graphql_name='error')


class MaxTable(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('name', 'columns')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    columns = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(MaxColumn))), graphql_name='columns')


class Mutation(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('create_max_copilot_skill_chat_question', 'update_max_copilot_skill_chat_question', 'delete_max_copilot_skill_chat_question', 'update_chat_answer_payload', 'ask_chat_question')
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
    update_chat_answer_payload = sgqlc.types.Field(JSON, graphql_name='updateChatAnswerPayload', args=sgqlc.types.ArgDict((
        ('answer_id', sgqlc.types.Arg(sgqlc.types.non_null(UUID), graphql_name='answerId', default=None)),
        ('payload', sgqlc.types.Arg(sgqlc.types.non_null(JSON), graphql_name='payload', default=None)),
))
    )
    ask_chat_question = sgqlc.types.Field(JSON, graphql_name='askChatQuestion', args=sgqlc.types.ArgDict((
        ('copilot_id', sgqlc.types.Arg(sgqlc.types.non_null(UUID), graphql_name='copilotId', default=None)),
        ('question', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='question', default=None)),
        ('thread_id', sgqlc.types.Arg(UUID, graphql_name='threadId', default=None)),
))
    )


class Query(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('ping', 'get_copilot_skill_artifact_by_path', 'get_copilot_info', 'get_copilot_skill', 'run_copilot_skill', 'execute_sql_query', 'execute_rql_query', 'get_dataset_id', 'get_dataset', 'get_domain_object', 'get_domain_object_by_name', 'llmapi_config_for_sdk', 'user_chat_threads', 'user_chat_entries')
    ping = sgqlc.types.Field(String, graphql_name='ping')
    get_copilot_skill_artifact_by_path = sgqlc.types.Field(CopilotSkillArtifact, graphql_name='getCopilotSkillArtifactByPath', args=sgqlc.types.ArgDict((
        ('copilot_id', sgqlc.types.Arg(sgqlc.types.non_null(UUID), graphql_name='copilotId', default=None)),
        ('copilot_skill_id', sgqlc.types.Arg(sgqlc.types.non_null(UUID), graphql_name='copilotSkillId', default=None)),
        ('artifact_path', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='artifactPath', default=None)),
))
    )
    get_copilot_info = sgqlc.types.Field(MaxCopilot, graphql_name='getCopilotInfo', args=sgqlc.types.ArgDict((
        ('copilot_id', sgqlc.types.Arg(sgqlc.types.non_null(UUID), graphql_name='copilotId', default=None)),
))
    )
    get_copilot_skill = sgqlc.types.Field(MaxCopilotSkill, graphql_name='getCopilotSkill', args=sgqlc.types.ArgDict((
        ('copilot_id', sgqlc.types.Arg(sgqlc.types.non_null(UUID), graphql_name='copilotId', default=None)),
        ('copilot_skill_id', sgqlc.types.Arg(sgqlc.types.non_null(UUID), graphql_name='copilotSkillId', default=None)),
))
    )
    run_copilot_skill = sgqlc.types.Field(CopilotSkillRunResponse, graphql_name='runCopilotSkill', args=sgqlc.types.ArgDict((
        ('copilot_id', sgqlc.types.Arg(sgqlc.types.non_null(UUID), graphql_name='copilotId', default=None)),
        ('skill_name', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='skillName', default=None)),
        ('parameters', sgqlc.types.Arg(JSON, graphql_name='parameters', default=None)),
))
    )
    execute_sql_query = sgqlc.types.Field(ExecuteSqlQueryResponse, graphql_name='executeSqlQuery', args=sgqlc.types.ArgDict((
        ('database_id', sgqlc.types.Arg(sgqlc.types.non_null(UUID), graphql_name='databaseId', default=None)),
        ('sql_query', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='sqlQuery', default=None)),
        ('row_limit', sgqlc.types.Arg(Int, graphql_name='rowLimit', default=None)),
        ('copilot_id', sgqlc.types.Arg(UUID, graphql_name='copilotId', default=None)),
))
    )
    execute_rql_query = sgqlc.types.Field(ExecuteRqlQueryResponse, graphql_name='executeRqlQuery', args=sgqlc.types.ArgDict((
        ('dataset_id', sgqlc.types.Arg(sgqlc.types.non_null(UUID), graphql_name='datasetId', default=None)),
        ('rql_query', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='rqlQuery', default=None)),
        ('row_limit', sgqlc.types.Arg(Int, graphql_name='rowLimit', default=None)),
        ('copilot_id', sgqlc.types.Arg(UUID, graphql_name='copilotId', default=None)),
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


class AzureOpenaiCompletionLLMApiConfig(sgqlc.types.Type, LLMApiConfig):
    __schema__ = schema
    __field_names__ = ('api_base_url', 'api_version', 'openai_model_name', 'max_tokens_content_generation', 'temperature', 'top_p', 'presence_penalty', 'frequency_penalty')
    api_base_url = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='apiBaseUrl')
    api_version = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='apiVersion')
    openai_model_name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='openaiModelName')
    max_tokens_content_generation = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='maxTokensContentGeneration')
    temperature = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='temperature')
    top_p = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='topP')
    presence_penalty = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='presencePenalty')
    frequency_penalty = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='frequencyPenalty')


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
    __field_names__ = ('organization', 'max_tokens_content_generation', 'temperature', 'top_p', 'presence_penalty', 'frequency_penalty')
    organization = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='organization')
    max_tokens_content_generation = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='maxTokensContentGeneration')
    temperature = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='temperature')
    top_p = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='topP')
    presence_penalty = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='presencePenalty')
    frequency_penalty = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='frequencyPenalty')


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

