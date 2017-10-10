#!/usr/bin/python
from django.shortcuts import render_to_response,render,Http404,HttpResponse,redirect
from django.http import HttpResponseRedirect
from django.template import RequestContext
from Graduation.forms import *
import psycopg2
from itertools import chain
import operator
import json
from Graduation.models import *
import time
from math import *
import threading
from recommendations import *
from socket import gethostname, gethostbyname



from django.views.decorators.csrf import csrf_exempt
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from threading import Timer


from django.core.files import File
import os
from django.conf import settings
from settings import IMAGES_FOLDER





def search(request):
    test=[1,2,3,3]
    s1=recent_posts()
    s2=recent_images()
    Images=[]

    s=json.dumps(test)
    all_data=[]

    query_id=[]
    append_result=[]
    count = {}





    ##get the recommenation
    key = []
    conn = psycopg2.connect(database="market", user="abdullah", password="mypass", host="127.0.0.1",
                            port="5432")
    cur=conn.cursor()
    cur2 = conn.cursor()
    cur2.execute("""SELECT *  from  "Graduation_recommendationtraining" ;""")
    data = cur2.fetchall()
    SimilarItems={}

    for i in data:
        key.append(i[1])

    for j in key:
        temp = []

        for i in data:

            if i[1] == j:
                temp.append((i[2], i[3]))

        SimilarItems[j] = temp
    cur3 = conn.cursor()
    cur3.execute("""SELECT *  from  "Graduation_recommenationdatas" ;""" )
    data=cur3.fetchall()
    data_recommend = [list(element) for element in data]
    transformed_data = {}
    for i in range(len(data_recommend)):
        transformed_data.setdefault(data_recommend[i][1], {})
        transformed_data[data_recommend[i][1]][data_recommend[i][2]] = data_recommend[i][3]

    recommended_stuffs = getRecommendedItems(transformed_data, SimilarItems, u'04/05/2017')
    print recommended_stuffs
    final_data=[]
    for id_ in range(len(recommended_stuffs)):
        cur.execute("""SELECT *  from  "Graduation_iteminformation"  WHERE  "id"='%s';""" % (recommended_stuffs[id_][1]))
        final_data.append(cur.fetchall())
    show=[list(i) for elem in final_data for i in elem]
    image=[]
    for id_ in range(len(recommended_stuffs)):
        cur.execute(
            """SELECT *  from  "Graduation_uploadimages" WHERE  "id"='%s';""" % (recommended_stuffs[id_][1]))
        image.append(cur.fetchall())
    image =[list(i) for elem in image for i in elem]
    convert_image = json.dumps(image)
    convert_data=json.dumps(show)
    ##############################
    conn = psycopg2.connect(database="market", user="abdullah", password="mypass", host="127.0.0.1", port="5432")
    cur = conn.cursor()

    if request.method == 'POST':
        form = search_text(request.POST)
        if form.is_valid():
            get_text= form.cleaned_data["search"]
            inserts=get_text.split(' ')
            for i in range(len(inserts)):

                keys=str(inserts[i]).lower().replace(',', '')



                cur.execute("SELECT id,SUM(frequency)  from  TF_IDF WHERE word::tsquery  = (SELECT to_tsquery ('%s')) GROUP BY id;"%(keys))


                rows = cur.fetchall()
                query_id.append(rows)
            queries=list(chain.from_iterable(query_id))

            for k, v in queries:
                if k in count:
                    count[k] += v
                else:
                    count[k] = v
            sorted_x = list(reversed(sorted(count.items(), key=operator.itemgetter(1))))
            if sorted_x:
                for j in range(len(sorted_x)):
                    pass_id=sorted_x[j][0]
                    cur.execute("""SELECT *  from  "Graduation_iteminformation" WHERE id='%s';"""%(pass_id))
                    result = cur.fetchall()
                    append_result.append(result)
                for i in append_result:
                        all_data.append(list(chain.from_iterable(i)))
                convert=json.dumps(all_data)
                # print convert
                for i in range(len(all_data)):

                    cur.execute("""SELECT *  from  "Graduation_uploadimages" WHERE id='%s';""" % (all_data[i][9]))
                    Images.append(cur.fetchall())
                ItemImages = [list(i) for elem in Images for i in elem]
                ImagesConveted=json.dumps(ItemImages)



                return render(request, "bootstrap-shop/products.html", {"convert": convert,'ImagesConveted':ImagesConveted})
            else:

                return HttpResponse("No result found")















    else:
            form=search_text()
    return render_to_response('bootstrap-shop/index_test.html',{'form':form,"convert_image":convert_image,"convert_data":convert_data,"s1":s1,"s2":s2},context_instance=RequestContext(request))

