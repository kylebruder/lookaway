from django.contrib import messages
from django.db import models
from django.http import HttpResponseRedirect

class MarshmallowMixin(models.Model):

    class Meta:
        abstract = True

    marshmallows = models.ManyToManyField('members.marshmallow', blank=True)
    weight = models.FloatField(default=0)

class MemberOwnershipView:

    def form_valid(self, form):
        if self.request.member == self.object.owner:
            form.save()
            messages.add_message(
                self.request, messages.INFO,
                '{} has been successfully modified.'.format(self.object)
            )
            return HttpResponseRedirect(self.get_success_url())
        else:
            messages.add_message(
                self.request, messages.ERROR,
                'You do not own {}. Modification Failed. It is not nice to \
modify other people\'s work!'.format(self.object)
            )
            return HttpResponseRedirect(self.get_success_url())
        
class MemberOwnershipModel:

    def delete(self, request, pk):
        instance = self.model.objects.get(pk=pk)
        if request.member == instance.owner:
            instance.delete()
            messages.add_message(
                request, messages.INFO,
                '{} has been deleted.'.format(instance)
            )
            return HttpResponseRedirect(self.get_success_url())
        else:
            messages.add_message(
                request, messages.ERROR,
                'You do not own {}. Delete Failed. It is not nice to delete \
other people\'s work!'.format(instance)
            )
            return HttpResponseRedirect(self.get_success_url())
