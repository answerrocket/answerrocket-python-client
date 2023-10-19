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
    __field_names__ = ('id', 'api_type', 'model_type', 'model_name', 'is_active')
    id = sgqlc.types.Field(sgqlc.types.non_null(UUID), graphql_name='id')
    api_type = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='apiType')
    model_type = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='modelType')
    model_name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='modelName')
    is_active = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='isActive')


class MaxDomainObject(sgqlc.types.Interface):
    __schema__ = schema
    __field_names__ = ('type', 'id', 'name', 'description', 'output_label', 'synonyms', 'output_label_plural', 'hide_from_user')
    type = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='type')
    id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='id')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    description = sgqlc.types.Field(String, graphql_name='description')
    output_label = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='outputLabel')
    synonyms = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))), graphql_name='synonyms')
    output_label_plural = sgqlc.types.Field(String, graphql_name='outputLabelPlural')
    hide_from_user = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='hideFromUser')


class MaxDomainAttribute(sgqlc.types.Interface):
    __schema__ = schema
    __field_names__ = ('type', 'id', 'name', 'description', 'output_label', 'synonyms', 'output_label_plural', 'hide_from_user', 'display_format', 'headline_name', 'is_favorite', 'domain_entity')
    type = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='type')
    id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='id')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    description = sgqlc.types.Field(String, graphql_name='description')
    output_label = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='outputLabel')
    synonyms = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))), graphql_name='synonyms')
    output_label_plural = sgqlc.types.Field(String, graphql_name='outputLabelPlural')
    hide_from_user = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='hideFromUser')
    display_format = sgqlc.types.Field(String, graphql_name='displayFormat')
    headline_name = sgqlc.types.Field(String, graphql_name='headlineName')
    is_favorite = sgqlc.types.Field(Boolean, graphql_name='isFavorite')
    domain_entity = sgqlc.types.Field('MaxDomainEntity', graphql_name='domainEntity')


class MaxDimensionAttribute(sgqlc.types.Interface):
    __schema__ = schema
    __field_names__ = ('type', 'id', 'name', 'description', 'output_label', 'synonyms', 'output_label_plural', 'hide_from_user', 'display_format', 'headline_name', 'is_favorite', 'domain_entity', 'default_filter_value', 'is_required_in_query')
    type = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='type')
    id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='id')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    description = sgqlc.types.Field(String, graphql_name='description')
    output_label = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='outputLabel')
    synonyms = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))), graphql_name='synonyms')
    output_label_plural = sgqlc.types.Field(String, graphql_name='outputLabelPlural')
    hide_from_user = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='hideFromUser')
    display_format = sgqlc.types.Field(String, graphql_name='displayFormat')
    headline_name = sgqlc.types.Field(String, graphql_name='headlineName')
    is_favorite = sgqlc.types.Field(Boolean, graphql_name='isFavorite')
    domain_entity = sgqlc.types.Field('MaxDomainEntity', graphql_name='domainEntity')
    default_filter_value = sgqlc.types.Field(String, graphql_name='defaultFilterValue')
    is_required_in_query = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='isRequiredInQuery')


class MaxDomainEntity(sgqlc.types.Interface):
    __schema__ = schema
    __field_names__ = ('type', 'id', 'name', 'description', 'output_label', 'synonyms', 'output_label_plural', 'hide_from_user', 'db_table', 'attributes')
    type = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='type')
    id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='id')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    description = sgqlc.types.Field(String, graphql_name='description')
    output_label = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='outputLabel')
    synonyms = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))), graphql_name='synonyms')
    output_label_plural = sgqlc.types.Field(String, graphql_name='outputLabelPlural')
    hide_from_user = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='hideFromUser')
    db_table = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='dbTable')
    attributes = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(MaxDomainAttribute)), graphql_name='attributes')


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


class ExecuteSqlQueryResponse(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('success', 'code', 'error', 'data')
    success = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='success')
    code = sgqlc.types.Field(String, graphql_name='code')
    error = sgqlc.types.Field(String, graphql_name='error')
    data = sgqlc.types.Field(JSON, graphql_name='data')