# def list_product(request):
#     return  render_to_response('list_products.html',context_instance=RequestContext(request))
#
# def select(request):
#     # if request.user.is_authenticated():
#     form1 = Radio_select(request.POST)
#     Post_item_Detalis = Post_item(request.POST)
#     # form3=Post_item1(request.POST)
#     formMainImage=MainImage(request.POST or None, request.FILES or None)
#     formSecondImage=secondImage(request.POST or None, request.FILES or None)
#     formThirdImage=thirdImage(request.POST or None, request.FILES or None)
#     Status_Detalis=Status(request.POST)
#     ItemSub=Post_item1(request.POST)
#     search_ = search_text(request.POST)
#
#
#     if request.method == 'POST':
#
#
#             # if form1.is_valid():
#             #     get_select = form1.cleaned_data["select"]
#             #     if get_select=='select1':
#             #         return redirect('/Post-job/')
#             #     else:
#             #         return redirect('/Post-item/')
#             # if form2.is_valid():
#             #
#             #     if form3.is_valid():
#             #         IType2 = form3.cleaned_data["ItemSubType"]
#             #         print IType2
#
#             if formMainImage.is_valid():
#                 mainImages1 = request.FILES['Image1']
#                 saveImage=uploadImagess()
#                 saveImage.Image1=mainImages1
#                 if formSecondImage.is_valid():
#                     mainImages2 = request.FILES['Image2']
#                     saveImage.Image2 = mainImages2
#                 else:
#                     saveImage.Image2='static/Images/NoPhoto.png'
#                 if formThirdImage.is_valid():
#                     mainImages3 = request.FILES['Image3']
#                     saveImage.Image3 = mainImages3
#                 else:
#                     saveImage.Image3='static/Images/NoPhoto.png'
#                 saveImage.save()
#
#
#
#
#             else:
#                 saveImage=uploadImagess()
#
#                 saveImage.Image1='static/Images/NoPhoto.png'
#                 saveImage.Image2='static/Images/NoPhoto.png'
#                 saveImage.Image3='static/Images/NoPhoto.png'
#                 saveImage.save()
#             if Post_item_Detalis.is_valid():
#                 itemtype=Post_item_Detalis.cleaned_data['ItemType']
#                 if Status_Detalis.is_valid():
#                     itemStatuse=Status_Detalis.cleaned_data['ItemStatus']
#                     if ItemSub.is_valid():
#                             getsub=ItemSub.cleaned_data['ItemSubType']
#                             valueOfSub=dict(ItemSub.fields['ItemSubType'].choices)[getsub]
#
#                             ItemInformation(ItemTitle=Post_item_Detalis.cleaned_data['ItemName'],
#                                 Price=Post_item_Detalis.cleaned_data['ItemPrice'],
#                                 Description=Post_item_Detalis.cleaned_data['ItemDescrption'],
#                                 Status=dict(Status_Detalis.fields['ItemStatus'].choices)[itemStatuse],
#
#
#                                 type=dict(Post_item_Detalis.fields['ItemType'].choices)[itemtype],
#                                 subType=valueOfSub,
#                                 username=request.user.get_full_name(),
#                                 Date=time.strftime("%d/%m/%Y"),
#                                 ImageID=ItemInformation.objects.filter().count()+1
#
#                                 ).save()
#                             tf_idf(Post_item_Detalis.cleaned_data['ItemName'],Post_item_Detalis.cleaned_data['ItemDescrption'])
#                             return HttpResponse('HI')
#
#
#
#
#
#
#
#
#
#     else:
#         form1=Radio_select()
#         Post_item_Detalis=Post_item()
#         ItemSub=Post_item1()
#         Status_Detalis=Status()
#         formMainImage = MainImage()
#         formSecondImage = secondImage()
#         formThirdImage = thirdImage()
#     return render_to_response('bootstrap-shop/register.html',{'form1':form1,'Post_item_Detalis':Post_item_Detalis,'ItemSub':ItemSub,
#                                                               'formMainImage':formMainImage,'formSecondImage':formSecondImage,'formThirdImage':formThirdImage,'Status_Detalis':Status_Detalis},context_instance=RequestContext(request))
#     #else:
#         #return HttpResponse('You have you login with sehir mail in order to post an item')
#


