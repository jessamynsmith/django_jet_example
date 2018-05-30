from django.db import models


class Person(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return '{}'.format(self.name)


class Tag(models.Model):
    value = models.CharField(max_length=20)

    def __str__(self):
        return '{}'.format(self.value)


class PersonTag(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('person', 'tag'),)

    def __str__(self):
        return '{}-{}'.format(self.person, self.tag)
