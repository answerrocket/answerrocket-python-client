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


class ContentBlockType(sgqlc.types.Enum):
    __schema__ = schema
    __choices__ = ('INSIGHTS', 'VISUAL')


class DatasetDataInterval(sgqlc.types.Enum):
    __schema__ = schema
    __choices__ = ('DATE', 'MONTH', 'QUARTER', 'WEEK', 'YEAR')


DateTime = sgqlc.types.datetime.DateTime

class DpsAggMethod(sgqlc.types.Enum):
    __schema__ = schema
    __choices__ = ('AVG', 'COUNT', 'CUSTOM', 'MAX', 'MIN', 'NONE', 'SUM')


class FeedbackType(sgqlc.types.Enum):
    __schema__ = schema
    __choices__ = ('CHAT_NEGATIVE', 'CHAT_POSITIVE')


Float = sgqlc.types.Float

class GrowthType(sgqlc.types.Enum):
    __schema__ = schema
    __choices__ = ('DIFFERENCE', 'PERCENT_CHANGE')


Int = sgqlc.types.Int

class JSON(sgqlc.types.Scalar):
    __schema__ = schema


class LlmResponse(sgqlc.types.Scalar):
    __schema__ = schema


class MetricType(sgqlc.types.Enum):
    __schema__ = schema
    __choices__ = ('BASIC', 'RATIO', 'SHARE')


class ModelTypes(sgqlc.types.Enum):
    __schema__ = schema
    __choices__ = ('CHAT', 'EMBEDDINGS', 'NARRATIVE')


class QuestionType(sgqlc.types.Enum):
    __schema__ = schema
    __choices__ = ('DRILLDOWN', 'EXAMPLE', 'FOLLOWUP', 'RESEARCHER_REPORT', 'SAVED', 'SCHEDULED', 'SHARED', 'SKILL_PREVIEW', 'TEST_RUN', 'USER_WRITTEN', 'XML_CALLBACK')


class SimplifiedDataType(sgqlc.types.Enum):
    __schema__ = schema
    __choices__ = ('BOOLEAN', 'DATE', 'NUMBER', 'STRING')


String = sgqlc.types.String

class TableSearchType(sgqlc.types.Enum):
    __schema__ = schema
    __choices__ = ('TABLES_AND_VIEWS', 'TABLES_ONLY', 'VIEWS_ONLY')


class ThreadType(sgqlc.types.Enum):
    __schema__ = schema
    __choices__ = ('CHAT', 'COPILOT_QUESTION_PREVIEW', 'RESEARCH', 'SHARED', 'SKILL', 'TEST')


class UUID(sgqlc.types.Scalar):
    __schema__ = schema



########################################################################
# Input Objects
########################################################################
class ChatArtifactSearchInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('name_contains', 'created_utc_start', 'created_utc_end', 'misc_info')
    name_contains = sgqlc.types.Field(String, graphql_name='nameContains')
    created_utc_start = sgqlc.types.Field(DateTime, graphql_name='createdUtcStart')
    created_utc_end = sgqlc.types.Field(DateTime, graphql_name='createdUtcEnd')
    misc_info = sgqlc.types.Field(JSON, graphql_name='miscInfo')


class DatabaseSearchInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('name_contains',)
    name_contains = sgqlc.types.Field(String, graphql_name='nameContains')


class DatabaseTableSearchInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('name_contains', 'table_search_type')
    name_contains = sgqlc.types.Field(String, graphql_name='nameContains')
    table_search_type = sgqlc.types.Field(TableSearchType, graphql_name='tableSearchType')


class DatasetSearchInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('database_id', 'name_contains')
    database_id = sgqlc.types.Field(UUID, graphql_name='databaseId')
    name_contains = sgqlc.types.Field(String, graphql_name='nameContains')


class FunctionCallMessageInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('name', 'arguments')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    arguments = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='arguments')


class LlmChatMessage(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('role', 'content')
    role = sgqlc.types.Field(String, graphql_name='role')
    content = sgqlc.types.Field(String, graphql_name='content')


class LlmModelSelection(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('assistant_id', 'model_override')
    assistant_id = sgqlc.types.Field(UUID, graphql_name='assistantId')
    model_override = sgqlc.types.Field(String, graphql_name='modelOverride')


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


class PagingInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('page_num', 'page_size')
    page_num = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='pageNum')
    page_size = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='pageSize')



########################################################################
# Output Objects and Interfaces
########################################################################
class DomainArtifact(sgqlc.types.Interface):
    __schema__ = schema
    __field_names__ = ('id', 'name', 'description', 'output_label', 'is_active', 'misc_info')
    id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='id')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    description = sgqlc.types.Field(String, graphql_name='description')
    output_label = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='outputLabel')
    is_active = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='isActive')
    misc_info = sgqlc.types.Field(String, graphql_name='miscInfo')


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
    __field_names__ = ('type', 'id', 'name', 'description', 'output_label', 'synonyms', 'output_label_plural', 'hide_from_user', 'misc_info', 'display_format', 'headline_name', 'is_favorite', 'simplified_data_type', 'sql', 'domain_entity', 'dimension_value_mapping_list', 'dimension_values', 'default_filter_value', 'is_required_in_query', 'db_sort_column')
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
    dimension_values = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))), graphql_name='dimensionValues')
    default_filter_value = sgqlc.types.Field(String, graphql_name='defaultFilterValue')
    is_required_in_query = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='isRequiredInQuery')
    db_sort_column = sgqlc.types.Field(String, graphql_name='dbSortColumn')


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


class BlockData(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('answer_id', 'block_index', 'content_block')
    answer_id = sgqlc.types.Field(sgqlc.types.non_null(UUID), graphql_name='answerId')
    block_index = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='blockIndex')
    content_block = sgqlc.types.Field(sgqlc.types.non_null('ContentBlock'), graphql_name='contentBlock')


