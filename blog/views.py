from django.shortcuts import redirect
from django.urls import reverse
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views.generic import View
from django.contrib.auth.models import User as Users
from django.http import HttpResponse

from .models import *
from .utils import *
from .forms import TagForm, PostForm, ProfileForm,UserRegistrationForm

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator

from django.db.models import Q

import datetime


from django.contrib.auth import models

# group = models.Group.objects.get(name='blogger')
# users = group.user_set.all()

def posts_list(request):
    search_querry = request.GET.get('search','')

    if search_querry:
        posts = Post.objects.filter(Q(title__icontains=search_querry) | Q(body__icontains=search_querry))
    else:
        posts = Post.objects.all()

    new = False

    for post in posts:
        post_list = list(str(post.date_pub))
        time_now_list = list(str(datetime.date.today()))
        for i in range(22):
            del post_list[-1]
        for i in range(8):
            del post_list[0]
            del time_now_list[0]
        if post_list[0] == "0":
            del post_list[0]
        if time_now_list[0] == "0":
            del time_now_list[0]
        text_p = ""
        for el in post_list:
            text_p += el
        text_n = ""
        for el in time_now_list:
            text_n += el
        if int(text_p) <= int(text_n):
            new = True
        else:
            new = False

    user_id = request.user.id

    context = {
        'posts': posts,
        'new': new,
        'user_id': user_id,
    }

    return render(request, 'blog/index.html', context=context)

# def contact(request):
#     return render(request, 'blog/news_detail.html')

def profiles_detail(request):
    users = Users.objects.all()
    return render(request, 'blog/profiles_detail.html', context={"users": users})

def profile_detail(request, id):
    user_id = id
    id_this_user = request.user.id
    name_user = Users.objects.filter(id=user_id)
    name_this_user = Users.objects.filter(id=id_this_user)

    message_token = str(user_id) + "_" + str(id_this_user)

    if int(id_this_user) == int(user_id):
        my_acc = True
    else:
        my_acc = False

    profile_this_us = Profile.objects.filter(user_id = id_this_user)
    profile_this_user = ''
    for prof in profile_this_us:
        profile_this_user = prof

    profile_id_1 = profile_this_user.profile_id
    str_profile_id = str(profile_id_1)

    friends = Friend.objects.filter(friend_id = profile_id_1)
    len_friends = len(friends)

    profile_this_user_2 = Profile.objects.filter(user_id = id_this_user)
    profile_2 = ''
    for i in profile_this_user_2:
        profile_2 = i
    my_profile = profile_2.profile_id

    profile = profile_this_user

    id_friend_user_id = Friend.objects.filter(user_id = id_this_user)
    friend_id_check = ''
    
    friend_profil = Friend.objects.filter(user_id = user_id)
    print()
    print()
    print()
    print()
    friend_profile = ""
    for fr_profile in friend_profil:
        friend_profile = fr_profile

    print("K:")
    print(friend_profile)

    print()
    print()
    print()
    print()
    in_friend = ''

    if friend_profile == "":
        in_friend = False
    else:
        friend_frid = friend_profile.friend_id
        print()
        print("Ff:")
        print(friend_frid)
        print()
        print()
        print("Fp:")
        print(friend_profile.friend_id)
        print()
        if friend_frid == my_profile:
            in_friend = True
        else:
            in_friend = False
    
    print()
    print("In:")
    print(in_friend)
    print()
    print("In:")
    print(in_friend)
    print()
    print()

    context = {
        'id_this_user':id_this_user,
        'user_id':user_id,
        'name_user':name_user,
        'message_token':message_token,
        'my_acc':my_acc,
        'friends':friends,
        'len_friends':len_friends,
        'str_profile_id':str_profile_id,
        'profile':profile,
        'my_profile':my_profile,
        'in_friend':in_friend,
    }

    print()
    print()
    print(context)
    print()
    print()

    return render(request, 'blog/profile_detail.html', context=context)

def message_detail(request):
    messages = MessageChat.objects.all()
    id_this_user = request.user.id

    href_chat = {}
    name_chat = {}

    for message in messages:
        message_id = message.message_id
        list_message_id = message_id
        id_del_me = 0
        for i in range(len(list_message_id)):
            if "_" in list_message_id[i]:
                id_del_me = i
                break

        first_list = list_message_id[0:id_del_me]
        second_list = list_message_id[id_del_me + 1:]

        first_number = int("".join(first_list))
        second_number = int("".join(second_list))

        if id_this_user == first_number or id_this_user == second_number:
            if message.from_user_id in href_chat:
                pass
            elif message.from_user_id == "":
                pass
            else:
                a = Users.objects.filter(id = message.from_user_id)
                for b in a:
                    href_chat[message_id] = b

    return render(request, 'blog/message_detail.html', context={'href_chat': href_chat})

