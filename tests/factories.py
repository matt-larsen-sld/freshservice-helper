from datetime import timezone

from faker import Faker
from faker.providers import BaseProvider

faker = Faker()


class FreshServiceServiceItemProvider(BaseProvider):
    def service_item(self):
        def this_year():
            dt_isoformat = faker.date_time_this_year(tzinfo=timezone.utc).isoformat()
            dt_isoformat = dt_isoformat.replace("+00:00", "Z")
            return dt_isoformat

        id = faker.pyint(max_value=9999999999)
        dict_data = {
            "id": id,
            "created_at": this_year(),
            "updated_at": this_year(),
            "name": faker.text(max_nb_chars=30),
            "delivery_time": faker.pyint(),
            "display_id": faker.pyint(),
            "category_id": faker.pyint(),
            "product_id": None,
            "quantity": None,
            "deleted": None,
            "icon_name": faker.text(max_nb_chars=30),
            "group_visibility": 1,
            "item_type": 1,
            "ci_type_id": None,
            "cost_visibility": True,
            "delivery_time_visibility": True,
            "configs": None,
            "botified": False,
            "visibility": 2,
            "allow_attachments": False,
            "allow_quantity": faker.pybool(),
            "is_bundle": False,
            "create_child": False,
        }
        return dict_data


class FreshServiceServiceItemsResponseProvider(BaseProvider):
    def service_items_response(self, nb_items: int):
        items = []
        faker.add_provider(FreshServiceServiceItemProvider)
        for i in range(nb_items):
            items.append(faker.service_item())
        return {"service_items": items}
