import xlwt
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from stock.forms import Create_ItmDist_Form, item_list_create
from stock.models import ItemDist, ItemName, ItemModel, ac_block
from django.db.models import Sum, Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from .filters import Item_dstFilter
import json

items = ""


# Create your views here.

def home(request):
    comp = ItemDist.objects.all().filter(item_name=1, act=1).aggregate(Sum('item_qty'))
    printer = ItemDist.objects.all().filter(item_name=2, act=1).aggregate(Sum('item_qty'))
    proj = ItemDist.objects.all().filter(item_name=3, act=1).aggregate(Sum('item_qty'))
    scan = ItemDist.objects.all().filter(item_name=4, act=1).aggregate(Sum('item_qty'))
    up = ItemDist.objects.all().filter(item_name=8, act=1).aggregate(Sum('item_qty'))
    updated_on = ItemDist.objects.latest('updated_at')
    choices = {'computer': comp, 'printer': printer, 'projector': proj, 'scanner': scan, 'ups': up,'updt':updated_on}
    return render(request, 'home.html', choices)


def item_list(request):
    item_lst = ItemDist.objects.all().filter(act=1).order_by('acblock', 'room')
    z = request.GET
    item_filter = Item_dstFilter(z, queryset=item_lst)
    global items
    items = z
    item_qty = item_filter.qs.aggregate(Sum('item_qty'))
    choices = {'filter': item_filter, 'totality': item_qty}
    return render(request, 'item_list.html', choices)


def export_users_xls(request):
    # call global variable item1
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="item.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('items')
    # Sheet header, first row
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['item Name', 'Model', 'Block', 'Room', 'Room Type', 'Deptartment','user', 'Quantity', ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    # Sheet body, remaining row
    font_style = xlwt.XFStyle()
    item_lst = ItemDist.objects.all().filter(act=1).order_by('acblock', 'room')
    item_filter = Item_dstFilter(items, queryset=item_lst)
    aa = item_filter.qs
    rows = aa.values_list('item_name__item_name', 'item_model__model_name', 'acblock__name', 'room',
                          'room_type__room_type', 'inst__Inst_name','user', 'item_qty')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
    wb.save(response)
    return response


def labs(request):
    item_name_b = ItemDist.objects.all().filter(item_name=1, room='102 B', acblock__name='AB- 9')
    item_qty_b = ItemDist.objects.all().filter(item_name=1, room='102 B', acblock__name='AB- 9').aggregate(
        Sum('item_qty'))
    item_name_c = ItemDist.objects.all().filter(item_name=1, room='102 C', acblock__name='AB- 9')
    item_qty_c = ItemDist.objects.all().filter(item_name=1, room='102 C', acblock__name='AB- 9').aggregate(
        Sum('item_qty'))
    item_name_d = ItemDist.objects.all().filter(item_name=1, room='102 D', acblock__name='AB- 9')
    item_qty_d = ItemDist.objects.all().filter(item_name=1, room='102 D', acblock__name='AB- 9').aggregate(
        Sum('item_qty'))
    item_name_e = ItemDist.objects.all().filter(item_name=1, room='102 E', acblock__name='AB- 9')
    item_qty_e = ItemDist.objects.all().filter(item_name=1, room='102 E', acblock__name='AB- 9').aggregate(
        Sum('item_qty'))
    # itm = ItemDist.objects.all().order_by('room')
    choices = {'ItemName_b': item_name_b, 'ItemQty_b': item_qty_b, 'ItemName_c': item_name_c, 'ItemQty_c': item_qty_c,
               'ItemName_d': item_name_d, 'ItemQty_d': item_qty_d, 'ItemName_e': item_name_e, 'ItemQty_e': item_qty_e}
    return render(request, 'labs.html', choices)


@login_required
def cpanel(request):
    queryset1 = ItemDist.objects.values('item_name__item_name').filter(act=1).annotate(
        total_qty_c=Sum('item_qty')).order_by('item_name__item_name')
    queryset = ItemDist.objects.values('acblock__name').annotate(
        total_qty_c=Sum('item_qty', filter=Q(item_name=1, act=1)),
        total_qty_p=Sum('item_qty', filter=Q(item_name=2, act=1)),
        total_qty_pro=Sum('item_qty', filter=Q(item_name=3, act=1)),
        total_qty_s=Sum('item_qty', filter=Q(item_name=4, act=1))) \
        .order_by('acblock')
    choices = {'dataset': queryset, 'ds1': queryset1}
    return render(request, 'cpanel/AdminHome.html', choices)

# Sign out/Logout  View #
def signout(request):
    logout(request)
    return redirect('home')


# Admin Panel Item List View #
@login_required
def citem_list(request):
    if not request.user.has_perm('auth.view_group'):
        return render(request, 'cpanel/error.html')
    else:
        item_lst = ItemDist.objects.all().order_by('act', 'acblock', 'room')
        z = request.GET
        item_filter = Item_dstFilter(z, queryset=item_lst)
        global items
        items = z
        page = request.GET.get('page', 1)
        paginator = Paginator(item_filter.qs, 10)
        try:
            itm = paginator.page(page)
        except PageNotAnInteger:
            itm = paginator.page(1)
        except EmptyPage:
            itm = paginator.page(paginator.num_pages)
        item_qty = item_filter.qs.aggregate(Sum('item_qty'))
        choices = {'filter': item_filter, 'totality': item_qty}
    return render(request, 'cpanel/Item/item_list.html', choices)


@login_required
def update_item_list(request, item_id, template_name='cpanel/Item/upadate_item_list.html'):
    if not request.user.has_perm('auth.change_group'):
        return render(request, 'cpanel/error.html')
    else:
        post = get_object_or_404(ItemDist, pk=item_id)  # ItemDist is a  Model
        form = item_list_create(request.POST or None, instance=post)
        if form.is_valid():
            form.save()
            return redirect('item_list')
    return render(request, template_name, {'form': form})


@login_required
def delete_item(request, item_id):
    if not request.user.has_perm('auth.delete_group'):
        return render(request, 'cpanel/error.html')
    else:
        obj = get_object_or_404(ItemDist, id=item_id)
        context = {'items': obj}
        if request.method == "POST":
            # delete object
            obj.delete()
            return redirect("item_list")
    return render(request, "cpanel/Item/Delete_items.html", context)


@login_required
def item_approved(request, item_id):
    if not request.user.has_perm('auth.change_group'):
        return render(request, 'cpanel/error.html')
    else:
        obj = get_object_or_404(ItemDist, id=item_id)
        obj.act = 1
        obj.save()
        return redirect("item_list")


@login_required
def create_item_list(request):
    if not request.user.has_perm('auth.add_group'):
        return render(request, 'cpanel/error.html')
    else:
        upload = Create_ItmDist_Form()  # Create_ItmDist_Form is a form
        if request.method == 'POST':
            upload = Create_ItmDist_Form(request.POST, request.FILES)
            if upload.is_valid():
                upload.save()
                return redirect('create_item_list1')
        return render(request, 'cpanel/Item/Create_ItemDist.html', {'upload_form': upload})

    

def load_ItemModel(request):
    item_name_id = request.GET.get('item_name')
    item_model = ItemModel.objects.filter(item_name_id=item_name_id).order_by('model_name')
    return render(request, 'cpanel/modelname_dropdown.html', {'model': item_model})


@login_required
def chart_bar(request):
    labels = []
    data = []

    queryset = ItemDist.objects.values('acblock__name').filter(item_name=1, act=1).annotate(total_qty=Sum('item_qty')) \
        .order_by('acblock')
    for entry in queryset:
        labels.append(entry['acblock__name'])
        data.append(entry['total_qty'])

    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })


