"""Forms for the Empresa model and related business logic."""

from typing import Any, ClassVar

from django import forms

from .models import Empresa


class EmpresaForm(forms.ModelForm):
    """Form for creating and updating Empresa instances."""

    ciudad = forms.ChoiceField(
        choices=[("", "---------")],
        widget=forms.Select(attrs={"class": "form-control"}),
        required=False,
    )
    pais = forms.ChoiceField(
        choices=[
            ("", "---------"),
            ("Colombia", "Colombia"),
            ("Perú", "Perú"),
            ("Ecuador", "Ecuador"),
            ("Venezuela", "Venezuela"),
            ("Chile", "Chile"),
        ],
        widget=forms.Select(attrs={"class": "form-control"}),
        required=False,
    )

    class Meta:
        """Meta options for EmpresaForm, specifying model, fields, and widgets."""

        model = Empresa
        fields: ClassVar[list[str]] = ["nombre", "nit", "razon_social", "tipo_empresa", "segmento",
                 "tamaño", "email", "telefono", "direccion", "ciudad", "pais",
                 "sitio_web", "descripcion", "numero_empleados", "activa", "requiere_2fa", "politica_estricta"]
        widgets: ClassVar[dict[str, Any]] = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "nit": forms.TextInput(attrs={"class": "form-control"}),
            "razon_social": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "telefono": forms.TextInput(attrs={"class": "form-control"}),
            "direccion": forms.Textarea(attrs={"class": "form-control"}),
            "sitio_web": forms.URLInput(attrs={"class": "form-control"}),
            "descripcion": forms.Textarea(attrs={"class": "form-control"}),
            "numero_empleados": forms.NumberInput(attrs={"class": "form-control"}),
            "activa": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "requiere_2fa": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "politica_estricta": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "tipo_empresa": forms.Select(attrs={"class": "form-control"}),
            "segmento": forms.Select(attrs={"class": "form-control"}),
            "tamaño": forms.Select(attrs={"class": "form-control"}),
            "ciudad": forms.Select(attrs={"class": "form-control"}),
            "pais": forms.Select(attrs={"class": "form-control"}),
        }
    def __init__(self, *args: str, **kwargs: str) -> None:
        """Initialize EmpresaForm with custom choices for 'ciudad' and 'pais' fields."""
        super().__init__(*args, **kwargs)
        # Default empty choices for ciudad
        self.fields["ciudad"].choices = [("", "---------")]

        # Set available countries
        self.fields["pais"].choices = [
            ("", "---------"),
            ("Colombia", "Colombia"),
            ("Perú", "Perú"),
            ("Ecuador", "Ecuador"),
            ("Venezuela", "Venezuela"),
            ("Chile", "Chile"),
        ]

        # Dynamically set ciudad choices if data is present (for POST or instance)
        pais = None
        if self.data.get("pais"):
            pais = self.data.get("pais")
        elif self.instance and getattr(self.instance, "pais", None):
            pais = self.instance.pais

        if pais == "Colombia":
            ciudades = [
                ("Bogotá", "Bogotá"), ("Medellín", "Medellín"), ("Cali", "Cali"),
                ("Barranquilla", "Barranquilla"), ("Cartagena", "Cartagena"),
                ("Bucaramanga", "Bucaramanga"), ("Cúcuta", "Cúcuta"),
                ("Ibagué", "Ibagué"), ("Pereira", "Pereira"), ("Manizales", "Manizales"),
            ]
            self.fields["ciudad"].choices += ciudades
        elif pais == "Perú":
            ciudades = [
                ("Lima", "Lima"), ("Arequipa", "Arequipa"), ("Trujillo", "Trujillo"),
                ("Cusco", "Cusco"), ("Iquitos", "Iquitos"),
            ]
            self.fields["ciudad"].choices += ciudades
        # Add more countries and their cities as needed

    def clean(self) -> dict[str, Any]:
        """Clean and validate the form data, ensuring city-country consistency."""
        cleaned_data = super().clean()
        pais = cleaned_data.get("pais")
        ciudad = cleaned_data.get("ciudad")

        # Validación de ciudad según el país
        if pais and ciudad:
            # Aquí podrías agregar la lógica específica para cada país
            if pais == "Colombia":
                ciudades_colombia = [
                    "Bogotá", "Medellín", "Cali", "Barranquilla", "Cartagena",
                    "Bucaramanga", "Cúcuta", "Ibagué", "Pereira", "Manizales",
                ]
                if ciudad not in ciudades_colombia:
                    self.add_error("ciudad", f"La ciudad no es válida para {pais}")
            elif pais == "Perú":
                ciudades_peru = [
                    "Lima", "Arequipa", "Trujillo", "Cusco", "Iquitos",
                ]
                if ciudad not in ciudades_peru:
                    self.add_error("ciudad", f"La ciudad no es válida para {pais}")
            # Agrega más países según sea necesario

        return cleaned_data