class ChatArtifact(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('chat_artifact_id', 'name', 'owner_user_id', 'chat_entry_id', 'content_block_id', 'block_data', 'misc_info', 'created_utc')
    chat_artifact_id = sgqlc.types.Field(sgqlc.types.non_null(UUID), graphql_name='chatArtifactId')
    name = sgqlc.types.Field(String, graphql_name='name')
    owner_user_id = sgqlc.types.Field(sgqlc.types.non_null(UUID), graphql_name='ownerUserId')
    chat_entry_id = sgqlc.types.Field(sgqlc.types.non_null(UUID), graphql_name='chatEntryId')
    content_block_id = sgqlc.types.Field(sgqlc.types.non_null(UUID), graphql_name='contentBlockId')
    block_data = sgqlc.types.Field(BlockData, graphql_name='blockData')
    misc_info = sgqlc.types.Field(JSON, graphql_name='miscInfo')
    created_utc = sgqlc.types.Field(sgqlc.types.non_null(DateTime), graphql_name='createdUtc')


class ChatFeedback(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('type', 'feedback', 'user_id')
    type = sgqlc.types.Field(String, graphql_name='type')
    feedback = sgqlc.types.Field(JSON, graphql_name='feedback')
    user_id = sgqlc.types.Field(UUID, graphql_name='userId')


class ContentBlock(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('id', 'title', 'payload', 'layout_json', 'type', 'export_as_landscape')
    id = sgqlc.types.Field(sgqlc.types.non_null(UUID), graphql_name='id')
    title = sgqlc.types.Field(String, graphql_name='title')
    payload = sgqlc.types.Field(String, graphql_name='payload')
    layout_json = sgqlc.types.Field(String, graphql_name='layoutJson')
    type = sgqlc.types.Field(ContentBlockType, graphql_name='type')
    export_as_landscape = sgqlc.types.Field(Boolean, graphql_name='exportAsLandscape')


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


class CopilotTopic(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('copilot_topic_id', 'name', 'description', 'research_outline', 'presentation_outline', 'created_user_id', 'created_user_name', 'created_utc', 'last_modified_user_id', 'last_modified_user_name', 'last_modified_utc', 'is_active')
    copilot_topic_id = sgqlc.types.Field(sgqlc.types.non_null(UUID), graphql_name='copilotTopicId')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    description = sgqlc.types.Field(String, graphql_name='description')
    research_outline = sgqlc.types.Field(String, graphql_name='researchOutline')
    presentation_outline = sgqlc.types.Field(String, graphql_name='presentationOutline')
    created_user_id = sgqlc.types.Field(sgqlc.types.non_null(UUID), graphql_name='createdUserId')
    created_user_name = sgqlc.types.Field(String, graphql_name='createdUserName')
    created_utc = sgqlc.types.Field(sgqlc.types.non_null(DateTime), graphql_name='createdUtc')
    last_modified_user_id = sgqlc.types.Field(sgqlc.types.non_null(UUID), graphql_name='lastModifiedUserId')
    last_modified_user_name = sgqlc.types.Field(String, graphql_name='lastModifiedUserName')
    last_modified_utc = sgqlc.types.Field(sgqlc.types.non_null(DateTime), graphql_name='lastModifiedUtc')
    is_active = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='isActive')


class CostInfo(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('completion_tokens', 'prompt_tokens', 'total_tokens', 'cost_estimate_usd', 'model')
    completion_tokens = sgqlc.types.Field(Int, graphql_name='completionTokens')
    prompt_tokens = sgqlc.types.Field(Int, graphql_name='promptTokens')
    total_tokens = sgqlc.types.Field(Int, graphql_name='totalTokens')
    cost_estimate_usd = sgqlc.types.Field(Float, graphql_name='costEstimateUsd')
    model = sgqlc.types.Field(String, graphql_name='model')


class CreateDatasetFromTableResponse(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('dataset_id', 'queued_task_guid', 'error')
    dataset_id = sgqlc.types.Field(UUID, graphql_name='datasetId')
    queued_task_guid = sgqlc.types.Field(UUID, graphql_name='queuedTaskGuid')
    error = sgqlc.types.Field(String, graphql_name='error')


class CreateMaxCopilotSkillChatQuestionResponse(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('copilot_skill_chat_question_id', 'success', 'code', 'error')
    copilot_skill_chat_question_id = sgqlc.types.Field(UUID, graphql_name='copilotSkillChatQuestionId')
    success = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='success')
    code = sgqlc.types.Field(String, graphql_name='code')
    error = sgqlc.types.Field(String, graphql_name='error')


class Database(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('database_id', 'name', 'dbms', 'description', 'llm_description', 'mermaid_er_diagram', 'k_shot_limit')
    database_id = sgqlc.types.Field(sgqlc.types.non_null(UUID), graphql_name='databaseId')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    dbms = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='dbms')
    description = sgqlc.types.Field(String, graphql_name='description')
    llm_description = sgqlc.types.Field(String, graphql_name='llmDescription')
    mermaid_er_diagram = sgqlc.types.Field(String, graphql_name='mermaidErDiagram')
    k_shot_limit = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='kShotLimit')


class DatabaseTable(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('table_name',)
    table_name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='tableName')


class Dataset(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('dataset_id', 'name', 'description', 'database_id', 'dimensions', 'metrics', 'misc_info', 'source_table', 'source_sql', 'derived_table_alias', 'data_interval', 'dataset_min_date', 'dataset_max_date', 'query_row_limit', 'use_database_casing', 'k_shot_limit')
    dataset_id = sgqlc.types.Field(sgqlc.types.non_null(UUID), graphql_name='datasetId')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    description = sgqlc.types.Field(String, graphql_name='description')
    database_id = sgqlc.types.Field(sgqlc.types.non_null(UUID), graphql_name='databaseId')
    dimensions = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of('Dimension')), graphql_name='dimensions')
    metrics = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of('Metric')), graphql_name='metrics')
    misc_info = sgqlc.types.Field(String, graphql_name='miscInfo')
    source_table = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='sourceTable')
    source_sql = sgqlc.types.Field(String, graphql_name='sourceSql')
    derived_table_alias = sgqlc.types.Field(String, graphql_name='derivedTableAlias')
    data_interval = sgqlc.types.Field(DatasetDataInterval, graphql_name='dataInterval')
    dataset_min_date = sgqlc.types.Field(DateTime, graphql_name='datasetMinDate')
    dataset_max_date = sgqlc.types.Field(DateTime, graphql_name='datasetMaxDate')
    query_row_limit = sgqlc.types.Field(Int, graphql_name='queryRowLimit')
    use_database_casing = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='useDatabaseCasing')
    k_shot_limit = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='kShotLimit')


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


class GenerateVisualizationResponse(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('success', 'code', 'error', 'visualization')
    success = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='success')
    code = sgqlc.types.Field(String, graphql_name='code')
    error = sgqlc.types.Field(String, graphql_name='error')
    visualization = sgqlc.types.Field(JSON, graphql_name='visualization')


class GroundedValueResponse(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('matched_value', 'match_quality', 'match_type', 'mapped_indicator', 'mapped_value', 'preferred', 'domain_entity', 'other_matches')
    matched_value = sgqlc.types.Field(String, graphql_name='matchedValue')
    match_quality = sgqlc.types.Field(Float, graphql_name='matchQuality')
    match_type = sgqlc.types.Field(String, graphql_name='matchType')
    mapped_indicator = sgqlc.types.Field(Boolean, graphql_name='mappedIndicator')
    mapped_value = sgqlc.types.Field(String, graphql_name='mappedValue')
    preferred = sgqlc.types.Field(Boolean, graphql_name='preferred')
    domain_entity = sgqlc.types.Field(String, graphql_name='domainEntity')
    other_matches = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(JSON)), graphql_name='otherMatches')


class HydratedReport(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('copilot_id', 'copilot_skill_id', 'dataset_id', 'dataset_ids', 'detailed_description', 'key', 'name', 'package_name', 'parameters', 'scheduling_only', 'tool_description', 'tool_name', 'tool_type', 'type', 'use_predicate_filters', 'meta')
    copilot_id = sgqlc.types.Field(sgqlc.types.non_null(UUID), graphql_name='copilotId')
    copilot_skill_id = sgqlc.types.Field(sgqlc.types.non_null(UUID), graphql_name='copilotSkillId')
    dataset_id = sgqlc.types.Field(UUID, graphql_name='datasetId')
    dataset_ids = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='datasetIds')
    detailed_description = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='detailedDescription')
    key = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='key')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    package_name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='packageName')
    parameters = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('SkillParameter'))), graphql_name='parameters')
    scheduling_only = sgqlc.types.Field(Boolean, graphql_name='schedulingOnly')
    tool_description = sgqlc.types.Field(String, graphql_name='toolDescription')
    tool_name = sgqlc.types.Field(String, graphql_name='toolName')
    tool_type = sgqlc.types.Field(String, graphql_name='toolType')
    type = sgqlc.types.Field(String, graphql_name='type')
    use_predicate_filters = sgqlc.types.Field(Boolean, graphql_name='usePredicateFilters')
    meta = sgqlc.types.Field(JSON, graphql_name='meta')


