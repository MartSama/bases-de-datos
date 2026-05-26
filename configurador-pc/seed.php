<?php

// Llena la base con datos de ejemplo. Se puede correr varias veces:
// borra las colecciones antes de volver a insertar.
// Uso:  php seed.php

require_once __DIR__ . '/src/db.php';

$db = base();

foreach (['marcas', 'categorias', 'componentes', 'computadoras', 'clientes', 'pedidos'] as $c) {
    $db->selectCollection($c)->drop();
}

// Marcas
$marcasData = [
    ['nombre' => 'Intel',    'pais' => 'Estados Unidos', 'sitio_web' => 'intel.com'],
    ['nombre' => 'AMD',      'pais' => 'Estados Unidos', 'sitio_web' => 'amd.com'],
    ['nombre' => 'NVIDIA',   'pais' => 'Estados Unidos', 'sitio_web' => 'nvidia.com'],
    ['nombre' => 'Corsair',  'pais' => 'Estados Unidos', 'sitio_web' => 'corsair.com'],
    ['nombre' => 'Samsung',  'pais' => 'Corea del Sur',  'sitio_web' => 'samsung.com'],
    ['nombre' => 'ASUS',     'pais' => 'Taiwan',         'sitio_web' => 'asus.com'],
    ['nombre' => 'Kingston', 'pais' => 'Estados Unidos', 'sitio_web' => 'kingston.com'],
    ['nombre' => 'Seasonic', 'pais' => 'Taiwan',         'sitio_web' => 'seasonic.com'],
    ['nombre' => 'NZXT',     'pais' => 'Estados Unidos', 'sitio_web' => 'nzxt.com'],
];
$resMarcas = col('marcas')->insertMany($marcasData);
$marca = [];
foreach ($resMarcas->getInsertedIds() as $i => $id) {
    $marca[$marcasData[$i]['nombre']] = $id;
}

// Categorias de armado
$categoriasData = [
    ['nombre' => 'Gaming',      'descripcion' => 'Equipos enfocados en videojuegos de alto rendimiento'],
    ['nombre' => 'Oficina',     'descripcion' => 'Equipos para tareas de productividad y uso diario'],
    ['nombre' => 'Workstation', 'descripcion' => 'Equipos para diseno, render y trabajo profesional'],
    ['nombre' => 'Streaming',   'descripcion' => 'Equipos para transmitir y crear contenido'],
    ['nombre' => 'Economica',   'descripcion' => 'Equipos de bajo costo para necesidades basicas'],
];
$resCat = col('categorias')->insertMany($categoriasData);
$cat = [];
foreach ($resCat->getInsertedIds() as $i => $id) {
    $cat[$categoriasData[$i]['nombre']] = $id;
}

