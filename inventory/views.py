from django.http import HttpResponse,  JsonResponse, HttpResponseServerError, HttpResponseBadRequest
from django.core.paginator import Paginator
from .models import Item, Item_Status, Item_Category, Image, Purchase_List
from .services import scrap, download_image, getUrl, scrapInfoByNumCodeService
from django.views.decorators.csrf import csrf_exempt
from .serializers import ItemStatusSerializer, ItemSerializer, ItemCategorySerializer
from staff.serializers import ProfileSerializer
from rest_framework.response import Response
from rest_framework.exceptions import APIException, ValidationError
from staff.models import Profile
from rest_framework.decorators import api_view, parser_classes
from rest_framework.views import APIView
import json
from urllib.parse import urljoin
import os
from django.core.files.storage import default_storage
from utils.file import image_upload_to, get_extension
from rest_framework.renderers import JSONRenderer
import logging
import dotenv

dotenv.load_dotenv()

logger = logging.getLogger('django')

DOMAIN = os.getenv('DOMAIN')

# Create your views here.
# Input code
# Output succuss if find item, return item list
# Output not found if not find item
@api_view(['GET'])
def getItemInfoByCode(request, code):
    try:
        items = None
        print('code', code)

        if code.startswith('B'):
            items = Item.objects.filter(b_code=code)
        # elif code.startswith('X'):
        #     items = Item.objects.filter(fnsku_code=code)
        # elif code.startswith('LPN'):
        #     items = Item.objects.filter(lpn_code=code)
        elif code.isdigit():
            items = Item.objects.filter(upc_ean_code=code)
        elif code.startswith('LPN'):
            items = Item.objects.filter(lpn_code=code)
        else:
            return JsonResponse({'status': 'not found', 'message': 'Code formate like ' + code + ' is not recongnized.'})
        print('after search code in item table')
        print('items value', items)
        if len(items) == 0:
            print('queryset result len is 0')
            if code.startswith('B'):
                print('code start with B and scrap on web')
                return scrapInfoByBOCode(request, code)
            elif code.isdigit():
                print('code is digit and scrap on web')
                return scrapInfoByNumCode(request, code=code)
            elif code.startswith('LPN'):
                items = Purchase_List.objects.filter(lpn_code=code)
                print('LPN items value', items)
                if len(items) == 0:
                    return JsonResponse({'status': 'not found',
                                         'message': 'Code ' + code + ' not found in database, please scan the digital code of this product.'})
                else:
                    print('find lpn in purchase list')
                    return scrapInfoByBOCode(request, items[0].b_code)
            # return JsonResponse({'status': 'not found', 'message': 'Code ' + code + ' not found in database.'})
        else:
            serialize_item = ItemSerializer(items[0])
            # return Response({'status': "success", 'data': serialize_item.data})
            d = serialize_item.data
            print('*****', d)
            d_cate = Item_Category.objects.get(id=int(d['category_id']))
            d['category'] = {
                'id': str(d_cate.id),
                'name': d_cate.name,
            }
            d['price'] = d['msrp_price']
            print('d, id', d['id'])
            print('d, id type', type(d['id']))
            pics_with_item = Image.objects.filter(item_id=d['id'])
            print('pics_with_item', pics_with_item)
            pics = []
            for p in pics_with_item[:3]:
                pics.append({'id': p.id,
                             'url': urljoin('http://', DOMAIN, '/inventory/media/' + p.local_image.url),
                             'has_saved': True})

            d['pics'] = pics
            return Response({'status': "success", 'data': d})
    except Exception as e:
        print(e)


def scrapInfoByBOCode(request, code):
    url = getUrl(code)
    result = scrap(url=url, code=code)
    print('result', result)
    if result['status'] == 1:
        return JsonResponse({'status': 'success', 'data': result['data']})
    elif result['status'] == 0:
        return JsonResponse({'status': 'not found', 'message': result['message']})
    elif result['status'] == 2:
        return HttpResponseServerError(result['message'])
    else:
        return HttpResponseServerError("Server Error, please contact developer.")


