import os
import json
import sys 

import vertexai
from vertexai.generative_models import GenerativeModel

PROJECT_ID = "stone-poetry-473315-a9"
LOCATION = "us-central1"

PRIMARY_MODEL = "gemini-1.5-flash"

# Colores ANSI
class Colors:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    
    # Colores básicos
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    
    # Colores de fondo
    BG_RED = '\033[101m'
    BG_GREEN = '\033[102m'
    BG_YELLOW = '\033[103m'
    BG_BLUE = '\033[104m'
    BG_MAGENTA = '\033[105m'
    BG_CYAN = '\033[106m'


def _django_bootstrap() -> None:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    # Suprimir logs de gRPC/Vertex ruidosos en consola
    os.environ.setdefault("GRPC_VERBOSITY", "NONE")
    os.environ.setdefault("GRPC_TRACE", "")
    import django

    django.setup()

def list_products(only_available: bool = False) -> list[dict]:
    from productos.models import Product

    qs = Product.objects.all().order_by("name")
    if only_available:
        qs = qs.filter(quantity__gt=0)
    return [{"id": p.id, "name": p.name, "quantity": p.quantity, "description": p.description} for p in qs]

def add_product(name: str, quantity: int = 0, description: str = "") -> dict:
    from productos.models import Product

    obj = Product.objects.create(name=name, quantity=max(0, quantity), description=description)
    return {"id": obj.id, "name": obj.name, "quantity": obj.quantity, "description": obj.description}

def update_product(product_id: int | None, name: str | None = None, quantity: int | None = None, description: str | None = None) -> dict:
    from productos.models import Product

    if product_id is None and name is None:
        raise ValueError("Proporciona 'product_id' o 'name' para actualizar.")
    obj = None
    if product_id is not None:
        obj = Product.objects.filter(id=product_id).first()
    if obj is None and name is not None:
        # Búsqueda flexible por nombre (contiene)
        obj = Product.objects.filter(name__icontains=name).first()
    if obj is None:
        raise ValueError("Producto no encontrado para actualizar.")

    if name is not None:
        obj.name = name
    if quantity is not None:
        obj.quantity = max(0, quantity)
    if description is not None:
        obj.description = description
    obj.save()
    return {"id": obj.id, "name": obj.name, "quantity": obj.quantity, "description": obj.description}


def delete_product(product_id: int | None = None, name: str | None = None) -> int:
    from productos.models import Product

    if product_id is not None:
        return Product.objects.filter(id=product_id).delete()[0]
    if name is not None:
        # Búsqueda flexible por nombre (contiene)
        return Product.objects.filter(name__icontains=name).delete()[0]
    raise ValueError("Proporciona 'product_id' o 'name' para eliminar.")


SYSTEM_INSTRUCTIONS = (
    "Eres un asistente que convierte instrucciones en una orden JSON. "
    "No expliques, solo responde con JSON válido. Campos: \n"
    "{\"action\": one_of['listar','listar_disponibles','añadir','actualizar','eliminar','salir'],\n"
    " \"name\": string|null, \"quantity\": int|null, \"description\": string|null, \"id\": int|null} \n"
    "Ejemplos: \n"
    "- 'lista todo' -> {\"action\":\"listar\", \"name\":null, \"quantity\":null, \"description\":null, \"id\":null}\n"
    "- 'qué hay disponible' -> {\"action\":\"listar_disponibles\", ...}\n"
    "- 'añade 5 teclados mecánicos' -> {\"action\":\"añadir\", \"name\":\"Teclado mecánico\", \"quantity\":5, \"description\":null, \"id\":null}\n"
    "- 'actualiza monitor 24 a 12' -> {\"action\":\"actualizar\", \"name\":\"Monitor 24 pulgadas\", \"quantity\":12, \"description\":null, \"id\":null}\n"
    "- 'elimina mouse inalámbrico' -> {\"action\":\"eliminar\", \"name\":\"Mouse Inalámbrico\", \"quantity\":null, \"description\":null, \"id\":null}\n"
    "- 'salir' -> {\"action\":\"salir\", ...}\n"
)


def call_llm(user_text: str) -> dict:
    vertexai.init(project=PROJECT_ID, location=LOCATION)
    model = GenerativeModel(PRIMARY_MODEL)
    prompt = f"{SYSTEM_INSTRUCTIONS}\nUsuario: {user_text}\nJSON:"
    resp = model.generate_content(prompt)
    text = resp.text if hasattr(resp, "text") else str(resp)
    # Intentar extraer el primer bloque JSON
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        text = text[start : end + 1]
    return json.loads(text)

