from django.shortcuts import render,get_object_or_404
from django.template import loader
from django.http import HttpResponse, Http404,HttpResponseRedirect
from .models import Item, Item_Status,Item_Category
from django.urls import reverse
from django.views import generic

# Create your views here.

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
class DescriptionView(generic.DetailView):
    model = Item
    template_name = "inventory/description.html"
    # try:
    #     i = Item.objects.get(pk=item_id)
    # except Item.DoesNotExist:
    #     raise Http404("Item does not exist")
    # return render(request, "inventory/description.html", {"item": i})
def set_description(request, item_id):
    try:
        # The request is a POST request, get the post request field named description
        des = request.POST['description']
        i = get_object_or_404(Item, pk=item_id)
        i.description = des
        i.save();
    except Item.DoesNotExist:
        raise Http404("Item does not exist")
    return HttpResponseRedirect(reverse("inventory:success"))
class StatusView(generic.DetailView):
    model = Item
    template_name = "inventory/status.html"
    # i = get_object_or_404(Item, pk=item_id)
    # return render(request, "inventory/status.html", {"status": i.status_id})

class BoCodeView(generic.DetailView):
    model = Item
    template_name = "inventory/bo_code.html"
    # i = get_object_or_404(Item, pk=item_id)
    # return render(request, "inventory/status.html", {"status": i.status_id})


class SuccessView(generic.DetailView):
    model = Item
    template_name = "inventory/success.html"
    # return render(request, "inventory/success.html", {})