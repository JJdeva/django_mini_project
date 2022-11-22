from django.shortcuts import render, redirect
from django.http import Http404
from django.views.generic import View

from django.utils import timezone, dateformat
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator  
from django.db.models import Count
from .models import Store, Menu, Category, BusinessHours
from users.models import Review, User
from .forms import SearchForm

import folium
from folium import plugins

class IndexView(View):
    def get(self, request, *args, **kwargs):
        main = Store.objects.all().order_by('id')[:6]


        star = []
        for i in main.values():
            try:
                num = int(i['store_stars'])
                point = float(i['store_stars']) - num
                ls = [1 for _ in range(num)]
                if (point >= 0.25) and (point < 0.99):
                    ls.append(2)
                elif point < 0.25:
                    ls.append(0)
                if len(ls) != 5:
                    for _ in range(5-len(ls)):
                        ls.append(0)
                star.append({'name': i['id'], 'star': ls})
            except:
                star.append({'name': i['id'], 'star': [0, 0, 0, 0, 0]})

        categories = Category.objects.distinct('main_category')

        localdata = ['강남', '강동', '강북', '강서', '관악', '광진', '구로', '금천', '노원', 
                     '도봉', '동대문', '동작', '마포', '서대문', '서초', '성남', '성동', '성북', 
                    '송파', '양천', '영등포', '용산', '은평', '종로', '중구', '중랑']
        loc_ls = []
        for i in localdata:
            loc_ls.append({'local':i})
        context = {'main': main, 'star': star, 'categories':categories, 'local':loc_ls}
        return render(request, 'place/index.html', context)

class PlaceDetailView(View):
    def get(self, request, store_id, *args, **kwargs):
        try:
            place = Store.objects.get(id=store_id)
            menu = Menu.objects.filter(menus_id=store_id)

            # 영업시간
            btime = BusinessHours.objects.filter(hours_id=store_id)

            # 지도
            x = place.store_latitude
            y = place.store_longitude
            map = folium.Map(location=[x,y] ,zoom_start=18, width='100%', height='100%',)
            folium.Marker([x,y], tooltip = place.store_name).add_to(map)
            plugins.Fullscreen(position='topright',  # Full screen
                   force_separate_button=True).add_to(map)
            # plugins.ScrollZoomToggler().add_to(map)
            maps=map._repr_html_()  #지도를 템플릿에 삽입하기위해 iframe이 있는 문자열로 반환

            # 리뷰 리스트
            reviews = Review.objects.filter(store_id=store_id)
            paginator = Paginator(reviews, 10)  # 페이지당 10개씩 보여주기
            page_number = request.GET.get('page', '1')
            page_obj = paginator.get_page(page_number)
     

            localdata = ['강남', '강동', '강북', '강서', '관악', '광진', '구로', '금천', '노원', 
                     '도봉', '동대문', '동작', '마포', '서대문', '서초', '성남', '성동', '성북', 
                    '송파', '양천', '영등포', '용산', '은평', '종로', '중구', '중랑']
            loc_ls = []
            for i in localdata:
                loc_ls.append({'local':i})

            categories = Category.objects.values('main_category').annotate(
                max_count=Count('main_category')).values('main_category', 'max_count')
        

        except Store.DoesNotExist:
            raise Http404('장소가 존재하지 않아요')

        return render(request, 'place/place_detail.html', context={'place':place, 'menu':menu, 'map':maps, 
                                                                   'btime':btime, 'local':loc_ls, 'categories':categories, 
                                                                   'reviews':reviews, 'page_obj': page_obj,})

def place_search_list_view(request):

    category = request.GET.get('category', None)
    region = request.GET.get('region', None)
    if category != None and region == None:
        category_id = Category.objects.filter(main_category__contains=category).values('main_category','categories')
        query_id = [i['categories'] for i in category_id]
        place_list = Store.objects.filter(id__in=query_id)

    elif category == None and region != None:
        # category_id = Category.objects.all().values('main_category', 'categories')[:40]
        category_id = ''
        query_id = ''#[i['categories'] for i in category_id]
        place_list = Store.objects.filter(store_address__contains=region)

    elif category != None and region != None:
        category_id = Category.objects.filter(main_category__contains=category).values('main_category', 'categories')
        query_id = [i['categories'] for i in category_id]
        place_list = Store.objects.filter(id__in=query_id).filter(store_address__contains=region)

    else:
        category_id = Category.objects.all().values('main_category', 'categories')[:40]
        query_id = [i['categories'] for i in category_id]
        place_list = Store.objects.filter(id__in=query_id).order_by('-pk')
        # raise ValidationError('둘 중 하나의 값은 넣어줘야해요')


    date = dateformat.format(timezone.now(), 'Y년 m월 d일')

    categories = Category.objects.values('main_category').annotate(
        max_count=Count('main_category')).values('main_category', 'max_count')

    
    paginator = Paginator(place_list, 10)  # 페이지당 10개씩 보여주기
    page_number = request.GET.get('page', '1')
    page_obj = paginator.get_page(page_number)


    localdata = ['강남', '강동', '강북', '강서', '관악', '광진', '구로', '금천', '노원', 
                     '도봉', '동대문', '동작', '마포', '서대문', '서초', '성남', '성동', '성북', 
                    '송파', '양천', '영등포', '용산', '은평', '종로', '중구', '중랑']
    loc_ls = []
    for loc in localdata:
        loc_ls.append({'local':loc, 'count':len(Store.objects.filter(store_address__contains=loc))})
 
    star = []
    for i in page_obj.object_list:#place_list.values():
        try:
            num = int(i.store_stars)#int(i['store_stars'])
            point = float(i.store_stars)-num#float(i['store_stars']) - num
            ls = [1 for _ in range(num)]
            if (point >= 0.25) and (point < 0.99):
                ls.append(2)
            elif point < 0.25:
                ls.append(0)
            if len(ls) != 5:
                for _ in range(5-len(ls)):
                    ls.append(0)
            star.append({'name': i.id, 'star': ls})
        except:
            star.append({'name': i.id, 'star': [0, 0, 0, 0, 0]})
        #      star.append({'name': i['id'], 'star': ls})
        # except:
        #     star.append({'name': i['id'], 'star': [0, 0, 0, 0, 0]})
  
    keyword = {'category':category, 'region':region, 'place_count':len(place_list)}

    # 지도
    x_data = [data.store_latitude for data in place_list]#page_obj.object_list]
    y_data = [data.store_longitude for data in place_list]#page_obj.object_list]
    sname_data = [data.store_name for data in place_list]#page_obj.object_list]
    map = folium.Map(location=[sum(x_data)/len(x_data),sum(y_data)/len(y_data)] ,zoom_start=10, width='100%', height='100%',)
    for i in range(len(x_data)):
        folium.Marker([x_data[i],y_data[i]], tooltip = sname_data[i]).add_to(map)
    # plugins.Fullscreen(position='topright',  # Full screen
    #         force_separate_button=True).add_to(map)
    # plugins.ScrollZoomToggler().add_to(map)
    maps=map._repr_html_()  #지도를 템플릿에 삽입하기위해 iframe이 있는 문자열로 반환
    
  
    return render(request, 'place/place_list.html', {'places':place_list, 'now':date, 
                                                         'star':star, 'category':category_id,
                                                         'categories':categories, 'local':loc_ls, 
                                                         'keyword':keyword, 'page_obj':page_obj,
                                                         'map':maps,})
