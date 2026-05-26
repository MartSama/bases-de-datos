<?php

require_once __DIR__ . '/../src/db.php';

$paginas = [
    'inicio'       => 'Inicio',
    'configurador' => 'Configurador',
    'computadoras' => 'Armados',
    'componentes'  => 'Componentes',
    'marcas'       => 'Marcas',
    'categorias'   => 'Categorias',
    'clientes'     => 'Clientes',
    'pedidos'      => 'Pedidos',
];

$page = $_GET['page'] ?? 'inicio';
if (!isset($paginas[$page])) {
    $page = 'inicio';
}

// Se ejecuta la pagina dentro de un buffer. Asi puede hacer redirecciones
// (header Location) antes de que se mande nada de HTML.
ob_start();
require __DIR__ . "/pages/$page.php";
$contenido = ob_get_clean();

require __DIR__ . '/partials/header.php';
echo $contenido;
require __DIR__ . '/partials/footer.php';
