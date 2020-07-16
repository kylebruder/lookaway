from django.contrib import messages
from django.db import models
from django.http import HttpResponseRedirect


class MemberOwnershipModel:
    pass

class MarshmallowMixin(models.Model):

    class Meta:
        abstract = True

    marshmallows = models.ManyToManyField('members.marshmallow', blank=True)
    weight = models.FloatField(default=0)

class MemberOwnershipView:

    def form_valid(self, form):
        if self.request.user.pk == self.object.owner.pk:
            form.save()
            messages.add_message(
                self.request, messages.INFO,
                '"{}" has been successfully modified.'.format(self.object)
            )
            return HttpResponseRedirect(self.get_success_url())
        else:
            messages.add_message(
                self.request, messages.ERROR,
                'You do not own "{}". Modification Failed. It is not nice to \
modify other people\'s work!'.format(self.object)
            )
            return HttpResponseRedirect(self.get_success_url())

class MemberDeleteView:

    def post(self, request, *args, **kwargs):
        instance = self.model.objects.get(pk=kwargs['pk'])
        if self.request.POST and self.request.user.pk == instance.owner.pk:
            instance.delete()                
            messages.add_message(
                request, messages.INFO,
                '"{}" has been deleted.'.format(instance)
            )
            return HttpResponseRedirect(self.get_success_url())
        else:
            messages.add_message(
                request, messages.ERROR,
                'You do not own "{}". Delete Failed. It is not nice to delete \
other people\'s work!'.format(instance)
            )
            return HttpResponseRedirect(self.get_success_url())
