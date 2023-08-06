from advanced_filters.admin import AdminAdvancedFiltersMixin
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from novadata_utils.functions import get_prop


class NovadataModelAdmin(
    ImportExportModelAdmin,
    AdminAdvancedFiltersMixin,
    admin.ModelAdmin,
):
    """
    Classe para realizar funcionalidades default em todas as classes do admin,
    a mesma adiciona todos os campos possíveis nas seguintes propriedades:
    - list_display
    - list_filter
    - autocomplete_fields
    - filter_horizontal
    """

    filter_horizontal: list = []

    def get_list_display(self, request):
        """
        Retorna a lista de campos que serão exibidos na listagem do admin.
        """

        super().get_list_display(request)

        model = self.model
        list_display = get_prop(model, "list_display")

        return list_display

    def get_list_filter(self, request):
        """
        Retorna a lista de campos que serão exibidos no filtro da listagem do
        admin.
        """

        super().get_list_filter(request)

        model = self.model
        list_filter = get_prop(model, "list_filter")

        return list_filter

    def get_autocomplete_fields(self, request):
        """
        Retorna a lista de campos que serão exibidos no autocomplete
        do admin.
        """

        super().get_autocomplete_fields(request)

        model = self.model
        autocomplete_fields = get_prop(model, "autocomplete_fields")

        return autocomplete_fields

    def get_filter_horizontal(self):
        """
        Retorna a lista de campos que serão exibidos no filtro horizontal
        do admin.
        """

        model = self.model
        filter_horizontal = get_prop(model, "filter_horizontal")

        return filter_horizontal

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filter_horizontal = self.get_filter_horizontal()
