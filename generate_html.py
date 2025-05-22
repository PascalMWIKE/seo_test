<!DOCTYPE html>
<html lang="de">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>SEO Bericht Übersicht</title>
  <link rel="stylesheet" href="css/style.css" />
</head>
<body>
  <div class="container">
    <h1>📊 SEO-Bericht</h1>
    <section class="pdf-view">
      <embed src="{{LATEST_PDF_PATH}}" type="application/pdf" width="100%" height="600px" />
    </section>
    <section class="downloads">
      <h2>🔽 Alle Berichte</h2>
      <ul>
        {{DOWNLOAD_LINKS}}
      </ul>
    </section>
    <footer>
      {{FOOTER_GAME}}
    </footer>
  </div>
</body>
</html>
