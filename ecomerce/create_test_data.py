import os
import django

# Configurar Django - CORREGIDO: usar 'ecomerce' en lugar de 'ecommerce'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecomerce.settings')
django.setup()

from products.models import Category, Product
from django.contrib.auth import get_user_model

# Obtener el modelo de usuario personalizado
User = get_user_model()

def create_test_data():
    print("🚀 Iniciando creación de datos de prueba...")
    
    # Crear categorías
    categories_data = [
        {'name': 'Electrónicos', 'description': 'Dispositivos electrónicos y tecnología'},
        {'name': 'Ropa', 'description': 'Prendas de vestir y accesorios'},
        {'name': 'Hogar', 'description': 'Artículos para el hogar y decoración'},
        {'name': 'Libros', 'description': 'Libros y literatura'},
        {'name': 'Deportes', 'description': 'Artículos deportivos y fitness'},
        {'name': 'Productos Financieros', 'description': 'Servicios financieros, seguros e inversiones'},
    ]
    
    print("\n📁 Creando categorías...")
    for cat_data in categories_data:
        category, created = Category.objects.get_or_create(
            name=cat_data['name'],
            defaults={'description': cat_data['description']}
        )
        if created:
            print(f"   ✅ Categoría creada: {category.name}")
        else:
            print(f"   ℹ️  Categoría ya existe: {category.name}")
    
    # Obtener categorías
    try:
        electronics = Category.objects.get(name='Electrónicos')
        ropa = Category.objects.get(name='Ropa')
        hogar = Category.objects.get(name='Hogar')
        financial = Category.objects.get(name='Productos Financieros')
        deportes = Category.objects.get(name='Deportes')
        print("   ✅ Todas las categorías obtenidas correctamente")
    except Category.DoesNotExist as e:
        print(f"   ❌ Error al obtener categorías: {e}")
        return
    
    # Crear productos - Electrónicos
    electronics_products = [
        {
            'name': 'Smartphone Premium',
            'description': 'Smartphone de última generación con cámara profesional de 108MP, procesador octa-core y 256GB de almacenamiento',
            'price': 599.99,
            'category': electronics,
            'stock': 15
        },
        {
            'name': 'Laptop Gaming',
            'description': 'Laptop para gaming con procesador Intel i7, RTX 4060, 16GB RAM y SSD 1TB',
            'price': 1299.99,
            'category': electronics,
            'stock': 8
        },
        {
            'name': 'Auriculares Bluetooth',
            'description': 'Auriculares inalámbricos con cancelación de ruido activa y batería de 30 horas',
            'price': 149.99,
            'category': electronics,
            'stock': 25
        },
        {
            'name': 'Smartwatch Pro',
            'description': 'Reloj inteligente con GPS, monitor de salud 24/7 y resistencia al agua',
            'price': 249.99,
            'category': electronics,
            'stock': 12
        },
        {
            'name': 'Tablet 11 pulgadas',
            'description': 'Tablet con pantalla OLED, procesador A15 Bionic y compatibilidad con stylus',
            'price': 449.99,
            'category': electronics,
            'stock': 20
        },
    ]
    
    # Crear productos - Ropa
    ropa_products = [
        {
            'name': 'Camiseta Casual Premium',
            'description': 'Camiseta de algodón 100% orgánico con corte moderno y colores variados',
            'price': 25.99,
            'category': ropa,
            'stock': 50
        },
        {
            'name': 'Jeans Clásicos',
            'description': 'Jeans de mezclilla premium con corte recto y acabado stone wash',
            'price': 89.99,
            'category': ropa,
            'stock': 30
        },
        {
            'name': 'Chaqueta Deportiva',
            'description': 'Chaqueta impermeable ideal para actividades al aire libre',
            'price': 129.99,
            'category': ropa,
            'stock': 15
        },
    ]
    
    # Crear productos - Hogar
    hogar_products = [
        {
            'name': 'Cafetera Automática',
            'description': 'Cafetera programable con molinillo integrado y sistema de filtrado avanzado',
            'price': 199.99,
            'category': hogar,
            'stock': 10
        },
        {
            'name': 'Aspiradora Robot',
            'description': 'Robot aspirador inteligente con mapeo láser y control por app',
            'price': 299.99,
            'category': hogar,
            'stock': 8
        },
    ]
    
    # Crear productos - Productos Financieros (Davivienda Style)
    financial_products = [
        {
            'name': 'Cuenta de Ahorros DaviPlata',
            'description': 'Cuenta de ahorros digital sin costo de manejo, con tarjeta débito y acceso a todos los canales digitales',
            'price': 0.00,  # Sin costo
            'category': financial,
            'stock': 100
        },
        {
            'name': 'CDT Mi Inversión',
            'description': 'Certificado de Depósito a Término con tasa de interés competitiva del 12% EA. Inversión mínima desde $1,000,000',
            'price': 1000000.00,
            'category': financial,
            'stock': 50
        },
        {
            'name': 'Crédito de Libre Inversión',
            'description': 'Crédito personal hasta $50,000,000 con tasa fija del 15% EA, aprobación express y desembolso inmediato',
            'price': 5000000.00,  # Monto promedio
            'category': financial,
            'stock': 25
        },
        {
            'name': 'Tarjeta de Crédito Visa Gold',
            'description': 'Tarjeta de crédito con cupo hasta $10,000,000, cashback del 2%, sin cuota de manejo primer año',
            'price': 150000.00,  # Cuota de manejo anual
            'category': financial,
            'stock': 40
        },
        {
            'name': 'Seguro de Vida Protegido',
            'description': 'Seguro de vida con cobertura hasta $200,000,000, incluye invalidez y enfermedades graves',
            'price': 89900.00,  # Prima mensual
            'category': financial,
            'stock': 75
        },
        {
            'name': 'Seguro Todo Riesgo Vehículo',
            'description': 'Seguro automotriz con cobertura integral: responsabilidad civil, daños propios, robo, grúa 24/7',
            'price': 234500.00,  # Prima mensual promedio
            'category': financial,
            'stock': 60
        },
        {
            'name': 'Fondo de Inversión Renta Fija',
            'description': 'Fondo de inversión en títulos de renta fija con rentabilidad promedio del 10% EA y liquidez diaria',
            'price': 500000.00,  # Inversión mínima
            'category': financial,
            'stock': 30
        },
        {
            'name': 'Crédito Hipotecario VIS',
            'description': 'Crédito hipotecario para vivienda de interés social, hasta 80% de financiación, plazo hasta 20 años',
            'price': 150000000.00,  # Monto promedio
            'category': financial,
            'stock': 15
        },
        {
            'name': 'Plan de Pensión Voluntaria',
            'description': 'Ahorro pensional voluntario con beneficios tributarios y rentabilidad promedio del 8% EA',
            'price': 300000.00,  # Aporte mensual sugerido
            'category': financial,
            'stock': 45
        },
        {
            'name': 'Seguro Hogar Integral',
            'description': 'Protección completa para tu hogar: incendio, robo, terremoto, responsabilidad civil y asistencia',
            'price': 145000.00,  # Prima mensual
            'category': financial,
            'stock': 55
        },
        {
            'name': 'Leasing de Vehículo',
            'description': 'Financiación de vehículo mediante leasing, hasta 90% de financiación, plazo hasta 5 años',
            'price': 80000000.00,  # Valor promedio vehículo
            'category': financial,
            'stock': 20
        },
        {
            'name': 'Tarjeta Empresarial Corporate',
            'description': 'Tarjeta corporativa para empresas con cupo hasta $50,000,000, programa de puntos y beneficios exclusivos',
            'price': 350000.00,  # Cuota de manejo anual
            'category': financial,
            'stock': 25
        },
    ]
    
    # Crear productos - Deportes
    deportes_products = [
        {
            'name': 'Bicicleta Montañera Pro',
            'description': 'Bicicleta de montaña con marco de aluminio, suspensión completa y 21 velocidades',
            'price': 589.99,
            'category': deportes,
            'stock': 12
        },
        {
            'name': 'Set de Pesas Ajustables',
            'description': 'Set completo de pesas ajustables de 5kg a 50kg por mancuerna, ideal para home gym',
            'price': 299.99,
            'category': deportes,
            'stock': 8
        },
    ]
    
    # Combinar todos los productos
    all_products = (
        electronics_products + 
        ropa_products + 
        hogar_products + 
        financial_products + 
        deportes_products
    )
    
    # Crear todos los productos
    print(f"\n📦 Creando {len(all_products)} productos...")
    created_count = 0
    existing_count = 0
    
    for prod_data in all_products:
        try:
            product, created = Product.objects.get_or_create(
                name=prod_data['name'],
                defaults=prod_data
            )
            if created:
                print(f"   ✅ Producto creado: {product.name} - ${product.price:,.2f}")
                created_count += 1
            else:
                print(f"   ℹ️  Producto ya existe: {product.name}")
                existing_count += 1
        except Exception as e:
            print(f"   ❌ Error creando producto {prod_data['name']}: {e}")

    # Crear usuario administrador si no existe
    print(f"\n👥 Creando usuarios...")
    if not User.objects.filter(username='admin').exists():
        try:
            admin_user = User.objects.create_user(
                username='admin',
                email='admin@davivienda.com',
                password='admin123',
                first_name='Administrador',
                last_name='Sistema',
                is_staff=True,
                is_superuser=True
            )
            print(f"   ✅ Usuario administrador creado: {admin_user.username}")
        except Exception as e:
            print(f"   ❌ Error creando admin: {e}")
    else:
        print(f"   ℹ️  Usuario admin ya existe")

    # Crear usuarios de prueba
    test_users_data = [
        {
            'username': 'cliente1',
            'email': 'cliente1@example.com',
            'password': 'cliente123',
            'first_name': 'Juan',
            'last_name': 'Pérez',
            'phone': '+57 310 123 4567',
            'address': 'Calle 100 #20-30, Bogotá'
        },
        {
            'username': 'cliente2',
            'email': 'cliente2@example.com',
            'password': 'cliente123',
            'first_name': 'María',
            'last_name': 'González',
            'phone': '+57 315 987 6543',
            'address': 'Carrera 15 #85-40, Medellín'
        },
        {
            'username': 'asesor_financiero',
            'email': 'asesor@davivienda.com',
            'password': 'asesor123',
            'first_name': 'Carlos',
            'last_name': 'Rodríguez',
            'phone': '+57 318 555 0123',
            'address': 'Centro Financiero Davivienda, Bogotá',
            'is_staff': True
        },
    ]
    
    user_created_count = 0
    for user_data in test_users_data:
        if not User.objects.filter(username=user_data['username']).exists():
            try:
                user = User.objects.create_user(**user_data)
                print(f"   ✅ Usuario creado: {user.username} ({user.get_full_name()})")
                user_created_count += 1
            except Exception as e:
                print(f"   ❌ Error creando usuario {user_data['username']}: {e}")
        else:
            print(f"   ℹ️  Usuario ya existe: {user_data['username']}")

    # Resumen final
    print("\n" + "="*60)
    print("🎉 RESUMEN DE DATOS CREADOS:")
    print("="*60)
    print(f"📁 Total Categorías: {Category.objects.count()}")
    print(f"📦 Total Productos: {Product.objects.count()}")
    print(f"   └── Nuevos productos creados: {created_count}")
    print(f"   └── Productos existentes: {existing_count}")
    print(f"👥 Total Usuarios: {User.objects.count()}")
    print(f"   └── Nuevos usuarios creados: 1 + {user_created_count}")
    
    print(f"\n💰 PRODUCTOS FINANCIEROS DAVIVIENDA:")
    financial_prods = Product.objects.filter(category__name='Productos Financieros')
    for prod in financial_prods:
        if prod.price == 0:
            print(f"   • {prod.name}: GRATIS")
        else:
            print(f"   • {prod.name}: ${prod.price:,.2f}")
    
    print("\n🔐 CREDENCIALES DE ACCESO:")
    print("   👨‍💼 Admin: admin / admin123")
    print("   👤 Cliente1: cliente1 / cliente123")
    print("   👤 Cliente2: cliente2 / cliente123")
    print("   💼 Asesor: asesor_financiero / asesor123")
    print("="*60)

if __name__ == '__main__':
    try:
        create_test_data()
        print("✅ ¡Datos de prueba creados exitosamente!")
        print("\n🚀 Próximos pasos:")
        print("   1. python manage.py runserver")
        print("   2. Ir a http://localhost:8000/admin/")
        print("   3. Probar la API: http://localhost:8000/api/products/")
    except Exception as e:
        print(f"❌ Error durante la ejecución: {e}")
        import traceback
        traceback.print_exc()