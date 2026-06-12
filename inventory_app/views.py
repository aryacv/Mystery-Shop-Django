from urllib import request

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Item, PurchasedItem, CharacterClass


def identity_gate(request):
    if 'character_name' in request.session:
        return redirect('catalog')
    if request.method == 'POST':
        name = request.POST.get('character_name')
        char_class = request.POST.get('character_class')
        
        try:
            requested_gold = int(request.POST.get('starting_gold', 10))
        except ValueError:
            requested_gold = 10

        if name and char_class:
            if requested_gold > 1000 or requested_gold < 10:
                messages.error(request, "Invalid gold allowance requested.")
                return redirect('identity_gate')

            request.session['character_name'] = name
            request.session['character_class'] = char_class
            request.session['starting_gold'] = requested_gold 
            
            messages.success(request, f"Welcome, {name} the {char_class}!")
            return redirect('catalog')
    available_classes = CharacterClass.objects.all()
    return render(request, 'inventory_app/identity_gate.html', {'available_classes': available_classes})

def catalog(request):
    if 'character_name' not in request.session:
        request.session['character_name'] = "Nameless Wanderer"
    if 'character_class' not in request.session:
        request.session['character_class'] = "Mercenary"
    if 'starting_gold' not in request.session:
        request.session['starting_gold'] = 500  # Gives you 500gp to test purchases immediately!

    # 3. Handle item purchase logic safely if it's a POST request
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        try:
            item = Item.objects.get(id=item_id)
            current_gold = request.session.get('starting_gold', 0)
            
            if current_gold >= item.cost and item.stock > 0:
                item.stock -= 1
                item.save()
                request.session['starting_gold'] = current_gold - item.cost
                
                # Log the purchase in the database
                PurchasedItem.objects.create(
                    character_name=request.session['character_name'],
                    item=item,
                    
                )
                messages.success(request, f"You successfully claimed the {item.name}!")
            else:
                messages.error(request, "Inadequate gold coin or depleted supply.")
        except Item.DoesNotExist:
            messages.error(request, "This relic does not exist.")
            
        return redirect('catalog')

    # 4. Fetch the goods for the grid template
    items = Item.objects.all()
    return render(request, 'inventory_app/catalog.html', {'items': items})

# NEW VIEW FOR THE VAULT PAGE
def vault(request):
    if 'character_name' not in request.session:
        return redirect('identity_gate')
        
    buyer = request.session['character_name']
    
    # Fetch only the items belonging to this specific character
    # .select_related('item') optimizes the query so it pulls the item details (name, cost, image) smoothly
    owned_items = PurchasedItem.objects.filter(character_name=buyer).select_related('item')
    
    context = {
        'owned_items': owned_items
    }
    
    return render(request, 'inventory_app/vault.html', context)

def leave_shop(request):
    request.session.flush() # Wipes the session clean
    return redirect('identity_gate')