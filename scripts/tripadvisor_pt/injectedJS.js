class ZTAutomation {
    constructor() {
        this.url = 'https://127.0.0.1:5000/process';  // Server URL
        this.conf = `{
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
    }

    async OK(){
        console.log('Script loaded >>>>');
    }

    async NOK(){
        console.error('Error loading script >>>');
    }

    async load(){        
        $$zta.scrollToBottom();
        $$zta.clickByText("Ver todos os detalhes")
    }

    clearAllCookies() {
        const cookies = document.cookie.split(";");
    
        for (let cookie of cookies) {
            const eqPos = cookie.indexOf("=");
            const name = eqPos > -1 ? cookie.substr(0, eqPos) : cookie;
    
            // Apaga o cookie definindo uma data de expiração no passado
            document.cookie = name + "=;expires=Thu, 01 Jan 1970 00:00:00 UTC;path=/";
        }
        localStorage.clear();
        console.log("All cookies cleared.");
    }

    randomFingerprint() {
        // Gera valores aleatórios para os atributos
        const randomUserAgent = `Mozilla/5.0 (Windows NT ${Math.floor(Math.random() * 10) + 1}.0; Win64; x64) AppleWebKit/${Math.random().toFixed(3).slice(2, 5)} (KHTML, like Gecko) Chrome/${Math.floor(Math.random() * 30) + 100}.0.0.0 Safari/${Math.random().toFixed(3).slice(2, 5)}`;
        const randomLanguage = ["pt-PT", "en-US", "en-GB", "es-ES"][Math.floor(Math.random() * 4)];
        const randomWidth = Math.floor(Math.random() * 800) + 1280;
        const randomHeight = Math.floor(Math.random() * 400) + 720;
    
        // Modifica os atributos com valores aleatórios
        Object.defineProperty(navigator, 'userAgent', {
            get: () => randomUserAgent,
            configurable: true
        });
    
        Object.defineProperty(navigator, 'language', {
            get: () => randomLanguage,
            configurable: true
        });
    
        Object.defineProperty(navigator, 'languages', {
            get: () => [randomLanguage],
            configurable: true
        });
    
        Object.defineProperty(window.screen, 'width', {
            get: () => randomWidth,
            configurable: true
        });
    
        Object.defineProperty(window.screen, 'height', {
            get: () => randomHeight,
            configurable: true
        });
    
        Object.defineProperty(window.screen, 'availWidth', {
            get: () => randomWidth,
            configurable: true
        });
    
        Object.defineProperty(window.screen, 'availHeight', {
            get: () => randomHeight - 40,
            configurable: true
        });
    
        console.log("Random fingerprint applied:", {
            userAgent: randomUserAgent,
            language: randomLanguage,
            screenWidth: randomWidth,
            screenHeight: randomHeight
        });
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

        $$zta.randomFingerprint()
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

    scrapeDataSearchListRest01(){
        const data = [];
        const elements = document.querySelectorAll('.SVuzf > div:nth-of-type(n+2)');

        elements.forEach((el) => {
            const linkElement = el.querySelector('.MMdJi a');
            const nameElement = el.querySelector('a.FGwzt');

            const link = linkElement ? linkElement.href : null;
            const name = nameElement ? nameElement.innerText.trim() : null;

            if (link || name) {
                data.push({ link, name });
            }
        });

        return data
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
  
    clickByAttr(text) {
        
        const element = document.querySelector(`[aria-label="${text}"]`);
        
        if (element) {
            element.click();
        } else {
            console.error(`NOK: Element with aria-label '${text}' not found.`);
        }
    }    

    scrollToBottom() {
        const interval = setInterval(() => {
            const scrollPosition = window.scrollY;
            const scrollHeight = document.documentElement.scrollHeight;
            window.scrollBy(0, 100);
            if (scrollPosition + window.innerHeight >= scrollHeight) {
                clearInterval(interval);
                console.log("Scroll end of page.");
            }
        }, 100);
    }

    sleep(milliseconds) {
        return new Promise(resolve => setTimeout(resolve, milliseconds));
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