def select(request):
    # if request.user.is_authenticated():
    form1 = Radio_select(request.POST)
    Post_item_Detalis = Post_item(request.POST)
    # form3=Post_item1(request.POST)
    formMainImage=MainImage(request.POST or None, request.FILES or None)
    formSecondImage=secondImage(request.POST or None, request.FILES or None)
    formThirdImage=thirdImage(request.POST or None, request.FILES or None)
    Status_Detalis=Status(request.POST)
    ItemSub=Post_item1(request.POST)


    if request.method == 'POST':

            # # if form1.is_valid():
            # #     get_select = form1.cleaned_data["select"]
            # #     if get_select=='select1':
            # #         return redirect('/Post-job/')
            # #     else:
            # #         return redirect('/Post-item/')
            # # if form2.is_valid():
            # #
            # #     if form3.is_valid():
            # #         IType2 = form3.cleaned_data["ItemSubType"]
            # #         print IType2
            #
            if formMainImage.is_valid():
                mainImages1 = request.FILES['Image1']
                saveImage=uploadImages()
                saveImage.Image1=mainImages1
                if formSecondImage.is_valid():
                    mainImages2 = request.FILES['Image2']
                    saveImage.Image2 = mainImages2
                else:
                    saveImage.Image2='static/Images/NoPhoto.png'
                if formThirdImage.is_valid():
                    mainImages3 = request.FILES['Image3']
                    saveImage.Image3 = mainImages3
                else:
                    saveImage.Image3='static/Images/NoPhoto.png'
                saveImage.save()




            else:
                saveImage=uploadImages()

                saveImage.Image1='static/Images/NoPhoto.png'
                saveImage.Image2='static/Images/NoPhoto.png'
                saveImage.Image3='static/Images/NoPhoto.png'
                saveImage.save()
            if Post_item_Detalis.is_valid():
                print 'done'

                itemtype=Post_item_Detalis.cleaned_data['ItemType']
                if Status_Detalis.is_valid():
                    print "ok"
                    itemStatuse=Status_Detalis.cleaned_data['ItemStatus']
                    if ItemSub.is_valid():
                            print "fine"
                            getsub=ItemSub.cleaned_data['ItemSubType']
                            valueOfSub=dict(ItemSub.fields['ItemSubType'].choices)[getsub]

                            ItemInformation(ItemTitle=Post_item_Detalis.cleaned_data['ItemName'],
                                Price=Post_item_Detalis.cleaned_data['ItemPrice'],
                                Description=Post_item_Detalis.cleaned_data['ItemDescrption'],
                                Status=dict(Status_Detalis.fields['ItemStatus'].choices)[itemStatuse],


                                type=dict(Post_item_Detalis.fields['ItemType'].choices)[itemtype],
                                subType=valueOfSub,
                                username=request.user.get_full_name(),
                                Date=time.strftime("%d/%m/%Y"),
                                ImageID=ItemInformation.objects.filter().count()+1

                                ).save()
                            tf_idf(Post_item_Detalis.cleaned_data['ItemName'],Post_item_Detalis.cleaned_data['ItemDescrption'])




            return redirect('http://127.0.0.1:8000/select-item/')


    else:
            form1=Radio_select()
            Post_item_Detalis=Post_item()
            ItemSub=Post_item1()
            Status_Detalis=Status()
            formMainImage = MainImage()
            formSecondImage = secondImage()
            formThirdImage = thirdImage()
    return render_to_response('bootstrap-shop/register.html',{'form1':form1,'Post_item_Detalis':Post_item_Detalis,'ItemSub':ItemSub,
                                                              'formMainImage':formMainImage,'formSecondImage':formSecondImage,'formThirdImage':formThirdImage,'Status_Detalis':Status_Detalis},context_instance=RequestContext(request))
    #else:
        #return HttpResponse('You have you login with sehir mail in order to post an item')



