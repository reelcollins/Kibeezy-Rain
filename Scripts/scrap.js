//WhatsApp Web Scrap

let phoneNumbers = Array.from(document.querySelectorAll("span._ao3e"))
    .map(el => el.innerText)
    .filter(text => text.includes("254"))
    .map(text => text.replace("+", ""))  // Remove the "+" symbol
    .join("\n");  // Join all numbers with a newline

console.log(phoneNumbers);