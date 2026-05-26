# Configurador de PCs (PHP + MongoDB)

CRUD de un configurador de computadoras. Permite armar equipos eligiendo
componentes y administrar marcas, categorias, clientes y pedidos. Las
relaciones entre colecciones se resuelven con `$lookup` (el "join" de MongoDB).

## Requisitos (Mac con chip M2 / Apple Silicon)

No se usa XAMPP. Todo es nativo ARM con Homebrew y el servidor que ya trae PHP.

```bash
# 1. Homebrew (si no lo tienes)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 2. PHP y Composer
brew install php composer

# 3. MongoDB Community y la shell
brew tap mongodb/brew
brew install mongodb-community mongosh
brew services start mongodb-community

# 4. Extension de Mongo para PHP
pecl install mongodb
# Verifica que aparezca "mongodb":
php -m | grep mongodb
```

Si `php -m | grep mongodb` no muestra nada, agrega esta linea al `php.ini`
(la ruta sale con `php --ini`) y reinicia la terminal:

```
extension=mongodb.so
```

## Instalar el proyecto

```bash
cd configurador-pc
composer install        # baja la libreria mongodb/mongodb a vendor/
php seed.php            # crea las colecciones y carga datos de ejemplo
```

## Correr

```bash
php -S localhost:8000 -t public
```

Abre http://localhost:8000

## Colecciones

- `marcas` (marca de los componentes)
- `categorias` (tipo de armado: gaming, oficina, etc)
- `componentes` -> referencia a `marcas`
- `computadoras` -> referencia a `categorias` y a varios `componentes` (muchos a muchos)
- `clientes`
- `pedidos` -> referencia a `clientes` y a `computadoras`

## Donde estan los joins ($lookup)

- `public/pages/componentes.php`: componente + su marca
- `public/pages/computadoras.php`: armado + categoria + componentes (con marca anidada)
- `public/pages/pedidos.php`: pedido + cliente + computadora
- `public/pages/inicio.php`: resumen de armados con su categoria