def myProduct(request):
     result2=[]

     if request.user.is_authenticated():
         # username=request.user.username
         username=request.user.get_full_name()

         conn = psycopg2.connect(database="market", user="abdullah", password="mypass", host="127.0.0.1", port="5432")
         cur = conn.cursor()
         cur.execute("""SELECT *  from  "Graduation_iteminformation" WHERE username='%s';""" % (username))

         result = cur.fetchall()
         for i in range(len(result)):
             if result:
                  cur.execute("""SELECT *  from  "Graduation_uploadimages" WHERE id='%s';""" % (result[i][9]))

                  result2.append(cur.fetchall())
         ItemInformationList=[list(elem) for elem in result]
         ItemImages = [list(i) for elem in result2 for i in elem]
         item1=json.dumps(ItemInformationList)
         item2=json.dumps(ItemImages)

         # print item1
         # print item2




         return render_to_response('bootstrap-shop/my-products.html',{'item1':item1,'item2':item2},context_instance=RequestContext(request))



@csrf_exempt

def productsDetalis(request,userId):



    result2=[]
    conn = psycopg2.connect(database="market", user="abdullah", password="mypass", host="127.0.0.1", port="5432")
    cur = conn.cursor()
    cur.execute("""SELECT *  from  "Graduation_iteminformation" WHERE id='%s';""" % (userId))

    result = cur.fetchall()
    for i in range(len(result)):
        if result:
            cur.execute("""SELECT *  from  "Graduation_uploadimages" WHERE id='%s';""" % (result[i][9]))

            result2.append(cur.fetchall())
    ItemInformationList = [list(elem) for elem in result]
    ItemImages = [list(i) for elem in result2 for i in elem]
    itemInformation = json.dumps(ItemInformationList)
    itemImage = json.dumps(ItemImages)
    #call the function recommenation
    if request.user.is_authenticated():
        username=request.user.get_full_name()

        RecommendtionData(username,userId)
    else:
        ip = gethostbyname(gethostname())
        username=ip+' '+time.strftime("%d/%m/%Y")
        RecommendtionData(username, userId)






    #get the receiver name
    cur1 = conn.cursor()
    cur1.execute("""SELECT "username"  from  "Graduation_iteminformation" WHERE id='%s';""" % (userId))
    receiver_name=cur1.fetchall()
    receiverName=receiver_name[0][0].split()




    #get the receriver email
    cur2 = conn.cursor()
    cur2.execute("""SELECT email  from  "auth_user" WHERE first_name='%s' and last_name='%s';""" % (receiverName[0],receiverName[1]))
    receiverEmail=cur2.fetchall()






    # print current_url


    if request.method == 'POST':
        form1 = sendmessage(request.POST)
        if form1.is_valid():
            message = form1.cleaned_data['sendMessage'].encode('utf-8')
            contacts(senderName=request.user.get_full_name(),receiverName=receiver_name[0][0],senderMail=request.user.email,
            receiverMail=receiverEmail[0][0],productID=userId,date=time.strftime("%d/%m/%Y"),time=time.strftime("%H:%M:%S"),message=message,
                     messageStatus='False').save()


    else:
        form1=sendmessage()
    return render_to_response('bootstrap-shop/testProduct.html',{'itemInformation':itemInformation,'itemImage':itemImage,'form1':form1},context_instance=RequestContext(request))










def tf_idf(title,descrption):
    data={}
    data[ItemInformation.objects.filter().count()]=title+''+descrption
    dataset={}

    inser={}




    for doc in sorted(data):
        list_of = []
        splitdoc = data[doc].lower().split()
        inser[doc]=splitdoc
        for term in inser[doc]:




                        frq=inser[doc].count(term.lower()) / float(len(inser[doc]))
                        list_of.append((term,frq))

                        dataset[doc]=list_of

    length = len(dataset.values()[0])




    test=[]
    conn = psycopg2.connect(database="market", user="abdullah", password="mypass", host="127.0.0.1", port="5432")
    cur = conn.cursor()
    for i in range(length):

        cur.execute("""SELECT COUNT (id) from "Graduation_iteminformation" WHERE "ItemTitle" LIKE '%%%s%%' or "Description" LIKE '%%%s%%';"""%(dataset.values()[0][i][0],dataset.values()[0][i][0]))
        rows = cur.fetchall()
        test.append(rows)
        if test[i][0][0]!=0:

            idf = 1.0 + log(float(ItemInformation.objects.filter().count()) /test[i][0][0])
            frq=idf*float(dataset.values()[0][i][1])
        else:
            frq = 1.0 * float(dataset.values()[0][i][1])
        query = "INSERT INTO TF_IDF (id, word, frequency) VALUES (%s, %s, %s);"
        data = (ItemInformation.objects.filter().count(),dataset.values()[0][i][0] , frq)
        cur.execute(query, data)

        conn.commit()
