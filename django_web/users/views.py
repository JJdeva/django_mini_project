from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import (
    View,
    ListView, 
    DetailView, 
    CreateView, 
    UpdateView, 
    DeleteView
)

from braces.views import LoginRequiredMixin, UserPassesTestMixin

from allauth.account.views import PasswordChangeView
from allauth.account.models import EmailAddress

from .models import Review, User
from .forms import ReviewForm, ProfileForm
from .functions import confirmation_required_redirect
from place.models import Store, Category
from django.db.models import Count

class ReviewListView(ListView):
    model = Review
    context_object_name = 'reviews'
    template_name = 'users/review_list.html'
    paginate_by = 8


class ReviewDetailView(DetailView):
    model = Review
    template_name = 'users/review_detail.html'
    pk_url_kwarg = 'review_id'


class ReviewCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView, View):
    model = Review
    form_class = ReviewForm
    template_name = 'users/review_form.html'

    redirect_unauthenticated_users = True
    raise_exception = confirmation_required_redirect
    
  
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
      
        
        return reverse('users:review-detail', kwargs={'review_id': self.object.id,})
 
    def test_func(self, user):
        return EmailAddress.objects.filter(user=user, verified=True).exists()
        

class ReviewUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = 'users/review_form.html'
    pk_url_kwarg = 'review_id'

    redirect_unauthenticated_users = False
    raise_exception = True

    def get_success_url(self):
        return reverse('users:review-detail', kwargs={'review_id': self.object.id})

    def test_func(self, user):
        review = self.get_object()
        return review.author == user


class ReviewDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Review
    template_name = 'users/review_confirm_delete.html'
    pk_url_kwarg = 'review_id'

    redirect_unauthenticated_users = False
    raise_exception = True

    def get_success_url(self):
        return reverse('place:index') 

    def test_func(self, user):
        review = self.get_object()
        return review.author == user


class ProfileView(DetailView):
    model = User
    template_name = 'users/profile.html'
    pk_url_kwarg = 'user_id'
    context_object_name = 'profile_user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_reviews'] = Review.objects.filter(author__id=self.kwargs.get('user_id'))[:4]

        localdata = ['강남', '강동', '강북', '강서', '관악', '광진', '구로', '금천', '노원', 
                     '도봉', '동대문', '동작', '마포', '서대문', '서초', '성남', '성동', '성북', 
                    '송파', '양천', '영등포', '용산', '은평', '종로', '중구', '중랑']
        loc_ls = []
        for i in localdata:
            loc_ls.append({'local':i})

        categories = Category.objects.values('main_category').annotate(
                max_count=Count('main_category')).values('main_category', 'max_count')

        
        context['local'] = loc_ls
        context['categories'] = categories
        return context


class UserReviewListView(ListView):
    model = Review
    template_name = 'users/user_review_list.html'
    context_object_name = 'user_reviews'
    paginate_by = 4

    def get_queryset(self):
        return Review.objects.filter(author__id=self.kwargs.get('user_id'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile_user'] = get_object_or_404(User, id=self.kwargs.get('user_id'))
        return context


class ProfileSetView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileForm
    template_name = 'users/profile_set_form.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse('place:index')


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileForm
    template_name = 'users/profile_update_form.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse('users:profile', kwargs={'user_id': self.request.user.id})


class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    def get_success_url(self):
        return reverse('users:profile', kwargs={'user_id': self.request.user.id})
        

# def user_login(request):
#     return render(request, 'account/login.html')

# def user_signup(request):
#     return render(request, 'account/signup.html')
