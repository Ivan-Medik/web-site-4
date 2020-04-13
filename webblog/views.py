from django.shortcuts import redirect
from django.shortcuts import render
from .forms import UserRegistrationForm
from blog.models import Profile
from django.contrib.auth.models import User as Users

def redirect_blog(response):
    return redirect('posts_list_url', permanent=True)

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            users = Users.objects.filter(username = new_user, email = new_user.email)
            id_user = 0
            for user in users:
                id_user = user.id
            profile_id = id_user + 1
            Profile.objects.create(user_name = new_user, user_id = id_user, profile_id = profile_id, friends = 0)
            return render(request, 'webblog/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'webblog/register.html', {'user_form': user_form})
