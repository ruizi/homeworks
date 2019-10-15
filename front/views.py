import datetime

import json
import random

from django.core.mail import send_mail
from django.shortcuts import render, render_to_response, redirect
import os

from front import models
from front.forms import *
from front import fogy_reduce_algorithm, SeamCarving, Sift, fliter, route, BP_Test

from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.
def show(request):
    if request.method == "GET":
        return render(request, 'index.html', locals())
    else:
        return render(request, 'show.html', locals())


def show_model(request):
    if request.method == "GET":
        return render(request, 'index0.html', locals())


def reduce_fogy(request):
    if request.method == "GET":
        image = ImageUploadForm()
        img_ob = models.UploadImages.objects.exclude(image_processed__contains="default").first() #越过数据库前几个不好的数据
        return render(request, "fogy.html", locals())
    else:
        image = ImageUploadForm(request.POST, request.FILES)
        PATH = os.getcwd()
        if image.is_valid():  # 获取数据
            img = image.cleaned_data['image']
            if img:
                ori_name = img.name.split('.')[0]
                ext_name = img.name.split('.')[-1]  # 得到格式
                today = datetime.date.today()  # 得到当天时间
                img.name = ori_name + '_' + str(today) + '.' + ext_name
                try:
                    print(img)
                    img_ob = models.UploadImages.objects.create()
                    img_ob.image = img
                    img_ob.save()
                    up_load_img = img_ob
                    fogy_reduced_picture = fogy_reduce_algorithm.start_to_calculate(up_load_img.image.path)
                    print(fogy_reduced_picture)
                    fogy_reduced_picture = fogy_reduced_picture.split('/media')[1]
                    img_ob.image_processed = fogy_reduced_picture
                    img_ob.save()
                    message = "finished"
                    return render(request, "fogy.html", locals())
                except:
                    message = "Upload_failed! Please try again!"
                    return render(request, "fogy.html", locals())
            else:
                message = "ImageField is None! try to use a default picture to calculator! if you want to try your own pictures,please use the filechooser to send a picture to the server!"
                # Define data path
                img_ob_ori = models.UploadImages.objects.first()
                temp_image = img_ob_ori.image
                #image = img_ob_ori.image.name.split("/")[1]
                data_path = PATH + '/media/' + img_ob_ori.image.name
                print(data_path)
                fogy_reduced_picture = fogy_reduce_algorithm.start_to_calculate(data_path)
                img_ob = models.UploadImages.objects.create()
                img_ob.image = temp_image
                img_ob.image_processed = fogy_reduced_picture.split('/media')[1]
                img_ob.save()
                image = ImageUploadForm()
                return render(request, "fogy.html", locals())


def seam_carving(request):
    if request.method == "GET":
        image = ImageUploadForm()
        img_ob = models.SeamCarvingPicture.objects.exclude(image_processed__contains="default").first()  # 越过数据库前几个不好的数据
        return render(request, "SeamCarving.html", locals())
    else:
        image = ImageUploadForm(request.POST, request.FILES)
        PATH = os.getcwd()
        t1 = request.POST.get("range", None)
        t1 = int(t1)
        print("t1:")
        print(t1)
        if image.is_valid():  # 获取数据
            img = image.cleaned_data['image']
            if img:
                ori_name = img.name.split('.')[0]
                ext_name = img.name.split('.')[-1]  # 得到格式
                today = datetime.date.today()  # 得到当天时间
                img.name = ori_name + '_' + str(today) + '.' + ext_name
                print(123525782)
                try:
                    print(img)
                    img_ob_after = models.SeamCarvingPicture.objects.create()
                    img_ob_after.image = img
                    img_ob_after.save()
                    up_load_img = img_ob_after
                    seam_carving_picture = SeamCarving.start_to_calculate(up_load_img.image.path, t1)
                    img_ob_after.image_processed = seam_carving_picture.split('/media')[1]

                    img_ob_after.save()
                    message = "finished"
                    image = ImageUploadForm()
                    return render(request, "SeamCarving.html", locals())
                except:
                    message = "Upload_failed! Please try again!"
                    return render(request, "SeamCarving.html", locals())
            else:
                message = "ImageField is None! try to use a default picture to calculator! if you want to try your own pictures,please use the filechooser to send a picture to the server!"
                # Define data path
                img_ob_ori = models.SeamCarvingPicture.objects.first()
                temp_image = img_ob_ori.image
                #image = img_ob_ori.image.name.split("/")[1]
                data_path = PATH + '/media/' + img_ob_ori.image.name
                print(data_path)
                seam_carving_picture = SeamCarving.start_to_calculate(data_path, t1)

                img_ob_after = models.SeamCarvingPicture.objects.create()
                img_ob_after.image = temp_image
                print(seam_carving_picture)
                img_ob_after.image_processed = seam_carving_picture.split('/media')[1]
                img_ob_after.save()
                image = ImageUploadForm()
                return render(request, "SeamCarving.html", locals())


