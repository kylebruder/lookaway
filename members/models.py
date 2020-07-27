import datetime
import os
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from objects.models import Image

# Create your models here.


class Member(User):

    class Meta:
        proxy = True

    def check_is_new(self, n=30):
        '''
        Returns True if less than n days have passed since the user was created.
        n defaults to 30 days if not passed.
        ''' 
        q = self.date_joined
        t = timezone.now() - datetime.timedelta(days=n)
        if t > q:
            return False
        else:
            return True

    def check_can_allocate(self, n=300):
        '''
        Returns True if the Member's last Marshmallow allocation occurred more
        than n seconds ago.
        n defaults to 300 seconds (5 minutes) if not passed.
        '''
        # get n seconds ago
        t = timezone.now() - datetime.timedelta(seconds=n)
        try:
            q = Profile.objects.select_related('member').get(member=self).last_marshmallow_allocation
            if t > q:
                return True
            else:
                return False
        except:
            return False

    def get_dir_size(self, path='.'):
        '''
        Returns the total bytes used within a given directory.
        Thanks to blakev!
        https://stackoverflow.com/questions/1392413/calculating-a-directorys-size-using-python
        '''
        total = 0
        for entry in os.scandir(path):
            if entry.is_file():
                total += entry.stat().st_size
            elif entry.is_dir():
                total += self.get_dir_size(entry.path)
        return total

    def check_free_media_capacity(self, directory):
        '''
        Checks total bytes under a dir and compares to the members capacity
        indicated bt the models .

        Arguments
        directory   - A string that indicates the directory path to check.

        Returns
        Boolean     - True if the bytes used is less than the given capacity.
        free        - The difference of capacity and bytes used.
                      Returns 0 if the bytes used is over capacity.
        used        - The total bytes used.
        '''
        bytes_used = self.get_dir_size(directory)
        capacity = self.profile.media_capacity
        if bytes_used < capacity:
            bytes_free = capacity - bytes_used
            return True, bytes_free, bytes_used
        else:
            return False, 0, bytes_used
        
    def get_adjusted_weight(self, n=30, m=5, *args, **kwargs):
        '''
        Returns this user's current adjusted weight as floating point number.
        The weight is adjusted based on the user's weight allocation frequency.
        The higher the frequency, the lower the weight (to prevent spamming).
        Arguments
        n       - Number of days ago to query in determining the allocation period.
                Defaults to 30 days.
        m       - Multiplier for the adjusted weight.
                Default is 5.
        model   - the model recieving the marshmallow
        '''
        # get n days ago
        t = timezone.now() - datetime.timedelta(days=n)
        ## number marshmallows allocated by the user in the last n days
        if 'model' in kwargs:
            q = kwargs['model'].objects.filter(
                marshmallows__member=self,
                marshmallows__date__gte=t,
            ).count()
        else:
            q = Marshmallow.objects.filter(member=self, date__gte=t).count()
        if q == 0:
            q += 1
        print('number of marshmalows allocated in last {0} days by {1}: {2}'.format(n, q, self))
        # weight allocation period
        p = n / q 
        # apply the multiplier
        return p * m

    def allocate_marshmallow(self, instance, *args, **kwargs):
        '''
        If the methods check_can_allocate() and check_is_new() return True,
        allocate a Marshmallow to a model instance. The Marshmallow's weight attribute
        is determined by the get_adjusted_weight() method.

        Arguments
        instance - A database model instance that uses Marshmallow Mixin
        model    - the model recieving the marshmallow

        Returns 
        self - The Member calling this function
        instance - The updated instance
        m.weight - The weight of the newly created Marshmallow model object as a float
        '''
        if  self.check_can_allocate() and not self.check_is_new():
            if 'model' in kwargs:
                # Create new Marshmallow adjusted by single model
                m = Marshmallow(
                    member=self, 
                    date=timezone.now(), 
                    weight=self.get_adjusted_weight(model=kwargs['model'])
                )
                m.save()
            else:
                # Create new Marshmallow adjusted universaly
                m = Marshmallow(
                    member=self, 
                    date=timezone.now(), 
                    weight=self.get_adjusted_weight()
                )
                m.save()
            # Add the Marshmalow to the object
            instance.marshmallows.add(m)
            instance.weight += m.weight
            instance.save()
            print('{} allocated a marshmallow weighing {} to {}'.format(self, m.weight, instance))
            p = Profile.objects.select_related('member').get(member=self)
            p.last_marshmallow_allocation = timezone.now()
            p.save()
            return True, instance, m.weight
        else:
            print("could not allocate weight")
            return False, instance, 0
        
    def __str__(self):
        if self.first_name and self.last_name:
            return '{} {}'.format(self.first_name, self.last_name)
        else:
            return self.username

class Profile(models.Model):

    member = models.OneToOneField(Member, on_delete=models.CASCADE)
    slug = models.SlugField()
    last_marshmallow_allocation = models.DateTimeField(default=timezone.now)
    media_capacity = models.PositiveIntegerField(default=5*10**8)
    image = models.ForeignKey(
        Image,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    def __str__(self):
        return str(self.member)

class Marshmallow(models.Model):

    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    weight = models.FloatField(default=0.0)

    def __str__(self):
        return '{} - {} - {}'.format(self.user, self.date, self.weight) 
