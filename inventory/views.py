from django.http import HttpResponse, JsonResponse, HttpResponseServerError, HttpResponseBadRequest
from django.core.paginator import Paginator
from django.db.models import Max
from .models import Item, Item_Status, Item_Category, Image, Purchase_List, Auction_Product_List
from .services import scrap, download_image, getUrl, scrapInfoByNumCodeService
from django.views.decorators.csrf import csrf_exempt
from .serializers import ItemStatusSerializer, ItemSerializer, ItemCategorySerializer, AuctionProductListSerializer
from staff.serializers import ProfileSerializer
from rest_framework.response import Response
from rest_framework.exceptions import APIException, ValidationError
from staff.models import Profile
from rest_framework.decorators import api_view, parser_classes
from rest_framework.views import APIView
import datetime
import csv
import zipfile
import json
from urllib.parse import urljoin
import os
from django.core.files.storage import default_storage
from utils.file import image_upload_to, get_extension, create_unique_filename, create_unique_imagename
from rest_framework.renderers import JSONRenderer
import logging
import dotenv

dotenv.load_dotenv()

logger = logging.getLogger('django')

MEDIA_DOMAIN = os.getenv('MEDIA_DOMAIN')


# Create your views here.
# Input code
# Output succuss if find item, return item list
# Output not found if not find item
@api_view(['GET'])
def getItemInfoByCode(request, code):
    try:
        items = None
        print('code', code)
        logger.info('item code' + code)
        if code.startswith('B'):
            items = Item.objects.filter(b_code=code).prefetch_related('images')
        # elif code.startswith('X'):
        #     items = Item.objects.filter(fnsku_code=code)
        # elif code.startswith('LPN'):
        #     items = Item.objects.filter(lpn_code=code)
        elif code.isdigit():
            items = Item.objects.filter(upc_ean_code=code).prefetch_related('images')
        elif code.startswith('LPN'):
            items = Item.objects.filter(lpn_code=code).prefetch_related('images')
        else:
            return JsonResponse(
                {'status': 'not found', 'message': 'Code formate like ' + code + ' is not recongnized.'})
        print('after search code in item table')
        print('items value', items)
        logger.info(f'items value, {items}')
        if len(items) == 0:
            print('queryset result len is 0')
            if code.startswith('B'):
                print('code start with B and scrap on web')
                return scrapInfoByBOCode(request, code=code)
            elif code.isdigit():
                print('code is digit and scrap on web')
                return scrapInfoByNumCode(request, code=code)
            elif code.startswith('LPN'):
                items = Purchase_List.objects.filter(lpn_code=code)
                logger.info(f'LPN items value: {items}')
                if len(items) == 0:
                    return JsonResponse({'status': 'not found',
                                         'message': 'Code ' + code + ' not found in database, please scan the digital code of this product.'})
                else:
                    print('find lpn in purchase list')
                    return scrapInfoByBOCode(request, code=items[0].b_code, lpn=code)
            # return JsonResponse({'status': 'not found', 'message': 'Code ' + code + ' not found in database.'})
        else:
            serialize_item = ItemSerializer(items[0])
            # return Response({'status': "success", 'data': serialize_item.data})
            # d = serialize_item.data
            # print('*****', d)
            # d_cate = Item_Category.objects.get(id=int(d['category_id']))
            # d['category'] = {
            #     'id': str(d_cate.id),
            #     'name': d_cate.name,
            # }
            # d['price'] = d['msrp_price']
            # print('d, id', d['id'])
            # print('d, id type', type(d['id']))

            # pics = []
            # print(type(d['images']))
            # print(d['images'])
            # for p in d['images'][:3]:
            #     temp_dict = {}
            #     for key, value in p.items():
            #         temp_dict[key] = value
            #         if key == 'full_image_url':
            #             temp_dict['url'] = value
            #     pics.append(temp_dict)
            # d['pics'] = pics

            # pics_with_item = Image.objects.filter(item_id=d['id'])
            # print('pics_with_item', pics_with_item)
            # pics = []
            # for p in pics_with_item[:3]:
            #     pics.append({'id': p.id,
            #                  'url': urljoin('http://', MEDIA_DOMAIN, p.local_image.url),
            #                  'has_saved': True})
            # d['pics'] = pics
            return Response({'status': "success", 'data': serialize_item.data})
    except Exception as e:
        print(e)