class Query(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('ping', 'get_copilot_skill_artifact_by_path', 'execute_sql_query', 'get_dataset_id', 'get_domain_object_by_name', 'llmapi_config_for_sdk')
    ping = sgqlc.types.Field(String, graphql_name='ping')
    get_copilot_skill_artifact_by_path = sgqlc.types.Field(CopilotSkillArtifact, graphql_name='getCopilotSkillArtifactByPath', args=sgqlc.types.ArgDict((
        ('copilot_id', sgqlc.types.Arg(sgqlc.types.non_null(UUID), graphql_name='copilotId', default=None)),
        ('copilot_skill_id', sgqlc.types.Arg(sgqlc.types.non_null(UUID), graphql_name='copilotSkillId', default=None)),
        ('artifact_path', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='artifactPath', default=None)),
))
    )
    execute_sql_query = sgqlc.types.Field(ExecuteSqlQueryResponse, graphql_name='executeSqlQuery', args=sgqlc.types.ArgDict((
        ('database_id', sgqlc.types.Arg(sgqlc.types.non_null(UUID), graphql_name='databaseId', default=None)),
        ('sql_query', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='sqlQuery', default=None)),
        ('row_limit', sgqlc.types.Arg(Int, graphql_name='rowLimit', default=None)),
))
    )
    get_dataset_id = sgqlc.types.Field(UUID, graphql_name='getDatasetId', args=sgqlc.types.ArgDict((
        ('dataset_name', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='datasetName', default=None)),
))
    )
    get_domain_object_by_name = sgqlc.types.Field(MaxDomainObject, graphql_name='getDomainObjectByName', args=sgqlc.types.ArgDict((
        ('dataset_id', sgqlc.types.Arg(sgqlc.types.non_null(UUID), graphql_name='datasetId', default=None)),
        ('rql_name', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='rqlName', default=None)),
))
    )
    llmapi_config_for_sdk = sgqlc.types.Field(LLMApiConfig, graphql_name='LLMApiConfigForSdk', args=sgqlc.types.ArgDict((
        ('model_type', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='modelType', default=None)),
))
    )


class AzureOpenaiCompletionLLMApiConfig(sgqlc.types.Type, LLMApiConfig):
    __schema__ = schema
    __field_names__ = ('api_base_url', 'api_version', 'openai_model_name', 'max_tokens_content_generation', 'temperature', 'top_p', 'presence_penalty', 'frequency_penalty', 'stop_sequence')
    api_base_url = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='apiBaseUrl')
    api_version = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='apiVersion')
    openai_model_name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='openaiModelName')
    max_tokens_content_generation = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='maxTokensContentGeneration')
    temperature = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='temperature')
    top_p = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='topP')
    presence_penalty = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='presencePenalty')
    frequency_penalty = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='frequencyPenalty')
    stop_sequence = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='stopSequence')


class AzureOpenaiEmbeddingLLMApiConfig(sgqlc.types.Type, LLMApiConfig):
    __schema__ = schema
    __field_names__ = ('api_base_url', 'api_version')
    api_base_url = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='apiBaseUrl')
    api_version = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='apiVersion')


class MaxCalculatedMetric(sgqlc.types.Type, MaxDomainObject):
    __schema__ = schema
    __field_names__ = ('display_format', 'rql', 'agg_method', 'is_positive_direction_up', 'can_be_averaged', 'is_not_additive', 'growth_output_format', 'hide_percentage_change')
    display_format = sgqlc.types.Field(String, graphql_name='displayFormat')
    rql = sgqlc.types.Field(String, graphql_name='rql')
    agg_method = sgqlc.types.Field(DpsAggMethod, graphql_name='aggMethod')
    is_positive_direction_up = sgqlc.types.Field(Boolean, graphql_name='isPositiveDirectionUp')
    can_be_averaged = sgqlc.types.Field(Boolean, graphql_name='canBeAveraged')
    is_not_additive = sgqlc.types.Field(Boolean, graphql_name='isNotAdditive')
    growth_output_format = sgqlc.types.Field(String, graphql_name='growthOutputFormat')
    hide_percentage_change = sgqlc.types.Field(Boolean, graphql_name='hidePercentageChange')


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
    __field_names__ = ('db_metric_column', 'agg_method', 'is_row_level_filter', 'is_positive_direction_up', 'can_be_averaged', 'is_not_additive', 'growth_output_format', 'hide_percentage_change')
    db_metric_column = sgqlc.types.Field(String, graphql_name='dbMetricColumn')
    agg_method = sgqlc.types.Field(DpsAggMethod, graphql_name='aggMethod')
    is_row_level_filter = sgqlc.types.Field(Boolean, graphql_name='isRowLevelFilter')
    is_positive_direction_up = sgqlc.types.Field(Boolean, graphql_name='isPositiveDirectionUp')
    can_be_averaged = sgqlc.types.Field(Boolean, graphql_name='canBeAveraged')
    is_not_additive = sgqlc.types.Field(Boolean, graphql_name='isNotAdditive')
    growth_output_format = sgqlc.types.Field(String, graphql_name='growthOutputFormat')
    hide_percentage_change = sgqlc.types.Field(Boolean, graphql_name='hidePercentageChange')


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
    __field_names__ = ('organization', 'max_tokens_content_generation', 'temperature', 'top_p', 'presence_penalty', 'frequency_penalty', 'stop_sequence')
    organization = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='organization')
    max_tokens_content_generation = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='maxTokensContentGeneration')
    temperature = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='temperature')
    top_p = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='topP')
    presence_penalty = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='presencePenalty')
    frequency_penalty = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='frequencyPenalty')
    stop_sequence = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='stopSequence')


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
schema.mutation_type = None
schema.subscription_type = None

