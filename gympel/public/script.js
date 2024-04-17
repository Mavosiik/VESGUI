// handleSubmit je funkcia, ktorá sa spustí keď sa bude mať odoslať náš formulár
function handleSubmit(e) {
	e.preventDefault(); // zabrániť vstavenému odosielaniu v prehliadači

	// this reprezentuje ten formular, ktory odosielame
	const ves = this.querySelector("textarea").value; // Načítame text z textarea
	const width = document.querySelector("section:nth-child(2)").clientWidth; // Načítame aktuálnu šírku výstupného okna

	const formular = new URLSearchParams(); // Vytvoríme štruktúru, ktorá bude reprezentovať formulár
	formular.append('ves', ves); // Pridáme tam naše hodnoty
	formular.append('width', width);

	const url = this.action; // Nacitame povodnu URL zadanu vo formulari
	const method = this.method; // NAcitame povodnu metodu zadanu vo formulari
	fetch(url, {method: method, body: formular}) // Urobíme HTTP požiadavku na náš server POST /render a formularom v tele požiadavky 
		.then((res) => res.blob()) // Dostali sme binárne dáta (blob)
		.then((image) => {
			document.querySelector("#output").src = URL.createObjectURL(image); // Nastavíme src našeho <img> na načítaný obrázok
		})
}
document.querySelector("form").addEventListener("submit", handleSubmit); // Nastavíme formulár, aby pri submit udalosti spustil našu handleSubmit funkciu