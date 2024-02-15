from django.shortcuts import render,get_object_or_404
from django.template import loader
from django.http import HttpResponse, Http404,HttpResponseRedirect, JsonResponse, HttpResponseNotFound, HttpResponseServerError
from .models import Item, Item_Status,Item_Category, Image
from django.urls import reverse
from django.views import generic
from django.core import serializers
from .services  import scrap, download_image, getUrl
from django.db.models import Q
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from .serializers import ItemStatusSerializer, ItemSerializer, ItemCategorySerializer
from staff.serializers import ProfileSerializer
from django.views.decorators.http import require_POST
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.exceptions import APIException, ValidationError
from staff.models import Profile
from rest_framework.decorators import api_view, parser_classes
from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser









# Create your views here.
# Input code
# Output succuss if find item, return item list
# Output not found if not find item
@api_view(['GET'])
def getItemInfoByCode(request, code):
        items = None
        if code.startswith('B'):
            items = Item.objects.filter(b_code=code)
        elif code.startswith('X'):
            items = Item.objects.filter(fnsku_code=code)
        elif code.startswith('LPN'):
            items = Item.objects.filter(lpn_code=code)
        elif code.isdigit:
            items = Item.objects.filter(Q(upc_code=code) | Q(ean_code=code))
        else:
            print('here')
            return JsonResponse({'status': 'not found', 'message': 'Code formate like ' + code + ' is not stored in database.'})
        if len(items) == 0:
            if code.startswith('B'):
                return scrapInfoByBOCode(request, code)
            print('here2')
            return JsonResponse({'status': 'not found', 'message': 'Code '+code+' not found in database.'})
        else:
            serialize_item = ItemSerializer(items[0])
            # return Response({'status': "success", 'data': serialize_item.data})

            d = serialize_item.data
            print('*****',d)
            d_cate = Item_Category.objects.get(id=int(d['category_id']))
            d['category'] = {
                'id': str(d_cate.id),
                'name': d_cate.name,
            }
            return Response({'status': "success", 'data': d})
def scrapInfoByBOCode(request, code):
        url = getUrl(code)
        result = scrap(url, code)
        print('result', result)
        if result['status'] == 1:
            return JsonResponse({'status': 'success', 'data': result['data']})
        elif result['status'] == 0:
            return JsonResponse({'status': 'not found', 'message': result['message']})
        elif result['status'] == 2:
            return  HttpResponseServerError(result['message'])
        else:
            return  HttpResponseServerError("Server Error, please contact developer.")


def scrapInfoByURL(request, url):
    try:
        result = scrap(url)
        print('result', result)
        if result['status'] == 1:
            return JsonResponse({'status': 'success', 'data': result['data']})
        elif result['status'] == 0:
            return JsonResponse({'status': 'not found', 'message': result['message']})
        elif result['status'] == 2:
            return HttpResponseServerError(result['message'])
        else:
            return HttpResponseServerError("Server Error, please contact developer.")
    except:
        return HttpResponseServerError('scrapInfoByURL failed, error happen in server')

@csrf_exempt
@parser_classes([FileUploadParser])
def addNewItem(request):
    # Get staff last issued item number
    try:
        print('here')
        print('here', request)
        print('here', request.data)
        if 'item' in request.FILES:
            itm = request.FILES['item']
            stf = Profile.objects.get(user_id=itm['add_staff_id'])
            # Set staff last issued number + 1 to new added item number
            data = itm.copy()
            if stf.last_issued_number + 1 <= stf.item_end:
                data['item_number'] = stf.last_issued_number + 1
            else:
                raise  ValidationError(detail="Item number has reach the staff's limit, please contact admin")
            # Serialize data and save it
            serializer_itm = ItemSerializer(data=data)
            serializer_stf = ProfileSerializer(stf, data={'last_issued_number': stf.last_issued_number + 1},partial=True)
            if serializer_itm.is_valid() and serializer_stf.is_valid():
                serializer_itm.save()
                serializer_stf.save()
                # Add images to the
                if 'pics' in request.FILES:
                    pics = request.FILES['pics']
                    for pic in pics:
                        if pic['has_saved']:
                            set_image_fk(pic['id'], serializer_itm.id)
                        else:
                            create_img_with_fk({'uri': pic['url'], 'type': pic['type']})
                    return Response(serializer_itm.data, status=201)
                raise ValidationError('Item has been saved, but image missed.')
            else:
                print('err1', serializer_itm.errors)
                print('err2', serializer_stf.errors)
                raise  ValidationError()
    except Exception as err:
        print('err', err)
        raise APIException()


