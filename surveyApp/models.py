from django.db import models

class InputCategory(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Input(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    category = models.ForeignKey(InputCategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Productive(models.Model):
    category = models.ForeignKey(Input, on_delete=models.CASCADE)
    productivity = models.FloatField()
    is_selected = models.BooleanField(default=False)

class EmployWelfare(models.Model):
    category = models.ForeignKey(Input, on_delete=models.CASCADE)
    employ_welfare = models.FloatField()
    is_selected = models.BooleanField(default=False)
