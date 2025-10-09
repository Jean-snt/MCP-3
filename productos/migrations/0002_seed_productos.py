from django.db import migrations


def seed_products(apps, schema_editor):
    Producto = apps.get_model("productos", "Producto")
    productos = [
        {"nombre": "Teclado Mecánico RGB", "descripcion": "Teclado retroiluminado con switches azules.", "cantidad": 15},
        {"nombre": "Mouse Inalámbrico", "descripcion": "Mouse ergonómico con conexión 2.4GHz.", "cantidad": 30},
        {"nombre": "Monitor 24 pulgadas", "descripcion": "Pantalla Full HD con panel IPS.", "cantidad": 10},
        {"nombre": "Audífonos USB", "descripcion": "Sonido estéreo con micrófono integrado.", "cantidad": 0},
    ]
    for data in productos:
        Producto.objects.get_or_create(nombre=data["nombre"], defaults=data)


def unseed_products(apps, schema_editor):
    Producto = apps.get_model("productos", "Producto")
    Producto.objects.filter(nombre__in=[
        "Teclado Mecánico RGB",
        "Mouse Inalámbrico",
        "Monitor 24 pulgadas",
        "Audífonos USB",
    ]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("productos", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_products, unseed_products),
    ]