def deleteItem(request):
    try:
        print('deleteItem')
        print(request.body)
    except:
        print('do nothing')
    return HttpResponse('deleteItem success')


def updateItem(request, id):
    try:
        print('updateItem')
    except:
        print('do nothing')
    return HttpResponse('updateItem success')

def getItem(request, id):
    try:
        print('getItem')
    except:
        print('do nothing')
    return HttpResponse('getItem success')

# class GetStatusView(generic.ListView):
#     # template_name = "inventory/index.html"
# # context_object_name = "latest_item_list"
#     list = Item_Status.objects.all();
#     return JsonResponse({'status': "success", 'data': model_to_dict(items[0])})
#
#     def get_queryset(self):
#         return  []
# class GetCategoriesView(generic.ListView):
#     # template_name = "inventory/index.html"
# # context_object_name = "latest_item_list"
#     def get_queryset(self):
#         return  []
# class GetSizesByCategoryView(generic.ListView):
#     # model = Article
#     # template_name = 'articles/article_list.html'
#     def get_queryset(self):
#         queryset = super().get_queryset()  # Get the original queryset
#         category = self.request.GET.get('category')  # Get the 'category' query parameter
#
#         return  []
#
# class GetColorsByCategoryView(generic.ListView):
#     # model = Article
#     # template_name = 'articles/article_list.html'
#     def get_queryset(self):
#         queryset = super().get_queryset()  # Get the original queryset
#         category = self.request.GET.get('category')  # Get the 'category' query parameter
#         return  []


class IndexView(generic.ListView):
        template_name = "inventory/index.html"
        context_object_name = "latest_item_list"
        def get_queryset(self):
            # Get the fisrt 100 items in recent added item list.

            lastest_item_list = Item.objects.order_by("-add_date")[:100]

            # context = {
            #     "lastest_item_list": lastest_item_list,
            # }
            # 2 return the template render
            # template = loader.get_template("inventory/index.html")
            # return  HttpResponse(template.render(context, request))

            # 1 return requst url
            # output = ", ".join([i.item_title for i in lastest_item_list])
            # return  HttpResponse(output)

            # 3 return template directly wtih context
            # return  render(request, "inventory/index.html", context)

            # 4 using in build views and redefine it as class and func in it
            return lastest_item_list;
# class TitleView(generic.DetailView):
#     model = Item
#     template_name = "inventory/title.html"
#     # return HttpResponse("You're looking at title %s." % item_id)


# def set_description(request, item_id):
#     try:
#         # The request is a POST request, get the post request field named description
#         des = request.POST['description']
#         i = get_object_or_404(Item, pk=item_id)
#         i.description = des
#         i.save();
#     except Item.DoesNotExist:
#         raise Http404("Item does not exist")
#     return HttpResponseRedirect(reverse("inventory:success"))

class StatusView(APIView):
    model = Item_Status
    template_name = "inventory/status.html"
    def get(self, request, format=None):
        items = Item_Status.objects.all().values('status', 'id');
        serialize_sts = ItemStatusSerializer(items, many=True)
        return Response(serialize_sts.data);


class CategoryView(APIView):
    model = Item_Category
    template_name = "inventory/status.html"
    def get(self, request, format=None):
        items = Item_Category.objects.all().values('name', 'id');
        serialize_cates = ItemCategorySerializer(items, many=True)
        return Response(serialize_cates.data)



    # def get(self, request, *args, **kwargs):
    #     list = Item_Category.objects.all();
    #     print(list[0])
    #     # print('here')
    #     # data = serializers.serialize('json', list)
    #     return HttpResponse();

        # return JsonResponse(data, safe=false);


def addImage(request):
    item_instance = Item(id=553)
    image_instance = Image(item=item_instance)
    image_instance.external_url = 'https://media.wired.com/photos/5b8999943667562d3024c321/master/w_960,c_limit/trash2-01.jpg'
    download_image(image_instance, 'https://media.wired.com/photos/5b8999943667562d3024c321/master/w_960,c_limit/trash2-01.jpg')
    return HttpResponse(image_instance.id)

@csrf_exempt
def deleteImage(request, pk):
    image_instance = Image.objects.get(pk=pk)
    image_instance.delete()
    return HttpResponse('success')