def sift(request):
    if request.method == "GET":
        new_image = ImageUploadForm1()
        img_ob = models.sift.objects.first()
        return render(request, "sift.html", locals())
    else:
        new_images = ImageUploadForm1(request.POST, request.FILES)
        PATH = os.getcwd()
        if new_images.is_valid():  # 获取数据
            img1 = new_images.cleaned_data['image1']
            img2 = new_images.cleaned_data['image2']
            if img1 and img2:
                ori_name1 = img1.name.split('.')[0]
                ext_name1 = img1.name.split('.')[-1]  # 得到格式
                ori_name2 = img2.name.split('.')[0]
                ext_name2 = img2.name.split('.')[-1]  # 得到格式
                today = datetime.date.today()  # 得到当天时间
                img1.name = ori_name1 + '_' + str(today) + '.' + ext_name1
                img2.name = ori_name2 + '_' + str(today) + '.' + ext_name2
                try:
                    # print(img)
                    img_ob = models.sift.objects.create()
                    img_ob.image1 = img1
                    img_ob.image2 = img2
                    img_ob.save()
                    up_load_img = img_ob
                    sift_picture = Sift.start_to_calculate(img_ob.image1.path,
                                                           img_ob.image2.path)
                    img_ob.image_processed = sift_picture.split('/media')[1]
                    img_ob.save()
                    message = "finished"
                    new_image = ImageUploadForm1()
                    return render(request, "sift.html", locals())
                except:
                    message = "Upload_failed! Please try again!"
                    new_image = ImageUploadForm1()
                    return render(request, "sift.html", locals())
            else:
                message = "ImageField is None! try to use a default picture to calculator! if you want to try your own pictures,please use the filechooser to sent a picture to the server!"
                img_ob_after = models.sift.objects.first()
                image = ImageUploadForm1()
                return render(request, "sift.html", locals())


def flr_set(request):
    if request.method == "GET":
        new_image = ImageUploadForm()
        img_ob = models.flr_set.objects.first()
        return render(request, "fliter.html", locals())
    else:
        image = ImageUploadForm(request.POST, request.FILES)
        PATH = os.getcwd()
        if image.is_valid():  # 获取数据
            img = image.cleaned_data['image']
            if img:
                ori_name = img.name.split('.')[0]
                ext_name = img.name.split('.')[-1]  # 得到格式
                today = datetime.date.today()  # 得到当天时间
                img.name = ori_name + '_' + str(today) + '.' + ext_name
                try:
                    print(img)
                    img_ob = models.flr_set.objects.create()
                    img_ob.image = img
                    img_ob.save()
                    up_load_img = img_ob
                    # filter_picture = fliter.start_to_calculate(up_load_img.image.path, "Gus")
                    if "Gus" in request.POST:
                        print(up_load_img.image.path)
                        filter_picture = fliter.start_to_calculate(up_load_img.image.path, "Gus")
                    elif "avg" in request.POST:
                        filter_picture = fliter.start_to_calculate(up_load_img.image.path, "avg")
                    elif "rec" in request.POST:
                        filter_picture = fliter.start_to_calculate(up_load_img.image.path, "rec")
                    elif "rev" in request.POST:
                        filter_picture = fliter.start_to_calculate(up_load_img.image.path, "rev")
                    elif "rod" in request.POST:
                        filter_picture = fliter.start_to_calculate(up_load_img.image.path, "rod")
                    elif "add" in request.POST:
                        filter_picture = fliter.start_to_calculate(up_load_img.image.path, "add")
                    print(filter_picture)
                    # filter_picture = filter_picture.split('/media/')[1]
                    img_ob.image_processed = filter_picture.split('/media')[1]
                    img_ob.save()
                    new_image = ImageUploadForm()
                    message = "finished"
                    return render(request, "fliter.html", locals())
                except:
                    message = "Upload_failed! Please try again!"
                    return render(request, "fliter.html", locals())
            else:
                message = "ImageField is None! try to use a default picture to calculator! if you want to try your own pictures,please use the filechooser to sent a picture to the server!"
                # Define data path
                # data_path = PATH + '\media\image' + '\img1.jpg'
                # fogy_reduced_picture_path = fogy_reduce_algorithm.start_to_calculate(data_path)
                #
                # fogy_reduced_picture_path = fogy_reduced_picture_path.split('\\')[-2] + "\\" + \
                #                             fogy_reduced_picture_path.split('\\')[-1]
                return render(request, "fliter.html", locals())