@login_required
def chart_bar1(request):
    queryset = ItemDist.objects.values('acblock__name').annotate(
        total_qty_c=Sum('item_qty', filter=Q(item_name=1, act=1)),
        total_qty_p=Sum('item_qty', filter=Q(item_name=2, act=1)),
        total_qty_pro=Sum('item_qty', filter=Q(item_name=3, act=1)),
        total_qty_s=Sum('item_qty', filter=Q(item_name=4, act=1))) \
        .order_by('acblock')

    blocks = list()
    computer = list()
    printer = list()
    projector = list()
    scanner = list()

    for entry in queryset:
        blocks.append(entry['acblock__name'])
        computer.append(entry['total_qty_c'])
        printer.append(entry['total_qty_p'])
        projector.append(entry['total_qty_pro'])
        scanner.append(entry['total_qty_s'])
    choices = {'blocks': json.dumps(blocks),
               'computer': json.dumps(computer),
               'printer': json.dumps(printer),
               'projector': json.dumps(projector),
               'scanner': json.dumps(scanner)}
    return render(request, 'cpanel/chart_bar.html', choices)


@login_required
def new_user(request):
    if request.method == "POST":
        if request.POST.get('password1') == request.POST.get('password2'):
            try:
                saveuser = User.objects.create_user(request.POST.get('username'),
                                                    password=request.POST.get('password1'))
                saveuser.save()
                return render(request, 'cpanel/Users/NewUser.html', {'form': UserCreationForm,
                                                                     'info': 'User ' + request.POST.get(
                                                                         'username') + ' Create Succesfull'})
            except IntegrityError:
                return render(request, 'cpanel/Users/NewUser.html', {'form': UserCreationForm,
                                                                     'info': 'User ' + request.POST.get(
                                                                         'username') + ' Already Exists !!'})
        else:
            return render(request, 'cpanel/Users/NewUser.html',
                          {'form': UserCreationForm, 'error': 'the password is not match'})
    else:

        return render(request, 'cpanel/user/NewUser.html', {'form': UserCreationForm})


def update_user_profile(request):
    return render(request, 'cpanel/user/user_profile.html')
