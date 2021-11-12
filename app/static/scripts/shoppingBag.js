const BAG_KEY = "SHOPPING_BAG"

function goToShoppingBag() {
    const xhr = new XMLHttpRequest();
    xhr.open('POST', '/checkout')
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onload = () => {
        if (xhr.status === 200 || xhr.status === 404) {
            document.open();
            document.write(xhr.responseText);
            document.close();
        } else {
            alert('Erro ' + xhr.status);
        }
    }
    xhr.send(JSON.stringify(getShoppingBag()));
}

function getShoppingBag() {
    return JSON.parse(localStorage.getItem(BAG_KEY));
}

function addItemToBag(item_id, item_name, item_price) {
    let bag = getShoppingBag() || [];

    let item = bag.find(el => el.id == item_id);

    if (item) {
        item.quantity += 1;
    } else {
        item = {
            id: item_id,
            name: item_name,
            price: item_price,
            quantity: 1
        };

        bag.push(item);
    }

    localStorage.setItem(BAG_KEY, JSON.stringify(bag));
}