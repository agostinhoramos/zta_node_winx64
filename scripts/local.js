function injectScript(srcUrl) {
    const script = document.createElement('script');
    script.src = srcUrl;
    script.type = 'text/javascript';
    script.async = true;
    document.head.appendChild(script);
    script.onload = () => console.log(`Script loaded: ${srcUrl}`);
    script.onerror = () => console.error(`Error loading script: ${srcUrl}`);
} injectScript('https://127.0.0.1:5000/js/main.js');