// Componentes (cada uno referencia una marca)
$componentesData = [
    ['nombre' => 'Core i5-13400F',      'tipo' => 'CPU',           'marca_id' => $marca['Intel'],    'precio' => 4200,  'specs' => '10 nucleos, 2.5 GHz base', 'stock' => 20],
    ['nombre' => 'Core i7-13700K',      'tipo' => 'CPU',           'marca_id' => $marca['Intel'],    'precio' => 8900,  'specs' => '16 nucleos, 3.4 GHz base', 'stock' => 12],
    ['nombre' => 'Ryzen 5 7600',        'tipo' => 'CPU',           'marca_id' => $marca['AMD'],      'precio' => 4800,  'specs' => '6 nucleos, 3.8 GHz base',  'stock' => 18],
    ['nombre' => 'Ryzen 7 7800X3D',     'tipo' => 'CPU',           'marca_id' => $marca['AMD'],      'precio' => 9500,  'specs' => '8 nucleos, cache 3D',      'stock' => 9],
    ['nombre' => 'GeForce RTX 4060',    'tipo' => 'GPU',           'marca_id' => $marca['NVIDIA'],   'precio' => 6500,  'specs' => '8 GB GDDR6',               'stock' => 15],
    ['nombre' => 'GeForce RTX 4070',    'tipo' => 'GPU',           'marca_id' => $marca['NVIDIA'],   'precio' => 12500, 'specs' => '12 GB GDDR6X',             'stock' => 7],
    ['nombre' => 'Vengeance 16GB',      'tipo' => 'RAM',           'marca_id' => $marca['Corsair'],  'precio' => 1100,  'specs' => 'DDR5 5200 MHz',            'stock' => 40],
    ['nombre' => 'Fury 32GB',           'tipo' => 'RAM',           'marca_id' => $marca['Kingston'], 'precio' => 2200,  'specs' => 'DDR5 6000 MHz',            'stock' => 25],
    ['nombre' => '980 Pro 1TB',         'tipo' => 'Almacenamiento','marca_id' => $marca['Samsung'],  'precio' => 1900,  'specs' => 'SSD NVMe Gen4',            'stock' => 30],
    ['nombre' => '990 Pro 2TB',         'tipo' => 'Almacenamiento','marca_id' => $marca['Samsung'],  'precio' => 3600,  'specs' => 'SSD NVMe Gen4',            'stock' => 14],
    ['nombre' => 'ROG B650-A',          'tipo' => 'Motherboard',   'marca_id' => $marca['ASUS'],     'precio' => 4300,  'specs' => 'Socket AM5, ATX',          'stock' => 16],
    ['nombre' => 'Prime B760M',         'tipo' => 'Motherboard',   'marca_id' => $marca['ASUS'],     'precio' => 2700,  'specs' => 'Socket LGA1700, mATX',     'stock' => 22],
    ['nombre' => 'Focus GX-750',        'tipo' => 'Fuente',        'marca_id' => $marca['Seasonic'], 'precio' => 2400,  'specs' => '750W 80+ Gold',            'stock' => 19],
    ['nombre' => 'RM850e',              'tipo' => 'Fuente',        'marca_id' => $marca['Corsair'],  'precio' => 2800,  'specs' => '850W 80+ Gold',            'stock' => 11],
    ['nombre' => 'H5 Flow',             'tipo' => 'Gabinete',      'marca_id' => $marca['NZXT'],     'precio' => 1800,  'specs' => 'ATX media torre',          'stock' => 13],
    ['nombre' => 'Kraken 240',          'tipo' => 'Disipador',     'marca_id' => $marca['NZXT'],     'precio' => 2600,  'specs' => 'Liquida 240mm',            'stock' => 10],
];
$resComp = col('componentes')->insertMany($componentesData);
$comp = [];
foreach ($resComp->getInsertedIds() as $i => $id) {
    $comp[$componentesData[$i]['nombre']] = $id;
}

// Funcion para calcular el total de un armado a partir de sus componentes.
$preciosPorNombre = [];
foreach ($componentesData as $c) {
    $preciosPorNombre[$c['nombre']] = $c['precio'];
}
$armar = function (array $items) use ($comp, $preciosPorNombre) {
    $lista = [];
    $total = 0;
    foreach ($items as $nombre => $cantidad) {
        $lista[] = ['componente_id' => $comp[$nombre], 'cantidad' => $cantidad];
        $total += $preciosPorNombre[$nombre] * $cantidad;
    }
    return [$lista, $total];
};