def page_not_found(request):
    return render(request, '404.html')


def permission_denied(request):
    return render(request, '403.html')


def page_error(request):
    return render(request, '500.html')


def al_route(request):
    if request.method == "GET":
        return render(request, 'route.html', locals())
    else:
        point_number = request.POST.get("point_number", None)
        PATH = os.getcwd()
        try:
            img_ob = models.al_route.objects.create()
            img_ob.image = "image/test_board1.png"
            img_ob.save()
            up_load_img = img_ob
            x, img_path_out = route.add_point(up_load_img.image.path, point_number)
            print(123)
            print(img_path_out)
            img_path_out = img_path_out.split('\media\\')[1]
            print(img_path_out)
            img_ob.image_add_points = img_path_out
            img_ob.save()
            message = "finished"
            request.session['points_loc'] = x
            request.session['picture_id'] = img_ob.id
            return render(request, 'route_algorithms.html', locals())
        except:
            message = "Upload_failed! Please try again!"
            return render(request, "route_algorithms.html", locals())


def al_route_alo(request):
    if request.method == "GET":
        return redirect('front:route')
    # else:
    #     points_loc = request.session.get('points_loc', False)
    #     picture_id = request.session.get('picture_id', False)
    #     try:
    #         img_ob = models.al_route.get(id=picture_id)
    #     except:
    #         message = "Failed"
    #     print(points_loc)
    #     up_load_img = img_ob
    #     img_path_out = route.add_point(up_load_img.image.path, points_loc)
    #     return render(request, 'route_algorithms.html', locals())


def BP(request):
    if request.method == "GET":
        return render(request, 'BP.html', locals())
    else:
        function = request.POST.get("function", None)
        loss = request.POST.get("loss", None)
        h_l_c = request.POST.get("h_l_c", None)
        h_l_n = request.POST.get("h_l_n", None)
        l_r = request.POST.get("l_r", None)
        PATH = os.getcwd()
        try:
            print(loss)
            print(h_l_c)
            print(h_l_n)
            print(l_r)
            input_data, out_list, ideal_output, time, step_arr, loss_arr, test_input_data, test_ideal_output, forword_out_list_test = BP_Test.start_to_calculate(
                h_l_c, h_l_n, 100,
                100,
                l_r, function,
                loss)
            print(step_arr)
            print(loss_arr)
            return render(request, "BP.html", locals())
        except:
            message = "Failed! Please try again!"
            return render(request, "BP.html", locals())