class MatchValues(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('automatic_db_whitelist', 'constrained_values', 'dataset_id', 'default_performance_metric', 'inverse_map', 'phrase_template', 'popular_values', 'value_collection_name', 'dataset_date_dimensions', 'dataset_dimensions', 'dataset_metrics', 'predicate_vocab')
    automatic_db_whitelist = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='automaticDbWhitelist')
    constrained_values = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='constrainedValues')
    dataset_id = sgqlc.types.Field(String, graphql_name='datasetId')
    default_performance_metric = sgqlc.types.Field(JSON, graphql_name='defaultPerformanceMetric')
    inverse_map = sgqlc.types.Field(JSON, graphql_name='inverseMap')
    phrase_template = sgqlc.types.Field(String, graphql_name='phraseTemplate')
    popular_values = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='popularValues')
    value_collection_name = sgqlc.types.Field(String, graphql_name='valueCollectionName')
    dataset_date_dimensions = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='datasetDateDimensions')
    dataset_dimensions = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='datasetDimensions')
    dataset_metrics = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='datasetMetrics')
    predicate_vocab = sgqlc.types.Field(JSON, graphql_name='predicateVocab')


class MaxAgentWorkflow(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('agent_workflow_id', 'trace')
    agent_workflow_id = sgqlc.types.Field(sgqlc.types.non_null(UUID), graphql_name='agentWorkflowId')
    trace = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('MaxToolCall'))), graphql_name='trace')


class MaxAgentWorkflowReferencedState(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('name', 'content')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    content = sgqlc.types.Field(JSON, graphql_name='content')


class MaxAgentWorkflowTool(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('name', 'description')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    description = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='description')


class MaxAgentWorkflowUpdatedState(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('name', 'content')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    content = sgqlc.types.Field(JSON, graphql_name='content')


class MaxChatEntry(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('id', 'thread_id', 'question', 'answer', 'feedback', 'user', 'skill_memory_payload')
    id = sgqlc.types.Field(sgqlc.types.non_null(UUID), graphql_name='id')
    thread_id = sgqlc.types.Field(UUID, graphql_name='threadId')
    question = sgqlc.types.Field('MaxChatQuestion', graphql_name='question')
    answer = sgqlc.types.Field('MaxChatResult', graphql_name='answer')
    feedback = sgqlc.types.Field(ChatFeedback, graphql_name='feedback')
    user = sgqlc.types.Field('MaxChatUser', graphql_name='user')
    skill_memory_payload = sgqlc.types.Field(JSON, graphql_name='skillMemoryPayload')


class MaxChatQuestion(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('asked_at', 'nl')
    asked_at = sgqlc.types.Field(DateTime, graphql_name='askedAt')
    nl = sgqlc.types.Field(String, graphql_name='nl')


class MaxChatResult(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('answer_id', 'answered_at', 'copilot_skill_id', 'has_finished', 'error', 'is_new_thread', 'message', 'report_results', 'thread_id', 'user_id', 'general_diagnostics', 'chat_pipeline_profile', 'messages_after_token_limit')
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
    general_diagnostics = sgqlc.types.Field(JSON, graphql_name='generalDiagnostics')
    chat_pipeline_profile = sgqlc.types.Field(JSON, graphql_name='chatPipelineProfile')
    messages_after_token_limit = sgqlc.types.Field(Int, graphql_name='messagesAfterTokenLimit')


class MaxChatThread(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('id', 'entry_count', 'title', 'copilot_id', 'entries')
    id = sgqlc.types.Field(sgqlc.types.non_null(UUID), graphql_name='id')
    entry_count = sgqlc.types.Field(Int, graphql_name='entryCount')
    title = sgqlc.types.Field(String, graphql_name='title')
    copilot_id = sgqlc.types.Field(sgqlc.types.non_null(UUID), graphql_name='copilotId')
    entries = sgqlc.types.Field(sgqlc.types.list_of(MaxChatEntry), graphql_name='entries')


class MaxChatUser(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('id', 'given_name', 'family_name', 'email_address', 'groups')
    id = sgqlc.types.Field(sgqlc.types.non_null(UUID), graphql_name='id')
    given_name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='givenName')
    family_name = sgqlc.types.Field(String, graphql_name='familyName')
    email_address = sgqlc.types.Field(String, graphql_name='emailAddress')
    groups = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='groups')


class MaxColumn(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('name', 'jdbc_type', 'length', 'precision', 'scale')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    jdbc_type = sgqlc.types.Field(String, graphql_name='jdbcType')
    length = sgqlc.types.Field(Int, graphql_name='length')
    precision = sgqlc.types.Field(Int, graphql_name='precision')
    scale = sgqlc.types.Field(Int, graphql_name='scale')


class MaxContentBlock(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('id', 'title', 'payload', 'type', 'layout_json')
    id = sgqlc.types.Field(sgqlc.types.non_null(UUID), graphql_name='id')
    title = sgqlc.types.Field(String, graphql_name='title')
    payload = sgqlc.types.Field(String, graphql_name='payload')
    type = sgqlc.types.Field(String, graphql_name='type')
    layout_json = sgqlc.types.Field(String, graphql_name='layoutJson')


class MaxCopilot(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('copilot_id', 'name', 'description', 'system_prompt', 'beta_yaml', 'global_python_code', 'copilot_questions', 'connection_datasets', 'copilot_skill_ids', 'copilot_topics', 'database_id', 'dataset_id')
    copilot_id = sgqlc.types.Field(sgqlc.types.non_null(UUID), graphql_name='copilotId')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    description = sgqlc.types.Field(String, graphql_name='description')
    system_prompt = sgqlc.types.Field(String, graphql_name='systemPrompt')
    beta_yaml = sgqlc.types.Field(String, graphql_name='betaYaml')
    global_python_code = sgqlc.types.Field(String, graphql_name='globalPythonCode')
    copilot_questions = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('MaxCopilotQuestion'))), graphql_name='copilotQuestions')
    connection_datasets = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('MaxCopilotConnectionDataset'))), graphql_name='connectionDatasets')
    copilot_skill_ids = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(UUID))), graphql_name='copilotSkillIds')
    copilot_topics = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(CopilotTopic))), graphql_name='copilotTopics')
    database_id = sgqlc.types.Field(UUID, graphql_name='databaseId')
    dataset_id = sgqlc.types.Field(UUID, graphql_name='datasetId')


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
    __field_names__ = ('copilot_skill_id', 'name', 'copilot_skill_type', 'detailed_name', 'description', 'detailed_description', 'dataset_id', 'parameters', 'skill_chat_questions', 'yaml_code', 'skill_code', 'misc_info', 'scheduling_only', 'copilot_skill_nodes', 'capabilities', 'limitations', 'example_questions', 'parameter_guidance')
    copilot_skill_id = sgqlc.types.Field(sgqlc.types.non_null(UUID), graphql_name='copilotSkillId')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    copilot_skill_type = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='copilotSkillType')
    detailed_name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='detailedName')
    description = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='description')
    detailed_description = sgqlc.types.Field(String, graphql_name='detailedDescription')
    dataset_id = sgqlc.types.Field(UUID, graphql_name='datasetId')
    parameters = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('MaxCopilotSkillParameter'))), graphql_name='parameters')
    skill_chat_questions = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of('MaxCopilotSkillChatQuestion')), graphql_name='skillChatQuestions')
    yaml_code = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='yamlCode')
    skill_code = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='skillCode')
    misc_info = sgqlc.types.Field(JSON, graphql_name='miscInfo')
    scheduling_only = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='schedulingOnly')
    copilot_skill_nodes = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('MaxCopilotSkillNode'))), graphql_name='copilotSkillNodes')
    capabilities = sgqlc.types.Field(String, graphql_name='capabilities')
    limitations = sgqlc.types.Field(String, graphql_name='limitations')
    example_questions = sgqlc.types.Field(String, graphql_name='exampleQuestions')
    parameter_guidance = sgqlc.types.Field(String, graphql_name='parameterGuidance')


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
    skill_component_id = sgqlc.types.Field(UUID, graphql_name='skillComponentId')
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


