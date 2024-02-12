from django.shortcuts import render,get_object_or_404
from django.template import loader
from django.http import HttpResponse, Http404,HttpResponseRedirect, JsonResponse, HttpResponseNotFound, HttpResponseServerError
from .models import Item, Item_Status,Item_Category, Image
from django.urls import reverse
from django.views import generic
from django.core import serializers
from .services  import scrap, download_image
from django.db.models import Q
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt





# Create your views here.
# Input code
# Output succuss if find item, return item list
# Output not found if not find item
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
            return JsonResponse({'status': 'not found', 'message': 'Code formate like ' + code + ' is not stored in database.'})
        if len(items) == 0:
            if code.startswith('B'):
                return scrapInfoByBOCode(request, code)
            return JsonResponse({'status': 'not found', 'message': 'Code '+code+' not found in database.'})
        else:
            return JsonResponse({'status': "success", 'data': model_to_dict(items[0])})
def scrapInfoByBOCode(request, code):
        result = scrap(code)
        print('result', result)
        if result['status'] == 1:
            print('here 1')
            return JsonResponse({'status': 'success', 'data': result['data']})
        elif result['status'] == 0:
            return JsonResponse({'status': 'not found', 'message': result['message']})
        elif result['status'] == 2:
            return  HttpResponseServerError(result['message'])
        else:
            return  HttpResponseServerError("Server Error, please contact developer.")


def scrapInfoByURL(request, url):
    try:
        print('scrapInfoByURL')
    except:
        print('do nothing')
    return HttpResponse('scrapInfoByURL success')

def addNewItem(request):
    try:
        print('addNewItem')
        print(request.body)
    except:
        print('do nothing')
    return HttpResponse('addNewItem success')

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
class StatusView(generic.ListView):
    model = Item_Status
    template_name = "inventory/status.html"
    def get(self, request, *args, **kwargs):
        items = Item_Status.objects.all().values('status');
        l = [d ['status'] for d in items]
        return JsonResponse(l, safe=False);


class CategoryView(generic.ListView):
    model = Item_Category
    template_name = "inventory/status.html"

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
