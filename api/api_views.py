from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status

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

    def post(self, request):
        salary = Salaries.objects.create(
            name=request.data['name'],
            position=request.data['position'],
            department=request.data['department'],
            salary=request.data['salary']
        )
        serializer = SalariesSerializer(salary, context={'request': request})
        return Response(serializer.data, content_type='application/json')

    def put(self, request, *args):
        pk = self.request.query_params.get('id', None)
        if pk is not None:
            salaryObj = Salaries.objects.get(pk=pk)
            salaryObj.salary = request.data['salary']
            salaryObj.save()
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({}, status=status.HTTP_404_NOT_FOUND)