class MaxCopilotSkillParameter(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('copilot_skill_parameter_id', 'name', 'value', 'parameter_source_key', 'is_multi', 'llm_description', 'metadata_field', 'constrained_values', 'description', 'copilot_parameter_type', 'is_active', 'is_deleted', 'created_user_id', 'created_utc', 'last_modified_user_id', 'last_modified_utc', 'version')
    copilot_skill_parameter_id = sgqlc.types.Field(sgqlc.types.non_null(UUID), graphql_name='copilotSkillParameterId')
    name = sgqlc.types.Field(String, graphql_name='name')
    value = sgqlc.types.Field(String, graphql_name='value')
    parameter_source_key = sgqlc.types.Field(String, graphql_name='parameterSourceKey')
    is_multi = sgqlc.types.Field(Boolean, graphql_name='isMulti')
    llm_description = sgqlc.types.Field(String, graphql_name='llmDescription')
    metadata_field = sgqlc.types.Field(String, graphql_name='metadataField')
    constrained_values = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='constrainedValues')
    description = sgqlc.types.Field(String, graphql_name='description')
    copilot_parameter_type = sgqlc.types.Field(String, graphql_name='copilotParameterType')
    is_active = sgqlc.types.Field(Boolean, graphql_name='isActive')
    is_deleted = sgqlc.types.Field(Boolean, graphql_name='isDeleted')
    created_user_id = sgqlc.types.Field(sgqlc.types.non_null(UUID), graphql_name='createdUserId')
    created_utc = sgqlc.types.Field(sgqlc.types.non_null(DateTime), graphql_name='createdUtc')
    last_modified_user_id = sgqlc.types.Field(sgqlc.types.non_null(UUID), graphql_name='lastModifiedUserId')
    last_modified_utc = sgqlc.types.Field(sgqlc.types.non_null(DateTime), graphql_name='lastModifiedUtc')
    version = sgqlc.types.Field(sgqlc.types.non_null(UUID), graphql_name='version')


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
    __field_names__ = ('dataset_id', 'name', 'description', 'domain_objects', 'metrics', 'dimensions', 'misc_info', 'database', 'tables', 'dimension_value_distribution_map', 'date_range_boundary_attribute_id', 'dimension_hierarchies', 'metric_hierarchies', 'domain_attribute_statistics', 'default_performance_metric_id', 'dataset_min_date', 'dataset_max_date', 'query_row_limit', 'use_database_casing')
    dataset_id = sgqlc.types.Field(sgqlc.types.non_null(UUID), graphql_name='datasetId')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    description = sgqlc.types.Field(String, graphql_name='description')
    domain_objects = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(MaxDomainObject))), graphql_name='domainObjects')
    metrics = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of('Metric')), graphql_name='metrics')
    dimensions = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of('Dimension')), graphql_name='dimensions')
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
    __field_names__ = ('title', 'report_name', 'parameters', 'custom_payload', 'content_blocks', 'gzipped_dataframes_and_metadata')
    title = sgqlc.types.Field(String, graphql_name='title')
    report_name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='reportName')
    parameters = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(MaxReportParamsAndValues)), graphql_name='parameters')
    custom_payload = sgqlc.types.Field(JSON, graphql_name='customPayload')
    content_blocks = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(MaxContentBlock)), graphql_name='contentBlocks')
    gzipped_dataframes_and_metadata = sgqlc.types.Field(sgqlc.types.list_of(JSON), graphql_name='gzippedDataframesAndMetadata')


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


class MaxToolCall(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('tool', 'parameters', 'referenced_state', 'return_value', 'updated_state', 'additional_tool_state')
    tool = sgqlc.types.Field(sgqlc.types.non_null(MaxAgentWorkflowTool), graphql_name='tool')
    parameters = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('MaxToolCallParameter'))), graphql_name='parameters')
    referenced_state = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(MaxAgentWorkflowReferencedState))), graphql_name='referencedState')
    return_value = sgqlc.types.Field(sgqlc.types.non_null('MaxToolCallResponse'), graphql_name='returnValue')
    updated_state = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(MaxAgentWorkflowUpdatedState))), graphql_name='updatedState')
    additional_tool_state = sgqlc.types.Field(JSON, graphql_name='additionalToolState')


class MaxToolCallParameter(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('name', 'description', 'value')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    description = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='description')
    value = sgqlc.types.Field(JSON, graphql_name='value')


class MaxToolCallResponse(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('success', 'error_code', 'return_value')
    success = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='success')
    error_code = sgqlc.types.Field(String, graphql_name='errorCode')
    return_value = sgqlc.types.Field(String, graphql_name='returnValue')


