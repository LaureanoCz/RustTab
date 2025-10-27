document.addEventListener("DOMContentLoaded", function () {
  const VF = Vex.Flow;
  const div = document.getElementById("tab");
  const renderer = new VF.Renderer(div, VF.Renderer.Backends.SVG);

  const renderWidth = div.clientWidth;
  const margin = 20;
  const staveHeight = 80; // espacio vertical entre filas de compases
  renderer.resize(renderWidth, 400);
  const context = renderer.getContext();

  // Estilos (igual que vos venías)
  context.setFont("Arial", 12, "").setFillStyle("#919191ff").setStrokeStyle("#919191ff");
  context.setBackgroundFillStyle("#1f1f1f");

  // ===== Configs =====
  const totalMeasures = 12;        // cuántos compases querés dibujar
  const measuresPerRow = 4;        // sugerencia visual (pero usamos auto-wrap)
  const compasWidth = Math.floor((renderWidth - margin * 2) / measuresPerRow); // ancho objetivo por compás
  const startX = margin;
  let currentX = startX;
  let currentY = 20;               // posición vertical inicial
  let measureNumber = 1;

  // Ejemplo de contenido por compás (podés cambiar o generar dinámicamente)
  // Aquí definimos 3 patrones para rotar y que no quede todo igual.
  const measurePatterns = [
    [
      new VF.TabNote({ positions: [{ str: 3, fret: 5 }], duration: "8" }),
      new VF.TabNote({ positions: [{ str: 3, fret: 7 }], duration: "8" }),
      new VF.TabNote({ positions: [{ str: 2, fret: 5 }], duration: "q" }),
      new VF.TabNote({ positions: [{ str: 2, fret: 7 }], duration: "8" }),
      new VF.TabNote({ positions: [{ str: 1, fret: 5 }], duration: "8" }),
    ],
    [
      new VF.TabNote({ positions: [{ str: 1, fret: 7 }], duration: "8" }),
      new VF.TabNote({ positions: [{ str: 1, fret: 5 }], duration: "8" }),
      new VF.TabNote({ positions: [{ str: 2, fret: 7 }], duration: "8" }),
      new VF.TabNote({ positions: [{ str: 2, fret: 5 }], duration: "8" })
    ],
    [
      new VF.TabNote({ positions: [{ str: 4, fret: 2 }], duration: "q" }),
      new VF.TabNote({ positions: [{ str: 3, fret: 2 }], duration: "q" })
    ]
  ];

  // Helper: crear y dibujar un compás con notas
  function drawMeasure(x, y, width, num, notes, isLast) {
    const stave = new VF.TabStave(x, y, width);

    // barras: si es el primer compás en la fila ponemos línea simple (opcional)
    if (x === startX) stave.setBegBarType(VF.Barline.type.SINGLE);

    // si es último compás del sistema global, ponemos barra de END
    if (isLast) stave.setEndBarType(VF.Barline.type.END);

    stave.setMeasure(num);           // numeración del compás
    stave.setContext(context).draw();

    // estilo de notas (mismo look)
    notes.forEach(note => note.setStyle({ fillStyle: "#919191ff", strokeStyle: "#f0f0f0" }));

    // Usamos Formatter para acomodar las notas dentro del ancho del compás
    // Nota: substraemos un pequeño padding para que no choque con las barras
    const padding = 8;
    VF.Formatter.FormatAndDraw(context, stave, notes);

    // Si quisieras beams automáticos: crear beams manualmente por grupo de corcheas
    // (ejemplo simple: si todas son 8, las unimos)
    const only8s = notes.every(n => n.getDuration() && n.getDuration() === "8");
    if (only8s && notes.length > 1) {
      try {
        const beam = new VF.Beam(notes);
        beam.setContext(context).draw();
      } catch (e) {
        // si falla por formato, lo ignora
      }
    }
  }

  // ===== Loop que dibuja measures y hace wrap automático =====
  for (let i = 0; i < totalMeasures; i++) {
    // Auto-wrap: si no entra el compás en la fila actual, saltamos a la siguiente fila
    if (currentX + compasWidth > renderWidth - margin) {
      currentY += staveHeight;
      currentX = startX;
    }

    // Elegir patrón (puede ser dinámico o todo igual)
    const pattern = measurePatterns[i % measurePatterns.length];

    // Dibujo del compás (el último compás global marcamos la barra final)
    const isLastGlobal = (i === totalMeasures - 1);
    drawMeasure(currentX, currentY, compasWidth, measureNumber, pattern, isLastGlobal);

    // Avanzar X y números
    currentX += compasWidth; // next measure sits right after
    measureNumber++;
  }

});