def android_pay(request):
    if request.method == 'POST':
        item_spend = request.POST.get('item_spend')
        id = request.POST.get('id')
        money = request.POST.get('money')
        year = request.POST.get('year')
        month = request.POST.get('month')
        day = request.POST.get('day')
        isPri = request.POST.get('isPri')
        fun = request.POST.get('fun')
        if fun == '1':
            models.Pay.objects.create(id=id, item_spend=item_spend, money=money, year=year, month=month, day=day,
                                      isPri=isPri)
            try:
                t = models.Pay.objects.get(id=id)
                return HttpResponse("add_ok")
            except ObjectDoesNotExist:
                return HttpResponse("add_error")
        elif fun == '2':
            try:
                temp = models.Pay.objects.get(id=id)
                temp.delete()
                return HttpResponse("delete_ok")
            except ObjectDoesNotExist:
                return HttpResponse("not_found")
    else:
        # 如果是get形式返回所有当前记录数据，完成信息同步
        try:
            items = models.Pay.objects.all()
            list = []
            i = 1
            for item in items:
                data = {}
                data['id'] = i
                data['item_spend'] = item.item_spend
                data['money'] = item.money
                data['year'] = item.year
                data['month'] = item.month
                data['day'] = item.day
                data['isPri'] = item.isPri
                list.append(data)
                i += 1
            print(list)
            response = json.dumps(list, ensure_ascii=False)
            print(response)
            return HttpResponse(response)
        except:
            return HttpResponse("error")


def add_pay_web(request):
    if request.method == "GET":
        new_pay = AddPayForm()
        print(123)
        return render(request, 'add_pay_web.html', locals())
    else:
        item_spend = request.POST.get("item", None)
        money = request.POST.get("cost", None)
        date = request.POST.get("date", None)
        isPri = request.POST.get("isPri", None)
        print(date)
        print(isPri)
        year = int(date.split('-')[0])  # 得到格式
        month = int(date.split('-')[1])  # 得到格式
        day = int(date.split('-')[2])  # 得到格式
        print(year)
        print(month)
        print(day)

        # models.Pay.objects.create(id=id, item_spend=item_spend, money=money, year=year, month=month, day=day,
        #                           isPri=isPri)
        # try:
        #     t = models.Pay.objects.get(id=id)
        #     return HttpResponse("add_ok")
        # except ObjectDoesNotExist:
        #     return HttpResponse("add_error")
        return render(request, 'add_pay_web.html', locals())


def show_pay_web(request):
    if request.method == "GET":
        print(123)
        # 如果是get形式返回所有当前记录数据，完成信息同步
        try:
            items = models.Pay.objects.all()
            print(123)
            list = []
            i = 1
            for item in items:
                data = {}
                data['id'] = i
                data['item_spend'] = item.item_spend
                data['money'] = item.money
                data['year'] = item.year
                data['month'] = item.month
                data['day'] = item.day
                data['isPri'] = item.isPri
                list.append(data)
                i += 1
            print(list)
            response = json.dumps(list, ensure_ascii=False)
            print(response)
            return HttpResponse(response)
        except:
            return HttpResponse('error')


def android_login_api(request):
    if request.method == 'POST':
        email = request.POST.get("email", None)
        password = request.POST.get("password", None)

        print(email)
        print(password)
        try:
            user = models.User.objects.get(Email=email, Password=password)
            list = []
            data = {}
            data['name'] = user.Name
            data['email'] = user.Email
            data['password'] = user.Password
            list.append(data)
            response = json.dumps(list, ensure_ascii=False)
            return HttpResponse(response)
        except ObjectDoesNotExist:
            return HttpResponse("Error")


def android_register_api(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        name = request.POST.get('name')
        password = request.POST.get('password')
        try:
            models.User.objects.create(Email=email, Name=name, Password=password)
            return HttpResponse("OK")
        except ObjectDoesNotExist:
            return HttpResponse("Error")


def android_get_password_back(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        # 值1：  邮件标题   值2： 邮件主体
        # 值3： 发件人      值4： 收件人
        emaillist= [email]
        code = random.randint(1000, 9999)
        text = "您的验证码为：" + str(code)
        res = send_mail('验证码',
                        text,
                        'buct_dongwu@163.com',
                        emaillist)
        if res == 1:
            return HttpResponse(code)
        else:
            return HttpResponse('Error')


def android_get_password_back_db_operation(request):
    if request.method == "POST":
        email = request.POST.get('email')
        newpassword = request.POST.get('newpassword')
        try:
            user = models.User.objects.get(Email=email)
            user.Password = newpassword
            user.save()
            return HttpResponse("OK")
        except ObjectDoesNotExist:
            return HttpResponse("Error")