class MaxUser(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('first_name', 'last_name', 'email_address')
    first_name = sgqlc.types.Field(String, graphql_name='firstName')
    last_name = sgqlc.types.Field(String, graphql_name='lastName')
    email_address = sgqlc.types.Field(String, graphql_name='emailAddress')


class Mutation(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('create_max_copilot_skill_chat_question', 'update_max_copilot_skill_chat_question', 'delete_max_copilot_skill_chat_question', 'create_max_copilot_question', 'update_max_copilot_question', 'delete_max_copilot_question', 'set_max_agent_workflow', 'import_copilot_skill_from_zip', 'reload_dataset', 'update_database_name', 'update_database_description', 'update_database_llm_description', 'update_database_mermaid_er_diagram', 'update_database_kshot_limit', 'update_dataset_name', 'update_dataset_description', 'update_dataset_date_range', 'update_dataset_data_interval', 'update_dataset_misc_info', 'update_dataset_source', 'update_dataset_query_row_limit', 'update_dataset_use_database_casing', 'update_dataset_kshot_limit', 'create_dataset', 'create_dataset_from_table', 'create_dimension', 'update_dimension', 'delete_dimension', 'create_metric', 'update_metric', 'delete_metric', 'update_chat_answer_payload', 'ask_chat_question', 'evaluate_chat_question', 'queue_chat_question', 'cancel_chat_question', 'create_chat_thread', 'add_feedback', 'set_skill_memory', 'share_thread', 'update_loading_message', 'create_chat_artifact', 'delete_chat_artifact')
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
    set_max_agent_workflow = sgqlc.types.Field(sgqlc.types.non_null(MaxMutationResponse), graphql_name='setMaxAgentWorkflow', args=sgqlc.types.ArgDict((
        ('entry_id', sgqlc.types.Arg(sgqlc.types.non_null(UUID), graphql_name='entryId', default=None)),
        ('agent_run_state', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(JSON))), graphql_name='agentRunState', default=None)),
))
    )
    import_copilot_skill_from_zip = sgqlc.types.Field(sgqlc.types.non_null(MaxMutationResponse), graphql_name='importCopilotSkillFromZip', args=sgqlc.types.ArgDict((
        ('entry_id', sgqlc.types.Arg(sgqlc.types.non_null(UUID), graphql_name='entryId', default=None)),
        ('skill_name', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='skillName', default=None)),
))
    )
    reload_dataset = sgqlc.types.Field(sgqlc.types.non_null(MaxMutationResponse), graphql_name='reloadDataset', args=sgqlc.types.ArgDict((
        ('dataset_id', sgqlc.types.Arg(UUID, graphql_name='datasetId', default=None)),
        ('database_id', sgqlc.types.Arg(UUID, graphql_name='databaseId', default=None)),
        ('table_names', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='tableNames', default=None)),
))
    )
    update_database_name = sgqlc.types.Field(MaxMutationResponse, graphql_name='updateDatabaseName', args=sgqlc.types.ArgDict((
        ('database_id', sgqlc.types.Arg(sgqlc.types.non_null(UUID), graphql_name='databaseId', default=None)),
        ('name', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='name', default=None)),
))
    )
    update_database_description = sgqlc.types.Field(MaxMutationResponse, graphql_name='updateDatabaseDescription', args=sgqlc.types.ArgDict((
        ('database_id', sgqlc.types.Arg(sgqlc.types.non_null(UUID), graphql_name='databaseId', default=None)),
        ('description', sgqlc.types.Arg(String, graphql_name='description', default=None)),
))
    )
    update_database_llm_description = sgqlc.types.Field(MaxMutationResponse, graphql_name='updateDatabaseLlmDescription', args=sgqlc.types.ArgDict((
        ('database_id', sgqlc.types.Arg(sgqlc.types.non_null(UUID), graphql_name='databaseId', default=None)),
        ('llm_description', sgqlc.types.Arg(String, graphql_name='llmDescription', default=None)),
))
    )
    update_database_mermaid_er_diagram = sgqlc.types.Field(MaxMutationResponse, graphql_name='updateDatabaseMermaidErDiagram', args=sgqlc.types.ArgDict((
        ('database_id', sgqlc.types.Arg(sgqlc.types.non_null(UUID), graphql_name='databaseId', default=None)),
        ('mermaid_er_diagram', sgqlc.types.Arg(String, graphql_name='mermaidErDiagram', default=None)),
))
    )
    update_database_kshot_limit = sgqlc.types.Field(MaxMutationResponse, graphql_name='updateDatabaseKShotLimit', args=sgqlc.types.ArgDict((
        ('database_id', sgqlc.types.Arg(sgqlc.types.non_null(UUID), graphql_name='databaseId', default=None)),
        ('k_shot_limit', sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name='kShotLimit', default=None)),
))
    )
    update_dataset_name = sgqlc.types.Field(MaxMutationResponse, graphql_name='updateDatasetName', args=sgqlc.types.ArgDict((
        ('dataset_id', sgqlc.types.Arg(sgqlc.types.non_null(UUID), graphql_name='datasetId', default=None)),
        ('name', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='name', default=None)),
))
    )
    update_dataset_description = sgqlc.types.Field(MaxMutationResponse, graphql_name='updateDatasetDescription', args=sgqlc.types.ArgDict((
        ('dataset_id', sgqlc.types.Arg(sgqlc.types.non_null(UUID), graphql_name='datasetId', default=None)),
        ('description', sgqlc.types.Arg(String, graphql_name='description', default=None)),
))
    )
    update_dataset_date_range = sgqlc.types.Field(MaxMutationResponse, graphql_name='updateDatasetDateRange', args=sgqlc.types.ArgDict((
        ('dataset_id', sgqlc.types.Arg(sgqlc.types.non_null(UUID), graphql_name='datasetId', default=None)),
        ('dataset_min_date', sgqlc.types.Arg(DateTime, graphql_name='datasetMinDate', default=None)),
        ('dataset_max_date', sgqlc.types.Arg(DateTime, graphql_name='datasetMaxDate', default=None)),
))
    )
    update_dataset_data_interval = sgqlc.types.Field(MaxMutationResponse, graphql_name='updateDatasetDataInterval', args=sgqlc.types.ArgDict((
        ('dataset_id', sgqlc.types.Arg(sgqlc.types.non_null(UUID), graphql_name='datasetId', default=None)),
        ('data_interval', sgqlc.types.Arg(DatasetDataInterval, graphql_name='dataInterval', default=None)),
))
    )
    update_dataset_misc_info = sgqlc.types.Field(MaxMutationResponse, graphql_name='updateDatasetMiscInfo', args=sgqlc.types.ArgDict((
        ('dataset_id', sgqlc.types.Arg(sgqlc.types.non_null(UUID), graphql_name='datasetId', default=None)),
        ('misc_info', sgqlc.types.Arg(String, graphql_name='miscInfo', default=None)),
))
    )
    update_dataset_source = sgqlc.types.Field(MaxMutationResponse, graphql_name='updateDatasetSource', args=sgqlc.types.ArgDict((
        ('dataset_id', sgqlc.types.Arg(sgqlc.types.non_null(UUID), graphql_name='datasetId', default=None)),
        ('source_table', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='sourceTable', default=None)),
        ('source_sql', sgqlc.types.Arg(String, graphql_name='sourceSql', default=None)),
        ('derived_table_alias', sgqlc.types.Arg(String, graphql_name='derivedTableAlias', default=None)),
))
    )
    update_dataset_query_row_limit = sgqlc.types.Field(MaxMutationResponse, graphql_name='updateDatasetQueryRowLimit', args=sgqlc.types.ArgDict((
        ('dataset_id', sgqlc.types.Arg(sgqlc.types.non_null(UUID), graphql_name='datasetId', default=None)),
        ('query_row_limit', sgqlc.types.Arg(Int, graphql_name='queryRowLimit', default=None)),
))
    )
    update_dataset_use_database_casing = sgqlc.types.Field(MaxMutationResponse, graphql_name='updateDatasetUseDatabaseCasing', args=sgqlc.types.ArgDict((
        ('dataset_id', sgqlc.types.Arg(sgqlc.types.non_null(UUID), graphql_name='datasetId', default=None)),
        ('use_database_casing', sgqlc.types.Arg(sgqlc.types.non_null(Boolean), graphql_name='useDatabaseCasing', default=None)),
))
    )
    update_dataset_kshot_limit = sgqlc.types.Field(MaxMutationResponse, graphql_name='updateDatasetKShotLimit', args=sgqlc.types.ArgDict((
        ('dataset_id', sgqlc.types.Arg(sgqlc.types.non_null(UUID), graphql_name='datasetId', default=None)),
        ('k_shot_limit', sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name='kShotLimit', default=None)),
))
    )
    create_dataset = sgqlc.types.Field(sgqlc.types.non_null(MaxMutationResponse), graphql_name='createDataset', args=sgqlc.types.ArgDict((
        ('dataset', sgqlc.types.Arg(sgqlc.types.non_null(JSON), graphql_name='dataset', default=None)),
))
    )
    create_dataset_from_table = sgqlc.types.Field(sgqlc.types.non_null(CreateDatasetFromTableResponse), graphql_name='createDatasetFromTable', args=sgqlc.types.ArgDict((
        ('database_id', sgqlc.types.Arg(sgqlc.types.non_null(UUID), graphql_name='databaseId', default=None)),
        ('table_name', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='tableName', default=None)),
))
    )
    create_dimension = sgqlc.types.Field(sgqlc.types.non_null(MaxMutationResponse), graphql_name='createDimension', args=sgqlc.types.ArgDict((
        ('dataset_id', sgqlc.types.Arg(sgqlc.types.non_null(UUID), graphql_name='datasetId', default=None)),
        ('dimension', sgqlc.types.Arg(sgqlc.types.non_null(JSON), graphql_name='dimension', default=None)),
))
    )
    update_dimension = sgqlc.types.Field(sgqlc.types.non_null(MaxMutationResponse), graphql_name='updateDimension', args=sgqlc.types.ArgDict((
        ('dataset_id', sgqlc.types.Arg(sgqlc.types.non_null(UUID), graphql_name='datasetId', default=None)),
        ('dimension', sgqlc.types.Arg(sgqlc.types.non_null(JSON), graphql_name='dimension', default=None)),
))
    )
    delete_dimension = sgqlc.types.Field(sgqlc.types.non_null(MaxMutationResponse), graphql_name='deleteDimension', args=sgqlc.types.ArgDict((
        ('dataset_id', sgqlc.types.Arg(sgqlc.types.non_null(UUID), graphql_name='datasetId', default=None)),
        ('dimension_id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='dimensionId', default=None)),
))
    )
    create_metric = sgqlc.types.Field(sgqlc.types.non_null(MaxMutationResponse), graphql_name='createMetric', args=sgqlc.types.ArgDict((
        ('dataset_id', sgqlc.types.Arg(sgqlc.types.non_null(UUID), graphql_name='datasetId', default=None)),
        ('metric', sgqlc.types.Arg(sgqlc.types.non_null(JSON), graphql_name='metric', default=None)),
))
    )
    update_metric = sgqlc.types.Field(sgqlc.types.non_null(MaxMutationResponse), graphql_name='updateMetric', args=sgqlc.types.ArgDict((
        ('dataset_id', sgqlc.types.Arg(sgqlc.types.non_null(UUID), graphql_name='datasetId', default=None)),
        ('metric', sgqlc.types.Arg(sgqlc.types.non_null(JSON), graphql_name='metric', default=None)),
))
    )
    delete_metric = sgqlc.types.Field(sgqlc.types.non_null(MaxMutationResponse), graphql_name='deleteMetric', args=sgqlc.types.ArgDict((
        ('dataset_id', sgqlc.types.Arg(sgqlc.types.non_null(UUID), graphql_name='datasetId', default=None)),
        ('metric_id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='metricId', default=None)),
))
    )
    update_chat_answer_payload = sgqlc.types.Field(JSON, graphql_name='updateChatAnswerPayload', args=sgqlc.types.ArgDict((
        ('answer_id', sgqlc.types.Arg(sgqlc.types.non_null(UUID), graphql_name='answerId', default=None)),
        ('payload', sgqlc.types.Arg(sgqlc.types.non_null(JSON), graphql_name='payload', default=None)),
        ('entry_answer_id', sgqlc.types.Arg(UUID, graphql_name='entryAnswerId', default=None)),
        ('nudge_entry_id', sgqlc.types.Arg(UUID, graphql_name='nudgeEntryId', default=None)),
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
        ('load_all_skills', sgqlc.types.Arg(Boolean, graphql_name='loadAllSkills', default=None)),
        ('history', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(MessageHistoryInput)), graphql_name='history', default=None)),
        ('question_type', sgqlc.types.Arg(QuestionType, graphql_name='questionType', default=None)),
        ('thread_type', sgqlc.types.Arg(ThreadType, graphql_name='threadType', default=None)),
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
        ('load_all_skills', sgqlc.types.Arg(Boolean, graphql_name='loadAllSkills', default=None)),
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
    add_feedback = sgqlc.types.Field(Boolean, graphql_name='addFeedback', args=sgqlc.types.ArgDict((
        ('entry_id', sgqlc.types.Arg(sgqlc.types.non_null(UUID), graphql_name='entryId', default=None)),
        ('feedback_type', sgqlc.types.Arg(sgqlc.types.non_null(FeedbackType), graphql_name='feedbackType', default=None)),
        ('message', sgqlc.types.Arg(String, graphql_name='message', default=None)),
))
    )
    set_skill_memory = sgqlc.types.Field(Boolean, graphql_name='setSkillMemory', args=sgqlc.types.ArgDict((
        ('entry_id', sgqlc.types.Arg(sgqlc.types.non_null(UUID), graphql_name='entryId', default=None)),
        ('skill_memory_payload', sgqlc.types.Arg(sgqlc.types.non_null(JSON), graphql_name='skillMemoryPayload', default=None)),
))
    )
    share_thread = sgqlc.types.Field(sgqlc.types.non_null('SharedThread'), graphql_name='shareThread', args=sgqlc.types.ArgDict((
        ('original_thread_id', sgqlc.types.Arg(UUID, graphql_name='originalThreadId', default=None)),
))
    )
    update_loading_message = sgqlc.types.Field(UUID, graphql_name='updateLoadingMessage', args=sgqlc.types.ArgDict((
        ('answer_id', sgqlc.types.Arg(sgqlc.types.non_null(UUID), graphql_name='answerId', default=None)),
        ('message', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='message', default=None)),
        ('nudge_entry_id', sgqlc.types.Arg(UUID, graphql_name='nudgeEntryId', default=None)),
))
    )
    create_chat_artifact = sgqlc.types.Field(sgqlc.types.non_null(MaxMutationResponse), graphql_name='createChatArtifact', args=sgqlc.types.ArgDict((
        ('chat_artifact', sgqlc.types.Arg(sgqlc.types.non_null(JSON), graphql_name='chatArtifact', default=None)),
))
    )
    delete_chat_artifact = sgqlc.types.Field(sgqlc.types.non_null(MaxMutationResponse), graphql_name='deleteChatArtifact', args=sgqlc.types.ArgDict((
        ('chat_artifact_id', sgqlc.types.Arg(sgqlc.types.non_null(UUID), graphql_name='chatArtifactId', default=None)),
))
    )


class PagedChatArtifacts(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('total_rows', 'rows')
    total_rows = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='totalRows')
    rows = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ChatArtifact))), graphql_name='rows')


