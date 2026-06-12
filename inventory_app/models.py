from django.db import models

class CharacterClass(models.Model):
    # e.g., "Arcane Mage", "Shadow Rogue", "Plague Doctor"
    class_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.class_name

class Item(models.Model):
    name = models.CharField(max_length=100)
    cost = models.IntegerField()
    stock = models.IntegerField(default=10)
    image = models.ImageField(upload_to='item_artwork/', blank=True, null=True)

    def __str__(self):
        return self.name


class PurchasedItem(models.Model):
    character_name = models.CharField(max_length=100)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    purchased_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.character_name} - {self.item.name} ({self.quantity})"