def update(request,id):
    conn = psycopg2.connect(database="market", user="abdullah", password="mypass", host="127.0.0.1", port="5432")
    cur = conn.cursor()
    cur1=conn.cursor()
    cur.execute("""SELECT *  from  "Graduation_iteminformation" WHERE id='%s';""" % (id))
    result = [list(element) for element in cur.fetchall()]
    cur1.execute("""SELECT *  from  "Graduation_uploadimages" WHERE id='%s';""" % (result[0][9]))
    Images=[list(element) for element in cur1.fetchall()]
    updateItem = json.dumps(result)
    updateImages=json.dumps(Images)
    # print updateItem
    # print updateImages



    # if request.user.is_authenticated():
    DeleteImages1=DeleteImage1(request.POST)
    DeleteImages2=DeleteImage2(request.POST)
    DeleteImages3=DeleteImage3(request.POST)


    form1 = Radio_select(request.POST)
    Post_item_Detalis = Post_item(request.POST)
    # form3=Post_item1(request.POST)
    formMainImage = MainImage(request.POST or None, request.FILES or None)
    formSecondImage = secondImage(request.POST or None, request.FILES or None)
    formThirdImage = thirdImage(request.POST or None, request.FILES or None)
    Status_Detalis = Status(request.POST)
    ItemSub = Post_item1(request.POST)

    if request.method == 'POST':
        if Post_item_Detalis.is_valid():
            itemtype = Post_item_Detalis.cleaned_data['ItemType']
            if Status_Detalis.is_valid():
                itemStatuse = Status_Detalis.cleaned_data['ItemStatus']
                if ItemSub.is_valid():
                    getsub = ItemSub.cleaned_data['ItemSubType']
                    valueOfSub = dict(ItemSub.fields['ItemSubType'].choices)[getsub]


                    updateItemInformation= ItemInformation.objects.get(id=id)
                    updateItemInformation.ItemTitle=Post_item_Detalis.cleaned_data['ItemName']
                    updateItemInformation.Price=Post_item_Detalis.cleaned_data['ItemPrice']
                    updateItemInformation.Description=Post_item_Detalis.cleaned_data['ItemDescrption']
                    updateItemInformation.Status=dict(Status_Detalis.fields['ItemStatus'].choices)[itemStatuse]
                    updateItemInformation.type=dict(Post_item_Detalis.fields['ItemType'].choices)[itemtype]

                    updateItemInformation.subType=valueOfSub

                    updateItemInformation.save()
            updateItemImages = uploadImages.objects.get(id=id)
            if formMainImage.is_valid():

                if DeleteImages1.is_valid():
                    updateItemImages.Image1=request.FILES['Image1']
                else:
                    updateItemImages.Image1 = request.FILES['Image1']

            else:
                if DeleteImages1.is_valid():
                    updateItemImages.Image1='static/Images/NoPhoto.png'
                else:
                    "don't do any thing"

            if formSecondImage.is_valid():

                        if DeleteImages2.is_valid():
                            updateItemImages.Image2 = request.FILES['Image2']
                        else:
                            updateItemImages.Image2= request.FILES['Image2']

            else:
                        if DeleteImages2.is_valid():
                            updateItemImages.Image2 = 'static/Images/NoPhoto.png'
                        else:
                            "don't do any thing"

            if formSecondImage.is_valid():

                    if DeleteImages3.is_valid():
                                    updateItemImages.Image3 = request.FILES['Image3']
                    else:
                                    updateItemImages.Image3 = request.FILES['Image3']

            else:
                                if DeleteImages3.is_valid():
                                    updateItemImages.Image3 = 'static/Images/NoPhoto.png'
                                else:
                                    "don't do any thing"

            updateItemImages.save()




            return HttpResponse('DONE')



    else:




        return render_to_response('bootstrap-shop/update-item.html',{'updateItem':updateItem,'updateImages':updateImages},context_instance=RequestContext(request))





