import datetime
import os
import pytz
from hashlib import md5
from random import randrange
from django.db import models
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils import timezone
from lookaway.settings import BASE_DIR, DEFAULT_MEMBER_STORAGE, FOUNDER_CUTOFF
from objects.models import Image


class Member(User):

    class Meta:
        proxy = True

    def check_is_founder(self):
        '''
        Checks to see if the Member joined before the FOUNDER_CUTOFF date
        variable from settings.py.
        '''
        utc = pytz.UTC
        cutoff = utc.localize(FOUNDER_CUTOFF)
        if cutoff > self.date_joined:
            return True
        else:
            return False

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
        directory   - A string that indicates the relative directory path to check.
                      Uses BASE_DIR as the working directory.

        Returns
        Boolean     - True if the bytes used is less than the given capacity.
        free        - The difference of capacity and bytes used.
                      Returns 0 if the bytes used is over capacity.
        used        - The total bytes used.
        '''
        try:
            bytes_used = self.get_dir_size(
                os.path.join(BASE_DIR, directory),
            )
        except:
            bytes_used = 0
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
            print('{} gave a {} marshmallows to {}'.format(self, m.weight, instance))
            if m.weight > 100:
                amount = "a shipment of marshmallows"
            elif m.weight > 50:
                amount = "several bags of marshmallows"
            elif m.weight > 10:
                amount = "a grip of marshmallows"
            elif m.weight > 5:
                amount = "a handful of marshmallows"
            elif m.weight > 1:
                amount = "a few marshmallows"
            elif m.weight == 1:
                amount = "a marshmallow"
            elif m.weight < 1 and m.weight > 0.05 :
                amount = "a piece of marshmallow"
            else:
                amount = "a spec of marshmallow"
            p = Profile.objects.select_related('member').get(member=self)
            p.last_marshmallow_allocation = timezone.now()
            p.save()
            return True, m.weight, amount
        else:
            print("could not allocate weight")
            return False, 0
        
    def __str__(self):
        if self.first_name and self.last_name:
            return '{} {}'.format(self.first_name, self.last_name)
        elif self.profile.display_name:
            return self.profile.display_name
        else:
            return self.username

class Profile(models.Model):

    member = models.OneToOneField(Member, on_delete=models.CASCADE)
    display_name = models.CharField(
        max_length=64,
        unique=True,
        blank=True,
        null=True,
    )
    slug = models.SlugField(max_length=255, unique=True)
    last_marshmallow_allocation = models.DateTimeField(default=timezone.now)
    media_capacity = models.BigIntegerField(default=DEFAULT_MEMBER_STORAGE)
    text = models.TextField(
        blank=True,
        null=True,
    )
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
        return '{} - {} - {}'.format(self.member, self.date, self.weight) 

class InviteLink(models.Model):

    slug = models.SlugField(
        max_length=32,
        unique=True,
    )
    expiration_date = models.DateTimeField(
        default=timezone.now
    )
    label = models.CharField(
        max_length=64,
        unique=True,
    )
    note = models.TextField(
        max_length=256,
        blank=True,
        null=True,
    )

    def make_slug(self):
        string = str(randrange(0,10**8))+str(timezone.now())
        return md5(string.encode()).hexdigest()

    def __str__(self):
        return self.label