def scrapInfoByBOCode(request, **kwargs):
    code = kwargs.get('code')
    lpn = kwargs.get('lpn') or None
    result = scrap(code=code, lpn=lpn)
    logger.info(f'result: {result}')
    if result['status'] == 1:
        logger.info(result['data'])
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
    result = scrapInfoByNumCodeService(code, 'https://www.amazon.ca/')
    logger.info(f'result: {result}')
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
        logger.info(f'url: {url}')
        result = scrap(url=url)
        logger.info(f'result: {result}')
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
            logger.info(f'item string is: {item_string}')
            is_new_string = request.data.get('is_new')
            logger.info(f'is_new_string is: {is_new_string}')
            is_new = json.loads(is_new_string)
            itm = json.loads(item_string)
            # print('here', request.FILES.get('image').uri)
            if itm:
                stf = Profile.objects.get(user_id=itm['add_staff'])
                logger.debug(type(itm['add_staff']))
                logger.debug(itm['status'])
                # Set staff last issued number + 1 to new added item number
                data = itm.copy()
                new_last_issued_number = None
                if not itm.get('item_number'):
                    logger.debug(f'last issued number: {stf.last_issued_number}')
                    if stf.last_issued_number + 1 <= stf.item_end:
                        data['item_number'] = stf.last_issued_number + 1
                        new_last_issued_number = stf.last_issued_number + 1
                    else:
                        raise ValidationError(detail="Item number has reach the staff's limit, please contact admin")
                else:
                    new_last_issued_number = itm.get('item_number')
                # Serialize data and save it
                if is_new:
                    serializer_itm = ItemSerializer(data=data)
                else:
                    old_item = Item.objects.get(id=data['id'])
                    serializer_itm = ItemSerializer(old_item, data=data, partial=True)
                serializer_stf = ProfileSerializer(stf, data={'last_issued_number': new_last_issued_number},
                                                   partial=True)
                if serializer_itm.is_valid() and serializer_stf.is_valid():
                    itm_instance = serializer_itm.save()
                    serializer_stf.save()
                    # Add or update images to the item
                    ids = request.data.getlist('img_id')
                    # update items for removing images by deleting images that not in ids
                    if not is_new:
                        old_images = Image.objects.filter(item_id=data['id'])
                        images_to_delete = old_images.exclude(pk__in=ids)
                        images_to_delete.delete()
                    i = 1
                    if ids:
                        # for id in ids:
                        #     id = int(id)
                        for id in ids:
                            saved_img = Image.objects.get(id=id)
                            # update items with its image updating to new item id
                            if not is_new:
                                saved_img.item_id = data['id']
                                saved_img.save()
                                continue
                            # scrapped image but haven't set foreign key to any item
                            if not saved_img.item:
                                logger.info('Not saved image')
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
                                logger.info('Saved image')
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
                    logger.info(f'err1: {serializer_itm.errors}')
                    logger.info(f'err2 {serializer_stf.errors}')
                    raise ValidationError()
        except Exception as err:
            logger.info(f'err: {err}')
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

@api_view(['DELETE'])
@csrf_exempt
def deleteItem(request, pk):
    try:
        Item.objects.filter(pk=pk).delete()
        logger.debug('delete success')
        return Response({'status': 'success'})
    except Exception as e:
        logger.error(e)
        return HttpResponseServerError('Server error')


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
        items = Item.objects.order_by('-add_date').prefetch_related('images').select_related('add_staff').select_related(
            'status')
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