def scrapInfoByNumCode(request, code):
    # url = getUrl(code)
    # result = scrap(url=url, code=code)
    # print('result', result)
    result = scrapInfoByNumCodeService(code);
    if result['status'] == 1:
        return JsonResponse({'status': 'success', 'data': result['data']})
    elif result['status'] == 0:
        return JsonResponse({'status': 'not found', 'message': result['message']})
    elif result['status'] == 2:
        return HttpResponseServerError(result['message'])
    else:
        return HttpResponseServerError("Server Error, please contact developer.")


def scrapInfoByURL(request):
    try:
        url = request.GET.get('url', '')
        print('url', url)
        result = scrap(url=url)
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


# class IndexView(generic.ListView):


class StatusView(APIView):
    renderer_classes = [JSONRenderer]

    def get(self, request, format=None):
        # IS_DEVELOPMENT = os.getenv('IS_DEVELOPMENT') == 'TRUE'
        # WEBDRIVER_PATH = os.getenv('WEBDRIVER_PATH')
        # logger.info(f'**************This is a debug message IS_DEVELOPMENT: {IS_DEVELOPMENT}')
        # logger.info(f'**************This is a debug message WEBDRIVER_PATH: {WEBDRIVER_PATH}')
        # with open('django.log', 'a') as log_file:
        #     log_file.write(WEBDRIVER_PATH)
        items = Item_Status.objects.all().values('status', 'id');
        serialize_sts = ItemStatusSerializer(items, many=True)
        return Response(serialize_sts.data);


class CategoryView(APIView):
    renderer_classes = [JSONRenderer]

    def get(self, request, format=None):
        items = Item_Category.objects.all().values('name', 'id');
        serialize_cates = ItemCategorySerializer(items, many=True)
        return Response(serialize_cates.data)


class AddNewItemView(APIView):
    renderer_classes = [JSONRenderer]

    def post(self, request, *args, **kwargs):
        # Get staff last issued item number
        try:
            # data = request.POST
            # dataset_form = DatasetForm(request.POST, request.FILES)
            # print('here', request.FILES.get('image').file)

            item_string = request.data.get('item')
            itm = json.loads(item_string)
            # print('here', request.FILES.get('image').uri)
            if itm:
                print('here1')
                stf = Profile.objects.get(user_id=itm['add_staff'])
                print('here2', type(itm['add_staff']))

                # Set staff last issued number + 1 to new added item number
                data = itm.copy()
                # data['category_id'] = int(data['category_id'])
                # print('c id******',data['category_id'])
                # print('c id******',type(data['category_id']))
                if not itm.get('item_number'):
                    if stf.last_issued_number + 1 <= stf.item_end:
                        data['item_number'] = stf.last_issued_number + 1
                    else:
                        raise ValidationError(detail="Item number has reach the staff's limit, please contact admin")
                # Serialize data and save it
                serializer_itm = ItemSerializer(data=data)
                serializer_stf = ProfileSerializer(stf, data={'last_issued_number': stf.last_issued_number + 1},
                                                   partial=True)
                if serializer_itm.is_valid() and serializer_stf.is_valid():
                    itm_instance = serializer_itm.save()
                    print('*********', itm_instance.category_id)
                    stf_instance = serializer_stf.save()
                    # Add or update images to the item
                    ids = request.data.getlist('img_id')
                    i = 1
                    if ids:
                        for id in ids:
                            id = int(id)
                        for id in ids:
                            saved_img = Image.objects.get(id=id)
                            # scrapped image and haven't set foreign key to any item
                            if not saved_img.item_id:
                                print('here not')

                                old_file = saved_img.local_image.path
                                exts = get_extension(saved_img.local_image.name)
                                new_file_relative = str(itm_instance.id) + '_' + str(i) + exts
                                new_file = os.path.join(os.path.dirname(old_file), new_file_relative)
                                new_name = image_upload_to(new_file_relative)
                                if not default_storage.exists(new_file):
                                    os.rename(old_file, new_file)
                                    saved_img.local_image.name = new_name
                                    i = i + 1
                                saved_img.item_id = itm_instance.id
                                saved_img.save()
                            else:
                                print('here')
                                new_img = saved_img
                                # copy the new instance
                                new_img.pk = None
                                new_img.item_id = itm_instance.id
                                new_img.save()
                    imgs = request.FILES.getlist('image')
                    if imgs:
                        for img in imgs:
                            exts = get_extension(img.name)
                            new_img = Image(local_image=img, item_id=itm_instance.id)
                            new_img.local_image.name = str(itm_instance.id) + '_' + str(i) + exts
                            i = i + 1
                            new_img.save()
                    return Response(serializer_itm.data, status=201)
                else:
                    print('err1', serializer_itm.errors)
                    print('err2', serializer_stf.errors)
                    raise ValidationError()
        except Exception as err:
            print('err', err)
            raise APIException()


