from django.shortcuts import render ,get_object_or_404 
from rest_framework.decorators import api_view , permission_classes
from .pagination import CustomPagination   
from .filters import ProductFilter
from .models import Product ,Review
from rest_framework.response import Response
from .serializers import ProductSerializer , ReviewSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.db.models import Avg

# Create your views here.

@api_view(['GET'])
def get_all_products(request):
    filterset = ProductFilter(request.GET,queryset=Product.objects.all().order_by('id'))
    pagenator = CustomPagination()
    quaryset = pagenator.paginate_queryset(filterset.qs,request)
    
    
    serializer = ProductSerializer(quaryset,many = True)
    return Response({"products":serializer.data}) 


@api_view(['GET'])
def get_string_products(request,pk):
    products = get_object_or_404(Product,id=pk)
    serializer = ProductSerializer(products,many = False)
    print(products)
    return Response({"products":serializer.data})



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def new_product(request):
    incoming_data = request.data 
    serializer = ProductSerializer(data = incoming_data)

    if serializer.is_valid():
        product = Product.objects.create(**incoming_data,user =request.user)
        
        res = ProductSerializer(product,many = False)


        return Response({"products":res.data})
    else:
        return Response(serializer.errors)




@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_product(request,pk):
    print(request.data)
    product = get_object_or_404(Product,id=pk)
    if product.user != request.user :
        return Response({"error":"sorry you can not update this product"}
                        ,status=status.HTTP_403_FORBIDDEN)
    product.name = request.data.get('name',product.name)
    product.description = request.data.get('description',product.description)
    product.price = request.data.get('price',product.price)
    product.brand = request.data.get('brand',product.brand)
    product.category = request.data.get('category',product.category)
    product.rating = request.data.get('rating',product.rating)
    product.stock = request.data.get('stock',product.stock)
    
    product.save()
    
    serializer = ProductSerializer(product, many = False)
    return Response({'product':serializer.data})



@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_product(request,pk):
    print(request.data)
    product = get_object_or_404(Product,id=pk)
    if product.user != request.user :
        return Response({"error":"sorry you can not update this product"}
                        ,status=status.HTTP_403_FORBIDDEN)
    product.delete()
    
    return Response({'details':"the product deleted succesfully"},status=status.HTTP_200_OK)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_review(request, pk):
    user = request.user
    product = get_object_or_404(Product, id=pk)
    review = product.reviews.filter(user=user)
    incoming_data = request.data
    serializer = ReviewSerializer(data=incoming_data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    rating = incoming_data.get('rating')
    if rating is None or rating < 0 or rating > 5:
        return Response({"error": "please select between 1 to 5"}, status=status.HTTP_400_BAD_REQUEST)

    elif review.exists():
        new_review = {'rating': incoming_data['rating'], 'comment': incoming_data['comment']}
        review.update(**new_review)

        product.rating = product.reviews.aggregate(avg=Avg('rating'))['avg'] or 0
        product.save()

        return Response({"message": "review updated"}, status=status.HTTP_200_OK)

    else:
        product.reviews.create(user=user, rating=incoming_data['rating'], comment=incoming_data.get('comment', ''))

        product.rating = product.reviews.aggregate(avg=Avg('rating'))['avg'] or 0
        product.save()


        return Response({"message": "review created"}, status=status.HTTP_201_CREATED)

 

#products = Product.objects.all()
    # serializer = ProductSerializer(products,many = True)
    #print(products)