chrome.action.onClicked.addListener(async (tab) => {
    try {
        await chrome.sidePanel.open({
            windowId: tab.windowId
        });
    } catch (error) {
        console.error("Open panel error:", error);
    }
});


chrome.runtime.onMessage.addListener((message, sender) => {

    if (message.action !== "hidePanel") {
        return;
    }

    (async () => {

        try {

            const tabs = await chrome.tabs.query({
                active: true,
                currentWindow: true
            });

            if (!tabs.length || !tabs[0].windowId) {
                console.error("Could not find active window.");
                return;
            }

            await chrome.sidePanel.close({
                windowId: tabs[0].windowId
            });

        } catch (error) {

            console.error(
                "QA DevOps AI: close panel failed:",
                error
            );

        }

    })();
});
