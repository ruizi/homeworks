from django import forms


class ImageUploadForm(forms.Form):
    image = forms.ImageField(label="封面图片", required=False)


class ImageUploadForm1(forms.Form):
    image1 = forms.ImageField(label="封面图片", required=False)
    image2 = forms.ImageField(label="封面图片", required=False)


class ImageUploadForm2(forms.Form):
    image = forms.ImageField(label="封面图片", required=False)


class AddPayForm(forms.Form):
    CHOICES = (
        ('显式', "显式"),
        ('隐式', "隐式"),
    )
    item_spend = forms.CharField(label="项目", max_length=128,
                                 widget=forms.TextInput(attrs={'class': 'form-control'}))
    money = forms.IntegerField(label="花费")
    date = forms.DateField(label="日期")
    isPri = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)
