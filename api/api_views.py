from rest_framework.generics import GenericAPIView

from api.models import Salaries
from api.serializers import SalariesSerializer


class SalariesAPIView(GenericAPIView):
    queryset = Salaries.objects.all()
    serializer_class = SalariesSerializer

    def get(self, request, *args, **kwargs):
        name = self.request.query_params.get('name', None)
        queryset = self.paginate_queryset(queryset=self.queryset)
        if name is not None:
            queryset = self.paginate_queryset(queryset=self.queryset.filter(name__icontains=name))
        serializer = SalariesSerializer(instance=queryset, many=True)
        return self.get_paginated_response(serializer.data)