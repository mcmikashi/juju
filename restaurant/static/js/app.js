function showToast() {
var toastElList = [].slice.call(document.querySelectorAll('.toast'));
var option = {
    "delay": 3000
  }
var toastList = toastElList.map(function (toastEl) {
  return new bootstrap.Toast(toastEl,option)
});
    if (toastList.length >1) {
        for (let index = 0; index < toastList.length-1; index++) {
            toastList[index].hide();
        }
        toastList[toastList.length - 1].show();        
    } else {
        toastList[toastList.length - 1].show(); 
    }
    
}

var btn = document.getElementById("btn-pannier");
btn.onclick = afficherPannier;
function afficherPannier(){
    var pannier = document.getElementById("pannier");
    pannier.classList.toggle("d-none");
    pannier.classList.toggle("d-flex");

}
function rechercheCarte(){
    recherche = document.querySelector('input[name=recherche-nouriture]').value
    fetch("http://127.0.0.1:8000/recherche-nouriture/"+recherche, {
        headers:{
            'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest', 
        },
    })
    .then(response => {
        return response.json() 
    })
    .then(data => {
        carteCreation(data);
    })

}
function categorieCarte(id){
    fetch("http://127.0.0.1:8000/categorie-nouriture/"+id, {
        headers:{
            'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest', 
        },
    })
    .then(response => {
        return response.json() 
    })
    .then(data => {
        carteCreation(data);
    })

}
function viderPannier(){
    fetch("http://127.0.0.1:8000/vider-pannier/", {
        headers:{
            'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest', 
        },
    })
    .then(response => {
        return response.json() 
    })
    .then(data => {
        pannierCreation(data);
        document.getElementById("taost-info").innerHTML += "<div class='toast align-items-center text-white bg-danger border-0' role='alert' aria-live='assertive' aria-atomic='true'> <div class='d-flex'> <div class='toast-body'>Le panier a été vidé</div><button type='button' class='btn-close btn-close-white me-2 m-auto' data-bs-dismiss='toast' aria-label='Close'></button> </div></div>";
        showToast()
    })

}
function effacerPannier(id){
    fetch("http://127.0.0.1:8000/delete-pannier/"+id, {
        headers:{
            'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest', 
        },
    })
    .then(response => {
        return response.json() 
    })
    .then(data => {
        pannierCreation(data);
        document.getElementById("taost-info").innerHTML += "<div class='toast align-items-center text-white bg-danger border-0' role='alert' aria-live='assertive' aria-atomic='true'> <div class='d-flex'> <div class='toast-body'><span class='text-capitalize'>"+data.resultat+"</span>a été enlevé de votre panier</div><button type='button' class='btn-close btn-close-white me-2 m-auto' data-bs-dismiss='toast' aria-label='Close'></button> </div></div>"
        showToast()
    })

}
function carteCreation(data) {
    document.getElementById("carte-container").innerHTML = "";
    data.carte.forEach(function(item){
        document.getElementById("carte-container").innerHTML += "<div class='col-10 col-sm-6 col-lg-4 mx-auto my-3'> <div class='card item-restaurant'> <div class='img-container'> <img src='/upload/"+item.image+"' class='card-img-top' alt='"+item.nom+"'> <a class='store-item-icon stretched-link link-dark' onclick='ajouterPannier(1)'> <i class='fas fa-shopping-cart'></i> </a> </div><div class='card-body'> <div class='card-text d-flex justify-content-between text-capitalize'> <h5>"+item.nom+"</h5> <h5>"+item.prix+" €</h5> </div></div></div></div>";
    });
}
function pannierCreation(data) {
    if (data.nombre==0) {
        data.nombre = "Vide -";
        data.totale = "0 €";
    }else{
        data.nombre =  data.nombre+" éléments -";
        data.totale = data.totale+" €";
    }
    document.getElementById("nombre-item").textContent = data.nombre ;
    document.getElementById("totale-item").textContent= data.totale;
    document.getElementById("container-pannier").innerHTML = "";
    data.pannier.forEach(function(item){
        document.getElementById("container-pannier").innerHTML += "<div class='d-flex justify-content-around my-3 text-capitalize'><img class='rounded-circle img-mini' src='/upload/"+item.nouriture__image+"' alt='"+item.nouriture__nom+"'><div class='info-pannier text-center'><p class='fw-bold mb-0'>"+item.nouriture__nom+"</p><p class='fw-bold mb-0'>Quantité : "+item.quantite+"</p><p class='fw-bold mb-0'>Prix Unitaire :"+item.nouriture__prix+"</p></div><button class='btn btn-outline-danger' type='submit' onclick='effacerPannier("+item.id+")'><i class='fas fa-trash-alt'></i></button></div>";
    });

    document.getElementById("container-pannier").innerHTML +="<div class='text-center my-3'> <h4> <span>Totale :</span> <span> "+data.totale+"</span> </h4> </div><div class='d-flex d-flex justify-content-around my-3'> <button class='btn btn-outline-danger' onclick='viderPannier()'>Vider pannier</button> <a href='/commande/' class='btn btn-outline-success'>Commander</a> </div>";
}
function ajouterPannier(id){
    fetch("http://127.0.0.1:8000/ajouter-pannier/"+id, {
        headers:{
            'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest', 
        },
    })
    .then(response => {
        return response.json() 
    })
    .then(data => {
        pannierCreation(data);
        document.getElementById("taost-info").innerHTML += "<div class='toast align-items-center text-white bg-success border-0' role='alert' aria-live='assertive' aria-atomic='true'> <div class='d-flex'> <div class='toast-body'><span class='text-capitalize'>"+data.resultat+"</span>a été ajouté à votre panier</div><button type='button' class='btn-close btn-close-white me-2 m-auto' data-bs-dismiss='toast' aria-label='Close'></button> </div></div>"
        showToast()
    })

}
