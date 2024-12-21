//const form = document.getElementById("myform");
//const add_btn = document.getElementById("add_line");
//let num = 0;
//
//const createInput = (name, placeholder, isAutocomplete = false) => {
//    const input = document.createElement("input");
//    input.name = `${name}_${num}`;
//    input.placeholder = placeholder;
//    if (isAutocomplete) {
//        input.classList.add("product-autocomplete");
//        input.setAttribute("data-url", "/api/products/"); // URL de l'API d'autocomplétion
//    }
//    return input;
//};
//
//const setupAutocomplete = (input) => {
//    // Utilisez une bibliothèque d'autocomplétion comme Autocomplete.js ou implémentez votre propre logique
//    // Cet exemple utilise fetch pour obtenir les suggestions de l'API
//    input.addEventListener('input', async (e) => {
//        const query = e.target.value;
//        if (query.length < 2) return; // Attendez au moins 2 caractères avant de faire une requête
//
//        const response = await fetch(`${input.dataset.url}?query=${encodeURIComponent(query)}`);
//        const products = await response.json();
//
//        // Affichez les suggestions (ceci est un exemple simple, vous voudrez probablement une UI plus sophistiquée)
//        const suggestionList = document.createElement('ul');
//        products.forEach(product => {
//            const li = document.createElement('li');
//            li.textContent = product.name;
//            li.addEventListener('click', () => {
//                input.value = product.name;
//                suggestionList.remove();
//            });
//            suggestionList.appendChild(li);
//        });
//
//        // Supprimez l'ancienne liste de suggestions s'il y en a une
//        const oldList = input.nextElementSibling;
//        if (oldList && oldList.tagName === 'UL') {
//            oldList.remove();
//        }
//
//        input.parentNode.insertBefore(suggestionList, input.nextSibling);
//    });
//};
//
//add_btn.addEventListener("click", function() {
//    const div_element = document.createElement("div");
//    div_element.className = "form-line";
//
//    const inputs = [
//        { name: "invoice", placeholder: "invoice" },
//        { name: "product", placeholder: "product", isAutocomplete: true },
//        { name: "quantity", placeholder: "quantity" },
//        { name: "price", placeholder: "price" }
//    ];
//
//    inputs.forEach(input => {
//        const inputElement = createInput(input.name, input.placeholder, input.isAutocomplete);
//        div_element.appendChild(inputElement);
//        if (input.isAutocomplete) {
//            setupAutocomplete(inputElement);
//        }
//    });
//
//    form.appendChild(div_element);
//    num++;
//});

const form = document.getElementById("myform");
const add_btn = document.getElementById("add_line");
const submit_btn = document.getElementById("submit_form");
let num = 0;

const createInput = (name, placeholder) => {
    const input = document.createElement("input");
    input.name = `${name}_${num}`;
    input.placeholder = placeholder;
    input.required = true; // rendre les champs obligatoires
    return input;
};

add_btn.addEventListener("click", function() {
    const div_element = document.createElement("div");
    div_element.className = "form-line";

    const inputs = [
        { name: "invoice", placeholder: "invoice" },
        { name: "product", placeholder: "product" },
        { name: "quantity", placeholder: "quantity" },
        { name: "price", placeholder: "price" }
    ];

    inputs.forEach(input => {
        div_element.appendChild(createInput(input.name, input.placeholder));
    });

    form.appendChild(div_element);
    num++;
});

// Fonction pour collecter les données du formulaire en tant qu'objet
const collectFormData = () => {
    const formData = new FormData(form);
    let data = {};

    formData.forEach((value, key) => {
        let [name, index] = key.split("_");
        if (!data[index]) {
            data[index] = {};
        }
        data[index][name] = value;
    });

    return data;
};

// Envoi du formulaire via AJAX
submit_btn.addEventListener("click", function(e) {
    e.preventDefault(); // Empêche le rechargement de la page

    const data = collectFormData();

    fetch("/supplier/create_invoice/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value // CSRF Token pour Django
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        console.log("Success:", result);
    })
    .catch(error => {
        console.error("Error:", error);
    });
});
