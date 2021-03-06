
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from .serializers import *

class ValidatorApiView(APIView):

    def get(self, request):
        rows = FieldTesting.objects.filter(tpt_id_key__iexact=request.GET['typeahead'])
        if rows.count() == 0:
            return Response({'valid': False})
        else:
            return Response({'valid': True})


class SearchApiView(ListAPIView):
    serializer_class = SearchSerializer
    def get_queryset(self):
        if 'query' in self.request.GET and self.request.GET['query'] != '':
            return self.serializer_class.Meta.model.objects.filter(tpt_id_key__iexact=self.request.GET['query'])[:50]
        else:
            return self.serializer_class.Meta.model.objects.all()[:50]

class KeywordsApiView(ListAPIView):
    serializer_class = KeywordsSerializer

    def get_queryset(self):
        if 'input' in self.request.GET:
            return self.serializer_class.Meta.model.objects.filter(tpt_id_key__icontains = self.request.GET['input'])[:20];
        else:
            return self.serializer_class.Meta.model.objects.all()[:20]

    def list(self, request, *args, **kwargs):
        serializer_data = self.get_queryset()
        serializer = self.serializer_class(serializer_data, many=True)
        data = {item['tpt_id_key'] for item in serializer.data}
        return Response(data)

        # states = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California',
        # 'Colorado', 'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Hawaii',
        # 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana',
        # 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota',
        # 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire',
        # 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota',
        # 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island',
        # 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont',
        # 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming'
        # ]
        # return Response(states)

        # states = ["HA19VSFM14","HD19RAP1RRFR","FD19AUSHM4QB29","FD19AUSHM4QB28","FR19GRCP2M"]
        # return Response(states)
