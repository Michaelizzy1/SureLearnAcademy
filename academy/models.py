from django.db import models
from django.urls import reverse


class Track(models.Model):
    """One of the three course tracks (Exam Prep, Tech, Creative)."""

    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, help_text="Used in the courses page anchor, e.g. 'exam-prep'")
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.name


class Course(models.Model):
    track = models.ForeignKey(Track, on_delete=models.CASCADE, related_name="courses")
    code = models.CharField(max_length=20, help_text="e.g. EXM-01, TEC-03")
    title = models.CharField(max_length=150)
    description = models.TextField()
    best_for = models.CharField(max_length=150)
    duration = models.CharField(max_length=100, help_text="e.g. '8–12 weeks'")
    format = models.CharField(max_length=100, default="Home or online")
    price_min = models.PositiveIntegerField(help_text="Naira, lower end of monthly range")
    price_max = models.PositiveIntegerField(help_text="Naira, upper end of monthly range")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["track__order", "order", "id"]

    def __str__(self):
        return f"{self.code} — {self.title}"

    @property
    def price_range_display(self):
        return f"₦{self.price_min:,}–{self.price_max:,}/mo"


class Tutor(models.Model):
    name = models.CharField(max_length=150)
    role = models.CharField(max_length=150, default="Tutor")
    bio = models.TextField()
    photo = models.ImageField(upload_to="tutors/", blank=True, null=True)
    tags = models.CharField(max_length=255, blank=True, help_text="Comma-separated, e.g. 'SSCE & JAMB Prep, Web Development'")
    based_in = models.CharField(max_length=150, default="Abuja, Nigeria")
    teaches_mode = models.CharField(max_length=150, default="Home visits & online")
    education = models.CharField(max_length=255, blank=True)
    is_founder = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.name

    @property
    def tag_list(self):
        return [t.strip() for t in self.tags.split(",") if t.strip()]


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.CharField(max_length=100, help_text="e.g. Exam Tips, Study Advice")
    excerpt = models.TextField(help_text="Short summary shown on the blog list page")
    body = models.TextField(help_text="Full article. Plain paragraphs, one per line; blank line = new paragraph.")
    author_name = models.CharField(max_length=150, default="SureLearn Academy")
    cover_image = models.ImageField(upload_to="blog/", blank=True, null=True)
    tags = models.CharField(max_length=255, blank=True, help_text="Comma-separated")
    read_time_minutes = models.PositiveIntegerField(default=5)
    published_at = models.DateTimeField()
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ["-published_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("academy:blog_detail", args=[self.slug])

    @property
    def tag_list(self):
        return [t.strip() for t in self.tags.split(",") if t.strip()]

    @property
    def body_paragraphs(self):
        return [p.strip() for p in self.body.split("\n\n") if p.strip()]


class ContactSubmission(models.Model):
    MODE_CHOICES = [
        ("home", "Home visits"),
        ("online", "Online"),
        ("either", "Either"),
    ]

    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=30)
    course_interest = models.CharField(max_length=150, blank=True, help_text="Free text: course/subject they're asking about")
    level = models.CharField(max_length=100, blank=True)
    preferred_mode = models.CharField(max_length=10, choices=MODE_CHOICES, default="either")
    preferred_time = models.CharField(max_length=150, blank=True)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    handled = models.BooleanField(default=False, help_text="Tick once you've followed up")

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.created_at:%Y-%m-%d})"
