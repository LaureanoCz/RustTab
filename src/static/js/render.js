class GuitarTablature {
    constructor(canvasId, tabData) {
        this.canvas = document.getElementById(canvasId);
        this.tabData = tabData;
        this.context = null;
    }
    
    render() {
        if (!this.tabData || !this.tabData.measures) {
            this.canvas.innerHTML = '<p style="color: red;">Error: Datos de tablatura inválidos</p>';
            return false;
        }
        
        try {
            this.canvas.innerHTML = '';
            this.tabData.measures.forEach((measure, idx) => {
                this.renderMeasure(measure, idx);
            });
            return true;
        } catch (error) {
            console.error('Error renderizando tablatura:', error);
            this.canvas.innerHTML = `<p style="color: red;">Error: ${error.message}</p>`;
            return false;
        }
    }
    
    renderMeasure(measure, index) {
        const svg = this.createSVGMeasure(measure, index);
        this.canvas.appendChild(svg);
    }
    
    createSVGMeasure(measure, index) {
        const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
        svg.setAttribute('width', '450');
        svg.setAttribute('height', '150');
        svg.setAttribute('style', 'border: 1px solid #ddd; margin: 10px 0;');
        
        const lineSpacing = 20;
        const startX = 30;
        const startY = 20;
        
        // Líneas de tablatura (6 cuerdas)
        for (let i = 0; i < 6; i++) {
            const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
            line.setAttribute('x1', startX);
            line.setAttribute('y1', startY + (i * lineSpacing));
            line.setAttribute('x2', 430);
            line.setAttribute('y2', startY + (i * lineSpacing));
            line.setAttribute('stroke', '#999');
            line.setAttribute('stroke-width', '1');
            svg.appendChild(line);
        }
        
        // Número de compás
        const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        text.setAttribute('x', startX);
        text.setAttribute('y', startY - 10);
        text.setAttribute('font-weight', 'bold');
        text.setAttribute('font-size', '12');
        text.textContent = `Compás ${index + 1}`;
        svg.appendChild(text);
        
        // Notas
        if (measure.notes) {
            let noteX = startX + 20;
            measure.notes.forEach(note => {
                this.drawNoteOnSVG(svg, note, noteX, startY, lineSpacing);
                noteX += 35;
            });
        }
        
        return svg;
    }
    
    drawNoteOnSVG(svg, note, x, startY, lineSpacing) {
        const string = parseInt(note.string) || 0;
        const fret = note.fret || '0';
        
        const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
        circle.setAttribute('cx', x);
        circle.setAttribute('cy', startY + (string * lineSpacing));
        circle.setAttribute('r', '12');
        circle.setAttribute('fill', '#667eea');
        svg.appendChild(circle);
        
        const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        text.setAttribute('x', x);
        text.setAttribute('y', startY + (string * lineSpacing) + 4);
        text.setAttribute('text-anchor', 'middle');
        text.setAttribute('fill', 'white');
        text.setAttribute('font-weight', 'bold');
        text.setAttribute('font-size', '14');
        text.textContent = fret;
        svg.appendChild(text);
    }
    
    getNotes() {
        const notes = [];
        if (this.tabData.measures) {
            this.tabData.measures.forEach(measure => {
                if (measure.notes) {
                    notes.push(...measure.notes);
                }
            });
        }
        return notes;
    }
    
    getTabInfo() {
        return {
            totalMeasures: this.tabData.measures ? this.tabData.measures.length : 0,
            totalNotes: this.getNotes().length,
            tuning: this.tabData.tuning || ['E', 'A', 'D', 'G', 'B', 'E'],
            tempo: this.tabData.tempo || 'N/A'
        };
    }
}