// Computadoras (armados). Relacion muchos a muchos con componentes.
list($c1, $t1) = $armar(['Core i7-13700K' => 1, 'GeForce RTX 4070' => 1, 'Fury 32GB' => 1, '990 Pro 2TB' => 1, 'Prime B760M' => 1, 'RM850e' => 1, 'H5 Flow' => 1, 'Kraken 240' => 1]);
list($c2, $t2) = $armar(['Ryzen 5 7600' => 1, 'GeForce RTX 4060' => 1, 'Vengeance 16GB' => 2, '980 Pro 1TB' => 1, 'ROG B650-A' => 1, 'Focus GX-750' => 1, 'H5 Flow' => 1]);
list($c3, $t3) = $armar(['Core i5-13400F' => 1, 'Vengeance 16GB' => 1, '980 Pro 1TB' => 1, 'Prime B760M' => 1, 'Focus GX-750' => 1, 'H5 Flow' => 1]);
list($c4, $t4) = $armar(['Ryzen 7 7800X3D' => 1, 'GeForce RTX 4070' => 1, 'Fury 32GB' => 2, '990 Pro 2TB' => 1, 'ROG B650-A' => 1, 'RM850e' => 1, 'H5 Flow' => 1, 'Kraken 240' => 1]);

$computadorasData = [
    ['nombre' => 'Titan Gamer',     'categoria_id' => $cat['Gaming'],      'componentes' => $c1, 'precio_total' => $t1, 'descripcion' => 'Equipo gama alta para juegos en 1440p'],
    ['nombre' => 'Creador Pro',     'categoria_id' => $cat['Streaming'],   'componentes' => $c2, 'precio_total' => $t2, 'descripcion' => 'Balance entre juego y transmision'],
    ['nombre' => 'Oficina Basica',  'categoria_id' => $cat['Oficina'],     'componentes' => $c3, 'precio_total' => $t3, 'descripcion' => 'Equipo ligero para trabajo diario'],
    ['nombre' => 'Estudio X3D',     'categoria_id' => $cat['Workstation'], 'componentes' => $c4, 'precio_total' => $t4, 'descripcion' => 'Maximo rendimiento para render y diseno'],
];
$resPC = col('computadoras')->insertMany($computadorasData);
$pc = [];
foreach ($resPC->getInsertedIds() as $i => $id) {
    $pc[$computadorasData[$i]['nombre']] = $id;
}

// Clientes
$clientesData = [
    ['nombre' => 'Ana Torres',     'email' => 'ana.torres@correo.com',   'telefono' => '5512345678'],
    ['nombre' => 'Luis Martinez',  'email' => 'luis.mtz@correo.com',     'telefono' => '5523456789'],
    ['nombre' => 'Sofia Ramirez',  'email' => 'sofia.rmz@correo.com',    'telefono' => '5534567890'],
    ['nombre' => 'Diego Herrera',  'email' => 'diego.herrera@correo.com','telefono' => '5545678901'],
];
$resCli = col('clientes')->insertMany($clientesData);
$cli = [];
foreach ($resCli->getInsertedIds() as $i => $id) {
    $cli[$clientesData[$i]['nombre']] = $id;
}

// Pedidos (relacionan cliente con computadora)
$pedidosData = [
    ['cliente_id' => $cli['Ana Torres'],    'computadora_id' => $pc['Titan Gamer'],    'fecha' => '2026-05-10', 'estado' => 'entregado',  'total' => $t1],
    ['cliente_id' => $cli['Luis Martinez'], 'computadora_id' => $pc['Oficina Basica'], 'fecha' => '2026-05-15', 'estado' => 'enviado',    'total' => $t3],
    ['cliente_id' => $cli['Sofia Ramirez'], 'computadora_id' => $pc['Estudio X3D'],    'fecha' => '2026-05-20', 'estado' => 'procesando', 'total' => $t4],
    ['cliente_id' => $cli['Ana Torres'],    'computadora_id' => $pc['Creador Pro'],    'fecha' => '2026-05-24', 'estado' => 'procesando', 'total' => $t2],
];
col('pedidos')->insertMany($pedidosData);

echo "Datos cargados:\n";
echo '  marcas: '       . count($marcasData)       . "\n";
echo '  categorias: '   . count($categoriasData)   . "\n";
echo '  componentes: '  . count($componentesData)  . "\n";
echo '  computadoras: ' . count($computadorasData) . "\n";
echo '  clientes: '     . count($clientesData)     . "\n";
echo '  pedidos: '      . count($pedidosData)      . "\n";
