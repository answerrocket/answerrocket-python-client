import sgqlc.types
import sgqlc.types.datetime


schema = sgqlc.types.Schema()



########################################################################
# Scalars and Enumerations
########################################################################
Boolean = sgqlc.types.Boolean

DateTime = sgqlc.types.datetime.DateTime

String = sgqlc.types.String

class UUID(sgqlc.types.Scalar):
    __schema__ = schema



########################################################################
# Input Objects
########################################################################

########################################################################
# Output Objects and Interfaces
########################################################################
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


class Query(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('ping', 'get_copilot_skill_artifact_by_path')
    ping = sgqlc.types.Field(String, graphql_name='ping')
    get_copilot_skill_artifact_by_path = sgqlc.types.Field(CopilotSkillArtifact, graphql_name='getCopilotSkillArtifactByPath', args=sgqlc.types.ArgDict((
        ('copilot_id', sgqlc.types.Arg(sgqlc.types.non_null(UUID), graphql_name='copilotId', default=None)),
        ('copilot_skill_id', sgqlc.types.Arg(sgqlc.types.non_null(UUID), graphql_name='copilotSkillId', default=None)),
        ('artifact_path', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='artifactPath', default=None)),
))
    )



########################################################################
# Unions
########################################################################

########################################################################
# Schema Entry Points
########################################################################
schema.query_type = Query
schema.mutation_type = None
schema.subscription_type = None