def chat_detail(request, message_token):
    if request.user.is_authenticated:
        id_chat = message_token
        messages = MessageChat.objects.filter(message_id=id_chat)
        lm = len(messages)
        if lm > 0:
            id_chat = message_token
            list_id_chat = list(id_chat)
            id_del_me = 0
            for i in range(len(list_id_chat)):
                if "_" in list_id_chat[i]:
                    id_del_me = i
                    break

            first_list = list_id_chat[0:id_del_me]
            second_list = list_id_chat[id_del_me + 1:]

            first_number = int("".join(first_list))
            second_number = int("".join(second_list))

            id_this_user = request.user.id

            if id_this_user == first_number or id_this_user == second_number:
                id_chat = message_token
                id_this_user = str(request.user.id)
                messages = MessageChat.objects.filter(message_id=id_chat)
                list_id_chat = list(str(id_chat))
                id_del_me = 0
                for i in range(len(list_id_chat)):
                    if "_" in list_id_chat[i]:
                        id_del_me = i
                        break
                del list_id_chat[id_del_me + 1:]
                list_id_chat.remove("_")
                from_user_id = ''.join(list_id_chat)

                if request.method == "POST":
                    if len(request.POST['name']) == 0:
                        pass
                    else:
                        MessageChat.objects.create(body = request.POST['name'], message_id=id_chat, user_id=id_this_user, from_user_id=from_user_id)

                lm = len(messages)

                context = {
                    'id_chat': id_chat,
                    'messages': messages,
                    'id_this_user': id_this_user,
                    'lm': lm,
                }

                return render(request, 'blog/chat_detail.html', context=context)

            else:

                return render(request, 'blog/anonim_user.html')
        else:
            id_chat = message_token
            messages = MessageChat.objects.filter(message_id=id_chat)
            if request.method == "POST":
                if len(request.POST['name']) == 0:
                    pass
                else:
                    MessageChat.objects.create(body = request.POST['name'], message_id=id_chat)
            return render(request, 'blog/chat_detail.html', context={'id_chat':id_chat,'messages': messages})
    else:

        return render(request, 'blog/chat_detail.html')

def friends_detail(request, id):
    id_this_user = request.user.id
    profile_this_us = Profile.objects.filter(user_id = id_this_user)
    profile_this_user = ''
    for prof in profile_this_us:
        profile_this_user = prof

    profile_id = profile_this_user.profile_id

    friends_list = {}

    friends = Friend.objects.filter(friend_id = profile_id)

    for friend in friends:
        if friend in friends_list:
            pass
        else:
            a = friend.user_id
            # list_friend = list(friend)
            # id_del_me = 0
            # for i in range(len(list_friend)):
            #    if "_" in list_friend[i]:
            #         id_del_me = i
            #         break
            # del list_friend[list_friend:]
            friends_list[friend] = a


    len_friends = len(friends)

    obj = Profile.objects.get(profile_id__iexact=profile_id)
    dict_new_form = {
        'user_name': profile_this_user.user_name,
        'user_id': profile_this_user.user_id,
        'status': profile_this_user.status,
        'friends': len_friends,
        'profile_id': profile_this_user.profile_id,
        }
    bound_form = ProfileForm(dict_new_form, instance=obj)
    if bound_form.is_valid():
        new_obj = bound_form.save()

    context = {
        'friends':friends,
        'len_friends':len_friends,
        'friends_list':friends_list
    }

    return render(request, 'blog/friends_detail.html', context=context)

def friends_add_detail(request, id):
    id_this_user = id
    profile_this_us = Profile.objects.filter(user_id = id_this_user)
    profile_this_user = ''
    for prof in profile_this_us:
        profile_this_user = prof

    profile_id = profile_this_user.profile_id

    id_user_2 = request.user.id
    profile_us_2 = Profile.objects.filter(user_id = id_user_2)
    profile_user_2 = ''
    for prof in profile_us_2:
        profile_user_2 = prof

    friend_id = profile_user_2.profile_id

    Friend.objects.create(user_name = profile_this_user.user_name, user_id = id_this_user, friend_id = friend_id)

    friends = Friend.objects.filter(friend_id = profile_id)

    len_friends = len(friends)

    print()
    print()
    print(profile_user_2)
    print(friends)
    print(len_friends)
    print()
    print()

    obj = Profile.objects.get(profile_id__iexact=profile_id)
    dict_new_form = {
        'user_name': profile_this_user.user_name,
        'user_id': profile_this_user.user_id,
        'status': profile_this_user.status,
        'friends': len_friends,
        'profile_id': profile_this_user.profile_id,
        }
    bound_form = ProfileForm(dict_new_form, instance=obj)
    # profile_this_user.friends = str(len_friends)
    if bound_form.is_valid():
        new_obj = bound_form.save()
    return redirect('/blog/profile/id' + str(id) + '/', permanent=True)

class PostDetail(ObjectDetailMixin, View):
    model = Post
    template = 'blog/post_detail.html'


class PostCreate(LoginRequiredMixin, ObjectCreateMixin, View):
    model_form = PostForm
    template = 'blog/post_create_form.html'
    raise_exception = True


class PostUpdate(LoginRequiredMixin, ObjectUpdateMixin, View):
    model = Post
    model_form = PostForm
    template = 'blog/post_update_form.html'
    raise_exception = True


class PostDelete(LoginRequiredMixin,ObjectDeleteMixin, View):
    model = Post
    template = 'blog/post_delete_form.html'
    redirect_url = 'posts_list_url'
    raise_exception = True


class TagDetail(ObjectDetailMixin, View):
    model = Tag
    template = 'blog/tag_detail.html'


class TagCreate(LoginRequiredMixin, ObjectCreateMixin, View):
    model_form = TagForm
    template = 'blog/tag_create.html'
    raise_exception = True


class TagUpdate(LoginRequiredMixin, ObjectUpdateMixin, View):
    model = Tag
    model_form = TagForm
    template = 'blog/tag_update_form.html'
    raise_exception = True


class TagDelete(LoginRequiredMixin, ObjectDeleteMixin, View):
    model = Tag
    template = 'blog/tag_delete_form.html'
    redirect_url = 'tags_list_url'
    raise_exception = True


def tags_list(request):
    tags = Tag.objects.all()
    return render(request, 'blog/tags_list.html', context={'tags': tags})
