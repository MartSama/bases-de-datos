<?php

$coleccion = col('computadoras');

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $accion = $_POST['accion'] ?? '';
    if ($accion === 'editar' && oid($_POST['id'] ?? '')) {
        $coleccion->updateOne(['_id' => oid($_POST['id'])], ['$set' => [
            'nombre'       => trim($_POST['nombre'] ?? ''),
            'categoria_id' => oid($_POST['categoria_id'] ?? ''),
            'descripcion'  => trim($_POST['descripcion'] ?? ''),
        ]]);
    } elseif ($accion === 'borrar' && oid($_POST['id'] ?? '')) {
        $coleccion->deleteOne(['_id' => oid($_POST['id'])]);
    }
    header('Location: /?page=computadoras');
    exit;
}

$editando = null;
if (isset($_GET['editar']) && oid($_GET['editar'])) {
    $editando = $coleccion->findOne(['_id' => oid($_GET['editar'])]);
}

$categorias = col('categorias')->find([], ['sort' => ['nombre' => 1]])->toArray();

// Join completo: categoria + detalle de cada componente con su marca.
// El segundo lookup usa un sub-pipeline para anidar la marca dentro de cada componente.
$armados = $coleccion->aggregate([
    ['$lookup' => [
        'from'         => 'categorias',
        'localField'   => 'categoria_id',
        'foreignField' => '_id',
        'as'           => 'categoria',
    ]],
    ['$unwind' => ['path' => '$categoria', 'preserveNullAndEmptyArrays' => true]],
    ['$lookup' => [
        'from'     => 'componentes',
        'let'      => ['ids' => '$componentes.componente_id'],
        'pipeline' => [
            ['$match' => ['$expr' => ['$in' => ['$_id', '$$ids']]]],
            ['$lookup' => [
                'from'         => 'marcas',
                'localField'   => 'marca_id',
                'foreignField' => '_id',
                'as'           => 'marca',
            ]],
            ['$unwind' => ['path' => '$marca', 'preserveNullAndEmptyArrays' => true]],
        ],
        'as' => 'detalle',
    ]],
    ['$sort' => ['nombre' => 1]],
])->toArray();

$catEditando = $editando && isset($editando['categoria_id']) ? (string) $editando['categoria_id'] : '';
?>

<div class="encabezado">
    <h1>Armados</h1>
    <a class="boton" href="/?page=configurador">Nuevo armado</a>
</div>

<?php if ($editando): ?>
    <section class="bloque tarjeta-form">
        <h2>Editar armado</h2>
        <form method="post" action="/?page=computadoras">
            <input type="hidden" name="accion" value="editar">
            <input type="hidden" name="id" value="<?= h($editando['_id']) ?>">
            <label>Nombre
                <input type="text" name="nombre" required value="<?= h($editando['nombre'] ?? '') ?>">
            </label>
            <label>Categoria
                <select name="categoria_id">
                    <option value="">Sin categoria</option>
                    <?php foreach ($categorias as $cat): ?>
                        <option value="<?= h($cat['_id']) ?>" <?= $catEditando === (string) $cat['_id'] ? 'selected' : '' ?>><?= h($cat['nombre']) ?></option>
                    <?php endforeach; ?>
                </select>
            </label>
            <label>Descripcion
                <textarea name="descripcion" rows="2"><?= h($editando['descripcion'] ?? '') ?></textarea>
            </label>
            <div class="acciones-form">
                <button type="submit" class="boton">Guardar</button>
                <a class="boton secundario" href="/?page=computadoras">Cancelar</a>
            </div>
        </form>
    </section>
<?php endif; ?>

<div class="armados">
    <?php foreach ($armados as $pc): ?>
        <?php
            // Cantidad por componente para combinarla con el detalle del join.
            $cantidades = [];
            foreach (($pc['componentes'] ?? []) as $item) {
                $cantidades[(string) $item['componente_id']] = (int) $item['cantidad'];
            }
        ?>
        <section class="bloque armado">
            <div class="armado-cab">
                <div>
                    <h2><?= h($pc['nombre']) ?></h2>
                    <span class="chip"><?= h($pc['categoria']['nombre'] ?? 'Sin categoria') ?></span>
                </div>
                <div class="armado-precio"><?= precio($pc['precio_total'] ?? 0) ?></div>
            </div>
            <?php if (!empty($pc['descripcion'])): ?>
                <p class="sub"><?= h($pc['descripcion']) ?></p>
            <?php endif; ?>
            <table class="tabla compacta">
                <thead>
                    <tr><th>Componente</th><th>Tipo</th><th>Marca</th><th>Cant.</th><th>Precio</th></tr>
                </thead>
                <tbody>
                    <?php foreach (($pc['detalle'] ?? []) as $d): ?>
                        <?php $cant = $cantidades[(string) $d['_id']] ?? 1; ?>
                        <tr>
                            <td><?= h($d['nombre']) ?></td>
                            <td><span class="chip"><?= h($d['tipo'] ?? '') ?></span></td>
                            <td><?= h($d['marca']['nombre'] ?? 'Sin marca') ?></td>
                            <td><?= $cant ?></td>
                            <td><?= precio(($d['precio'] ?? 0) * $cant) ?></td>
                        </tr>
                    <?php endforeach; ?>
                </tbody>
            </table>
            <div class="celda-acciones">
                <a class="enlace" href="/?page=computadoras&editar=<?= h($pc['_id']) ?>">Editar</a>
                <form method="post" action="/?page=computadoras" onsubmit="return confirm('Borrar este armado?');">
                    <input type="hidden" name="accion" value="borrar">
                    <input type="hidden" name="id" value="<?= h($pc['_id']) ?>">
                    <button type="submit" class="enlace peligro">Borrar</button>
                </form>
            </div>
        </section>
    <?php endforeach; ?>
    <?php if (!$armados): ?>
        <section class="bloque"><p class="vacio">No hay armados todavia. Ve al <a href="/?page=configurador">configurador</a>.</p></section>
    <?php endif; ?>
</div>
