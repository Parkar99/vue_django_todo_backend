import graphene
from graphene_django import DjangoObjectType

from .models import Task


class TaskType(DjangoObjectType):
    class Meta:
        model = Task


class CreateTask(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)

    task = graphene.Field(TaskType)

    @staticmethod
    def mutate(root, info, title):
        if len(title) == 0:
            return None
        task = Task.objects.create(title=title)
        return CreateTask(task=task)


class UpdateTask(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        is_completed = graphene.Boolean(required=True)

    task = graphene.Field(TaskType)

    @staticmethod
    def mutate(root, info, id, is_completed):
        try:
            task = Task.objects.get(id=id)
            task.is_completed = is_completed
            task.save()
            return UpdateTask(task=task)
        except Task.DoesNotExist:
            return None


class DeleteTask(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    detail = graphene.String()

    @staticmethod
    def mutate(root, info, id):
        try:
            task = Task.objects.get(id=id)
            task.delete()
            return DeleteTask(detail='Success')
        except Task.DoesNotExist:
            return None


class Query(graphene.ObjectType):
    task = graphene.Field(TaskType, id=graphene.Int(required=True))
    all_tasks = graphene.List(TaskType)

    @staticmethod
    def resolve_task(root, info, id):
        try:
            task = Task.objects.get(id=id)
            return task
        except Task.DoesNotExist:
            return None

    @staticmethod
    def resolve_all_tasks(root, info):
        return Task.objects.all()


class Mutation(graphene.ObjectType):
    create_task = CreateTask.Field()
    update_task = UpdateTask.Field()
    delete_task = DeleteTask.Field()