class PagedDatabaseTables(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('total_rows', 'rows')
    total_rows = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='totalRows')
    rows = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(DatabaseTable))), graphql_name='rows')


class PagedDatabases(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('total_rows', 'rows')
    total_rows = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='totalRows')
    rows = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(Database))), graphql_name='rows')


class PagedDatasets(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('total_rows', 'rows')
    total_rows = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='totalRows')
    rows = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(Dataset))), graphql_name='rows')


class ParameterDefinition(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('constraints', 'key', 'multi', 'type')
    constraints = sgqlc.types.Field(sgqlc.types.non_null(JSON), graphql_name='constraints')
    key = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='key')
    multi = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='multi')
    type = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='type')


class Query(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('ping', 'current_user', 'get_copilot_skill_artifact_by_path', 'get_copilots', 'get_copilot_info', 'get_copilot_skill', 'run_copilot_skill', 'get_skill_components', 'get_copilot_hydrated_reports', 'get_max_agent_workflow', 'execute_sql_query', 'execute_rql_query', 'get_databases', 'get_database', 'get_database_tables', 'get_dataset_id', 'get_dataset', 'get_dataset2', 'get_datasets', 'get_domain_object', 'get_domain_object_by_name', 'get_grounded_value', 'run_max_sql_gen', 'run_sql_ai', 'generate_visualization', 'llmapi_config_for_sdk', 'get_max_llm_prompt', 'user_chat_threads', 'user_chat_entries', 'chat_thread', 'chat_entry', 'user', 'all_chat_entries', 'skill_memory', 'chat_completion', 'narrative_completion', 'narrative_completion_with_prompt', 'sql_completion', 'research_completion', 'chat_completion_with_prompt', 'research_completion_with_prompt', 'get_chat_artifact', 'get_chat_artifacts')
    ping = sgqlc.types.Field(String, graphql_name='ping')
    current_user = sgqlc.types.Field(MaxUser, graphql_name='currentUser')
    get_copilot_skill_artifact_by_path = sgqlc.types.Field(CopilotSkillArtifact, graphql_name='getCopilotSkillArtifactByPath', args=sgqlc.types.ArgDict((
        ('copilot_id', sgqlc.types.Arg(sgqlc.types.non_null(UUID), graphql_name='copilotId', default=None)),
        ('copilot_skill_id', sgqlc.types.Arg(sgqlc.types.non_null(UUID), graphql_name='copilotSkillId', default=None)),
        ('artifact_path', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='artifactPath', default=None)),
))
    )
    get_copilots = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(MaxCopilot))), graphql_name='getCopilots')
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
        ('validate_parameters', sgqlc.types.Arg(Boolean, graphql_name='validateParameters', default=None)),
        ('tool_definition', sgqlc.types.Arg(JSON, graphql_name='toolDefinition', default=None)),
))
    )
    get_skill_components = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(MaxSkillComponent))), graphql_name='getSkillComponents')
    get_copilot_hydrated_reports = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(HydratedReport))), graphql_name='getCopilotHydratedReports', args=sgqlc.types.ArgDict((
        ('copilot_id', sgqlc.types.Arg(sgqlc.types.non_null(UUID), graphql_name='copilotId', default=None)),
        ('override_dataset_id', sgqlc.types.Arg(UUID, graphql_name='overrideDatasetId', default=None)),
        ('load_all_skills', sgqlc.types.Arg(Boolean, graphql_name='loadAllSkills', default=None)),
))
    )
    get_max_agent_workflow = sgqlc.types.Field(JSON, graphql_name='getMaxAgentWorkflow', args=sgqlc.types.ArgDict((
        ('agent_workflow_id', sgqlc.types.Arg(sgqlc.types.non_null(UUID), graphql_name='agentWorkflowId', default=None)),
        ('version', sgqlc.types.Arg(Int, graphql_name='version', default=None)),
))
    )
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
    get_databases = sgqlc.types.Field(sgqlc.types.non_null(PagedDatabases), graphql_name='getDatabases', args=sgqlc.types.ArgDict((
        ('search_input', sgqlc.types.Arg(sgqlc.types.non_null(DatabaseSearchInput), graphql_name='searchInput', default=None)),
        ('paging', sgqlc.types.Arg(sgqlc.types.non_null(PagingInput), graphql_name='paging', default=None)),
))
    )
    get_database = sgqlc.types.Field(Database, graphql_name='getDatabase', args=sgqlc.types.ArgDict((
        ('database_id', sgqlc.types.Arg(sgqlc.types.non_null(UUID), graphql_name='databaseId', default=None)),
))
    )
    get_database_tables = sgqlc.types.Field(sgqlc.types.non_null(PagedDatabaseTables), graphql_name='getDatabaseTables', args=sgqlc.types.ArgDict((
        ('database_id', sgqlc.types.Arg(sgqlc.types.non_null(UUID), graphql_name='databaseId', default=None)),
        ('search_input', sgqlc.types.Arg(sgqlc.types.non_null(DatabaseTableSearchInput), graphql_name='searchInput', default=None)),
        ('paging', sgqlc.types.Arg(sgqlc.types.non_null(PagingInput), graphql_name='paging', default=None)),
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
    get_dataset2 = sgqlc.types.Field(Dataset, graphql_name='getDataset2', args=sgqlc.types.ArgDict((
        ('dataset_id', sgqlc.types.Arg(sgqlc.types.non_null(UUID), graphql_name='datasetId', default=None)),
))
    )
    get_datasets = sgqlc.types.Field(sgqlc.types.non_null(PagedDatasets), graphql_name='getDatasets', args=sgqlc.types.ArgDict((
        ('search_input', sgqlc.types.Arg(sgqlc.types.non_null(DatasetSearchInput), graphql_name='searchInput', default=None)),
        ('paging', sgqlc.types.Arg(sgqlc.types.non_null(PagingInput), graphql_name='paging', default=None)),
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
    get_grounded_value = sgqlc.types.Field(GroundedValueResponse, graphql_name='getGroundedValue', args=sgqlc.types.ArgDict((
        ('dataset_id', sgqlc.types.Arg(sgqlc.types.non_null(UUID), graphql_name='datasetId', default=None)),
        ('domain_entity', sgqlc.types.Arg(String, graphql_name='domainEntity', default=None)),
        ('value', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='value', default=None)),
        ('copilot_id', sgqlc.types.Arg(UUID, graphql_name='copilotId', default=None)),
))
    )
    run_max_sql_gen = sgqlc.types.Field(sgqlc.types.non_null('RunMaxSqlGenResponse'), graphql_name='runMaxSqlGen', args=sgqlc.types.ArgDict((
        ('dataset_id', sgqlc.types.Arg(sgqlc.types.non_null(UUID), graphql_name='datasetId', default=None)),
        ('pre_query_object', sgqlc.types.Arg(JSON, graphql_name='preQueryObject', default=None)),
        ('copilot_id', sgqlc.types.Arg(UUID, graphql_name='copilotId', default=None)),
))
    )
    run_sql_ai = sgqlc.types.Field(sgqlc.types.non_null('RunSqlAiResponse'), graphql_name='runSqlAi', args=sgqlc.types.ArgDict((
        ('dataset_id', sgqlc.types.Arg(UUID, graphql_name='datasetId', default=None)),
        ('question', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='question', default=None)),
        ('model_override', sgqlc.types.Arg(String, graphql_name='modelOverride', default=None)),
        ('copilot_id', sgqlc.types.Arg(UUID, graphql_name='copilotId', default=None)),
        ('dataset_ids', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(UUID)), graphql_name='datasetIds', default=None)),
        ('database_id', sgqlc.types.Arg(UUID, graphql_name='databaseId', default=None)),
))
    )
    generate_visualization = sgqlc.types.Field(sgqlc.types.non_null(GenerateVisualizationResponse), graphql_name='generateVisualization', args=sgqlc.types.ArgDict((
        ('data', sgqlc.types.Arg(sgqlc.types.non_null(JSON), graphql_name='data', default=None)),
        ('column_metadata_map', sgqlc.types.Arg(sgqlc.types.non_null(JSON), graphql_name='columnMetadataMap', default=None)),
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
    user = sgqlc.types.Field(MaxChatUser, graphql_name='user', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(UUID), graphql_name='id', default=None)),
))
    )
    all_chat_entries = sgqlc.types.Field(sgqlc.types.list_of(MaxChatEntry), graphql_name='allChatEntries', args=sgqlc.types.ArgDict((
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('filters', sgqlc.types.Arg(JSON, graphql_name='filters', default=None)),
))
    )
    skill_memory = sgqlc.types.Field(JSON, graphql_name='skillMemory', args=sgqlc.types.ArgDict((
        ('entry_id', sgqlc.types.Arg(sgqlc.types.non_null(UUID), graphql_name='entryId', default=None)),
))
    )
    chat_completion = sgqlc.types.Field(LlmResponse, graphql_name='chatCompletion', args=sgqlc.types.ArgDict((
        ('messages', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(LlmChatMessage))), graphql_name='messages', default=None)),
        ('model_selection', sgqlc.types.Arg(LlmModelSelection, graphql_name='modelSelection', default=None)),
))
    )
    narrative_completion = sgqlc.types.Field(LlmResponse, graphql_name='narrativeCompletion', args=sgqlc.types.ArgDict((
        ('prompt', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='prompt', default=None)),
        ('model_selection', sgqlc.types.Arg(LlmModelSelection, graphql_name='modelSelection', default=None)),
))
    )
    narrative_completion_with_prompt = sgqlc.types.Field(LlmResponse, graphql_name='narrativeCompletionWithPrompt', args=sgqlc.types.ArgDict((
        ('prompt_name', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='promptName', default=None)),
        ('prompt_variables', sgqlc.types.Arg(JSON, graphql_name='promptVariables', default=None)),
        ('model_selection', sgqlc.types.Arg(LlmModelSelection, graphql_name='modelSelection', default=None)),
))
    )
    sql_completion = sgqlc.types.Field(LlmResponse, graphql_name='sqlCompletion', args=sgqlc.types.ArgDict((
        ('messages', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(LlmChatMessage))), graphql_name='messages', default=None)),
        ('model_selection', sgqlc.types.Arg(LlmModelSelection, graphql_name='modelSelection', default=None)),
))
    )
    research_completion = sgqlc.types.Field(LlmResponse, graphql_name='researchCompletion', args=sgqlc.types.ArgDict((
        ('messages', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(LlmChatMessage))), graphql_name='messages', default=None)),
        ('model_selection', sgqlc.types.Arg(LlmModelSelection, graphql_name='modelSelection', default=None)),
))
    )
    chat_completion_with_prompt = sgqlc.types.Field(LlmResponse, graphql_name='chatCompletionWithPrompt', args=sgqlc.types.ArgDict((
        ('prompt_name', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='promptName', default=None)),
        ('prompt_variables', sgqlc.types.Arg(JSON, graphql_name='promptVariables', default=None)),
        ('messages', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(LlmChatMessage)), graphql_name='messages', default=None)),
))
    )
    research_completion_with_prompt = sgqlc.types.Field(LlmResponse, graphql_name='researchCompletionWithPrompt', args=sgqlc.types.ArgDict((
        ('prompt_name', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='promptName', default=None)),
        ('prompt_variables', sgqlc.types.Arg(JSON, graphql_name='promptVariables', default=None)),
        ('messages', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(LlmChatMessage)), graphql_name='messages', default=None)),
))
    )
    get_chat_artifact = sgqlc.types.Field(ChatArtifact, graphql_name='getChatArtifact', args=sgqlc.types.ArgDict((
        ('chat_artifact_id', sgqlc.types.Arg(sgqlc.types.non_null(UUID), graphql_name='chatArtifactId', default=None)),
))
    )
    get_chat_artifacts = sgqlc.types.Field(sgqlc.types.non_null(PagedChatArtifacts), graphql_name='getChatArtifacts', args=sgqlc.types.ArgDict((
        ('search_input', sgqlc.types.Arg(sgqlc.types.non_null(ChatArtifactSearchInput), graphql_name='searchInput', default=None)),
        ('paging', sgqlc.types.Arg(sgqlc.types.non_null(PagingInput), graphql_name='paging', default=None)),
))
    )


