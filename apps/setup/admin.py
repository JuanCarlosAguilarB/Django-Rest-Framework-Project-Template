from django.apps import apps
from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered

# Get a list of all application configurations in the "apps" directory
app_configs = apps.get_app_configs()


class ModelDisplayAdmin(admin.ModelAdmin):
    """
    Custom admin class for displaying models in the admin site.
    """
    # Filter by id
    search_fields = ('id', )

    def get_list_display(self, request):
        """
        Customize the list of fields displayed in the admin list view.
        """
        fields = map(lambda field: field.name, self.model._meta.fields)
        list_display = tuple(
            filter(lambda field: field not in self.readonly_fields, fields))
        return list_display


# Add models to this list to exclude them from registration
excluded_models = []

# Loop through each application's models and register them in the admin site
# if not already registered
for app_config in app_configs:
    for model in app_config.get_models():
        # Check if the model is in the excluded list
        is_model_excluded = model._meta.model_name in excluded_models

        # Check if the model is not registered and not excluded
        if not admin.site.is_registered(model) and not is_model_excluded:
            try:
                # Register the model with the custom ModelDisplayAdmin
                admin.site.register(model, ModelDisplayAdmin)
            except AlreadyRegistered:
                pass
