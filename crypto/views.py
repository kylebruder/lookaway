from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.forms import ValidationError
from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse
from django.urls import reverse_lazy
from django.utils import timezone, text
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import CreateView, FormMixin, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from members.models import Member
from members.mixins import MemberCreateMixin, MemberUpdateMixin, MemberDeleteMixin
from .forms import BitcoinWalletForm, LitecoinWalletForm
from .models import BitcoinWallet, LitecoinWallet

# Create your views here.

# BitcoinWallet Views
class BitcoinWalletCreateView(LoginRequiredMixin, MemberCreateMixin, CreateView):

    model = BitcoinWallet
    form_class = BitcoinWalletForm
    template_name_suffix = '_form'

    def form_valid(self, form):
        form.instance.creation_date = timezone.now()
        form.instance.owner = Member.objects.get(pk=self.request.user.pk)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        else:
            return reverse('crypto:bitcoin_wallet_detail', kwargs={'pk': self.object.pk})

class BitcoinWalletListView(LoginRequiredMixin, ListView):

    model = BitcoinWallet
    paginate_by = 6
    queryset = BitcoinWallet.objects.filter(is_public=True)
    context_object_name = 'bitcoin_wallets'
    ordering = ['-creation_date']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class MemberBitcoinWalletView(LoginRequiredMixin, ListView):

    model = BitcoinWallet
    paginate_by = 6
    context_object_name = 'bitcoin_wallets'

    def get_queryset(self, *args, **kwargs):
        member = Member.objects.get(username=self.kwargs['member'])
        return BitcoinWallet.objects.filter(owner=member)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        member = Member.objects.get(username=self.kwargs['member'])
        context['user_only'] = True
        context['member'] = member
        return context

class BitcoinWalletDetailView(LoginRequiredMixin, DetailView):

    model = BitcoinWallet
    context_object_name = 'bitcoin_wallet'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        member = Member.objects.get(pk=self.request.user.pk)
        if member.check_can_allocate() and not member.check_is_new():
            context['can_add_marshmallow'] = True
        else:
            context['can_add_marshmallow'] = False
        return context

class BitcoinWalletUpdateView(LoginRequiredMixin, MemberUpdateMixin, UpdateView):

    model = BitcoinWallet
    form_class = BitcoinWalletForm
    template_name_suffix = '_form'

    def form_valid(self, form):
        form.instance.last_modified = timezone.now()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        else:
            return reverse('crypto:bitcoin_wallet_detail', kwargs={'pk': self.object.pk})

class BitcoinWalletDeleteView(LoginRequiredMixin, MemberDeleteMixin, DeleteView):

    model = BitcoinWallet

    def get_success_url(self):
        return reverse('members:studio')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

# LitecoinWallet Views
class LitecoinWalletCreateView(LoginRequiredMixin, MemberCreateMixin, CreateView):

    model = LitecoinWallet
    form_class = LitecoinWalletForm
    template_name_suffix = '_form'

    def form_valid(self, form):
        form.instance.creation_date = timezone.now()
        form.instance.owner = Member.objects.get(pk=self.request.user.pk)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        else:
            return reverse('crypto:litecoin_address_detail', kwargs={'pk': self.object.pk})

class LitecoinWalletListView(LoginRequiredMixin, ListView):

    model = LitecoinWallet
    paginate_by = 6
    queryset = LitecoinWallet.objects.filter(is_public=True)
    context_object_name = 'litecoin_addresses'
    ordering = ['-creation_date']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class MemberLitecoinWalletView(LoginRequiredMixin, ListView):

    model = LitecoinWallet
    paginate_by = 6
    context_object_name = 'litecoin_addresses'

    def get_queryset(self, *args, **kwargs):
        member = Member.objects.get(username=self.kwargs['member'])
        return LitecoinWallet.objects.filter(owner=member)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        member = Member.objects.get(username=self.kwargs['member'])
        context['user_only'] = True
        context['member'] = member
        return context

class LitecoinWalletDetailView(LoginRequiredMixin, DetailView):

    model = LitecoinWallet
    context_object_name = 'litecoin_address'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        member = Member.objects.get(pk=self.request.user.pk)
        if member.check_can_allocate() and not member.check_is_new():
            context['can_add_marshmallow'] = True
        else:
            context['can_add_marshmallow'] = False
        return context

class LitecoinWalletUpdateView(LoginRequiredMixin, MemberUpdateMixin, UpdateView):

    model = LitecoinWallet
    form_class = LitecoinWalletForm
    template_name_suffix = '_form'

    def form_valid(self, form):
        form.instance.last_modified = timezone.now()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        else:
            return reverse('crypto:litecoin_address_detail', kwargs={'pk': self.object.pk})

class LitecoinWalletDeleteView(LoginRequiredMixin, MemberDeleteMixin, DeleteView):

    model = LitecoinWallet

    def get_success_url(self):
        return reverse('members:studio')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
