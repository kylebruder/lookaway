from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.db import models
from django.http import HttpResponseRedirect

class MarshmallowMixin(models.Model):

    class Meta:
        abstract = True

    marshmallows = models.ManyToManyField('members.marshmallow', blank=True)
    weight = models.FloatField(default=0)

class MemberCreateMixin:

    def form_valid(self, form):
        instance = form.save()
        messages.add_message(
            self.request, messages.INFO,
            'The {} "{}" has been successfully created.'.format(
                self.model.__name__,
                instance,
            )
        )
        return super().form_valid(form)

class MemberUpdateMixin:

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user != self.object.owner:
            raise PermissionDenied
        return context

    def form_valid(self, form):
        if self.request.user.pk == self.object.owner.pk:
            instance = form.save()
            messages.add_message(
                self.request, messages.INFO,
                'The {} "{}" has been successfully updated.'.format(
                    self.model.__name__,
                    instance,
                )
            )
            return HttpResponseRedirect(self.get_success_url())
        else:
            messages.add_message(
                self.request, messages.ERROR,
                'You do not own "{}". Modification Failed. It is not nice to \
                modify other people\'s work!'.format(self.object)
            )
            return HttpResponseRedirect(self.get_success_url())

class MemberDeleteMixin:

    def post(self, request, *args, **kwargs):
        instance = self.model.objects.get(pk=kwargs['pk'])
        if self.request.POST and self.request.user.pk == instance.owner.pk:
            instance.delete()                
            messages.add_message(
                request, messages.INFO,
                'The {} "{}" has been successfully deleted.'.format(
                    self.model.__name__,
                    instance,
                )
            )
            return HttpResponseRedirect(self.get_success_url())
        else:
            messages.add_message(
                request, messages.ERROR,
                'You do not own "{}". Delete Failed. It is not nice to delete \
                other people\'s work!'.format(instance)
            )
            return HttpResponseRedirect(self.get_success_url())

class MemberOwnershipModel:
    '''
    This is here for compatibility reasons
    (to satisfy early database migration requirements).
    Do NOT remove!
    '''
    pass
