document.addEventListener("DOMContentLoaded", function () {
  const VF = Vex.Flow;
  const div = document.getElementById("tab");
  const renderer = new VF.Renderer(div, VF.Renderer.Backends.SVG);

  const renderWidth = div.clientWidth;
  const margin = 10;
  const staveHeight = 120;
  const context = renderer.getContext();

  // Estilos
  context.setFont("Arial", 12, "").setFillStyle("#919191ff").setStrokeStyle("#919191ff");
  context.setBackgroundFillStyle("#1f1f1f");

  // Configuración del layout
  const totalMeasures = 12;
  const measuresPerRow = 4;
  const compasWidth = Math.floor((renderWidth - margin * 2) / measuresPerRow);
  const startX = margin;
  let currentX = startX;
  let currentY = 20;
  let measureNumber = 1;

  // URL por defecto para cargar la tablatura
  const defaultTabUrl = 'static/tablatures/monster_skillet.json';

  // Mapea duraciones a identificadores de Vex.Flow
  function mapDuration(d) {
    if (!d && d !== 0) return 'q';
    if (typeof d === 'string') {
      return d;
    }
    if (typeof d === 'number') {
      switch (d) {
        case 16: return '16';
        case 8: return '8';
        case 4: return 'q';
        case 2: return 'h';
        case 1: return 'w';
        default: return String(d);
      }
    }
    return 'q';
  }

  // Construye una nota de tablatura desde un objeto del JSON
  function makeTabNote(n) {
    const str = n.str || n.string || n.stringNumber || n.s || n['string_number'] || 1;
    const fret = (n.fret !== undefined) ? n.fret : (n.f !== undefined ? n.f : 0);
    const duration = mapDuration(n.duration || n.d || n.len);
    const positions = Array.isArray(n.positions)
      ? n.positions.map(p => ({ str: p.str || p.string, fret: p.fret || p.f }))
      : [{ str: str, fret: fret }];
    return new VF.TabNote({ positions: positions, duration: duration });
  }

  // Renderiza desde la estructura JSON
  function renderFromJSON(data) {
    const measures = data.measures || data;
    const totalMeasures = measures.length;

    // Calcula las filas y redimensiona el renderer
    const rows = Math.ceil(totalMeasures / measuresPerRow);
    const neededHeight = rows * staveHeight + 40;
    renderer.resize(renderWidth, neededHeight);

    // Reinicia posiciones
    currentX = startX;
    currentY = -60;
    measureNumber = 1;

    for (let i = 0; i < totalMeasures; i++) {
      if (currentX + compasWidth > renderWidth - margin) {
        currentY += staveHeight;
        currentX = startX;
      }

      const measure = measures[i];
      const noteItems = measure.notes || measure.notesInMeasure || measure.events || measure;

      let pattern = [];
      if (Array.isArray(noteItems)) {
        pattern = noteItems.map(n => makeTabNote(n));
      } else {
        pattern = [ makeTabNote(noteItems) ];
      }

      const isLastGlobal = (i === totalMeasures - 1);
      drawMeasure(currentX, currentY, compasWidth, measure.number || measureNumber, pattern, isLastGlobal);
      currentX += compasWidth;
      measureNumber++;
    }
  }

  // Dibuja un compás con sus notas
  function drawMeasure(x, y, width, num, notes, isLast) {
    const stave = new VF.TabStave(x, y, width);

    if (x === startX) stave.setBegBarType(VF.Barline.type.SINGLE);
    if (isLast) stave.setEndBarType(VF.Barline.type.END);

    stave.setMeasure(num);
    stave.setContext(context).draw();

    // Estilos de las notas
    notes.forEach(note => note.setStyle({ fillStyle: "#919191ff", strokeStyle: "#f0f0f0" }));

    // Acomoda las notas dentro del ancho del compás
    VF.Formatter.FormatAndDraw(context, stave, notes);

    // Crea beams automáticos si todas las notas son corcheas
    const only8s = notes.every(n => n.getDuration() && n.getDuration() === "8");
    if (only8s && notes.length > 1) {
      try {
        const beam = new VF.Beam(notes);
        beam.setContext(context).draw();
      } catch (e) {
        // ignora si falla
      }
    }
  }

  // Carga la tablatura desde TAB_DATA (si viene de la plantilla) o desde fetch
  if (typeof TAB_DATA !== 'undefined' && TAB_DATA) {
    renderFromJSON(TAB_DATA);
  } else {
    const dataAttr = div.dataset.tablature;
    let url = (dataAttr && dataAttr.length) ? dataAttr : defaultTabUrl;
    if (!url.startsWith('/')) url = '/' + url;

    fetch(url)
      .then(res => {
        if (!res.ok) throw new Error('No se pudo cargar ' + url);
        return res.json();
      })
      .then(json => renderFromJSON(json))
      .catch(err => {
        // Si falla la carga, dibuja compases de ejemplo
        console.error('Error cargando tablatura:', err);
        const measurePatterns = [
          [
            new VF.TabNote({ positions: [{ str: 3, fret: 5 }], duration: '8' }),
            new VF.TabNote({ positions: [{ str: 3, fret: 7 }], duration: '8' })
          ],
          [
            new VF.TabNote({ positions: [{ str: 1, fret: 7 }], duration: '8' }),
            new VF.TabNote({ positions: [{ str: 1, fret: 5 }], duration: '8' })
          ]
        ];
        for (let i = 0; i < Math.min(totalMeasures, 8); i++) {
          if (currentX + compasWidth > renderWidth - margin) {
            currentY += staveHeight;
            currentX = startX;
          }
          const pattern = measurePatterns[i % measurePatterns.length];
          const isLastGlobal = (i === totalMeasures - 1);
          drawMeasure(currentX, currentY, compasWidth, measureNumber, pattern, isLastGlobal);
          currentX += compasWidth;
          measureNumber++;
        }
      });
  }
});