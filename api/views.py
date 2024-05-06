from .serializers import VendorSerializer, PurchaseOrderSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Vendor, PurchaseOrder
from rest_framework.views import APIView
from django.utils import timezone
# Create your views here.



class VendorsListViews(APIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]
    
    def get(self, request):
        vendors = Vendor.objects.all()
        
        sort_by = request.quary_params.get('sort_by')
        filter_by = request.quary_params.get('filter_by')
        
        if sort_by:
            vendors = vendors.order_by(sort_by)
        
        if filter_by:
            vendors = vendors.filter(filter_by)
            
        serializer = VendorSerializer(vendors, many = True)
        if serializer:
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
    
    def post(self, request):
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class VendorViews(APIView):
    
    def get(request, pk):
        vendor = Vendor.objects.get(pk = pk)
        if vendor:
            serializer = VendorSerializer(vendor)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
        
    def put(request, pk):
        vendor = Vendor.objects.get(pk = pk)
        if vendor:
            serializer = VendorSerializer(vendor, data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
    
    def delete(request, pk):
        vendor = Vendor.objects.get(pk = pk)
        if vendor:
            serializer = VendorSerializer(vendor)
            serializer.delete()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)
            
class PurchaseOrdersListViews(APIView):
    def get(self, request):
        purchase_orders = PurchaseOrder.objects.all()
        serializer = PurchaseOrderSerializer(purchase_orders, many = True)
        if serializer:
            return Response(serializer.data, status= status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status= status.HTTP_404_NOT_FOUND)
    
    def post(self, request):
        serializer = PurchaseOrderSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.date, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PurchaseOrderViews(APIView):
    def get(self, request, pk):
        purchase_order = PurchaseOrder.objects.get(pk = pk)
        serializer = PurchaseOrderSerializer(purchase_order)
        if purchase_order:
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
    
    
    def put(self, request, pk):
        purchase_order = PurchaseOrder.objects.get(pk = pk)
        serializer = PurchaseOrderSerializer(purchase_order, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        purchase_order = PurchaseOrder.objects.get(pk = pk)
        serializer = PurchaseOrderSerializer(purchase_order)
        if serializer.is_valid():
            serializer.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VendorPerformanceViews(APIView):
    def get(self, request, pk):
        performance = Vendor.objects.get(pk = pk)
        serializer = VendorSerializer(performance)
        if serializer:
            return Response({"on_time_delivery_rate":serializer.data['on_time_delivery_rate'], 
                            "quality_rating_avg":serializer.data['quality_rating_avg'],
                            "average_response_time":serializer.data['average_response_time'],
                            "fulfillment_rate":serializer.data['fulfillment_rate']},
                            status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Acknowledgement(APIView):
    def post(self, request, pk):
        purchase_order = PurchaseOrder.objects.get(pk = pk)
        
        if not purchase_order:
            return Response({"error": "Purchase order not found"}, status=status.HTTP_404_NOT_FOUND)
        purchase_order.acknowledgment_date = timezone.now()
        purchase_order.save()
        
        serializer = PurchaseOrderSerializer(purchase_order)
        if serializer:
            return Response({'acknowledge_date':serializer.date['acknowledgment_date']}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)