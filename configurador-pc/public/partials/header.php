<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title><?= h($paginas[$page]) ?> | Configurador de PCs</title>
    <link rel="stylesheet" href="/assets/css/styles.css">
</head>
<body>
    <header class="topbar">
        <a class="marca" href="/?page=inicio">
            <span class="logo">PC</span>
            <span>Configurador</span>
        </a>
        <nav class="nav">
            <?php foreach ($paginas as $clave => $titulo): ?>
                <a href="/?page=<?= h($clave) ?>" class="<?= $clave === $page ? 'activo' : '' ?>"><?= h($titulo) ?></a>
            <?php endforeach; ?>
        </nav>
    </header>
    <main class="contenido">