class RunMaxSqlGenResponse(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('success', 'code', 'error', 'sql', 'row_limit', 'data')
    success = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='success')
    code = sgqlc.types.Field(String, graphql_name='code')
    error = sgqlc.types.Field(String, graphql_name='error')
    sql = sgqlc.types.Field(String, graphql_name='sql')
    row_limit = sgqlc.types.Field(Int, graphql_name='rowLimit')
    data = sgqlc.types.Field(JSON, graphql_name='data')


class RunSqlAiResponse(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('success', 'code', 'error', 'sql', 'raw_sql', 'data', 'rendered_prompt', 'column_metadata_map', 'title', 'explanation', 'timing_info', 'prior_runs')
    success = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='success')
    code = sgqlc.types.Field(String, graphql_name='code')
    error = sgqlc.types.Field(String, graphql_name='error')
    sql = sgqlc.types.Field(String, graphql_name='sql')
    raw_sql = sgqlc.types.Field(String, graphql_name='rawSql')
    data = sgqlc.types.Field(JSON, graphql_name='data')
    rendered_prompt = sgqlc.types.Field(String, graphql_name='renderedPrompt')
    column_metadata_map = sgqlc.types.Field(JSON, graphql_name='columnMetadataMap')
    title = sgqlc.types.Field(String, graphql_name='title')
    explanation = sgqlc.types.Field(String, graphql_name='explanation')
    timing_info = sgqlc.types.Field(JSON, graphql_name='timingInfo')
    prior_runs = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('RunSqlAiResponse'))), graphql_name='priorRuns')


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


