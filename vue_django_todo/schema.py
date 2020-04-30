import graphene

from .graphql_api.schema import Query, Mutation

schema = graphene.Schema(query=Query, mutation=Mutation)
