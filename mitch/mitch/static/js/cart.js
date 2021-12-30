//adding a product to cart


let updatebtns = document.getElementsByClassName('update-cart')
for(i= 0; i < updatebtns.length; i++){
    updatebtns[i].addEventListener('click', function(){
        let productId = this.dataset.product
        let action = this.dataset.action
        console.log("productId:", productId, "action:", action  )
    
        console.log('USER:', user)
        if (user == 'AnonymousUser'){
            addCookieItem(productId, action )

        }else{
            updateUserOrder(productId, action)
        }

    })
}

function updateUserOrder(productId, action){
    console.log('User is logged in, dending data..')

    //using fetch api to send data to view function
    const url = '/update_item/'

    fetch(url, {
        method: 'POST',
        headers:{
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body:JSON.stringify({'productId': productId, 'action': action})
    })

    .then((response) => {
        return response.json()
    })

    .then((data) =>{
        console.log('data:', data)
        location.reload()
    })
}


function addCookieItem(productId, action){
    console.log('not logged in')

    if(action == 'add'){
        if(cart[productId] == undefined){
            cart[productId] = {'quantity':1}
        }else{
            cart[productId]['quantity'] += 1
        }
    }

    if(action == 'remove'){
        cart[productId]['quantity'] -= 1

        if(cart[productId]['quantity'] <= 0){
            console.log('Remove item')
            delete cart[productId]
        }
    }
    console.log('Cart Created', cart)
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
    location.reload()
}


