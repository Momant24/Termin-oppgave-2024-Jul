document.addEventListener('DOMContentLoaded', function() {
    // Henter produkt-ID fra URL
    const productId = new URLSearchParams(window.location.search).get('id');
    /*if (productId) {
        fetchProductData(productId);
    } else {
        console.log('Ingen produkt-ID funnet i URL');
    }*/
    
    // Sjekker om vi er på produktsiden eller handlekurvsiden
    const isProductPage = window.location.pathname.includes("prudukt.html");
    const isCartPage = window.location.pathname.includes("Handlekurv.html");
    

});
// Informasjon om produkter
const products = [
    { id: '1', name: "Rynkefjerner", price: "10 kr", image: "Bilder/Rynkefjerner.jpg", description: "Med daglig bruk av Rynkefjerner vil du oppleve en mer ungdommelig og strålende hudtone, med merkbart færre rynker og forbedret hudelastisitet. Ta steget mot en glattere og mer ungdommelig hud i dag med Rynkefjerner – din hemmelige allierte i kampen mot aldring!" },
    { id: '2', name: "Gelé", price: "1000 kr", image: "Bilder/Gele.jpg", description: "Fin gelé" },
    { id: '3', name: "Akvarium", price: "200 kr", image: "Bilder/Akvarium.jpg", description: "Perfekt for de som elsker fisker og vann" },
    { id: '4', name: "The finest slabs", price: "10000004 kr", image: "Bilder/Slab.jpg", description: "Bare de fineste slabs for deg. Laget med ekte mennskehender, svette og tårer." },
    { id: '5', name: "Usynlig pigmentmaling", price: "99999 kr", image: "Bilder/Usynligmaling.jpg", description: "Vakker maling selges billig. Laget med de beste matrialene 101% organisk, anbefaler!" },
    { id: '6', name: "Baby Beskyttelse", price: "69 kr", image: "Bilder/Beskyttelse.jpg", description: "Er du lei av masse gørr over alt? Vi har løsningen: Baby Beskyttelse. Du holder avstand fra alle bakteriene og holder deg trygg." },
    { id: '7', name: "Privatliv", price: "The original 12 bambu", image: "Bilder/Privatliv.jpg", description: "Er du lei av andre mennesker? Med privatliv kan du holde avstand til andre men fortsatt være med på morroa. PS! Personen på bildet følger med." },
    { id: '8', name: "Inntrengeralarm", price: "1 rotten flesh", image: "Bilder/Intrenger.jpg", description: "Inntrengeralarmen finner ut om det er inntrengere i ditt hus med ny avansert teknologi. Denne teknologien føler etter varme i nærheten og bytter farge på malingen på dolokket hvis noen setter seg på det. Aldri vær redd for inntrengere igjen. Alltid vær sikker på at toalettet er ubrukt." },
    { id: '9', name: "Gresskarkutter 10000", price: "599 kr", image: "Bilder/Greskar.jpg", description: "Gresskarkutter 10000 er perfekt for deg som ønsker å kutte gresskar....." },
    { id: '10', name: "Vakker nese 5000", price: "100 kr", image: "Bilder/Vakkerting.jpg", description: "Vakker nese 5000 hjelper deg med ønskenesa! Få en perfekt nese på under 5 minutt. PS! Vi tar ikke ansvar for ting som sitter fast i nesa." },
    { id: '11', name: "Rynke Revolveren", price: "1688 kr", image: "Bilder/Rynkerevolveren.jpg", description: "Perfekt for alle.........." },
    { id: '12', name: "Anti dobbelhake bandasje", price: "7000 kr", image: "Bilder/Antidobbelhake.png", description: "Gjør deg vakker! Må brukes 24/7. Ikke ta den av. Du er vakker med dette produktet. Ikke ta den av. Vi elsker deg som du er... med dette produktet. Ikke ta den... da blir du stygg." },
    { id: '13', name: "Baby", price: "3500 øre", image: "Bilder/Baby.jpg", description: "Fin baby, blir laget og personlig tilpasset dine behov. 8-9 månder leveringstid." },
    { id: '14', name: "Monster under sengen", price: "10 kr", image: "Bilder/Monster.jpg", description: "Er du lei av å vokne klokka 2 hver natt av skriking? Vi har løsningen for deg! Med monster under sengen vil du bare høre skriking maks en gang. PS! Dette produktet passer perfekt med baby og babygravstein." },
    { id: '15', name: "Grav", price: "50 millioner kr", image: "Bilder/Daubebi.jpg", description: "Perfekt for deg som nylig har brukt produktet beby og monster under sengen." },
    { id: '16', name: "Organiske sko", price: "Pris: 4 fisk", image: "Bilder/Organiskesko.jpg", description: "Disse skoene er 100% organiske. De er laget av naturlige produkter og kan brukes hvor enn du går. Vi tar ikke ansvar for slitasje da disse skoene er et premium produkt og burde byttes ut hver andre time." },
    { id: '17', name: "Cosplay", price: "Ett ekorn + 1000 kr", image: "Bilder/Cosplay.jpg", description: "For deg som vil se ut som ett ekorn. Dette produktet gjør at 10% av din kropp ser ut som et ekorn. Takk oss senere!" },
    { id: '18', name: "Vegansko", price: "2409 kr", image: "Bilder/Vegansko.jpg", description: "Disse skoene er antageligvis veganske. De er laget av gress som gjør at du endelig kan stoppe vennene dine fra å si ''touch some grass''. Perfekt for deg med irriterende venner, og fungerer godt for mødre. PS! Vi tar ikke ansvar hvis du ved et uhell får en slipper i fjeset ditt." },
    { id: '19', name: "Pakke løsning (Baby, Monster under sengen og Garv)", price: "50 milioner kr", image: "Bilder/Baby.jpg", description: "Du får mye rabatt." }
];

function fetchProductData(productId) {
    // Finner produktet basert på ID
    const product = products.find(p => p.id === productId);
    if (product) {
        updateProductPage(product);
        console.log(`Produkt funnet: ${product.name}`);
    } else {
        console.log('Produktet ble ikke funnet');
    }
}

function settHandlekurvLink(productId) {
    var handlekurvLink = document.getElementById("handlekurvLink");
    if (handlekurvLink) {
        handlekurvLink.href = "Handlekurv.html?id=" + productId;
        console.log('Link fiksa');
    } else {
        console.log('Handlekurv link ikke funnet');
    }
}

/*function leggTilIhandlekurv(product) {
handleKurv.push(product);
localStorage.setItem("handlekurv", JSON.stringify(handleKurv));
console.log("Lagt til i handlekurv");
visProdukter();
}

function visProdukter() {
let handleKurvVisning = document.getElementById("produkthandlekurv");
handleKurvVisning.innerHTML = ""; // Tømmer eksisterende innhold
products.forEach((produkt) => {
    handleKurvVisning.innerHTML += `
<div>
<div class="bildeogprodukt">
<img src="${produkt.image}" alt="${produkt.name}">
<div class="tekstprodukthandlekurv">
<p>${produkt.name}</p>
<p>${produkt.price}</p>
</div>
</div>
<div class="antall">
<div class="number-input">
<input type="number" min="0" value="1">
</div>
</div>
<div class="Tilsammenpris">
<p>${produkt.price}</p>
</div> </div>`;
});
}
function getProducts() {

let productList = [];

let handleKurv = JSON.parse(localStorage.getItem("handlekurv"));

handleKurv.map((id) => {
    productList.push(fetchProductData(id))
})
return productList;

} */