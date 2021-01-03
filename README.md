# Lookaway Content Management System

Lookaway Content Management System is an open source project for publishing and information sharing. It is a utilitarian approach to making content and information available in which security, privacy and respect are deeply considered at each decision in development. As much of the processing as possible is done server side to provide a better experience on thin and low power clients.

## Motivation

People want to participate in online discussions, forums, news media, and most importantly, to share their best work if it can possibly be expressed with the capabilities of the Internet. The open nature of the Internet has allowed diverse groups and individuals to create social media platforms in countless iterations over the years. By 2020 the social media market share has matured with only a few companies left in the race for category winner. However, when the task of providing social media platforms and stewarding our data is left to publicly traded corporations with a fiduciary obligation to increase profits over time, several conflicts of interest emerge.

The commercialization of data, metadata, information and inferences generated by our existence, behavior and consciousness has left us with no access or dividends and no way to know who has accessed our data. Insurance companies, prospective employers, educational institutions, and other scrupulous groups may purchase our data with an expectation of a return on investment. This means they will use our data to deny or grant our requests, determine how much debt to charge or absolve us, and to provide or withhold opportunities from us. Such are the hidden costs of the using free online services.

Whistle-blowers have exposed the use of psychological operations to increase engagement, dependence and screen time. According to claims, aspects of the user experience cause dopamine release and addiction, especially with younger people. Social experimentation without expressed consent or acknowledgment form platform users is also alleged. Even without smoking gun evidence, which is non-existent because of intellectual property law and a lack of transparency of the inner workings of the software, these allegations are quite plausible if not abundantly apparent to any causal observer.

Disclosures detailing interlinks between corporate data owners such as AWS, Google, Microsoft, Facebook, Oracle and state actors have not only informed the public about the collection, organization and utilization of our data, but also have publicized the debate about the nature of these arrangements. Cooperation between corporations and governments is commonplace in all economies. However when deals are made in secret that impact our civil rights, privacy and other constitutionally guaranteed freedoms, we must be critical and demand transparency. Government and corporate involvement in the private decisions that determine which information is presented to the public attenuates the check on power we have over our government.

Allowing misinformation and bigotry in paid advertisements has become a standard business practice online. Troll farms, PACs, and hate groups have seized the opportunity to use dark money to buy vast audiences of unwitting readers. Of course, nearly anyone in the post-industrial world can publish what ever they want on the Internet and their right to do so should be protected by the common interests of the public. The conflict of interest lies in the virtual monopoly the major social media platforms have on our attention.

A lack of controls for sprawling content moderation systems is threatening the livelihoods of the very people that contribute the content that draws people to the platform. When site registration is open to the world, the task of content moderation must be distributed and entrusted to groups of middle managers and moderators. Understandably, an individual's bias may distort their discretion when reviewing potential violations of policy. As a result, people who have staked their work, reputation, and social following on some platforms have seen their accounts, content, and follows removed without warning or recourse.

## Value Proposition

Lookaway CMS offers artists, musicians, writers, journalists, teachers, students, researchers and many other individuals and communities an opportunity to own and operate their own platform without the risk of being silenced. Instead of a pay-to-win trolling contest, Lookaway CMS ranks and sorts content based on the engagement of the membership base while highlighting new contributions. This results in a highly dynamic experience for members and visitors alike. Each detail page is interlinked using key-value pairs so one can easily discover new content. Members can consolidate their work into a dynamic one-stop landing page by sharing their profile URL with the rest of the Internet. Even if you have built your empire on one of the leading content platforms, preserving one's own copies of one's content on one's own platform and having it available and ready for the world at anytime is not only vital, but is within one's reach.

## Build Status

We are still in Version 0. Version 1 will be released when more tests are written and the code is fully reviewed by someone who is not me. Don't wait to start using or forking. Version 2 will be completely rebuilt to be serverless and will include a command line utility to export/import your databases to the new version.

## Code Style