def clear_screen():
    """Limpia la pantalla de la consola"""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header() -> None:
    """Imprime el encabezado del sistema"""
    print(f"\n{Colors.BOLD}{Colors.MAGENTA}{'🏪'*25}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}        SISTEMA DE INVENTARIO INTELIGENTE{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.MAGENTA}{'🏪'*25}{Colors.RESET}\n")


def print_capabilities() -> None:
    """Imprime el menú de opciones disponibles"""
    print(f"\n{Colors.BOLD}{Colors.YELLOW}{'='*70}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.YELLOW}📋 MENÚ DE OPCIONES{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.YELLOW}{'='*70}{Colors.RESET}")
    print(f"{Colors.CYAN}  1.{Colors.RESET} 🔍 {Colors.GREEN}inventario{Colors.RESET}  - Ver todo el inventario")
    print(f"{Colors.CYAN}  2.{Colors.RESET} ➕ {Colors.GREEN}añadir{Colors.RESET}      - Agregar nuevo producto") 
    print(f"{Colors.CYAN}  3.{Colors.RESET} ✏️  {Colors.GREEN}actualizar{Colors.RESET}  - Modificar producto existente")
    print(f"{Colors.CYAN}  4.{Colors.RESET} 🗑️  {Colors.GREEN}eliminar{Colors.RESET}    - Borrar producto")
    print(f"{Colors.CYAN}  5.{Colors.RESET} 🏠 {Colors.GREEN}menu{Colors.RESET}        - Volver a este menú")
    print(f"{Colors.CYAN}  6.{Colors.RESET} 🚪 {Colors.GREEN}salir{Colors.RESET}       - Salir del sistema")
    print(f"{Colors.BOLD}{Colors.YELLOW}{'='*70}{Colors.RESET}")
    print(f"{Colors.MAGENTA}💡 Tip:{Colors.RESET} {Colors.WHITE}Puedes escribir de forma natural:{Colors.RESET}")
    print(f"   {Colors.CYAN}• \"quiero añadir algo\"  • \"voy a actualizar un producto\"{Colors.RESET}")
    print(f"   {Colors.CYAN}• \"elimina algo\"       • \"muéstrame el inventario\"{Colors.RESET}\n")


def show_inventory() -> None:
    """Muestra el inventario actual"""
    rows = list_products(only_available=False)
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'─'*70}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}📦 INVENTARIO ACTUAL{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'─'*70}{Colors.RESET}")
    if not rows:
        print(f"{Colors.YELLOW}   (El inventario está vacío){Colors.RESET}")
    else:
        for r in rows:
            if r['quantity'] > 0:
                status = f"{Colors.GREEN}✅{Colors.RESET}"
                qty_color = Colors.GREEN
            else:
                status = f"{Colors.RED}❌{Colors.RESET}"
                qty_color = Colors.RED
            print(f"   {status} {Colors.CYAN}#{r['id']:2d}:{Colors.RESET} {Colors.WHITE}{r['name']:<25}{Colors.RESET} {qty_color}({r['quantity']:3d} unidades){Colors.RESET} - {Colors.YELLOW}{r['description']}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'─'*70}{Colors.RESET}\n")


