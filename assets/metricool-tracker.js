/* Ted Johnson Works public website analytics. Metricool Website Tracker.
   This script is intentionally limited to the TJW site and does not run
   on localhost, previews, or other organizations' domains. */
(() => {
  if (!/^(?:www\.)?tedjohnsonworks\.com$/i.test(window.location.hostname)) return;
  if (window.__tjwMetricoolLoaded) return;
  window.__tjwMetricoolLoaded = true;
  const script = document.createElement('script');
  script.src = 'https://tracker.metricool.com/resources/be.js';
  script.async = true;
  script.onload = () => {
    if (window.beTracker && typeof window.beTracker.t === 'function') {
      window.beTracker.t({ hash: '70363eeaa5b6e9588b4bb0fea90e2eec' });
    }
  };
  document.head.appendChild(script);
})();
