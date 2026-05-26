<?php

// Panel de inicio: conteos por coleccion y un resumen de armados
// usando un join ($lookup) con su categoria.

$conteos = [
    'Componentes'  => col('componentes')->countDocuments(),
    'Armados'      => col('computadoras')->countDocuments(),
    'Marcas'       => col('marcas')->countDocuments(),
    'Categorias'   => col('categorias')->countDocuments(),
    'Clientes'     => col('clientes')->countDocuments(),
    'Pedidos'      => col('pedidos')->countDocuments(),
];

$armados = col('computadoras')->aggregate([
    ['$lookup' => [
        'from'         => 'categorias',
        'localField'   => 'categoria_id',
        'foreignField' => '_id',
        'as'           => 'categoria',
    ]],
    ['$unwind' => ['path' => '$categoria', 'preserveNullAndEmptyArrays' => true]],
    ['$sort' => ['precio_total' => -1]],
])->toArray();
?>

<section class="hero">
    <h1>Configurador de PCs</h1>
    <p>Arma equipos a partir de componentes y administra todo el catalogo.</p>
    <a class="boton" href="/?page=configurador">Armar una PC</a>
</section>

<section class="tarjetas">
    <?php foreach ($conteos as $nombre => $total): ?>
        <div class="tarjeta">
            <span class="numero"><?= (int) $total ?></span>
            <span class="etiqueta"><?= h($nombre) ?></span>
        </div>
    <?php endforeach; ?>
</section>

<section class="bloque">
    <h2>Armados registrados</h2>
    <table class="tabla">
        <thead>
            <tr><th>Nombre</th><th>Categoria</th><th>Componentes</th><th>Precio</th></tr>
        </thead>
        <tbody>
            <?php foreach ($armados as $pc): ?>
                <tr>
                    <td><?= h($pc['nombre']) ?></td>
                    <td><span class="chip"><?= h($pc['categoria']['nombre'] ?? 'Sin categoria') ?></span></td>
                    <td><?= count($pc['componentes'] ?? []) ?></td>
                    <td><?= precio($pc['precio_total'] ?? 0) ?></td>
                </tr>
            <?php endforeach; ?>
            <?php if (!$armados): ?>
                <tr><td colspan="4" class="vacio">No hay armados. Corre <code>php seed.php</code> para cargar datos.</td></tr>
            <?php endif; ?>
        </tbody>
    </table>
</section>
