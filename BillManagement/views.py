from core.permissions import BillPermission
from rest_framework.viewsets import ModelViewSet
from .models import Bill
from .serializers import BillSerializer

# Create your views here.

class BillViewSet(ModelViewSet):
    queryset = Bill.objects.all()
    serializer_class = BillSerializer
    permission_classes = [BillPermission]

