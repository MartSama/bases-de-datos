<?php

$coleccion = col('categorias');

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $accion = $_POST['accion'] ?? '';
    $datos = [
        'nombre'      => trim($_POST['nombre'] ?? ''),
        'descripcion' => trim($_POST['descripcion'] ?? ''),
    ];
    if ($accion === 'crear') {
        $coleccion->insertOne($datos);
    } elseif ($accion === 'editar' && oid($_POST['id'] ?? '')) {
        $coleccion->updateOne(['_id' => oid($_POST['id'])], ['$set' => $datos]);
    } elseif ($accion === 'borrar' && oid($_POST['id'] ?? '')) {
        $coleccion->deleteOne(['_id' => oid($_POST['id'])]);
    }
    header('Location: /?page=categorias');
    exit;
}

$editando = null;
if (isset($_GET['editar']) && oid($_GET['editar'])) {
    $editando = $coleccion->findOne(['_id' => oid($_GET['editar'])]);
}

$categorias = $coleccion->find([], ['sort' => ['nombre' => 1]])->toArray();
?>

<div class="encabezado">
    <h1>Categorias</h1>
</div>

<div class="rejilla">
    <section class="bloque tarjeta-form">
        <h2><?= $editando ? 'Editar categoria' : 'Nueva categoria' ?></h2>
        <form method="post" action="/?page=categorias">
            <input type="hidden" name="accion" value="<?= $editando ? 'editar' : 'crear' ?>">
            <?php if ($editando): ?>
                <input type="hidden" name="id" value="<?= h($editando['_id']) ?>">
            <?php endif; ?>
            <label>Nombre
                <input type="text" name="nombre" required value="<?= h($editando['nombre'] ?? '') ?>">
            </label>
            <label>Descripcion
                <textarea name="descripcion" rows="3"><?= h($editando['descripcion'] ?? '') ?></textarea>
            </label>
            <div class="acciones-form">
                <button type="submit" class="boton"><?= $editando ? 'Guardar' : 'Agregar' ?></button>
                <?php if ($editando): ?>
                    <a class="boton secundario" href="/?page=categorias">Cancelar</a>
                <?php endif; ?>
            </div>
        </form>
    </section>

    <section class="bloque">
        <h2>Listado</h2>
        <table class="tabla">
            <thead>
                <tr><th>Nombre</th><th>Descripcion</th><th></th></tr>
            </thead>
            <tbody>
                <?php foreach ($categorias as $c): ?>
                    <tr>
                        <td><?= h($c['nombre']) ?></td>
                        <td><?= h($c['descripcion'] ?? '') ?></td>
                        <td class="celda-acciones">
                            <a class="enlace" href="/?page=categorias&editar=<?= h($c['_id']) ?>">Editar</a>
                            <form method="post" action="/?page=categorias" onsubmit="return confirm('Borrar esta categoria?');">
                                <input type="hidden" name="accion" value="borrar">
                                <input type="hidden" name="id" value="<?= h($c['_id']) ?>">
                                <button type="submit" class="enlace peligro">Borrar</button>
                            </form>
                        </td>
                    </tr>
                <?php endforeach; ?>
                <?php if (!$categorias): ?>
                    <tr><td colspan="3" class="vacio">Sin categorias.</td></tr>
                <?php endif; ?>
            </tbody>
        </table>
    </section>
</div>
