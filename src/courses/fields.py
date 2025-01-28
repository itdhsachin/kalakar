"""OrderField is a custom field built on PositiveIntegerField to add two functionalities:
1. Automatically assign an order value when no specific order is provided.
2. Order objects with respect to other fields.
"""

from django.core.exceptions import ObjectDoesNotExist
from django.db import models


class OrderField(models.PositiveIntegerField):
    """A custom field to manage ordering of objects.

    Attributes:
        for_fields (list): Fields to consider for ordering.
    """

    def __init__(self, for_fields=None, *args, **kwargs):
        """Initializes the OrderField.

        Args:
            for_fields (list, optional): Fields to consider for ordering.
            args: dynamic arguments.
            kwargs: dynamic keyword arguments.
        """
        self.for_fields = for_fields
        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        """Automatically assigns an order value before saving the model instance.

        Args:
            model_instance (Model): The instance of the model being saved.
            add (bool): Whether the instance is being added for the first time.

        Returns:
            int: The order value to be assigned.
        """
        # automatically assign value
        if getattr(model_instance, self.attname) is None:
            try:
                qs = self.model.objects.all()
                # order objects with respect to other fields
                if self.for_fields:
                    query = {
                        field: getattr(model_instance, field)
                        for field in self.for_fields
                    }
                    qs = qs.filter(**query)
                last_item = qs.latest(self.attname)
                value = last_item.order + 1
            except ObjectDoesNotExist:
                value = 0
            setattr(model_instance, self.attname, value)
            return value
        else:
            return super().pre_save(model_instance, add)
