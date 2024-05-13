from tortoise import Model, fields


class User(Model):
    telegram_id = fields.IntField(pk=True)
    phone = fields.CharField(unique=True, max_length=15)
    token = fields.TextField(max_length=100)