The code should be easy on the eyes. There is very liberal use of whitespace and new lines toward that aim. All efforts are made to avoid namespace collisions with Python keywords and existing names of django modules, classes, methods, etc. Variables use nouns. Functions and methods use verbs. All novel code should be commented using [PEP257](https://www.python.org/dev/peps/pep-0257/) for docstrings. Please reuse existing naming patterns (documentation on that coming soon) so that new apps may be developed or initiated programatically.

### Python

The Python code used in this projects closely adheres to PEP 8. Lines are kept to 80 characters or less when feasible. Code related to the general Django framework is not commented because the intention is implied to those familiar with using Django or have digested the Django documentation. Novel functions and methods should include an docstring. Inline comments are welcome and encouraged. Use above line if it doesn't fit within the 80 character limit.

### JS

JavaScript code portions are few and far between. This project generally avoids the use of browser scripting for two reasons: Information Security concerns surrounding browser side scripting and considerations for clients with low power or low compute capacity. JavaScript is, however, used throughout the project, the vast majority of which is Bootstrap4. The few remaining blocks of JS code are borrowed from people on the Internet the hardened and modified such that the coding style of these sections follows precedent, generally speaking.

### CSS

Note: I didn't know much about CSS when I started this project so to the seasoned web designers reading this, please excuse me. If anyone wants to help me overhaul the CSS that would be very welcome.

Each app has its own CSS file and its own prefix, though some may have more than one. In addition to that, apps that use the same design patterns use the same CSS class suffix. This allows for easy CSS customization between apps (without modifying the HTML templates) in case you don't want a uniform look across the site. The drawback is, if you do want a uniform look that is different from the default style, then many lines need to be changed. 

This isn't so much a problem with the use of Linux commands like sed and awk. For example, all title blocks begin with "<app-name>-title". 

Here are some of the title blocks
```
.art-title {
  font-family: 'Averia Serif Libre', serif;
}

.documentation-title {
  font-family: 'Averia Serif Libre', serif;
}

.music-title {
  font-family: 'Averia Serif Libre', serif;
}
```

So to change the main title font for all apps you could use the command
```
# Still need to test this line :0|
sed '/\-title \{/!b;n;c  font-family: 'Averia Serif Libre', serif;' static/css/*.css
```
I plan on including several CSS themes eventually, at least one of which will contain standardized styling across the entire site.

## Screenshots

### The Main Landing Page
![Lookaway screenshot of the main landing page on a smartphone ](https://lookaway.info/media/member_1/images/2021/01/03/lookaway_readme7.png)

### The Profile Page
![Lookaway screenshot of the profile page on a smartphone ](https://lookaway.info/media/member_1/images/2021/01/03/lookaway_readme8.png)

### The Studio View
![Lookaway screenshot of the studio view on a smartphone ](https://lookaway.info/media/member_1/images/2021/01/03/lookaway_readme2.png)

### The Art App
![Lookaway screenshot of visuals and galleries on a smartphone ](https://lookaway.info/media/member_1/images/2021/01/03/lookaway_readme1.png)

### The Gallery Detail View
![Lookaway screenshot of a visual ](https://lookaway.info/media/member_1/images/2021/01/03/lookaway_readme4.png)

### The Visual Submission Form
![Lookaway screenshot of the visual submission form ](https://lookaway.info/media/member_1/images/2021/01/03/lookaway_readme5.png)

### The Music App
![Lookaway screenshot of music video ](https://lookaway.info/media/member_1/images/2021/01/03/lookaway_readme10.png)

### The Images List
![Lookaway screenshot of the images list page  ](https://lookaway.info/media/member_1/images/2021/01/03/lookaway_readme6.png)

## Framework

Lookaway CMS is built using Django and Python. Although Lookaway CMS is designed to provide utility on its own, it is intended to be a starting point for developing web applications. The simple and elegant means Django provides are insufficient on their own for most use cases. For this reason, authentication, file system structure, meta data, data ownership, and other specifications have been extended simply and solidly to allow further development.


## Features

Lookaway CMS allows people to own and operate their own private social media site, blog, professional website, personal website. Many of the main functions of the major social media platforms are included with Lookaway CMS:

- Upload files to "the cloud"
- Post messages to the world
- Display your photos and artwork
- Release your own music, be your own record label
- Publish articles, stories, and documentation
- Let people know your status with up to the minute posts
- Share links to any URL

Lookaway CMS **DOES NOT**:

- Track private personal information or behavior
- Lay claim to or sell intellectual property
- Perform online transaction processing (OLTP)
- Automagically create content
- Warn you about or prevent you from breaking the laws of your jurisdiction

### Members App

Lookaway Members are people or groups of people that maintain access to a Member account on the site. Generally speaking, more than one person may share a Member account (excluding Staff and Admin accounts). However, one person should not maintain multiple accounts unless a Member account needs to be recreated or multiple Member accounts need to be merged.

For example, there might be a band with four members. Either they all share one account OR each member has their own account, NOT both.

All members can begin contributing and publishing media and content as soon as their account is created. After 30 days, a Member can start giving Marshmallows to any member contributions. This includes their own contributions as well! Giving Marshmallows helps to promote specific pieces of content or media.

Public content will appear in on a Members profile page instantly. If it is recent enough, it will also temporarily appear on the landing page until enough newer content is published.

#### Marshmallows
Online content can be promoted and ranked in a positive feedback system based on the principle of delayed gratification. The system is called Marshmallows, named after the Stanford Marshmallow Experiment. As content receives more marshmallows, it will become prominent on the site. The more times a member gives marshmallows to content over a period of time, the fewer marshmallows will be given each time. The intent is to equalize member influence on how the site and the membership are presented to the world.

Lookaway has inverted the model that nearly all content ranking systems use. Instead of promoting content based on the number of "likes" or comments, we take a more holistic approach to deciding what is at the top of our pages. Let's dispense with driving user engagement, red notifications, comments sections and rewards for spamming and trolling. Members with a fresh perspective can tip the scales fostering serendipity and discovery while attentive members can keep the beat with frequent feedback. Build your membership, let go of the controls and see what rises to the top.

#### Django User Model Inheritance
The Member model inherits the User model from the Django Authentication System in order to leverage all of the wonderful features Django has to offer. Django's authentication mechanisms provide top notch security for Member authentication due to their very well maintained code repository.

#### Profile Page
The Profile page is a page dedicated to the contributions of an individual Member. The content and media with the highest marshmallow weight is displayed on the Profile page. The Member's username will be displayed in the heading unless a first AND last name are provided. A Member can choose an Image to be displayed on their Profile and on pages on the site that call for a Member's Profile Image. A Member can add any string of text (safe of markup and code injections) that is less than 65,335 characters long including whitespaces to their Profile page.

#### Studio Page
The Studio Page is a graphical user interface that allows you and your members to upload files and create and edit web pages. The heads up display shows you objects that were recently created or modified to easily resume work. There is a progress bar that shows how much disk space you are allotted and currently using. 

#### Invite Links

Admins can create an Invite Link using a button that appears in the upper right corner of their Profile Page. The Invite form has two fields: Label and Note. Label is used to identify the name of the person or group that is being invited. Note is used to include a personal note for the invitee. Invites expire after 7 days. Invites can be managed by using the Django Admin Backend.

#### Automated Password Update
Lost member account passwords can be changed via email using an automated password update service. Account passwords are not stored in the database, rather the hash of your password is compared with a hash of the password provided during the authentication process. If your password is lost or forgotten, it must but updated using the password update service and the new password must be provided in order to authenticate.

### Objects App

The objects app handles file uploads, media creation, media deletion, text fields, tagging and metadata. Think of it as the engine that manages the multimedia building blocks used to build dynamic web pages. Each object can be added to other database models using a One-to-One, One-to-Many, or Many-to-Many relationship. For example, the Members app uses the Image object to store your profile picture.

#### Tags

Lookaway CMS Tags are key-value pairs that can be attached to any model class that inherits the MetaDataMixin(). These are displayed in list views and detail views as a hyper link at the bottom of the page or list item. Tag detail pages list model instances that have been tagged with the the repctive tag. Auxiliary Tag views are planned for future updates to provide even more ways to discover new content. Any Member can create and use tags. However, Staff can remove tags (just the tag not the objects tagged) and Admins can edit and remove them.

#### Images

The Image object is a database model that points to an uploaded image file on the storage filesystem and contains metadata and contextual data. 

*COMING SOON* - Uploaded image files are reformatted for optimal web page loading performance. The filename is randomized for added obfuscation. The upload handler will attempt to remove EXIF data as well.

#### Sounds

The Sound object is a database model that points to an uploaded audio file on the storage filesystem and contains metadata and contextual data. 

*COMING SOON* - Uploaded sound files are reformatted for optimal web page loading performance. The filename is randomized for added obfuscation. The upload handler will attempt to remove EXIF data as well

#### Videos

The video object is a database model that points to an uploaded video file on the storage filesystem and contains metadata and contextual data. 

*COMING SOON* - Uploaded video are reformatted for optimal web page loading performance. The filename is randomized for added obfuscation.

#### Code

Submit short code samples along with contextual data such as the language, version, file path, and more. 
 
#### Links

Add a URL link. After input validation, the link handler will attempt to discover the page title, description and favicon by scraping the response of a given URL.

### Posts - Example App
Publish a message along with an image, sound, video, link, and/or code sample. Posts can be private to members or public to site visitors as well. Respond to other members' posts to start a thread.

### Documentation - Example App
Create, update and publish living documents online. Add multiple, ordered, titled sections. Comes with 3 document types: Support, Article and Story.

#### Support Documents
Support documents are designed for disseminating factual, instructional and verifiable information. Although any Member can upvote Support Documents using Marshmallows, only Staff and Admin accounts can create and edit Support Documents. Support Documents can reference other Support Documents. Support Documents can be displayed as a numbered list optionally. Support Documents can include images, sounds, video, code, links, and tags.

*COMING SOON* - Staff and Admins can pin Support Documents.

#### Articles
Articles are designed for opinion and editorial writing. Any Member can create and publish an article. Articles can include images, sounds, video, code, links, and tags.

#### Stories
Stories are classified as fiction or non-fiction. Stories allow for additional data such as original author, publisher, original publication year, etc. Any Member can create and publish a story. Stories can include images, links and tags. 

### Music - Example App
Publish and release original digital music. In keeping with tradition, the nostalgic format is a nod to music industy practices of the 20th century. Before the Internet, when music was released as single releases on vinyl records, the term Track was used for the name of the grooved recess pressed into the vinyl. Larger records known as Albums featured a collection of singles on each side in formats such as Extended Play (a few songs) or Long Play (a full album).

#### Tracks
Tracks are digital versions of individual songs. They point to an uploaded sound file, can include an image and contextual data such as the artist, year of release, record label, etc. Any Member can create and publish a Track once they have uploaded a sound file.

#### Albums
Albums are a collection of Tracks displayed on a single page. Albums can include an ordered list of Tracks, a cover image and contextual data such as the artist, year of release, record label, etc.

### Art - Example App
Publish and curate original works of visual art including, digital art, photography, fine art, film, projections, drawings, or anything that can been seen. Videos are supported.

#### Visuals
Visuals are digital versions of individual works of art, photographs, videos, films or anything that can be digitized and experienced visually. They point to an uploaded image and/or video file and can include contextual data such as the artist, year of completion, links etc. Any Member can create and publish a Visual once they have uploaded an image file.

#### Galleries
Galleries are an online version of an art gallery. Galleries can include an ordered list of Visuals and contextual data such as the artist, year of opening, location (coming soon), etc.

## Code Samples

### MetaDataMixin()
```
class MetaDataMixin(models.Model):
    '''
    A model Mixin that adds meta data and methods which are common to
    all site objects.
    '''

    class Meta:
        abstract = True

    owner = models.ForeignKey(
        'members.member',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,

    )
    creation_date = models.DateTimeField(
        default=timezone.now,
    )
    last_modified = models.DateTimeField(
        default=timezone.now,
    )
    is_public = models.BooleanField(
        default=False,
    )
    publication_date = models.DateTimeField(
        blank=True,
        null=True,
    )
    tags = models.ManyToManyField(
        Tag,
        blank=True,
    )

    def publish(self, instance, member):
        '''
        If the instance passed belongs to the user then set
        it to public and set the publication date to now.
        Arguments:
        instance - Any instance of a DB model instance that uses MetaDataMixin
        user - Pass request.user when calling from a view
        Returns:
        True - If the instance belongs to the user
        False - If the above condition is not met
        '''
        if instance.owner == member:
            instance.is_public = True
            print("publishing {} on {}".format(instance, timezone.now()))
            instance.publication_date = timezone.now()
            instance.save()
            return True
        else:
            return False
```

### The Visual Model Class
```
class Visual(MetaDataMixin, ArtMetaData, MarshmallowMixin):

    order = models.DecimalField(
        max_digits=8,
        decimal_places=4,
    )
    image = models.ForeignKey(
        'objects.image',
        on_delete=models.CASCADE,
    )
    video = models.ForeignKey(
        'objects.video',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    year = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
    )
    medium = models.CharField(
        max_length=1028,
        blank=True,
    )
    dimensions = models.CharField(
        max_length=1028,
        blank=True,
    )
    credits = models.CharField(
        max_length=1028,
        blank=True,
    )
    links = models.ManyToManyField(
        'objects.link',
        blank=True,
    )

    def get_absolute_url(self):
        return reverse('art:visual_detail', kwargs={'slug': self.slug})

    class Meta:
        ordering = ('order',)

    def __str__(self):
        return self.title
```

### Tag List Template
```
{% for tag in object.tags.all %}
  <a href="{% url 'objects:tag_detail' tag.slug %}">
    <span class="badge badge-secondary">{{ tag }}</span>
  </a>
{% endfor %}
<br>
```

### Invite Link Create View
```
class InviteLinkCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):

    permission_required = 'members.add_invitelink'
    model = InviteLink
    fields = ['label', 'note']

    def form_valid(self, form):
        form.instance.slug = self.model.make_slug(form.instance)
        form.instance.expiration_date += datetime.timedelta(days=7)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('members:invite_link_detail', 
            kwargs={'slug': self.object.slug}
        )
```



## Installation

You can run a local instance of Lookaway on your device by downloading the code and running the development server on a Linux command line interface. You must have the latest versions of pip and python installed before proceeding. It is also recommended that the instance run in a virtual environment. Once the server starts, open a browser navigate to your local host on port 8000.

```
git clone https://github.com/kylebruder/lookaway.git
cd lookaway
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 8000
```

To deploy as a website on the Internet see:

https://lookaway.info/zine/information/production-server-deployment-lookaway-cms/



## Reference
[Lookaway CMS - Open Source Content Management System](https://lookaway.info/zine/information/this-is-only-a-test/)
## Tests

Currently, only the Objects App has tests written. These will check to make sure that the views will or will not certain HTTP responses depending on various contexts. Along with a slew of other web application testing tools, I make use of the Django/Python testing modules, even though they do not remotely resemble a true field test from the end user point of view. If you are forking this you surely have your own specific requirements so I will leave it up to you to implement those.

To run the tests simply issue this command while your virtual envirnment is active (if used) and your working directory is the base directory of the project:
```
python manage.py test
```

## How to Guides
[Initializing Lookaway Data on a Production Web Server - Ubuntu 20](https://lookaway.info/zine/information/initialization-ubuntu-20-lookaway-cms/)

[Installing Lookaway CMS Services - Ubuntu 20](https://lookaway.info/zine/information/installing-services-production-lookaway-cms/)

[Lookaway CMS Database Configuration - Postgresql 10](https://lookaway.info/zine/information/database-config-postgresql-10-lookaway-cms/)

[Configuring Lookaway CMS Services - Ubuntu 20](https://lookaway.info/zine/information/configuring-services-ubuntu-20-lookaway-cms/)

[Create and Activate a Virtual Environment - Python Development](https://lookaway.info/zine/information/create-and-activate-a-virtual-environment-python-development-lookaway-information/)

[Lookaway CMS Production Server - Ubuntu 20](https://lookaway.info/zine/information/production-server-deployment-lookaway-cms/)
(More Coming Soon)

## Contribute

Please consider a bitcoin or litecoin donation. This will help me pay my AWS bills and allow our Members to have more storage space to bring you world class content for free. This is a proof of concept project but if I get enough support I can hire some more experienced web designers to help me better maintain and improve this project. They would, of course, be paid in bitcoin or litecoin.

### Bitcoin Donation Address
```
3MnhNRKgrpTFQWstYicjF6GebY7u7dap4u
```
![bitcoin:3MnhNRKgrpTFQWstYicjF6GebY7u7dap4u](https://lookaway.info/media/member_1/images/2021/01/03/3MnhNRKgrpTFQWstYicjF6GebY7u7dap4u_btc.jpg)

### Litecoin Donation Address
```
MT61gm6pdp9rJoLyMWW5A1hnUpxAERnxqg
```
![litecoin:MT61gm6pdp9rJoLyMWW5A1hnUpxAERnxqg ](https://lookaway.info/media/member_1/images/2021/01/03/MT61gm6pdp9rJoLyMWW5A1hnUpxAERnxqg_ltc.jpg)

## Credits

Concept, design, and implementation for Lookaway CMS by Kyle Bruder. A very special thanks to the founding members Natty Batty, Chris Castro, Laura Schwamb, Picante Nate, Kento Murayama, and Richard Pereira for testing and contributing direction, feedback and most excellent content. Also a shoutout to all of the code borrowed from other projects and guides from the Internet. I will try and maintain an exhaustive list (coming soon) on this README. Please bear with me and hit me up if I left you out.

## Licence

Lookaway CMS is released under GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007# Lookaway CMS
