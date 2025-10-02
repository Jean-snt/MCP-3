from django.core.management.base import BaseCommand
from django.db import transaction
import os
import shutil

from inventario.models import Product, Sale, PurchaseOrder, InventoryAlert, Supplier, Category


class Command(BaseCommand):
    help = "Elimina datos de ejemplo (productos, ventas, órdenes, alertas) y borra modelos en ml_models."

    def add_arguments(self, parser):
        parser.add_argument(
            "--keep-catalog",
            action="store_true",
            help="Conserva Catálogos (Categorías y Proveedores)",
        )
        parser.add_argument(
            "--only-models",
            action="store_true",
            help="Solo elimina archivos de modelos en la carpeta ml_models",
        )

    def handle(self, *args, **options):
        only_models = options.get("only_models", False)
        keep_catalog = options.get("keep_catalog", False)

        removed_models_files = self._clear_ml_models()

        if only_models:
            self.stdout.write(self.style.SUCCESS(f"Archivos de modelos eliminados: {removed_models_files}"))
            return

        with transaction.atomic():
            Sale.objects.all().delete()
            PurchaseOrder.objects.all().delete()
            InventoryAlert.objects.all().delete()
            Product.objects.all().delete()

            if not keep_catalog:
                Supplier.objects.all().delete()
                Category.objects.all().delete()

        self.stdout.write(self.style.SUCCESS(
            f"Datos eliminados. Archivos de modelos borrados: {removed_models_files}"
        ))

    def _clear_ml_models(self) -> int:
        from django.conf import settings
        models_dir = os.path.join(settings.BASE_DIR, 'ml_models')
        if not os.path.isdir(models_dir):
            return 0
        removed = 0
        for name in os.listdir(models_dir):
            path = os.path.join(models_dir, name)
            try:
                if os.path.isfile(path):
                    os.remove(path)
                    removed += 1
                elif os.path.isdir(path):
                    shutil.rmtree(path)
                    removed += 1
            except Exception:
                continue
        return removed



