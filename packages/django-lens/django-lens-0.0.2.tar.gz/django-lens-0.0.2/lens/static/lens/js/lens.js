function copyToClipboard(event) {
    var copyBtn = event.currentTarget;
    navigator.clipboard.writeText(copyBtn.parentElement.querySelector('code').textContent);

    var copyLabel = copyBtn.querySelector('[data-action="copy"]')
    var copiedLabel = copyBtn.querySelector('[data-action="copied"]')

    // toggle copy/copied visibility in 1500ms
    htmx.addClass(copyLabel, "hidden");
    htmx.removeClass(copiedLabel, "hidden");
    htmx.removeClass(copyLabel, "hidden", 1500);
    htmx.addClass(copiedLabel, "hidden", 1500);
};
