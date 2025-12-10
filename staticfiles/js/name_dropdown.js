document.addEventListener("DOMContentLoaded", async () => {
    const input = document.getElementById("recipients-input");
    if (!input) return;

    // Load usernames from your existing API endpoint
    try {
        const response = await fetch("/users/api/usernames/");
        const data = await response.json();
        const usernames = data.usernames || [];
        
        // Initialize Tagify
        const tagify = new Tagify(input, {
            whitelist: usernames,
            maxTags: 20,
            enforceWhitelist: true,
            skipInvalid: true, 
            dropdown: {
                // show suggestions stright away on focus
                enabled: 0,
                maxItems: 40,
                highlightFirst: true,
                closeOnSelect: false
            },
            originalInputValueFormat: valuesArr => valuesArr.map(item => item.value).join(",")
        });

        // Match style
        tagify.DOM.input.classList.add("compose-input");

    } catch (err) {
        console.error("Error loading usernames for Tagify:", err);
    }
});