class SkillParameter(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('constrained_values', 'definition', 'description', 'is_hidden', 'is_multi', 'is_required', 'key', 'llm_description', 'metadata_field', 'skill_param_def_key', 'use_predicate_filters', 'value', 'default_value', 'additional_constraints', 'dataset_names', 'meta', 'match_values')
    constrained_values = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))), graphql_name='constrainedValues')
    definition = sgqlc.types.Field(ParameterDefinition, graphql_name='definition')
    description = sgqlc.types.Field(String, graphql_name='description')
    is_hidden = sgqlc.types.Field(Boolean, graphql_name='isHidden')
    is_multi = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='isMulti')
    is_required = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='isRequired')
    key = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='key')
    llm_description = sgqlc.types.Field(String, graphql_name='llmDescription')
    metadata_field = sgqlc.types.Field(String, graphql_name='metadataField')
    skill_param_def_key = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='skillParamDefKey')
    use_predicate_filters = sgqlc.types.Field(Boolean, graphql_name='usePredicateFilters')
    value = sgqlc.types.Field(String, graphql_name='value')
    default_value = sgqlc.types.Field(JSON, graphql_name='defaultValue')
    additional_constraints = sgqlc.types.Field(JSON, graphql_name='additionalConstraints')
    dataset_names = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='datasetNames')
    meta = sgqlc.types.Field(JSON, graphql_name='meta')
    match_values = sgqlc.types.Field(MatchValues, graphql_name='matchValues')


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


class Dimension(sgqlc.types.Type, DomainArtifact):
    __schema__ = schema
    __field_names__ = ('data_type', 'sql_expression', 'sql_sort_expression', 'sample_limit')
    data_type = sgqlc.types.Field(sgqlc.types.non_null(SimplifiedDataType), graphql_name='dataType')
    sql_expression = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='sqlExpression')
    sql_sort_expression = sgqlc.types.Field(String, graphql_name='sqlSortExpression')
    sample_limit = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='sampleLimit')


class MaxCalculatedAttribute(sgqlc.types.Type, MaxDomainObject, MaxDomainAttribute, MaxDimensionAttribute):
    __schema__ = schema
    __field_names__ = ('rql',)
    rql = sgqlc.types.Field(String, graphql_name='rql')


class MaxCalculatedMetric(sgqlc.types.Type, MaxDomainObject):
    __schema__ = schema
    __field_names__ = ('display_format', 'rql', 'sql', 'sql_agg_expression', 'agg_method', 'is_positive_direction_up', 'can_be_averaged', 'is_not_additive', 'growth_output_format', 'hide_percentage_change', 'simplified_data_type', 'metric_type')
    display_format = sgqlc.types.Field(String, graphql_name='displayFormat')
    rql = sgqlc.types.Field(String, graphql_name='rql')
    sql = sgqlc.types.Field(String, graphql_name='sql')
    sql_agg_expression = sgqlc.types.Field(String, graphql_name='sqlAggExpression')
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


class Metric(sgqlc.types.Type, DomainArtifact):
    __schema__ = schema
    __field_names__ = ('data_type', 'metric_type', 'display_format', 'sql_agg_expression', 'sql_row_expression', 'growth_type', 'growth_format')
    data_type = sgqlc.types.Field(sgqlc.types.non_null(SimplifiedDataType), graphql_name='dataType')
    metric_type = sgqlc.types.Field(sgqlc.types.non_null(MetricType), graphql_name='metricType')
    display_format = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='displayFormat')
    sql_agg_expression = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='sqlAggExpression')
    sql_row_expression = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='sqlRowExpression')
    growth_type = sgqlc.types.Field(sgqlc.types.non_null(GrowthType), graphql_name='growthType')
    growth_format = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='growthFormat')


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

