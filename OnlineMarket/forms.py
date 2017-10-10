from django import forms




class search_text(forms.Form):
    search = forms.CharField(max_length=1500)
#In order to select what we want to post
class Radio_select(forms.Form):
    CHOICES=[('select1','Post a job '),
         ('select2','Post an item to sell,')]

    select = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect())

#
class Post_item(forms.Form):


    CHOICES2=[('Electronic Devices', 'Electronic Devices'),
               ('Scholarship', 'Scholarship')
               ,('Books','Books'),
              ('Home staff','Home staff'),('Other','Other')]


    ItemName=forms.CharField(max_length=50)
    ItemType=forms.ChoiceField(choices=CHOICES2,required=True)
    ItemPrice=forms.FloatField()
    ItemDescrption=forms.CharField(max_length=100)

class Status(forms.Form):
    CHOICES = [('New','New'),
                ('Second Hand','Second Hand')]

    ItemStatus=forms.ChoiceField(choices=CHOICES,required=True)



class Post_item1(forms.Form):
    CHOICES3 = [('0 ', ' '),
        ('Computer', 'Computer'),
                ('Smart Phone', 'Smart Phone')
        , ('Tablet', 'Tablet'),
                ('Camera', 'Camera'), ('Accessories', 'Accessories')]
    # ItemName=forms.CharField(max_length=50)
    ItemSubType = forms.ChoiceField(choices=CHOICES3, required=True)

class MainImage(forms.Form):
    Image1 = forms.FileField()
class secondImage(forms.Form):
    Image2 = forms.FileField()
class thirdImage(forms.Form):
    Image3 = forms.FileField()

class DeleteImage1(forms.Form):
    delete1 = forms.BooleanField()
class DeleteImage2(forms.Form):
    delete2 = forms.BooleanField()

class DeleteImage3(forms.Form):
    delete3 = forms.BooleanField()

class sendmessage(forms.Form):
    sendMessage = forms.CharField(max_length=1500)