def test1(request):
    DeleteImage=DeleteImage1(request.POST)
    return render_to_response('search_results.html',{'DeleteImage':DeleteImage})


#Anas   part






@csrf_exempt
def inbox(request):
    ListItems = []
    # messList=[[['Anas Abdrabbuh','13:15','Iphone6s'],['hi','merhaba','anas','call me','go go']]]
    conn = psycopg2.connect(database="market", user="abdullah", password="mypass", host="127.0.0.1", port="5432")
    cur = conn.cursor()
    username=request.user.get_full_name()
    cur.execute("""SELECT "senderName","receiverName","productID" from "Graduation_contacts" WHERE "receiverName" LIKE '%%%s%%' or "senderName" LIKE  '%%%s%%'
                    GROUP By "senderName","receiverName","productID"; """% (username,username))
    ListItem=cur.fetchall()

    allItems=[list(element) for element in ListItem]

    # print allItems
    type_of_=[]
    for type_ in  range(len(allItems)):
        cur.execute("""SELECT "ItemTitle" from "Graduation_iteminformation" WHERE "id" = '%s' ;""" % (allItems[type_][2]))
        type_of_.append(cur.fetchall())
    type_of_=json.dumps(type_of_)
    print type_of_
    test=[]

    for i in range(len(allItems)):
        # print allItems[i][1]
        cur.execute("""SELECT "date","time","message" from "Graduation_contacts" WHERE "senderName" LIKE '%s' and  "receiverName"  LIKE  '%s' and "productID" = CAST(%d AS INT)
                           ;"""%(allItems[i][0],allItems[i][1],int(allItems[i][2])))
        test.append(cur.fetchall())


    messages=[]
    for i in range(len(test)):
        tempo = []
        for j in range(len(test[i])):
            tempo1=[]
            tempo1.append(test[i][j][0])
            tempo1.append( test[i][j][1])
            tempo1.append(test[i][j][2])
            tempo.append(tempo1)
        messages.append(tempo)



    messages0=json.dumps(messages)
    allItems0=json.dumps(allItems)
    # return render_to_response('inbox.html',{'allItems0':allItems0,'messages0':messages0}, RequestContext(request))
    return render_to_response('bootstrap-shop/inbox_.html',{'allItems0':allItems0,'messages0':messages0,"type_of_":type_of_},context_instance=RequestContext(request))




def mail(message,sender,receiver,product,receiverMail):

        subject = 'Unread Message'
        text = ""
        html = """\
                           <html>
                               <head></head>
                               <body>
                               <p>Dear <b>{receiver},</b><br>
                                   <br>You have an unread message about <b>{product}</b> from <b>{sender}.</b><br>
                                    <br><b>" {message} "</b><br>
                                    <br>To reply please click <a href="http://127.0.0.1:8000/products/user/{product}">here</a>,<br>
                                    <br>Sincerely,<br>
                                    <br>SEHIR Online Market<br>
                                </p>
                                </body>
                            </html>
                           """.format(**locals())

        sender = "sehiruniversityonlinemarket@gmail.com"

        receiver = receiverMail
        msg = MIMEMultipart('alternative')

        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = receiver

        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')

        msg.attach(part1)
        msg.attach(part2)

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender, "AnasAbdullah")  # here we should enter the password of mail
        text = msg.as_string()
        server.sendmail(sender, receiver, text)
        server.quit()

def sendMessage():
    print ''
    threading.Timer(10, sendMessage).start()

    conn = psycopg2.connect(database="market", user="abdullah", password="mypass", host="127.0.0.1", port="5432")
    cur3 = conn.cursor()
    cur3.execute("""SELECT *  from  "Graduation_contacts" WHERE "messageStatus"='False';""")

    ContactInfo = [list(element) for element in cur3.fetchall()]


    for i in range(len(ContactInfo)):
        mail(ContactInfo[i][8],ContactInfo[i][1],ContactInfo[i][2],ContactInfo[i][5],ContactInfo[i][4])
        chnage_statment = contacts.objects.get(id=ContactInfo[i][0])
        chnage_statment.messageStatus='True'
        chnage_statment.save()



sendMessage()
# def inbox(request):
#     return render_to_response('bootstrap-shop/inbox.html',context_instance=RequestContext(request))

