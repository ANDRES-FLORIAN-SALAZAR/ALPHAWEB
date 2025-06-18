"""Triggers and validation logic for the Empresa model."""

from django.core.exceptions import ValidationError
from django.db.models.signals import pre_save
from django.utils.translation import gettext_lazy as _

from empresa.models import Empresa

PEQUENA_EMPRESA_MIN_EMPLEADOS = 11
PEQUENA_EMPRESA_MAX_EMPLEADOS = 50
MICRO_EMPRESA_MAX_EMPLEADOS = 10
MEDIANA_EMPRESA_MIN_EMPLEADOS = 51
MEDIANA_EMPRESA_MAX_EMPLEADOS = 250
GRANDE_EMPRESA_MIN_EMPLEADOS = 251


class EmpresaTriggers:
    """Clase que contiene los triggers para el modelo Empresa."""

    @staticmethod
    def validar_tamano_empresa(_sender: type, instance: Empresa) -> None:
        """Valida que el número de empleados sea consistente con el tamaño de la empresa."""
        if instance.tamaño == "MICRO":
            if instance.numero_empleados < 1 or instance.numero_empleados > MICRO_EMPRESA_MAX_EMPLEADOS:
                raise ValidationError({
                    "numero_empleados": _("Las microempresas deben tener entre 1 y 10 empleados."),
                })
        elif instance.tamaño == "PEQUEÑA":
            if instance.numero_empleados < PEQUENA_EMPRESA_MIN_EMPLEADOS or instance.numero_empleados > PEQUENA_EMPRESA_MAX_EMPLEADOS:
                raise ValidationError({
                    "numero_empleados": _("Las pequeñas empresas deben tener entre 11 y 50 empleados."),
                })
        elif instance.tamaño == "MEDIANA":
            if instance.numero_empleados < MEDIANA_EMPRESA_MIN_EMPLEADOS or instance.numero_empleados > MEDIANA_EMPRESA_MAX_EMPLEADOS:
                raise ValidationError({
                    "numero_empleados": _("Las medianas empresas deben tener entre 51 y 250 empleados."),
                })
        elif instance.tamaño == "GRANDE" and instance.numero_empleados < GRANDE_EMPRESA_MIN_EMPLEADOS:
            raise ValidationError({
                "numero_empleados": _("Las grandes empresas deben tener más de 250 empleados."),
            })

    @staticmethod
    def validar_email_unico(_sender: type, instance: Empresa) -> None:
        """Valida que el email sea único por empresa."""
        if instance.pk is None and Empresa.objects.filter(email=instance.email).exists():  # Solo para creación
            raise ValidationError({
                "email": _("Este email ya está registrado para otra empresa."),
            })

    @staticmethod
    def validar_nit_unico(instance: Empresa) -> None:
        """Valida que el NIT sea único."""
        if instance.pk is None and Empresa.objects.filter(nit=instance.nit).exists():  # Solo para creación
            raise ValidationError({
                "nit": _("Este NIT ya está registrado para otra empresa."),
            })

    @staticmethod
    def validar_razon_social_unico(instance: Empresa) -> None:
        """Valida que la razón social sea única por empresa."""
        if instance.pk is None and Empresa.objects.filter(razon_social=instance.razon_social).exists():  # Solo para creación
            raise ValidationError({
                "razon_social": _("Esta razón social ya está registrada para otra empresa."),
            })

    @staticmethod
    def validar_segmento_tamano(instance: Empresa) -> None:
        """Valida que el segmento y tipo de empresa sean compatibles."""
        if instance.tipo_empresa and instance.segmento:
            # Aquí podrías agregar validaciones específicas según el tipo de empresa y segmento
            pass
# Conectar los triggers a las señales de Django
pre_save.connect(EmpresaTriggers.validar_tamano_empresa, sender=Empresa)
pre_save.connect(EmpresaTriggers.validar_email_unico, sender=Empresa)
pre_save.connect(lambda _sender, instance: EmpresaTriggers.validar_nit_unico(instance), sender=Empresa)
pre_save.connect(lambda _sender, instance: EmpresaTriggers.validar_razon_social_unico(instance), sender=Empresa)
pre_save.connect(EmpresaTriggers.validar_segmento_tamano, sender=Empresa)
