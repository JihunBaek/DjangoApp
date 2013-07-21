# -*- coding: utf-8 -*-
'''
Created on 2013. 7. 16.

@author: lacidjun
'''
from django import forms
import re
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

class RegistrationForm(forms.Form):
    username = forms.CharField(label='사용자 이름', max_length=30)
    email = forms.EmailField(label='메일')
    password1 = forms.CharField(
                                label='비밀번호',
                                widget=forms.PasswordInput()
                                )
    password2 = forms.CharField(
                                label='비밀번호(체크)',
                                widget=forms.PasswordInput()
                                )
    def clean_password2(self):
        if 'password1' in self.cleaned_data:
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']
            if password1 == password2:
                return password2
        raise forms.ValidationError('비밀번호가 일치하지 않음')
        
         
    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.search(r'^\w+$', username):
            raise forms.ValidationError('사용자 이름은 알페벳, 밑줄만 가능')
        try:
            User.objects.get(username=username)
        except ObjectDoesNotExist:
            return username
        raise forms.ValidationError('중복된 사용자 이름입니다.')

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file  = forms.FileField()
