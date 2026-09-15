/**
 * AFRIDI KHAN & TAMANNA ALI - SCRATCH & REVEAL ENGINE
 * Interactive HTML5 Canvas Gold Foil Scratch-off
 */

(function () {
  'use strict';

  function initScratch() {
    var canvas = document.getElementById('scratchCanvas');
    var container = document.querySelector('.scratch-container');
    if (!canvas || !container) return;

    var ctx = canvas.getContext('2d');
    var revealBtn = document.getElementById('btnRevealInstant');
    var progressText = document.getElementById('scratchProgressText');
    var celebrationWrap = document.getElementById('scratchCelebration');

    var isDrawing = false;
    var isRevealed = false;
    var lastX = null;
    var lastY = null;
    var brushRadius = 26;

    // Load gold foil texture
    var foilImg = new Image();
    foilImg.src = 'images/gold_foil_texture.jpg';

    function initCanvas() {
      var rect = container.getBoundingClientRect();
      if (rect.width === 0 || rect.height === 0) return;
      var dpr = window.devicePixelRatio || 1;
      canvas.width = Math.floor(rect.width * dpr);
      canvas.height = Math.floor(rect.height * dpr);
      canvas.style.width = rect.width + 'px';
      canvas.style.height = rect.height + 'px';
      ctx.scale(dpr, dpr);

      drawFoilCover(rect.width, rect.height);
    }

    function drawFoilCover(w, h) {
      if (foilImg.complete && foilImg.naturalWidth !== 0) {
        ctx.save();
        ctx.drawImage(foilImg, 0, 0, w, h);

        // Rich gold shimmer overlay
        var grad = ctx.createLinearGradient(0, 0, w, h);
        grad.addColorStop(0, 'rgba(255, 235, 170, 0.4)');
        grad.addColorStop(0.3, 'rgba(180, 130, 40, 0.2)');
        grad.addColorStop(0.6, 'rgba(255, 245, 200, 0.5)');
        grad.addColorStop(1, 'rgba(150, 100, 30, 0.3)');
        ctx.fillStyle = grad;
        ctx.fillRect(0, 0, w, h);

        // Gold ornate border
        ctx.strokeStyle = 'rgba(255, 240, 190, 0.85)';
        ctx.lineWidth = 2.5;
        ctx.strokeRect(10, 10, w - 20, h - 20);

        ctx.strokeStyle = 'rgba(160, 115, 30, 0.7)';
        ctx.lineWidth = 1;
        ctx.strokeRect(14, 14, w - 28, h - 28);

        // Center badge
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';

        ctx.font = 'bold 13px "Cinzel", Georgia, serif';
        ctx.fillStyle = '#5a0f1b';
        ctx.shadowColor = 'rgba(255, 255, 255, 0.6)';
        ctx.shadowBlur = 4;
        ctx.fillText('SCRATCH TO REVEAL DATES', w / 2, h / 2 - 8);

        ctx.font = '11px "Ovo", Georgia, serif';
        ctx.fillStyle = '#6a5140';
        ctx.shadowBlur = 0;
        ctx.fillText('Rub with finger or mouse', w / 2, h / 2 + 12);

        ctx.restore();
      } else {
        // Fallback procedural metallic gold gradient
        var fallbackGrad = ctx.createLinearGradient(0, 0, w, h);
        fallbackGrad.addColorStop(0, '#D4AF37');
        fallbackGrad.addColorStop(0.25, '#FBF5B7');
        fallbackGrad.addColorStop(0.5, '#D4AF37');
        fallbackGrad.addColorStop(0.75, '#FBF5B7');
        fallbackGrad.addColorStop(1, '#AA771C');
        ctx.fillStyle = fallbackGrad;
        ctx.fillRect(0, 0, w, h);

        ctx.strokeStyle = '#5a0f1b';
        ctx.lineWidth = 2;
        ctx.strokeRect(10, 10, w - 20, h - 20);

        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.font = 'bold 13px "Cinzel", Georgia, serif';
        ctx.fillStyle = '#5a0f1b';
        ctx.fillText('✨ SCRATCH TO REVEAL DATES ✨', w / 2, h / 2 - 8);

        ctx.font = '11px "Ovo", Georgia, serif';
        ctx.fillStyle = '#4a2612';
        ctx.fillText('Rub with finger or mouse', w / 2, h / 2 + 12);
      }
    }

    foilImg.onload = function () {
      if (!isRevealed) {
        var rect = container.getBoundingClientRect();
        drawFoilCover(rect.width, rect.height);
      }
    };

    function getCoords(e) {
      var rect = canvas.getBoundingClientRect();
      var clientX = e.clientX;
      var clientY = e.clientY;

      if (e.touches && e.touches.length > 0) {
        clientX = e.touches[0].clientX;
        clientY = e.touches[0].clientY;
      }

      return {
        x: clientX - rect.left,
        y: clientY - rect.top
      };
    }

    function scratch(x, y) {
      if (isRevealed) return;

      ctx.save();
      ctx.globalCompositeOperation = 'destination-out';
      ctx.beginPath();
      ctx.arc(x, y, brushRadius, 0, Math.PI * 2);
      ctx.fill();

      if (lastX !== null && lastY !== null) {
        ctx.lineWidth = brushRadius * 2;
        ctx.lineCap = 'round';
        ctx.lineJoin = 'round';
        ctx.beginPath();
        ctx.moveTo(lastX, lastY);
        ctx.lineTo(x, y);
        ctx.stroke();
      }
      ctx.restore();

      lastX = x;
      lastY = y;

      createSparkle(x, y);
    }

    function createSparkle(x, y) {
      var sparkle = document.createElement('div');
      sparkle.className = 'scratch-sparkle';
      sparkle.style.cssText = [
        'position: absolute;',
        'left: ' + (x + (Math.random() * 20 - 10)) + 'px;',
        'top: ' + (y + (Math.random() * 20 - 10)) + 'px;',
        'width: ' + (Math.random() * 5 + 3) + 'px;',
        'height: ' + (Math.random() * 5 + 3) + 'px;',
        'background: radial-gradient(circle, #FFF, #D4AF37);',
        'border-radius: 50%;',
        'pointer-events: none;',
        'z-index: 10;',
        'box-shadow: 0 0 6px #D4AF37;',
        'animation: sparkleFade 0.6s ease-out forwards;'
      ].join('');

      container.appendChild(sparkle);
      setTimeout(function () {
        if (sparkle.parentNode) sparkle.parentNode.removeChild(sparkle);
      }, 600);
    }

    function checkProgress() {
      if (isRevealed) return;

      var rect = canvas.getBoundingClientRect();
      var dpr = window.devicePixelRatio || 1;
      var w = Math.floor(rect.width * dpr);
      var h = Math.floor(rect.height * dpr);

      var sampleCols = 25;
      var sampleRows = 16;
      var stepX = Math.floor(w / sampleCols);
      var stepY = Math.floor(h / sampleRows);
      var totalSamples = sampleCols * sampleRows;
      var clearedSamples = 0;

      try {
        var imgData = ctx.getImageData(0, 0, w, h);
        var data = imgData.data;

        for (var r = 0; r < sampleRows; r++) {
          for (var c = 0; c < sampleCols; c++) {
            var pixelX = c * stepX + Math.floor(stepX / 2);
            var pixelY = r * stepY + Math.floor(stepY / 2);
            var index = (pixelY * w + pixelX) * 4 + 3;
            if (data[index] < 128) {
              clearedSamples++;
            }
          }
        }

        var percent = Math.round((clearedSamples / totalSamples) * 100);
        if (progressText) {
          progressText.textContent = percent + '% Uncovered';
        }

        if (percent >= 30) {
          revealFullDate();
        }
      } catch (err) {
        // Graceful fallback
      }
    }

    function revealFullDate() {
      if (isRevealed) return;
      isRevealed = true;

      canvas.style.opacity = '0';
      setTimeout(function () {
        canvas.style.display = 'none';
      }, 800);

      if (progressText) {
        progressText.textContent = '✨ Revealed with Love ✨';
        progressText.style.color = '#5a0f1b';
        progressText.style.fontWeight = '700';
      }

      if (revealBtn) {
        revealBtn.style.display = 'none';
      }

      triggerCelebrationConfetti();
    }

    function triggerCelebrationConfetti() {
      if (!celebrationWrap) return;
      var colors = ['#5a0f1b', '#D4AF37', '#FFDF73', '#FFFFFF', '#C5A059'];
      var count = 45;

      for (var i = 0; i < count; i++) {
        (function (index) {
          setTimeout(function () {
            var piece = document.createElement('div');
            var color = colors[Math.floor(Math.random() * colors.length)];
            var size = Math.random() * 7 + 5;
            var left = Math.random() * 100;
            var duration = Math.random() * 1.5 + 1.2;

            piece.style.cssText = [
              'position: absolute;',
              'left: ' + left + '%;',
              'top: 30%;',
              'width: ' + size + 'px;',
              'height: ' + (size * (Math.random() > 0.5 ? 1 : 1.5)) + 'px;',
              'background: ' + color + ';',
              'border-radius: ' + (Math.random() > 0.5 ? '50%' : '2px') + ';',
              'box-shadow: 0 0 6px ' + color + ';',
              'transform: rotate(' + (Math.random() * 360) + 'deg);',
              'pointer-events: none;',
              'z-index: 20;',
              'animation: confettiDrop ' + duration + 's ease-out forwards;'
            ].join('');

            celebrationWrap.appendChild(piece);
            setTimeout(function () {
              if (piece.parentNode) piece.parentNode.removeChild(piece);
            }, duration * 1000);
          }, index * 20);
        })(i);
      }
    }

    canvas.addEventListener('mousedown', function (e) {
      isDrawing = true;
      var c = getCoords(e);
      scratch(c.x, c.y);
    });

    window.addEventListener('mousemove', function (e) {
      if (!isDrawing) return;
      var c = getCoords(e);
      scratch(c.x, c.y);
    });

    window.addEventListener('mouseup', function () {
      if (isDrawing) {
        isDrawing = false;
        lastX = null;
        lastY = null;
        checkProgress();
      }
    });

    canvas.addEventListener('touchstart', function (e) {
      e.preventDefault();
      isDrawing = true;
      var c = getCoords(e);
      scratch(c.x, c.y);
    }, { passive: false });

    canvas.addEventListener('touchmove', function (e) {
      e.preventDefault();
      if (!isDrawing) return;
      var c = getCoords(e);
      scratch(c.x, c.y);
    }, { passive: false });

    canvas.addEventListener('touchend', function () {
      isDrawing = false;
      lastX = null;
      lastY = null;
      checkProgress();
    });

    if (revealBtn) {
      revealBtn.addEventListener('click', function () {
        revealFullDate();
      });
    }

    initCanvas();
    window.addEventListener('resize', function () {
      if (!isRevealed) {
        initCanvas();
      }
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initScratch);
  } else {
    setTimeout(initScratch, 300);
  }
})();
