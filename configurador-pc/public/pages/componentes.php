<?php

$coleccion = col('componentes');
$tipos = ['CPU', 'GPU', 'RAM', 'Almacenamiento', 'Motherboard', 'Fuente', 'Gabinete', 'Disipador'];

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $accion = $_POST['accion'] ?? '';
    $datos = [
        'nombre'   => trim($_POST['nombre'] ?? ''),
        'tipo'     => trim($_POST['tipo'] ?? ''),
        'marca_id' => oid($_POST['marca_id'] ?? ''),
        'precio'   => (float) ($_POST['precio'] ?? 0),
        'specs'    => trim($_POST['specs'] ?? ''),
        'stock'    => (int) ($_POST['stock'] ?? 0),
    ];
    if ($accion === 'crear') {
        $coleccion->insertOne($datos);
    } elseif ($accion === 'editar' && oid($_POST['id'] ?? '')) {
        $coleccion->updateOne(['_id' => oid($_POST['id'])], ['$set' => $datos]);
    } elseif ($accion === 'borrar' && oid($_POST['id'] ?? '')) {
        $coleccion->deleteOne(['_id' => oid($_POST['id'])]);
    }
    header('Location: /?page=componentes');
    exit;
}

$editando = null;
if (isset($_GET['editar']) && oid($_GET['editar'])) {
    $editando = $coleccion->findOne(['_id' => oid($_GET['editar'])]);
}

$marcas = col('marcas')->find([], ['sort' => ['nombre' => 1]])->toArray();

// Listado con join a marcas para mostrar el nombre de la marca.
$componentes = $coleccion->aggregate([
    ['$lookup' => [
        'from'         => 'marcas',
        'localField'   => 'marca_id',
        'foreignField' => '_id',
        'as'           => 'marca',
    ]],
    ['$unwind' => ['path' => '$marca', 'preserveNullAndEmptyArrays' => true]],
    ['$sort' => ['tipo' => 1, 'nombre' => 1]],
])->toArray();

$marcaEditando = $editando && isset($editando['marca_id']) ? (string) $editando['marca_id'] : '';
?>

<div class="encabezado">
    <h1>Componentes</h1>
</div>

<div class="rejilla">
    <section class="bloque tarjeta-form">
        <h2><?= $editando ? 'Editar componente' : 'Nuevo componente' ?></h2>
        <form method="post" action="/?page=componentes">
            <input type="hidden" name="accion" value="<?= $editando ? 'editar' : 'crear' ?>">
            <?php if ($editando): ?>
                <input type="hidden" name="id" value="<?= h($editando['_id']) ?>">
            <?php endif; ?>
            <label>Nombre
                <input type="text" name="nombre" required value="<?= h($editando['nombre'] ?? '') ?>">
            </label>
            <label>Tipo
                <select name="tipo">
                    <?php foreach ($tipos as $t): ?>
                        <option value="<?= h($t) ?>" <?= ($editando['tipo'] ?? '') === $t ? 'selected' : '' ?>><?= h($t) ?></option>
                    <?php endforeach; ?>
                </select>
            </label>
            <label>Marca
                <select name="marca_id">
                    <option value="">Sin marca</option>
                    <?php foreach ($marcas as $m): ?>
                        <option value="<?= h($m['_id']) ?>" <?= $marcaEditando === (string) $m['_id'] ? 'selected' : '' ?>><?= h($m['nombre']) ?></option>
                    <?php endforeach; ?>
                </select>
            </label>
            <label>Precio
                <input type="number" step="0.01" min="0" name="precio" value="<?= h($editando['precio'] ?? '') ?>">
            </label>
            <label>Especificaciones
                <input type="text" name="specs" value="<?= h($editando['specs'] ?? '') ?>">
            </label>
            <label>Stock
                <input type="number" min="0" name="stock" value="<?= h($editando['stock'] ?? '') ?>">
            </label>
            <div class="acciones-form">
                <button type="submit" class="boton"><?= $editando ? 'Guardar' : 'Agregar' ?></button>
                <?php if ($editando): ?>
                    <a class="boton secundario" href="/?page=componentes">Cancelar</a>
                <?php endif; ?>
            </div>
        </form>
    </section>

    <section class="bloque">
        <h2>Listado</h2>
        <table class="tabla">
            <thead>
                <tr><th>Nombre</th><th>Tipo</th><th>Marca</th><th>Precio</th><th>Stock</th><th></th></tr>
            </thead>
            <tbody>
                <?php foreach ($componentes as $c): ?>
                    <tr>
                        <td><?= h($c['nombre']) ?><div class="sub"><?= h($c['specs'] ?? '') ?></div></td>
                        <td><span class="chip"><?= h($c['tipo'] ?? '') ?></span></td>
                        <td><?= h($c['marca']['nombre'] ?? 'Sin marca') ?></td>
                        <td><?= precio($c['precio'] ?? 0) ?></td>
                        <td><?= (int) ($c['stock'] ?? 0) ?></td>
                        <td class="celda-acciones">
                            <a class="enlace" href="/?page=componentes&editar=<?= h($c['_id']) ?>">Editar</a>
                            <form method="post" action="/?page=componentes" onsubmit="return confirm('Borrar este componente?');">
                                <input type="hidden" name="accion" value="borrar">
                                <input type="hidden" name="id" value="<?= h($c['_id']) ?>">
                                <button type="submit" class="enlace peligro">Borrar</button>
                            </form>
                        </td>
                    </tr>
                <?php endforeach; ?>
                <?php if (!$componentes): ?>
                    <tr><td colspan="6" class="vacio">Sin componentes.</td></tr>
                <?php endif; ?>
            </tbody>
        </table>
    </section>
</div>
