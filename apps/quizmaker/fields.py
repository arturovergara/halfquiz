# Standard Libraries
from io import BytesIO

# Django Imports
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.forms.fields import FileField
from django.forms.widgets import FileInput


class ExcelField(FileField):
    default_validators = [FileExtensionValidator(["xls", "xlsx"])]
    default_error_message = {
        "invalid_excel": "Upload a valid excel. The file you uploaded was either not an excel or a corrupted file."
    }

    def to_python(self, data):
        """
        Check that the file-upload field data contains a valid excel file
        """
        f = super(ExcelField, self).to_python(data)

        if f is None:
            return None

        if hasattr(data, "temporary_file_path"):
            file = data.temporary_file_path()
        else:
            if hasattr(data, "read"):
                file = BytesIO(data.read())
            else:
                file = BytesIO(data["content"])

        try:
            # 3rd Party Libraries
            from openpyxl import load_workbook

            load_workbook(filename=file)
        except Exception as e:
            raise ValidationError(
                self.error_messages["invalid_excel"], code="invalid_excel"
            ) from e

        if hasattr(f, "seek") and callable(f.seek):
            f.seek(0)

        return f

    def widget_attrs(self, widget):
        attrs = super(ExcelField, self).widget_attrs(widget)

        if isinstance(widget, FileInput) and "accept" not in widget.attrs:
            attrs.setdefault("accept", ".xls,.xlsx")

        return attrs