def filteringCamera(request):
    ImagesInfo=[]
    conn = psycopg2.connect(database="market", user="abdullah", password="mypass", host="127.0.0.1", port="5432")
    cur = conn.cursor()
    cur1=conn.cursor()


    cur.execute("""SELECT *  from  "Graduation_iteminformation" WHERE "subType"='Camera';""" )
    CameraInfo=[list(element) for element in cur.fetchall()]
    for i in range  (len(CameraInfo)):
        cur1.execute("""SELECT *  from  "Graduation_uploadimages" WHERE id='%s';""" % (CameraInfo[i][9]))
        ImagesInfo.append(cur1.fetchall())
    CameraImages=[list(i) for elem in ImagesInfo for i in elem]

    # print CameraImages
    convert = json.dumps(CameraInfo)
    ImagesConveted = json.dumps(CameraImages)


    return render_to_response('bootstrap-shop/products.html',{'convert':convert,'ImagesConveted':ImagesConveted},context_instance=RequestContext(request))
def filteringele(request):
    ImagesInfo=[]
    conn = psycopg2.connect(database="market", user="abdullah", password="mypass", host="127.0.0.1", port="5432")
    cur = conn.cursor()
    cur1=conn.cursor()


    cur.execute("""SELECT *  from  "Graduation_iteminformation" WHERE "type"='Electronic Devices';""" )
    CameraInfo=[list(element) for element in cur.fetchall()]
    for i in range  (len(CameraInfo)):
        cur1.execute("""SELECT *  from  "Graduation_uploadimages" WHERE id='%s';""" % (CameraInfo[i][9]))
        ImagesInfo.append(cur1.fetchall())
    CameraImages=[list(i) for elem in ImagesInfo for i in elem]

    # print CameraImages
    convert = json.dumps(CameraInfo)
    ImagesConveted = json.dumps(CameraImages)


    return render_to_response('bootstrap-shop/products.html',{'convert':convert,'ImagesConveted':ImagesConveted},context_instance=RequestContext(request))
def filterinAccessories(request):
    ImagesInfo=[]
    conn = psycopg2.connect(database="market", user="abdullah", password="mypass", host="127.0.0.1", port="5432")
    cur = conn.cursor()
    cur1=conn.cursor()


    cur.execute("""SELECT *  from  "Graduation_iteminformation" WHERE "subType"='Accessories';""" )
    CameraInfo=[list(element) for element in cur.fetchall()]
    for i in range  (len(CameraInfo)):
        cur1.execute("""SELECT *  from  "Graduation_uploadimages" WHERE id='%s';""" % (CameraInfo[i][9]))
        ImagesInfo.append(cur1.fetchall())
    CameraImages=[list(i) for elem in ImagesInfo for i in elem]

    # print CameraImages
    convert = json.dumps(CameraInfo)
    ImagesConveted = json.dumps(CameraImages)


    return render_to_response('bootstrap-shop/products.html',{'convert':convert,'ImagesConveted':ImagesConveted},context_instance=RequestContext(request))
def filterinbooks(request):
    ImagesInfo=[]
    conn = psycopg2.connect(database="market", user="abdullah", password="mypass", host="127.0.0.1", port="5432")
    cur = conn.cursor()
    cur1=conn.cursor()


    cur.execute("""SELECT *  from  "Graduation_iteminformation" WHERE "type"='Books';""" )
    CameraInfo=[list(element) for element in cur.fetchall()]
    for i in range  (len(CameraInfo)):
        cur1.execute("""SELECT *  from  "Graduation_uploadimages" WHERE id='%s';""" % (CameraInfo[i][9]))
        ImagesInfo.append(cur1.fetchall())
    CameraImages=[list(i) for elem in ImagesInfo for i in elem]

    # print CameraImages
    convert = json.dumps(CameraInfo)
    ImagesConveted = json.dumps(CameraImages)


    return render_to_response('bootstrap-shop/products.html',{'convert':convert,'ImagesConveted':ImagesConveted},context_instance=RequestContext(request))