@api_view(['POST'])
def exportItems(request):
    zip_full_path = None
    try:
        ids = []
        auction = request.data['auction']
        data = request.data['data']
        # put ids into a list
        for x in data:
            ids.append(x['id'])
        print('ids', ids)
        # get items by ids, return a dictionary items with id as key
        items = Item.objects.filter(pk__in=ids).prefetch_related('images')
        for x in data:
            x['item'] = items.get(pk=x['id'])
        # export items to csv
        filename = "Auction {}".format(auction)
        date_prefix = datetime.datetime.now().strftime('%Y%m%d')
        dir = f'{os.getenv("EXPORT_DIR")}/{date_prefix}'
        extension = '.csv'
        # create unique filename, like Auction 65_1, Auction 65_2
        full_path = create_unique_filename(dir, filename, extension)
        with open(full_path, 'x', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([])
            for x in data:
                code = x.get('item').b_code or x.get('item').upc_ean_code or x.get('item').lpn_code or 'B09999999'
                writer.writerow([code,
                                 x.get('item').title,
                                 x.get('description'),
                                 x.get('item').msrp_price,
                                 x.get('sequence'),
                                 x.get('item').bid_start_price,
                                 x.get('image_number'),
                                 ])

        # create images zip file
        zip_extension = '.zip'
        zip_full_path = create_unique_filename(dir, filename, zip_extension)
        with zipfile.ZipFile(zip_full_path, 'w') as img_zip:
            img_zip.write(full_path, arcname=os.path.basename(full_path))
            for x in data:
                image_number = x.get('image_number')
                existing_names = []
                print('images', x.get('item').images.all())
                for img in x.get('item').images.all():
                    base_name, extension = os.path.splitext(img.local_image.url)
                    # create a unique image name
                    img_name = create_unique_imagename(existing_names, str(image_number) + extension)
                    # write to zip file
                    img_zip.write(os.getenv('MEDIA_DIR')+img.local_image.url, arcname=f'imgs/{img_name}')
                    # add name to existing names
                    existing_names.append(img_name)

        # insert items to auction product list
        print('before insert list')
        insert_list = []
        for x in data:
            d = {
                'auction': auction,
                'sequence': x.get('sequence'),
                'description': x.get('description'),
                'image_number': x.get('image_number'),
                'item': x.get('item').id,
            }
            insert_list.append(d)
        print('insert_list', insert_list)
        serializer = AuctionProductListSerializer(data=insert_list, many=True)
        print('after serialized')
        if serializer.is_valid():
            print('valid serializer')
            serializer.save()
            print('after save serializer')
            response = HttpResponse(open(zip_full_path, 'rb'), content_type='application/zip')
            response['Content-Disposition'] = f'attachment; filename={os.path.basename(zip_full_path)}'
            return response
        else:
            print('not valid serializer')
            os.remove(full_path)
            raise ValidationError(detail=serializer.errors)
    except IOError:
        return HttpResponseServerError('Read zip file error.')
    except Exception as e:
        print('err', e)
        return HttpResponseBadRequest('Export items to CSV error.')
    finally:
        if os.path.exists(zip_full_path):
            os.remove(zip_full_path)
@api_view(['GET'])
def getNextLotNumber(request, auction):
    m = Auction_Product_List.objects.filter(auction=auction).aggregate(Max('image_number'))['image_number__max']
    if not m:
        return Response(1+1)
    return Response(m + 1)
@api_view(['GET'])
def getAvailableSequences(request, auction):
    try:
        m = Auction_Product_List.objects.filter(auction=auction).aggregate(Max('sequence'))['sequence__max']
        sequences = list(Auction_Product_List.objects.filter(auction=auction).values_list('sequence', flat=True))
        if not m:
            return Response({'range': [[2, 9999]], 'list': []})
        l = [[]]
        for i in range(2, m+1):
            last = l[len(l) - 1]
            if i in sequences:
                if len(last) == 1:
                    last.append(i-1)
                    l.append([])
                continue
            else:
                if len(last) == 0:
                    last.append(i)
                elif len(last) == 1:
                    continue
        last = l[len(l) - 1]
        last.append(m+1)
        last.append(9999)
        return Response({'range': l, 'list': sequences})
    except Exception as e:
        print('e', e)

@api_view(['GET'])
def getLastItems(request, staff_id):
    try:
        page_number_from_last = request.query_params.get('page_number_from_last', None)
        if not page_number_from_last:
            return HttpResponseBadRequest('Please send page number from last.')
        page_number_from_last = int(page_number_from_last)
        staff_id = int(staff_id)
        print(staff_id)
        items = Item.objects.filter(add_staff_id=staff_id).order_by('add_date')
        paginator = Paginator(items, 10)
        last_page_number = paginator.num_pages
        if last_page_number + 1 - page_number_from_last <= 0:
            return Response([])
        page_number = max(1, last_page_number + 1 - page_number_from_last)  # Ensure it does not go below 1
        page_items = paginator.page(page_number)
        reversed_items = list(page_items.object_list)[::-1]
        print('second_last_page', reversed_items)
        serializer = ItemSerializer(reversed_items, many=True)
        return Response(serializer.data)

    except Exception as e:
        print('e', e)