def main() -> None:
    _django_bootstrap()
    
    # Limpiar pantalla e imprimir encabezado inicial
    clear_screen()
    print_header()
    show_inventory()
    print_capabilities()
    
    print(f"{Colors.BOLD}{Colors.CYAN}💬 ¿Qué deseas hacer? (escribe un número o habla natural){Colors.RESET}")
    
    while True:
        try:
            user_text = input(f"{Colors.BOLD}{Colors.MAGENTA}➤ {Colors.RESET}").strip()
        except EOFError:
            break
        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}⚠️  Operación cancelada{Colors.RESET}")
            continue
            
        if not user_text:
            continue

        # Permitir comandos por número
        if user_text == "1":
            user_text = "inventario"
        elif user_text == "2":
            user_text = "añadir"
        elif user_text == "3":
            user_text = "actualizar"
        elif user_text == "4":
            user_text = "eliminar"
        elif user_text == "5" or user_text.lower() in ["menu", "menú"]:
            clear_screen()
            print_header()
            show_inventory()
            print_capabilities()
            continue
        elif user_text == "6" or user_text.lower() in ["salir", "exit", "quit"]:
            print(f"\n{Colors.BOLD}{Colors.GREEN}👋 ¡Hasta luego! Que tengas un excelente día.{Colors.RESET}\n")
            break

        try:
            intent = call_llm(user_text)
        except Exception as e:
            print(f"{Colors.RED}❌ No pude interpretar la instrucción: {e}{Colors.RESET}")
            print(f"{Colors.YELLOW}💡 Tip: Escribe 'menu' para ver las opciones{Colors.RESET}")
            continue

        action = intent.get("action")
        name = intent.get("name")
        quantity = intent.get("quantity")
        description = intent.get("description")
        pid = intent.get("id")

        try:
            if action == "salir":
                print(f"\n{Colors.BOLD}{Colors.GREEN}👋 ¡Hasta luego! Que tengas un excelente día.{Colors.RESET}\n")
                break
            if action is None:
                print(f"{Colors.YELLOW}❓ No entendí la acción. Intenta de nuevo.{Colors.RESET}")
            elif action == "menu":
                clear_screen()
                print_header()
                show_inventory()
                print_capabilities()
            elif action == "listar":
                show_inventory()
                input(f"{Colors.CYAN}Presiona ENTER para continuar...{Colors.RESET}")
                clear_screen()
                print_header()
                show_inventory()
                print_capabilities()
            elif action == "añadir":
                print(f"\n{Colors.BOLD}{Colors.GREEN}{'─'*50}{Colors.RESET}")
                print(f"{Colors.BOLD}{Colors.GREEN}➕ AGREGAR NUEVO PRODUCTO{Colors.RESET}")
                print(f"{Colors.BOLD}{Colors.GREEN}{'─'*50}{Colors.RESET}")
                
                try:
                    if not name:
                        name = input(f"{Colors.CYAN}📝 Nombre del producto{Colors.RESET} (o 'cancelar'): ").strip()
                        if name.lower() == 'cancelar':
                            print(f"{Colors.YELLOW}⚠️  Operación cancelada{Colors.RESET}")
                            continue
                    while not name:
                        name = input(f"{Colors.CYAN}📝 Nombre del producto{Colors.RESET}: ").strip()
                    
                    if not isinstance(quantity, int):
                        while True:
                            qtxt = input(f"{Colors.CYAN}🔢 Cantidad{Colors.RESET} (o 'cancelar'): ").strip()
                            if qtxt.lower() == 'cancelar':
                                print(f"{Colors.YELLOW}⚠️  Operación cancelada{Colors.RESET}")
                                raise ValueError("Cancelado")
                            try:
                                quantity = int(qtxt)
                                break
                            except ValueError:
                                print(f"{Colors.RED}   ❌ Ingresa un número entero válido{Colors.RESET}")
                    
                    description = input(f"{Colors.CYAN}📄 Descripción{Colors.RESET} (opcional): ").strip()
                    
                    created = add_product(name=name, quantity=int(quantity), description=description)
                    print(f"\n{Colors.BOLD}{Colors.GREEN}✅ ¡PRODUCTO AGREGADO EXITOSAMENTE!{Colors.RESET}")
                    print(f"{Colors.CYAN}   ID:{Colors.RESET} {created['id']}")
                    print(f"{Colors.CYAN}   Nombre:{Colors.RESET} {created['name']}")
                    print(f"{Colors.CYAN}   Cantidad:{Colors.RESET} {created['quantity']}")
                    print(f"{Colors.CYAN}   Descripción:{Colors.RESET} {created['description']}")
                    print(f"{Colors.BOLD}{Colors.GREEN}{'─'*50}{Colors.RESET}\n")
                    
                    input(f"{Colors.CYAN}Presiona ENTER para continuar...{Colors.RESET}")
                    clear_screen()
                    print_header()
                    show_inventory()
                    print_capabilities()
                except ValueError as e:
                    if str(e) != "Cancelado":
                        print(f"{Colors.RED}❌ Error: {e}{Colors.RESET}")
                    continue
                    
            elif action == "actualizar":
                print(f"\n{Colors.BOLD}{Colors.YELLOW}{'─'*50}{Colors.RESET}")
                print(f"{Colors.BOLD}{Colors.YELLOW}✏️  ACTUALIZAR PRODUCTO{Colors.RESET}")
                print(f"{Colors.BOLD}{Colors.YELLOW}{'─'*50}{Colors.RESET}")
                
                # Mostrar productos actuales
                show_inventory()
                
                try:
                    if pid is None:
                        while True:
                            id_txt = input(f"{Colors.CYAN}🆔 ID del producto a actualizar{Colors.RESET} (o 'cancelar'): ").strip()
                            if id_txt.lower() == 'cancelar':
                                print(f"{Colors.YELLOW}⚠️  Operación cancelada{Colors.RESET}")
                                raise ValueError("Cancelado")
                            try:
                                pid = int(id_txt)
                                break
                            except ValueError:
                                print(f"{Colors.RED}   ❌ Ingresa un número entero válido{Colors.RESET}")
                    
                    if not name:
                        name = input(f"{Colors.CYAN}📝 Nuevo nombre{Colors.RESET} (o 'cancelar'): ").strip()
                        if name.lower() == 'cancelar':
                            print(f"{Colors.YELLOW}⚠️  Operación cancelada{Colors.RESET}")
                            raise ValueError("Cancelado")
                        while not name:
                            name = input(f"{Colors.CYAN}📝 Nuevo nombre{Colors.RESET}: ").strip()
                    
                    if not isinstance(quantity, int):
                        while True:
                            qtxt = input(f"{Colors.CYAN}🔢 Nueva cantidad{Colors.RESET} (o 'cancelar'): ").strip()
                            if qtxt.lower() == 'cancelar':
                                print(f"{Colors.YELLOW}⚠️  Operación cancelada{Colors.RESET}")
                                raise ValueError("Cancelado")
                            try:
                                quantity = int(qtxt)
                                break
                            except ValueError:
                                print(f"{Colors.RED}   ❌ Ingresa un número entero válido{Colors.RESET}")
                    
                    description = input(f"{Colors.CYAN}📄 Nueva descripción{Colors.RESET} (opcional): ").strip()
                    
                    updated = update_product(product_id=pid, name=name, quantity=int(quantity), description=description)
                    print(f"\n{Colors.BOLD}{Colors.GREEN}✅ ¡PRODUCTO ACTUALIZADO EXITOSAMENTE!{Colors.RESET}")
                    print(f"{Colors.CYAN}   ID:{Colors.RESET} {updated['id']}")
                    print(f"{Colors.CYAN}   Nombre:{Colors.RESET} {updated['name']}")
                    print(f"{Colors.CYAN}   Cantidad:{Colors.RESET} {updated['quantity']}")
                    print(f"{Colors.CYAN}   Descripción:{Colors.RESET} {updated['description']}")
                    print(f"{Colors.BOLD}{Colors.YELLOW}{'─'*50}{Colors.RESET}\n")
                    
                    input(f"{Colors.CYAN}Presiona ENTER para continuar...{Colors.RESET}")
                    clear_screen()
                    print_header()
                    show_inventory()
                    print_capabilities()
                except ValueError as e:
                    if str(e) != "Cancelado":
                        print(f"{Colors.RED}❌ Error: {e}{Colors.RESET}")
                    continue
                    
            elif action == "eliminar":
                print(f"\n{Colors.BOLD}{Colors.RED}{'─'*50}{Colors.RESET}")
                print(f"{Colors.BOLD}{Colors.RED}🗑️  ELIMINAR PRODUCTO{Colors.RESET}")
                print(f"{Colors.BOLD}{Colors.RED}{'─'*50}{Colors.RESET}")
                
                # Mostrar productos actuales
                show_inventory()
                
                try:
                    if pid is None and not name:
                        sel = input(f"{Colors.CYAN}🆔 ¿Qué producto eliminar? (ID o nombre){Colors.RESET} (o 'cancelar'): ").strip()
                        if sel.lower() == 'cancelar':
                            print(f"{Colors.YELLOW}⚠️  Operación cancelada{Colors.RESET}")
                            continue
                        if sel.isdigit():
                            pid = int(sel)
                        else:
                            name = sel
                    
                    # Confirmación
                    confirm = input(f"{Colors.RED}⚠️  ¿Estás seguro de eliminar este producto? (si/no):{Colors.RESET} ").strip().lower()
                    if confirm not in ['si', 'sí', 's', 'yes', 'y']:
                        print(f"{Colors.YELLOW}⚠️  Operación cancelada{Colors.RESET}")
                        continue
                    
                    deleted = delete_product(product_id=pid, name=name)
                    if deleted:
                        print(f"\n{Colors.BOLD}{Colors.GREEN}✅ ¡PRODUCTO ELIMINADO EXITOSAMENTE!{Colors.RESET}")
                        print(f"{Colors.CYAN}   Productos eliminados: {deleted}{Colors.RESET}")
                        print(f"{Colors.BOLD}{Colors.RED}{'─'*50}{Colors.RESET}\n")
                    else:
                        print(f"\n{Colors.RED}❌ No se encontró el producto a eliminar{Colors.RESET}")
                        print(f"{Colors.BOLD}{Colors.RED}{'─'*50}{Colors.RESET}\n")
                    
                    input(f"{Colors.CYAN}Presiona ENTER para continuar...{Colors.RESET}")
                    clear_screen()
                    print_header()
                    show_inventory()
                    print_capabilities()
                except ValueError as e:
                    print(f"{Colors.RED}❌ Error: {e}{Colors.RESET}")
                    continue
            else:
                print(f"{Colors.YELLOW}❓ No entendí la acción. Escribe 'menu' para ver las opciones{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}❌ Error inesperado: {e}{Colors.RESET}")


if __name__ == "__main__":
    main()


