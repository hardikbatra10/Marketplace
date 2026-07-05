from rest_framework import generics, permissions

from item.models import Item
from item.serializers import ItemSerializer


class MyItemsView(generics.ListAPIView):
    serializer_class = ItemSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Item.objects.filter(created_by=self.request.user)