class ImageUploadView(APIView):
    renderer_classes = [JSONRenderer]

    def post(self, request, *args, **kwargs):
        uploaded_file = request.FILES.getlist('img')
        for idx, f in enumerate(uploaded_file):
            print('idx', idx)
            img = Image(local_image=f)
            img.save()
        print('uploaded_file', uploaded_file)
        print('uploaded_file', uploaded_file[0].__dict__)
        # serializer = ImageSerializer(data=request.data)
        # serializer = ImageSerializer(img)
        # serializer.save()
        return Response('hello', status=200)

        if serializer.is_valid():
            print('serializer', serializer)
            serializer.save()
            return Response('hello', status=200)
        else:
            print(serializer.errors)
        return Response('hi', status=500)


def addImage(request):
    item_instance = Item(id=553)
    image_instance = Image(item=item_instance)
    image_instance.external_url = 'https://media.wired.com/photos/5b8999943667562d3024c321/master/w_960,c_limit/trash2-01.jpg'
    download_image(image_instance,
                   'https://media.wired.com/photos/5b8999943667562d3024c321/master/w_960,c_limit/trash2-01.jpg')
    return HttpResponse(image_instance.id)


@csrf_exempt
def deleteImage(request, pk):
    image_instance = Image.objects.get(pk=pk)
    image_instance.delete()
    return HttpResponse('success')


def deleteItem(request):
    try:
        print('deleteItem')
        print(request.body)
    except:
        print('do nothing')
    return HttpResponse('deleteItem success')

@api_view(['PATCH'])
@csrf_exempt
def updateItem(request, pk):
    try:
        item_instance = Item.objects.get(pk=pk)
    except Item.DoesNotExist:
        return HttpResponseBadRequest('Error, item does not exist.')
    print('request.data', request.data)
    serializer = ItemSerializer(item_instance, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return HttpResponse('Update item success!')
    else:
        print(serializer.errors)
        return HttpResponseBadRequest('Error, item field invalid.')




def getItem(request, id):
    try:
        print('getItem')
    except:
        print('do nothing')
    return HttpResponse('getItem success')

@api_view(['GET'])
def getItems(request):
    print('get items')
    try:
        page_size = int(request.GET.get('page_size'))
        page_number = int(request.GET.get('page_number'))
        items = Item.objects.order_by('id').prefetch_related('images').select_related('add_staff').select_related('status')
        paginator = Paginator(items, per_page=page_size)
        page_obj = paginator.get_page(page_number)
        serializer = ItemSerializer(page_obj, many=True)
        return Response(serializer.data)
    except Exception as e:
        print('e', e)
        return HttpResponseBadRequest('Page or page size is not well defined.')

@api_view(['GET'])
def getTotalItems(request):
    print('get items')
    try:
        total = Item.objects.all().count()
        return Response(total)
    except Exception as e:
        print('e', e)
        return HttpResponseBadRequest('Page or page size is not well defined.')


