from django.db.models import Q
from rest_framework import generics, permissions, viewsets

from .models import Category, Item
from .permissions import IsOwnerOrReadOnly
from .serializers import CategorySerializer, ItemSerializer


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.AllowAny,)


class ItemViewSet(viewsets.ModelViewSet):
    serializer_class = ItemSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    def get_queryset(self):
        items = Item.objects.all()

        if self.action != 'list':
            return items

        query = self.request.query_params.get('query', '')
        category_id = self.request.query_params.get('category', 0)
        items = items.filter(is_sold=False)

        if category_id:
            items = items.filter(category_id=category_id)

        if query:
            items = items.filter(Q(name__icontains=query) | Q(description__icontains=query))

        return items

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
