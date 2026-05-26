<?php

$coleccion = col('marcas');

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $accion = $_POST['accion'] ?? '';
    $datos = [
        'nombre'    => trim($_POST['nombre'] ?? ''),
        'pais'      => trim($_POST['pais'] ?? ''),
        'sitio_web' => trim($_POST['sitio_web'] ?? ''),
    ];
    if ($accion === 'crear') {
        $coleccion->insertOne($datos);
    } elseif ($accion === 'editar' && oid($_POST['id'] ?? '')) {
        $coleccion->updateOne(['_id' => oid($_POST['id'])], ['$set' => $datos]);
    } elseif ($accion === 'borrar' && oid($_POST['id'] ?? '')) {
        $coleccion->deleteOne(['_id' => oid($_POST['id'])]);
    }
    header('Location: /?page=marcas');
    exit;
}

$editando = null;
if (isset($_GET['editar']) && oid($_GET['editar'])) {
    $editando = $coleccion->findOne(['_id' => oid($_GET['editar'])]);
}

$marcas = $coleccion->find([], ['sort' => ['nombre' => 1]])->toArray();
?>

<div class="encabezado">
    <h1>Marcas</h1>
</div>

<div class="rejilla">
    <section class="bloque tarjeta-form">
        <h2><?= $editando ? 'Editar marca' : 'Nueva marca' ?></h2>
        <form method="post" action="/?page=marcas">
            <input type="hidden" name="accion" value="<?= $editando ? 'editar' : 'crear' ?>">
            <?php if ($editando): ?>
                <input type="hidden" name="id" value="<?= h($editando['_id']) ?>">
            <?php endif; ?>
            <label>Nombre
                <input type="text" name="nombre" required value="<?= h($editando['nombre'] ?? '') ?>">
            </label>
            <label>Pais
                <input type="text" name="pais" value="<?= h($editando['pais'] ?? '') ?>">
            </label>
            <label>Sitio web
                <input type="text" name="sitio_web" value="<?= h($editando['sitio_web'] ?? '') ?>">
            </label>
            <div class="acciones-form">
                <button type="submit" class="boton"><?= $editando ? 'Guardar' : 'Agregar' ?></button>
                <?php if ($editando): ?>
                    <a class="boton secundario" href="/?page=marcas">Cancelar</a>
                <?php endif; ?>
            </div>
        </form>
    </section>

    <section class="bloque">
        <h2>Listado</h2>
        <table class="tabla">
            <thead>
                <tr><th>Nombre</th><th>Pais</th><th>Sitio web</th><th></th></tr>
            </thead>
            <tbody>
                <?php foreach ($marcas as $m): ?>
                    <tr>
                        <td><?= h($m['nombre']) ?></td>
                        <td><?= h($m['pais'] ?? '') ?></td>
                        <td><?= h($m['sitio_web'] ?? '') ?></td>
                        <td class="celda-acciones">
                            <a class="enlace" href="/?page=marcas&editar=<?= h($m['_id']) ?>">Editar</a>
                            <form method="post" action="/?page=marcas" onsubmit="return confirm('Borrar esta marca?');">
                                <input type="hidden" name="accion" value="borrar">
                                <input type="hidden" name="id" value="<?= h($m['_id']) ?>">
                                <button type="submit" class="enlace peligro">Borrar</button>
                            </form>
                        </td>
                    </tr>
                <?php endforeach; ?>
                <?php if (!$marcas): ?>
                    <tr><td colspan="4" class="vacio">Sin marcas.</td></tr>
                <?php endif; ?>
            </tbody>
        </table>
    </section>
</div>
