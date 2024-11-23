class ZTAutomation {
    constructor() {
        this.url = 'https://192.168.1.87:5000/process';  // Server URL
    }

    load(){
        const configuration = `{
            "_id": "tripadvisor_pt",
            "startUrl": ["https://www.tripadvisor.pt/Restaurant_Review-g4914446-d25035356-Reviews-El_Pimenton-Amora_Setubal_District_Alentejo.html"],
            "selectors": [
                { "id": "title", "parentSelectors": ["_root"], "type": "SelectorText", "selector": "h1.biGQs", "multiple": false, "regex": "" },
                { "id": "desc", "parentSelectors": ["_root"], "type": "SelectorText", "selector": ".AYNtL div.pZUbB", "multiple": false, "regex": "" },
                { "id": "price_range", "parentSelectors": ["_root"], "type": "SelectorText", "selector": ".XKqDZ div:nth-of-type(2) div.alXOW", "multiple": false, "regex": "" },
                { "id": "address", "parentSelectors": ["_root"], "type": "SelectorText", "selector": ".e > div:nth-of-type(2) .BMQDV span.pZUbB", "multiple": false, "regex": "" },
                { "id": "features", "parentSelectors": ["_root"], "type": "SelectorText", "selector": "div.SFSXn:nth-of-type(2) div:nth-of-type(2) div.pZUbB", "multiple": false, "regex": "" },
                { "id": "meals_type", "parentSelectors": ["_root"], "type": "SelectorText", "selector": "div.SFSXn:nth-of-type(2) div:nth-of-type(1) div.pZUbB", "multiple": false, "regex": "" },
                { "id": "gastronomy", "parentSelectors": ["_root"], "type": "SelectorText", "selector": "div.SFSXn:nth-of-type(1) div:nth-of-type(2) div.pZUbB", "multiple": false, "regex": "" },
                { "id": "website", "parentSelectors": ["_root"], "type": "SelectorElementAttribute", "selector": "a[aria-label='Web site']", "multiple": false, "extractAttribute": "href" },
                { "id": "email", "parentSelectors": ["_root"], "type": "SelectorElementAttribute", "selector": "[aria-label='E-mail']", "multiple": false, "extractAttribute": "href" },
                { "id": "phone", "parentSelectors": ["_root"], "type": "SelectorText", "selector": "[aria-label='Call']", "multiple": false, "regex": "" },
                { "id": "classification_food", "parentSelectors": ["_root"], "type": "SelectorText", "selector": "svg[aria-labelledby=':lithium-r1b:']", "multiple": false, "regex": "" },
                { "id": "classification_service", "parentSelectors": ["_root"], "type": "SelectorText", "selector": "svg[aria-labelledby=':lithium-r1c:']", "multiple": false, "regex": "" },
                { "id": "classification_value", "parentSelectors": ["_root"], "type": "SelectorText", "selector": "div:nth-of-type(3) div.JSTna", "multiple": false, "regex": "" },
                { "id": "classification_environment", "parentSelectors": ["_root"], "type": "SelectorText", "selector": "div:nth-of-type(4) div.JSTna", "multiple": false, "regex": "" }
            ]
        }`;
        
        const configurationJson = JSON.parse(configuration);
        const selectors = configurationJson.selectors;
        
        $$zta.clickByText("Ver todos os detalhes")
    }

    // Sends a POST request to the server
    async sendPostRequest(url, data) {
        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data),
                mode: 'cors'
            });

            if (!response.ok) {
                throw new Error(`Request error: ${response.status}`);
            }

            return await response.json(); // Returns the data as JSON
        } catch (error) {
            console.error('Error sending request:', error);
            throw error; // Re-throws the error for external handling
        }
    }

    // Function to scrape data from the page based on selectors
    scrapeData(selectors) {
        const data = {};
        selectors.forEach(({ id, selector, type, extractAttribute }) => {
            try {
                const element = document.querySelector(selector);
                if (!element) {
                    data[id] = null;
                    return;
                }

                if (type === "SelectorText") {
                    data[id] = element.textContent.trim();
                } else if (type === "SelectorElementAttribute" && extractAttribute) {
                    data[id] = element.getAttribute(extractAttribute);
                } else {
                    data[id] = null;
                }
            } catch (error) {
                console.error(`Error extracting ${id}:`, error);
                data[id] = null;
            }
        });

        return data;
    }

    clickByText(text) { // Ver todos os detalhes
        const xpath = `//*[text()='${text}']`;
        const element = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
        if (element) {
            element.click();
        } else {
            console.error(`NOK: Element with text '${text}' not found.`);
        }
    }
}

const $$zta = new ZTAutomation();
// $$zta.load()


// Try to open the details of the page
// $$zta.openDetails();

// Perform data scraping
// const scrapedData = $$zta.scrapeData(selectors);
// console.log(scrapedData);

// Send the scraped data to the server
// $$zta.sendPostRequest($$zta.url, scrapedData)
//     .then(response => {
//         console.log('Server response:', response);
//     })
//     .catch(error => {
//         console.error('Error processing the request:', error);
//     });