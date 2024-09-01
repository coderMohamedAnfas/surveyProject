from django.db import models
class InputCategory(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Input(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    category = models.ForeignKey(InputCategory, on_delete=models.CASCADE, related_name='inputs')

    def __str__(self):
        return self.name

class Productive(models.Model):
    category = models.ForeignKey(Input, on_delete=models.CASCADE, related_name='productives')
    productivity = models.FloatField()
    is_selected = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.category.name} - {self.productivity}"


class EmployWelfare(models.Model):
    category = models.ForeignKey(Input, on_delete=models.CASCADE,related_name='employ_welfares')
    employ_welfare = models.FloatField()
    is_selected = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.category.name} - {self.employ_welfare}"