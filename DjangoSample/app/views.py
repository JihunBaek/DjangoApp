# Create your views here.
# -*- coding: utf-8 -*-
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.template import RequestContext, Context, loader
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib.auth import logout

import md5

from app.models import *
from app.forms import *

def index(request, page=1):
    per_page = 5
    start_pos = (page - 1) * per_page
    end_pos = start_pos + per_page
    total_entries = Entries.objects.count()
    page_title = '블로그 글 목록 화면'
    user = request.user
    
    res = total_entries % per_page
    npagination = total_entries / per_page
    
    if(res):
        npagination =+ 1
        
    entries = Entries.objects.all().order_by('-created')[start_pos:end_pos]
    tpl = loader.get_template('list.html')
    ctx = Context({
                   'page_title':page_title,
                   'entries':entries,
                   'current_page':page,
                   'total_entries':total_entries,
                   'npagination':range(1,npagination), # 글목록 인덱스 추가해야함
                   'user':user,
                   })
    ctx.update(csrf(request))
    return render_to_response('list.html', ctx)

def read(request, entry_id=None):
    page_title = '블로그 글 읽기 화면'
    try:
        current_entry = Entries.objects.get(id=int(entry_id))
    except:
        return HttpResponse('없는 글')
    
    try:
        prev_entry = current_entry.get_previous_by_created()
    except:
        prev_entry = None
    try:
        next_entry = current_entry.get_next_by_created() #get은 1개 반환
    except:
        next_entry = None
    
    comments = Comments.objects.filter(Entry=current_entry).order_by('created') #필터는 0개이상
    tpl = loader.get_template('read.html')
    ctx = Context({
                   'page_title':page_title,
                   'current_entry':current_entry,
                   'prev_entry':prev_entry,
                   'next_entry':next_entry,
                   'comments':comments
                   })
    ctx.update(csrf(request))
    #return render_to_response('read.html', ctx)
    return HttpResponse(tpl.render(ctx))

def write_form(request):
    page_title = '블로그 글 쓰기 화면'
    categories = Categories.objects.all()
    #tpl = loader.get_template('write.html')
    ctx = Context({
                   'page_title':page_title,
                   'categories':categories
                   })
    ctx.update(csrf(request))
    return render_to_response('write.html',ctx)

def add_post(request):
    if request.POST.has_key('title') == False :
        return HttpResponse('글 제목을 입력해주세요')
    else:
        if len(request.POST['title']) == 0 :
            return HttpResponse('글제목이 비어있네요')
        else:
            entry_title = request.POST['title']
            
    if request.POST.has_key('content') == False:
        return HttpResponse('글 본문을 입력해야 한다우.')
    else:
        if len(request.POST['content']) == 0:
            return HttpResponse('글 본문엔 적어도 한 글자는 넣자!')
        else:
            entry_content = request.POST['content']
    try:
        entry_category = Categories.objects.get(id=request.POST['category'])
    except:
        return HttpResponse('이상한 글 갈래구려')
    if request.POST.has_key('tags') == True:
        tags = map(lambda str: str.strip(), unicode(request.POST['tags']).split(','))
        tag_list = map(lambda tag: TagModel.objects.get_or_create(Title=tag)[0], tags)
    else:
        tag_list = []
        
    new_entry = Entries()
    new_entry.Title = entry_title
    new_entry.Content = entry_content
    new_entry.Category = entry_category
    try:
        new_entry.save()
    except:
        return HttpResponse('db저장 실패')
    
    for tag in tag_list:
        new_entry.Tags.add(tag)
    if len(tag_list) > 0 :
        try:
            new_entry.save()
        except:
            return HttpResponse('글 갈래 저장 실패')
    return HttpResponse('%s글 저장 성공' % new_entry.id) 

def add_comment(request):
# 글쓴이 이름 처리
    cmt_name = request.POST.get('name', '')
    if not cmt_name.strip() :
        return HttpResponse('글쓴이 이름을 입력하시오.')

# 비밀번호
    cmt_password = request.POST.get('password', '')
    if not cmt_password.strip() :
        return HttpResponse('비밀번호를 입력하시오.')
    cmt_password = md5.md5(cmt_password).hexdigest()

# 댓글 본문 처리
    cmt_content = request.POST.get('content', '')
    if not cmt_content.strip() :
        return HttpResponse('댓글 내용을 입력하시오.')
    
    if request.POST.has_key('entry_id') == False:
        return HttpResponse('댓글 달 글을 지정하세요')
    else:
        try:
            entry = Entries.objects.get(id=request.POST['entry_id'])
        except:
            return HttpResponse('없는 글')
    try:
        new_cmt = Comments(Name=cmt_name, Password=cmt_password, Content=cmt_content, Entry = entry)
        new_cmt.save()
        entry.Comments += 1
        entry.save()
        return HttpResponse('댓글이 성공적으로 저장댐')
    except:
        return HttpResponse('저장하지 못함')
    return HttpResponse('저장을 못했습니다')

def delete_comment(request):
    page_title = '댓글 삭제 화면'
    try:
        del_entry_id = request.POST.get('entry_id', '')
    except:
        return HttpResponse('없는 댓글입니다.')
    #tpl = loader.get_template('write.html')
    ctx = Context({
                   'del_entry_id':del_entry_id,
                   })
    ctx.update(csrf(request))
    return render_to_response('delete_comment_form.html',ctx)

def delete_comment_check(request):
    comment_entry = Entries.objects.get(id=request.POST['entry_id'])
    name = request.POST['name']
    try:
        del_comment = Comments.objects.get(Entry = comment_entry, Password = md5.md5(request.POST['password']).hexdigest(), Name = name)#컨텐츠까지 비교
    except:
        return HttpResponse('사용자와 비번이 맞지 않습니다')
    
    del_comment.delete()
    comment_entry.Comments -= 1
    comment_entry.save()
    return HttpResponse('삭제 성공')

@csrf_exempt
def get_comments(request, entry_id=None):
    print request.method
    if request.is_ajax():        
        with_layout = False
    else:        
        with_layout = True    
    current_entry = Entries.objects.get(id=entry_id)
    comments = Comments.objects.filter(Entry=entry_id).order_by('created')
    tpl = loader.get_template('comments.html')
    ctx = Context({
                   'current_entry':current_entry,
                   'comments':comments
                   })
    ctx.update(csrf(request))
    return render_to_response('comments.html', ctx)

def login(request):
    pass

def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/app')

def test(request):
    print request.method
    
def register_page(request):
    print request.method
    if request.method == 'POST':
        print request.method
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                                            username=form.cleaned_data['username'],
                                            password=form.cleaned_data['password1'],
                                            email=form.cleaned_data['email']
                                            )
            ctx = Context({
                           'user':user
                           })
            
            ctx.update(csrf(request))
            return render_to_response('registration/register_success.html',ctx)
    else:
        form = RegistrationForm()
    print request.method
    ctx = Context({
                   'form': form
                   })
    ctx.update(csrf(request))
    return render_to_response('registration/register.html',ctx)