def filterinscholarship(request):
    ImagesInfo=[]
    conn = psycopg2.connect(database="market", user="abdullah", password="mypass", host="127.0.0.1", port="5432")
    cur = conn.cursor()
    cur1=conn.cursor()


    cur.execute("""SELECT *  from  "Graduation_iteminformation" WHERE "type"='Scholarship';""" )
    CameraInfo=[list(element) for element in cur.fetchall()]
    for i in range  (len(CameraInfo)):
        cur1.execute("""SELECT *  from  "Graduation_uploadimages" WHERE id='%s';""" % (CameraInfo[i][9]))
        ImagesInfo.append(cur1.fetchall())
    CameraImages=[list(i) for elem in ImagesInfo for i in elem]

    # print CameraImages
    convert = json.dumps(CameraInfo)
    ImagesConveted = json.dumps(CameraImages)


    return render_to_response('bootstrap-shop/products.html',{'convert':convert,'ImagesConveted':ImagesConveted},context_instance=RequestContext(request))



def RecommendtionData(username,id):

    conn = psycopg2.connect(database="market", user="abdullah", password="mypass", host="127.0.0.1", port="5432")
    cur = conn.cursor()
    cur.execute("""SELECT *  from  "Graduation_recommenationdatas" WHERE "username"='%s' and  "productId"='%s';""" % (username,id))
    s=cur.fetchall()

    if not s:
        recommenationDatas(username=username,productId=id,visitedTime=1).save()
        print 'don'
    else:
        updateVisited=recommenationDatas.objects.get(id=s[0][0])
        updateVisited.visitedTime=s[0][3]+1
        updateVisited.save()
    cur2 = conn.cursor()
    data_dic={}
    cur2.execute("""SELECT *  from  "Graduation_recommenationdatas" ;""" )
    data=cur2.fetchall()
    data_recommend = [list(element) for element in data]
    # for i in range(len(data_recommend)):
        # data_dic[data_recommend[i][1]]={data_recommend[i][2]:data_recommend[i][3]}
    s = {}
    for i in range(len(data_recommend)):
        s.setdefault(data_recommend[i][1], {})
        s[data_recommend[i][1]][data_recommend[i][2]] = data_recommend[i][3]
    x = calculateSimilarItems(s, 2)
    print x

    # recommended_stuffs = getRecommendedItems(s, x,username)
    # print recommended_stuffs


def recommendationStorage():
    threading.Timer(2000, recommendationStorage).start()
    recommendationTraining.objects.all().delete()


    conn = psycopg2.connect(database="market", user="abdullah", password="mypass", host="127.0.0.1", port="5432")
    cur2 = conn.cursor()
    cur2.execute("""SELECT *  from  "Graduation_recommenationdatas" ;""")
    data = cur2.fetchall()
    data_recommend = [list(element) for element in data]
    s = {}
    for i in range(len(data_recommend)):
        s.setdefault(data_recommend[i][1], {})
        s[data_recommend[i][1]][data_recommend[i][2]] = data_recommend[i][3]
    traing = calculateSimilarItems(s, 2)
    for key, value in traing.items():
        for freq in traing[key]:
            recommendationTraining(number=key,frequency=freq[0],productId=freq[1]).save()










def recent_posts():
    totalPost=ItemInformation.objects.filter().count()
    conn = psycopg2.connect(database="market", user="abdullah", password="mypass", host="127.0.0.1", port="5432")
    cur = conn.cursor()
    # if totalPost<=4:

    cur.execute("""SELECT *  from  "Graduation_iteminformation" ;""")
    recent_post=cur.fetchall()
    # else:
    #      cur.execute("""SELECT * FROM "Graduation_iteminformation" ORDER BY "id" DESC LIMIT 4;""")
    #      recent_post=cur.fetchall()
    recent_posts = [list(element) for element in recent_post]
    recent_posts_=json.dumps(recent_posts)
    print recent_posts_
    return recent_posts_

def recent_images():

    totalPost = ItemInformation.objects.filter().count()
    conn = psycopg2.connect(database="market", user="abdullah", password="mypass", host="127.0.0.1", port="5432")
    cur = conn.cursor()
    # if totalPost <= 4:

    cur.execute("""SELECT *  from  "Graduation_uploadimages" ;""")
    recent_images = cur.fetchall()
    # else:
    # cur.execute("""SELECT * FROM "Graduation_uploadimages" ORDER BY "id" DESC LIMIT 4;""")
    # recent_images = cur.fetchall()
    recent_images_ = [list(element) for element in recent_images]
    recent_images12 = json.dumps(recent_images_)
    print recent_images12

    return recent_images12


def notfound(request):
    return render_to_response('bootstrap-shop/notfound.html',context_instance=RequestContext(request))




















