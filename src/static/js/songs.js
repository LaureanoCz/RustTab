document.addEventListener("DOMContentLoaded", function () {
  const VF = Vex.Flow;
  const div = document.getElementById("tab");
  
  if (!div) {
    console.error("Tab container not found");
    return;
  }

  const renderer = new VF.Renderer(div, VF.Renderer.Backends.SVG);
  const renderWidth = div.clientWidth;
  const margin = 20;
  const staveHeight = 80; // espacio vertical entre filas de compases
  const measuresPerRow = 4;        // sugerencia visual (pero usamos auto-wrap)
  
  // Parse tablature data from database or use default patterns
  let measurePatterns = [];
  let totalMeasures = 12;
  
  // Get totalMeasures from songData if available (will be set after parsing)
  if (typeof songData !== 'undefined' && songData && songData.compases) {
    totalMeasures = parseInt(songData.compases) || 12;
  }

  // Calculate initial height based on estimated measures
  const estimatedHeight = Math.ceil(totalMeasures / measuresPerRow) * staveHeight + 100;
  renderer.resize(renderWidth, Math.max(400, estimatedHeight));
  const context = renderer.getContext();

  // Estilos
  context.setFont("Arial", 12, "").setFillStyle("#919191ff").setStrokeStyle("#919191ff");
  context.setBackgroundFillStyle("#1f1f1f");

  // ===== Configs =====
  const compasWidth = Math.floor((renderWidth - margin * 2) / measuresPerRow); // ancho objetivo por compás
  const startX = margin;
  let currentX = startX;
  let currentY = 20;               // posición vertical inicial
  let measureNumber = 1;

  // Check if we have song data from the database
  if (typeof songData !== 'undefined' && songData && songData.tablatura_data) {
    try {
      // tablatura_data should be a JSON object with structure:
      // {
      //   "measures": [
      //     {
      //       "notes": [
      //         { "str": 3, "fret": 5, "duration": "8" },
      //         { "str": 3, "fret": 7, "duration": "8" }
      //       ]
      //     }
      //   ],
      //   "totalMeasures": 12
      // }
      const tabData = songData.tablatura_data;
      
      if (tabData.measures && Array.isArray(tabData.measures)) {
        totalMeasures = tabData.totalMeasures || tabData.measures.length;
        // Resize renderer based on actual measures
        const actualHeight = Math.ceil(totalMeasures / measuresPerRow) * staveHeight + 100;
        renderer.resize(renderWidth, Math.max(400, actualHeight));
        measurePatterns = tabData.measures.map(measure => {
          if (measure.notes && Array.isArray(measure.notes)) {
            return measure.notes.map(note => {
              return new VF.TabNote({
                positions: [{ str: note.str, fret: note.fret }],
                duration: note.duration || "q"
              });
            });
          }
          return [];
        });
      }
    } catch (error) {
      console.error("Error parsing tablature data:", error);
      // Fall back to default patterns
      measurePatterns = getDefaultPatterns();
    }
  } else {
    // Use default patterns if no data from database
    measurePatterns = getDefaultPatterns();
    if (typeof songData !== 'undefined' && songData && songData.compases) {
      totalMeasures = parseInt(songData.compases) || 12;
    }
  }

  // Default patterns function
  function getDefaultPatterns() {
    return [
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
  }

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
