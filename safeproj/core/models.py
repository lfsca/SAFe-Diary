from django.db import models

class SAFeChallanges(models.Model):
    titles = [
        ('planning', 'Planning'),
        ('resistence', 'Resistence to Change'),
        ('complexity', 'Framework Complexity'),
        ('communication', 'Communication'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=30, choices=titles)
    description = models.TextField()
    created_in = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_titleo_display()} - {self.created_in.strftime('%d/%m/%Y')}"
