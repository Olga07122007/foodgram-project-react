from rest_framework import mixins, viewsets


class ListRetrieveCustomViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    pass