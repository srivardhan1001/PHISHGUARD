document.addEventListener('DOMContentLoaded', () => {
  const fill = document.querySelector('.meter-fill');
  if (fill) {
    const score = parseInt(fill.getAttribute('data-score') || '0', 10);
    const width = Math.max(0, Math.min(100, score));
    setTimeout(() => { fill.style.width = width + '%'; }, 150);
    const label = document.getElementById('risk-label');
    if (label) {
      if (score >= 60) label.classList.add('bg-danger');
      else if (score >= 30) label.classList.add('bg-warning', 'text-dark');
      else label.classList.add('bg-success');
    }
  }
});

