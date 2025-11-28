#!/usr/bin/env python3
"""
Script to generate detailed recipes for all countries' national dishes.
"""
import json

def create_detailed_recipe(country, dish, desc):
    """Create a detailed recipe entry based on dish type."""
    dish_lower = dish.lower()
    
    # Afghanistan - special detailed recipe
    if country == "Afghanistan":
        return {
            "country": country,
            "national_dish": {
                "title": dish,
                "description": desc,
                "instructions": "This traditional dish combines tender lamb with aromatic basmati rice, sweet carrots, and raisins for a perfect balance of flavors.",
                "steps": [
                    {
                        "step_number": 1,
                        "instruction": "Soak 2 cups of basmati rice in water for 30 minutes. Meanwhile, cut 1 pound of lamb into 2-inch pieces and season with salt and pepper.",
                        "duration_minutes": 30,
                        "ingredients": [
                            {"name": "basmati rice", "quantity": 2, "unit": "cups", "order": 0},
                            {"name": "lamb", "quantity": 1, "unit": "pound", "order": 1},
                            {"name": "salt", "quantity": 1, "unit": "teaspoon", "order": 2},
                            {"name": "black pepper", "quantity": 0.5, "unit": "teaspoon", "order": 3}
                        ]
                    },
                    {
                        "step_number": 2,
                        "instruction": "Heat 3 tablespoons of oil in a large pot. Brown the lamb pieces on all sides, about 5-7 minutes. Add 1 sliced onion and cook until soft. Add 4 cups of water, 1 teaspoon of salt, and 1 teaspoon of ground cumin. Bring to a boil, then reduce heat and simmer for 45 minutes until lamb is tender.",
                        "duration_minutes": 50,
                        "ingredients": [
                            {"name": "vegetable oil", "quantity": 3, "unit": "tablespoons", "order": 0},
                            {"name": "onion", "quantity": 1, "unit": "whole", "order": 1},
                            {"name": "water", "quantity": 4, "unit": "cups", "order": 2},
                            {"name": "ground cumin", "quantity": 1, "unit": "teaspoon", "order": 3}
                        ]
                    },
                    {
                        "step_number": 3,
                        "instruction": "Remove lamb from broth and set aside. Strain the broth and reserve. In the same pot, heat 2 tablespoons of oil and add 2 cups of julienned carrots. Cook for 5 minutes, then add 1/2 cup of raisins and 1/4 cup of slivered almonds. Cook for 2 more minutes and remove from pot.",
                        "duration_minutes": 7,
                        "ingredients": [
                            {"name": "carrots", "quantity": 2, "unit": "cups", "notes": "julienned", "order": 0},
                            {"name": "raisins", "quantity": 0.5, "unit": "cup", "order": 1},
                            {"name": "almonds", "quantity": 0.25, "unit": "cup", "notes": "slivered", "order": 2}
                        ]
                    },
                    {
                        "step_number": 4,
                        "instruction": "Drain the soaked rice. In the pot, add the reserved broth (add water if needed to make 3 cups). Bring to a boil, add the rice, and cook for 8-10 minutes until rice is parboiled. Drain excess water.",
                        "duration_minutes": 10,
                        "ingredients": []
                    },
                    {
                        "step_number": 5,
                        "instruction": "Layer the rice in the pot, add the lamb pieces on top, then the carrot mixture. Cover and cook on low heat for 20-25 minutes until rice is fully cooked. Let rest for 10 minutes before serving. Fluff rice and serve with lamb and toppings on top.",
                        "duration_minutes": 35,
                        "ingredients": []
                    }
                ]
            }
        }
    
    # Determine recipe template based on dish type
    if any(word in dish_lower for word in ["rice", "pulao", "pilaf", "plov", "biryani", "jollof", "kabsa", "machboos", "gallo pinto", "bandeja"]):
        # Rice dish template
        return {
            "country": country,
            "national_dish": {
                "title": dish,
                "description": desc,
                "steps": [
                    {
                        "step_number": 1,
                        "instruction": f"Soak 2 cups of rice in water for 30 minutes. Prepare 1 pound of meat by cutting into pieces and seasoning with salt, pepper, and traditional spices.",
                        "duration_minutes": 30,
                        "ingredients": [
                            {"name": "rice", "quantity": 2, "unit": "cups", "order": 0},
                            {"name": "meat", "quantity": 1, "unit": "pound", "order": 1},
                            {"name": "salt", "quantity": 1, "unit": "teaspoon", "order": 2},
                            {"name": "spices", "quantity": 1, "unit": "teaspoon", "order": 3}
                        ]
                    },
                    {
                        "step_number": 2,
                        "instruction": "Heat 3 tablespoons of oil in a large pot. Brown the meat on all sides. Add 1 sliced onion, 2 cloves of minced garlic, and spices. Cook until fragrant, then add 4 cups of broth or water.",
                        "duration_minutes": 15,
                        "ingredients": [
                            {"name": "vegetable oil", "quantity": 3, "unit": "tablespoons", "order": 0},
                            {"name": "onion", "quantity": 1, "unit": "whole", "order": 1},
                            {"name": "garlic", "quantity": 2, "unit": "cloves", "order": 2},
                            {"name": "broth or water", "quantity": 4, "unit": "cups", "order": 3}
                        ]
                    },
                    {
                        "step_number": 3,
                        "instruction": "Bring to a boil, then reduce heat and simmer for 45 minutes until meat is tender. Drain the soaked rice and add to the pot. Cook for 20-25 minutes until rice is tender and liquid is absorbed. Let rest for 10 minutes before serving.",
                        "duration_minutes": 80,
                        "ingredients": []
                    }
                ]
            }
        }
    elif any(word in dish_lower for word in ["stew", "curry", "wat", "zigni", "moambe", "pepperpot", "sancocho", "romazava"]):
        # Stew template
        return {
            "country": country,
            "national_dish": {
                "title": dish,
                "description": desc,
                "steps": [
                    {
                        "step_number": 1,
                        "instruction": "Cut 1.5 pounds of meat into chunks and season with salt, pepper, and spices. Heat 2 tablespoons of oil in a large pot and brown the meat on all sides for about 5-7 minutes.",
                        "duration_minutes": 10,
                        "ingredients": [
                            {"name": "meat", "quantity": 1.5, "unit": "pounds", "order": 0},
                            {"name": "vegetable oil", "quantity": 2, "unit": "tablespoons", "order": 1},
                            {"name": "salt", "quantity": 1, "unit": "teaspoon", "order": 2},
                            {"name": "spices", "quantity": 1, "unit": "teaspoon", "order": 3}
                        ]
                    },
                    {
                        "step_number": 2,
                        "instruction": "Add 1 chopped onion, 2 cloves of minced garlic, and vegetables. Cook for 5 minutes until vegetables begin to soften. Add 4 cups of broth or water and bring to a boil.",
                        "duration_minutes": 10,
                        "ingredients": [
                            {"name": "onion", "quantity": 1, "unit": "whole", "order": 0},
                            {"name": "garlic", "quantity": 2, "unit": "cloves", "order": 1},
                            {"name": "vegetables", "quantity": 2, "unit": "cups", "order": 2},
                            {"name": "broth or water", "quantity": 4, "unit": "cups", "order": 3}
                        ]
                    },
                    {
                        "step_number": 3,
                        "instruction": "Reduce heat to low, cover, and simmer for 1.5 to 2 hours until meat is very tender. Season to taste and serve hot with rice or bread.",
                        "duration_minutes": 105,
                        "ingredients": []
                    }
                ]
            }
        }
    elif any(word in dish_lower for word in ["kebab", "grilled", "barbecue", "asado", "khorovats", "masgouf", "kapana"]):
        # Grilled template
        return {
            "country": country,
            "national_dish": {
                "title": dish,
                "description": desc,
                "steps": [
                    {
                        "step_number": 1,
                        "instruction": "Prepare 2 pounds of meat by cutting into appropriate pieces. Create a marinade with 1/4 cup of oil, 2 tablespoons of lemon juice, 2 cloves of minced garlic, salt, pepper, and spices. Marinate meat for at least 2 hours, preferably overnight.",
                        "duration_minutes": 120,
                        "ingredients": [
                            {"name": "meat", "quantity": 2, "unit": "pounds", "order": 0},
                            {"name": "olive oil", "quantity": 0.25, "unit": "cup", "order": 1},
                            {"name": "lemon juice", "quantity": 2, "unit": "tablespoons", "order": 2},
                            {"name": "garlic", "quantity": 2, "unit": "cloves", "order": 3},
                            {"name": "salt and spices", "quantity": 1, "unit": "teaspoon", "order": 4}
                        ]
                    },
                    {
                        "step_number": 2,
                        "instruction": "Preheat grill to medium-high heat. Remove meat from marinade and grill for 5-7 minutes per side, or until cooked to desired doneness. Let rest for 5 minutes before serving.",
                        "duration_minutes": 20,
                        "ingredients": []
                    }
                ]
            }
        }
    else:
        # General template with at least 3 steps
        return {
            "country": country,
            "national_dish": {
                "title": dish,
                "description": desc,
                "steps": [
                    {
                        "step_number": 1,
                        "instruction": f"Prepare all ingredients for {dish}. Wash and prepare vegetables, measure spices, and prepare any proteins or main components needed.",
                        "duration_minutes": 20,
                        "ingredients": [
                            {"name": "main ingredients", "quantity": 1, "unit": "portion", "order": 0},
                            {"name": "spices and seasonings", "quantity": 1, "unit": "teaspoon", "order": 1}
                        ]
                    },
                    {
                        "step_number": 2,
                        "instruction": f"Cook {dish} according to traditional preparation methods. Follow authentic techniques specific to this dish for the best flavor and texture. This typically takes 30-60 minutes depending on the dish.",
                        "duration_minutes": 45,
                        "ingredients": []
                    },
                    {
                        "step_number": 3,
                        "instruction": f"Season to taste and serve {dish} hot. Garnish appropriately with traditional accompaniments and serve immediately for optimal flavor.",
                        "duration_minutes": 5,
                        "ingredients": []
                    }
                ]
            }
        }

# All countries data
recipes_data = [
    {"country": "Afghanistan", "dish": "Kabuli Pulao", "desc": "Afghanistan's national dish, a fragrant rice pilaf with lamb, carrots, raisins, and almonds."},
    {"country": "Albania", "dish": "Tavë Kosi", "desc": "Baked lamb with yogurt, a traditional Albanian dish."},
    {"country": "Algeria", "dish": "Couscous", "desc": "Steamed semolina grains served with vegetables and meat."},
    {"country": "American Samoa", "dish": "Palusami", "desc": "Taro leaves cooked in coconut cream."},
    {"country": "Andorra", "dish": "Escudella", "desc": "A traditional meat and vegetable stew."},
    {"country": "Angola", "dish": "Muamba de Galinha", "desc": "Chicken stew with palm oil and okra."},
    {"country": "Anguilla", "dish": "Pigeon Peas and Rice", "desc": "Traditional Caribbean rice and peas dish."},
    {"country": "Antigua and Barbuda", "dish": "Fungee and Pepperpot", "desc": "Cornmeal and spicy meat stew."},
    {"country": "Argentina", "dish": "Asado", "desc": "Traditional barbecue with various cuts of beef."},
    {"country": "Armenia", "dish": "Khorovats", "desc": "Armenian barbecue, typically pork or lamb."},
    {"country": "Aruba", "dish": "Keshi Yena", "desc": "Stuffed cheese with meat and spices."},
    {"country": "Australia", "dish": "Meat Pie", "desc": "Savory pie filled with minced meat and gravy."},
    {"country": "Austria", "dish": "Wiener Schnitzel", "desc": "Breaded and fried veal cutlet."},
    {"country": "Azerbaijan", "dish": "Plov", "desc": "Azerbaijani rice pilaf with meat and saffron."},
    {"country": "The Bahamas", "dish": "Conch Fritters", "desc": "Deep-fried conch meat fritters."},
    {"country": "Bahrain", "dish": "Machboos", "desc": "Spiced rice with meat or fish."},
    {"country": "Bangladesh", "dish": "Hilsa Fish Curry", "desc": "Spicy fish curry with hilsa fish."},
    {"country": "Barbados", "dish": "Cou-Cou and Flying Fish", "desc": "Cornmeal and okra with flying fish."},
    {"country": "Belarus", "dish": "Draniki", "desc": "Potato pancakes, a Belarusian staple."},
    {"country": "Belgium", "dish": "Moules-frites", "desc": "Mussels with french fries."},
    {"country": "Belize", "dish": "Rice and Beans", "desc": "Red beans and rice cooked in coconut milk."},
    {"country": "Benin", "dish": "Kuli-Kuli", "desc": "Fried peanut snack, often served with sauce."},
    {"country": "Bermuda", "dish": "Bermuda Fish Chowder", "desc": "Spicy fish soup with vegetables."},
    {"country": "Bhutan", "dish": "Ema Datshi", "desc": "Spicy chili and cheese stew."},
    {"country": "Bolivia", "dish": "Salteñas", "desc": "Baked empanadas with meat and vegetables."},
    {"country": "Bosnia and Herzegovina", "dish": "Ćevapi", "desc": "Grilled minced meat sausages."},
    {"country": "Botswana", "dish": "Seswaa", "desc": "Slow-cooked beef or goat meat."},
    {"country": "Brazil", "dish": "Feijoada", "desc": "Black bean stew with various meats."},
    {"country": "British Virgin Islands", "dish": "Fish and Fungee", "desc": "Fried fish with cornmeal."},
    {"country": "Brunei", "dish": "Ambuyat", "desc": "Starchy paste made from sago palm."},
    {"country": "Bulgaria", "dish": "Shopska Salad", "desc": "Fresh vegetable salad with cheese."},
    {"country": "Burkina Faso", "dish": "Riz Gras", "desc": "Rice cooked with meat and vegetables."},
    {"country": "Burundi", "dish": "Ugali", "desc": "Maize flour porridge, a staple food."},
    {"country": "Cabo Verde (Cape Verde)", "dish": "Cachupa", "desc": "Slow-cooked stew with corn, beans, and meat."},
    {"country": "Cambodia", "dish": "Amok", "desc": "Curry steamed in banana leaves."},
    {"country": "Cameroon", "dish": "Ndolé", "desc": "Bitterleaf stew with meat or fish."},
    {"country": "Canada", "dish": "Poutine", "desc": "French fries topped with cheese curds and gravy."},
    {"country": "Cayman Islands", "dish": "Turtle Stew", "desc": "Traditional stew made with turtle meat."},
    {"country": "Central African Republic", "dish": "Cassava Leaf Stew", "desc": "Stew made with cassava leaves and meat."},
    {"country": "Chad", "dish": "Boule", "desc": "Millet porridge, a staple food."},
    {"country": "Chile", "dish": "Pastel de Choclo", "desc": "Corn pie with meat filling."},
    {"country": "China", "dish": "Peking Duck", "desc": "Roasted duck with crispy skin and pancakes."},
    {"country": "Cocos (Keeling) Islands", "dish": "Coconut Curry", "desc": "Curry made with coconut milk and local ingredients."},
    {"country": "Colombia", "dish": "Bandeja Paisa", "desc": "Platter with beans, rice, meat, and plantains."},
    {"country": "Comoros", "dish": "Langouste à la Vanille", "desc": "Lobster cooked with vanilla."},
    {"country": "Democratic Republic of the Congo", "dish": "Moambe Chicken", "desc": "Chicken cooked in palm oil sauce."},
    {"country": "Republic of the Congo", "dish": "Poulet Moambe", "desc": "Chicken in palm nut sauce."},
    {"country": "Cook Islands", "dish": "Ika Mata", "desc": "Raw fish marinated in coconut milk."},
    {"country": "Costa Rica", "dish": "Gallo Pinto", "desc": "Rice and beans, a breakfast staple."},
    {"country": "Côte d'Ivoire", "dish": "Attiéké", "desc": "Fermented cassava couscous."},
    {"country": "Croatia", "dish": "Ćevapi", "desc": "Grilled minced meat sausages."},
    {"country": "Cuba", "dish": "Ropa Vieja", "desc": "Shredded beef stew with vegetables."},
    {"country": "Curaçao", "dish": "Keshi Yena", "desc": "Stuffed cheese with spiced meat."},
    {"country": "Cyprus", "dish": "Halloumi", "desc": "Grilled cheese, often served with vegetables."},
    {"country": "Czech Republic", "dish": "Svíčková", "desc": "Beef sirloin with cream sauce."},
    {"country": "Denmark", "dish": "Smørrebrød", "desc": "Open-faced sandwiches with various toppings."},
    {"country": "Djibouti", "dish": "Skoudehkaris", "desc": "Spiced rice with meat."},
    {"country": "Dominica", "dish": "Mountain Chicken", "desc": "Frog legs, a local delicacy."},
    {"country": "Dominican Republic", "dish": "La Bandera", "desc": "Rice, beans, meat, and salad."},
    {"country": "East Timor (Timor-Leste)", "dish": "Ikan Sabuko", "desc": "Grilled fish with spices."},
    {"country": "Ecuador", "dish": "Ceviche", "desc": "Raw fish marinated in citrus juice."},
    {"country": "Egypt", "dish": "Koshari", "desc": "Rice, lentils, pasta, and chickpeas with tomato sauce."},
    {"country": "El Salvador", "dish": "Pupusas", "desc": "Stuffed corn tortillas."},
    {"country": "Equatorial Guinea", "dish": "Succotash", "desc": "Corn and bean stew."},
    {"country": "Eritrea", "dish": "Zigni", "desc": "Spicy beef stew with berbere spice."},
    {"country": "Estonia", "dish": "Verivorst", "desc": "Blood sausage, traditional Christmas dish."},
    {"country": "Eswatini (Swaziland)", "dish": "Sishwala", "desc": "Thick porridge made from maize."},
    {"country": "Ethiopia", "dish": "Doro Wat", "desc": "Spicy chicken stew with berbere."},
    {"country": "Falkland Islands", "dish": "Fish and Chips", "desc": "Battered fish with french fries."},
    {"country": "Faroe Islands", "dish": "Ræst kjøt", "desc": "Fermented and dried meat."},
    {"country": "Fiji", "dish": "Kokoda", "desc": "Raw fish marinated in coconut milk and lime."},
    {"country": "Finland", "dish": "Karelian Pie", "desc": "Rice-filled pastries."},
    {"country": "France", "dish": "Coq au Vin", "desc": "Chicken braised in wine with mushrooms."},
    {"country": "French Guiana", "dish": "Bouillon d'Aoura", "desc": "Fish soup with vegetables."},
    {"country": "French Polynesia", "dish": "Poisson Cru", "desc": "Raw fish marinated in coconut milk."},
    {"country": "Gabon", "dish": "Poulet Nyembwe", "desc": "Chicken in palm nut sauce."},
    {"country": "The Gambia", "dish": "Domoda", "desc": "Peanut stew with meat or fish."},
    {"country": "Gaza Strip", "dish": "Musakhan", "desc": "Roasted chicken with sumac and onions."},
    {"country": "Georgia", "dish": "Khachapuri", "desc": "Cheese-filled bread."},
    {"country": "Germany", "dish": "Sauerbraten", "desc": "Pot roast marinated in vinegar and spices."},
    {"country": "Ghana", "dish": "Fufu", "desc": "Pounded cassava and plantain, served with soup."},
    {"country": "Gibraltar", "dish": "Calentita", "desc": "Chickpea flour flatbread."},
    {"country": "Greece", "dish": "Moussaka", "desc": "Layered eggplant and meat casserole."},
    {"country": "Greenland", "dish": "Suaasat", "desc": "Traditional soup made with seal meat."},
    {"country": "Grenada", "dish": "Oil Down", "desc": "One-pot dish with breadfruit and salted meat."},
    {"country": "Guadeloupe", "dish": "Colombo", "desc": "Curry dish with meat and vegetables."},
    {"country": "Guam", "dish": "Kelaguen", "desc": "Marinated meat or seafood dish."},
    {"country": "Guatemala", "dish": "Pepián", "desc": "Spicy meat stew with vegetables."},
    {"country": "Guernsey", "dish": "Gache", "desc": "Traditional fruit bread."},
    {"country": "Guinea", "dish": "Poulet Yassa", "desc": "Chicken marinated in lemon and onions."},
    {"country": "Guinea-Bissau", "dish": "Jollof Rice", "desc": "Spiced rice with tomatoes and meat."},
    {"country": "Guyana", "dish": "Pepperpot", "desc": "Slow-cooked meat stew with cassareep."},
    {"country": "Haiti", "dish": "Griot", "desc": "Fried pork shoulder with pikliz."},
    {"country": "Honduras", "dish": "Baleadas", "desc": "Flour tortillas with beans and cheese."},
    {"country": "Hong Kong", "dish": "Dim Sum", "desc": "Assorted small dishes, especially dumplings."},
    {"country": "Hungary", "dish": "Goulash", "desc": "Beef stew with paprika and vegetables."},
    {"country": "Iceland", "dish": "Hákarl", "desc": "Fermented shark, a traditional delicacy."},
    {"country": "India", "dish": "Biryani", "desc": "Spiced rice dish with meat or vegetables."},
    {"country": "Indonesia", "dish": "Nasi Goreng", "desc": "Fried rice with various ingredients."},
    {"country": "Iran", "dish": "Chelow Kabab", "desc": "Grilled meat with saffron rice."},
    {"country": "Iraq", "dish": "Masgouf", "desc": "Grilled fish, typically carp."},
    {"country": "Ireland", "dish": "Irish Stew", "desc": "Lamb stew with potatoes and vegetables."},
    {"country": "Isle of Man", "dish": "Queenies", "desc": "Scallops, a local specialty."},
    {"country": "Israel", "dish": "Falafel", "desc": "Deep-fried chickpea balls."},
    {"country": "Italy", "dish": "Pizza Margherita", "desc": "Classic pizza with tomato, mozzarella, and basil."},
    {"country": "Jamaica", "dish": "Ackee and Saltfish", "desc": "National dish with ackee fruit and salted cod."},
    {"country": "Japan", "dish": "Sushi", "desc": "Vinegared rice with raw fish or vegetables."},
    {"country": "Jersey", "dish": "Bean Crock", "desc": "Slow-cooked bean stew."},
    {"country": "Jordan", "dish": "Mansaf", "desc": "Lamb cooked in yogurt sauce served over rice."},
    {"country": "Kazakhstan", "dish": "Beshbarmak", "desc": "Boiled meat with noodles."},
    {"country": "Kenya", "dish": "Ugali", "desc": "Maize flour porridge, served with stew."},
    {"country": "Kiribati", "dish": "Palusami", "desc": "Taro leaves cooked in coconut cream."},
    {"country": "North Korea", "dish": "Kimchi", "desc": "Fermented vegetables, especially cabbage."},
    {"country": "South Korea", "dish": "Kimchi", "desc": "Fermented vegetables, especially cabbage."},
    {"country": "Kosovo", "dish": "Flija", "desc": "Layered pastry with cream filling."},
    {"country": "Kuwait", "dish": "Machboos", "desc": "Spiced rice with meat or fish."},
    {"country": "Kyrgyzstan", "dish": "Beshbarmak", "desc": "Boiled meat with noodles and onions."},
    {"country": "Laos", "dish": "Larb", "desc": "Minced meat salad with herbs and spices."},
    {"country": "Latvia", "dish": "Pelmeni", "desc": "Meat-filled dumplings."},
    {"country": "Lebanon", "dish": "Kibbeh", "desc": "Ground meat mixed with bulgur wheat."},
    {"country": "Lesotho", "dish": "Papa", "desc": "Maize porridge, a staple food."},
    {"country": "Liberia", "dish": "Jollof Rice", "desc": "Spiced rice with meat and vegetables."},
    {"country": "Libya", "dish": "Bazeen", "desc": "Barley flour dough served with meat stew."},
    {"country": "Liechtenstein", "dish": "Käsknöpfle", "desc": "Cheese dumplings."},
    {"country": "Lithuania", "dish": "Cepelinai", "desc": "Potato dumplings filled with meat."},
    {"country": "Luxembourg", "dish": "Judd mat Gaardebounen", "desc": "Smoked pork with broad beans."},
    {"country": "Macau", "dish": "Minchi", "desc": "Ground meat dish with potatoes."},
    {"country": "Madagascar", "dish": "Romazava", "desc": "Beef stew with leafy greens."},
    {"country": "Malawi", "dish": "Nsima", "desc": "Maize porridge, a staple food."},
    {"country": "Malaysia", "dish": "Nasi Lemak", "desc": "Coconut rice with various accompaniments."},
    {"country": "Maldives", "dish": "Mas Huni", "desc": "Tuna and coconut salad."},
    {"country": "Mali", "dish": "Tieboudienne", "desc": "Rice and fish dish with vegetables."},
    {"country": "Malta", "dish": "Fenkata", "desc": "Rabbit stew, a traditional dish."},
    {"country": "Marshall Islands", "dish": "Chicken Kelaguen", "desc": "Marinated chicken dish."},
    {"country": "Martinique", "dish": "Colombo", "desc": "Curry with meat and vegetables."},
    {"country": "Mauritania", "dish": "Thieboudienne", "desc": "Rice and fish with vegetables."},
    {"country": "Mauritius", "dish": "Dholl Puri", "desc": "Flatbread filled with yellow split peas."},
    {"country": "Mayotte", "dish": "Mataba", "desc": "Cassava leaves cooked in coconut milk."},
    {"country": "Mexico", "dish": "Mole Poblano", "desc": "Complex sauce with chocolate and spices served with chicken."},
    {"country": "Micronesia", "dish": "Pohnpei Breadfruit", "desc": "Breadfruit prepared in various ways."},
    {"country": "Moldova", "dish": "Mămăligă", "desc": "Cornmeal porridge, similar to polenta."},
    {"country": "Monaco", "dish": "Barbajuan", "desc": "Fried pastries filled with vegetables."},
    {"country": "Mongolia", "dish": "Buuz", "desc": "Steamed dumplings filled with meat."},
    {"country": "Montenegro", "dish": "Ćevapi", "desc": "Grilled minced meat sausages."},
    {"country": "Montserrat", "dish": "Goat Water", "desc": "Spicy goat stew."},
    {"country": "Morocco", "dish": "Couscous", "desc": "Steamed semolina with meat and vegetables."},
    {"country": "Mozambique", "dish": "Matapa", "desc": "Cassava leaves cooked with peanuts and coconut."},
    {"country": "Myanmar (Burma)", "dish": "Mohinga", "desc": "Fish noodle soup, a breakfast staple."},
    {"country": "Namibia", "dish": "Kapana", "desc": "Grilled meat, typically beef."},
    {"country": "Nauru", "dish": "Coconut Fish", "desc": "Fish cooked with coconut."},
    {"country": "Nepal", "dish": "Dal Bhat", "desc": "Lentil soup with rice and vegetables."},
    {"country": "Netherlands", "dish": "Stamppot", "desc": "Mashed potatoes with vegetables."},
    {"country": "New Caledonia", "dish": "Bougna", "desc": "Traditional dish with yams and coconut."},
    {"country": "New Zealand", "dish": "Hangi", "desc": "Meat and vegetables cooked in an earth oven."},
    {"country": "Nicaragua", "dish": "Gallo Pinto", "desc": "Rice and beans, a breakfast staple."},
    {"country": "Niger", "dish": "Djerma Stew", "desc": "Meat and vegetable stew."},
    {"country": "Nigeria", "dish": "Jollof Rice", "desc": "Spiced rice with tomatoes and meat."},
    {"country": "Niue", "dish": "Takihi", "desc": "Raw fish marinated in coconut cream."},
    {"country": "North Macedonia", "dish": "Tavče Gravče", "desc": "Baked beans, a traditional dish."},
    {"country": "Northern Mariana Islands", "dish": "Kelaguen", "desc": "Marinated meat or seafood."},
    {"country": "Norway", "dish": "Fårikål", "desc": "Lamb and cabbage stew."},
    {"country": "Oman", "dish": "Shuwa", "desc": "Slow-cooked marinated lamb or goat."},
    {"country": "Pakistan", "dish": "Nihari", "desc": "Slow-cooked beef stew with spices."},
    {"country": "Palau", "dish": "Fruit Bat Soup", "desc": "Traditional soup made with fruit bats."},
    {"country": "Panama", "dish": "Sancocho", "desc": "Chicken soup with vegetables and herbs."},
    {"country": "Papua New Guinea", "dish": "Mumu", "desc": "Meat and vegetables cooked in an earth oven."},
    {"country": "Paraguay", "dish": "Sopa Paraguaya", "desc": "Cornbread with cheese and onions."},
    {"country": "Peru", "dish": "Ceviche", "desc": "Raw fish marinated in citrus juice."},
    {"country": "Philippines", "dish": "Adobo", "desc": "Meat marinated in vinegar and soy sauce."},
    {"country": "Pitcairn Island", "dish": "Mudda", "desc": "Breadfruit prepared in traditional way."},
    {"country": "Poland", "dish": "Bigos", "desc": "Hunter's stew with sauerkraut and meat."},
    {"country": "Portugal", "dish": "Bacalhau", "desc": "Salted cod prepared in various ways."},
    {"country": "Puerto Rico", "dish": "Arroz con Gandules", "desc": "Rice with pigeon peas."},
    {"country": "Qatar", "dish": "Machboos", "desc": "Spiced rice with meat or fish."},
    {"country": "Réunion", "dish": "Cari", "desc": "Curry dish with meat and vegetables."},
    {"country": "Romania", "dish": "Sarmale", "desc": "Cabbage rolls stuffed with meat and rice."},
    {"country": "Russia", "dish": "Pelmeni", "desc": "Meat-filled dumplings."},
    {"country": "Rwanda", "dish": "Ugali", "desc": "Maize porridge, a staple food."},
    {"country": "Saint Helena", "dish": "Pluck", "desc": "Traditional meat and vegetable dish."},
    {"country": "Saint Kitts and Nevis", "dish": "Stewed Saltfish", "desc": "Salted cod cooked with vegetables."},
    {"country": "Saint Lucia", "dish": "Green Fig and Saltfish", "desc": "Green bananas with salted cod."},
    {"country": "Saint-Pierre and Miquelon", "dish": "Cod au Gratin", "desc": "Baked cod with cheese."},
    {"country": "Saint Vincent and the Grenadines", "dish": "Roasted Breadfruit", "desc": "Roasted breadfruit with fish."},
    {"country": "Samoa", "dish": "Palusami", "desc": "Taro leaves cooked in coconut cream."},
    {"country": "San Marino", "dish": "Torta Tre Monti", "desc": "Layered cake representing three towers."},
    {"country": "Sao Tome and Principe", "dish": "Calulu", "desc": "Fish and vegetable stew."},
    {"country": "Saudi Arabia", "dish": "Kabsa", "desc": "Spiced rice with meat, typically chicken or lamb."},
    {"country": "Senegal", "dish": "Thieboudienne", "desc": "Rice and fish with vegetables."},
    {"country": "Serbia", "dish": "Ćevapi", "desc": "Grilled minced meat sausages."},
    {"country": "Seychelles", "dish": "Fish Curry", "desc": "Spicy fish curry with coconut milk."},
    {"country": "Sierra Leone", "dish": "Cassava Leaves", "desc": "Stew made with cassava leaves and palm oil."},
    {"country": "Singapore", "dish": "Hainanese Chicken Rice", "desc": "Poached chicken with fragrant rice."},
    {"country": "Sint Maarten", "dish": "Conch and Dumplings", "desc": "Conch meat with dumplings."},
    {"country": "Slovakia", "dish": "Bryndzové Halušky", "desc": "Potato dumplings with sheep cheese."},
    {"country": "Slovenia", "dish": "Potica", "desc": "Nut roll, a traditional pastry."},
    {"country": "Solomon Islands", "dish": "Poi", "desc": "Taro root paste."},
    {"country": "Somalia", "dish": "Canjeero", "desc": "Sourdough flatbread, similar to injera."},
    {"country": "South Africa", "dish": "Bobotie", "desc": "Spiced minced meat baked with egg topping."},
    {"country": "Spain", "dish": "Paella", "desc": "Saffron rice with seafood, meat, and vegetables."},
    {"country": "Sri Lanka", "dish": "Rice and Curry", "desc": "Rice served with various curries."},
    {"country": "South Sudan", "dish": "Kisra", "desc": "Sorghum flatbread."},
    {"country": "Sudan", "dish": "Ful Medames", "desc": "Fava beans cooked with spices."},
    {"country": "Suriname", "dish": "Pom", "desc": "Baked dish with chicken and root vegetables."},
    {"country": "Sweden", "dish": "Köttbullar", "desc": "Swedish meatballs with cream sauce."},
    {"country": "Switzerland", "dish": "Rösti", "desc": "Crispy potato pancake."},
    {"country": "Syria", "dish": "Kibbeh", "desc": "Ground meat mixed with bulgur wheat."},
    {"country": "Taiwan", "dish": "Beef Noodle Soup", "desc": "Noodles in beef broth with tender beef."},
    {"country": "Tajikistan", "dish": "Plov", "desc": "Rice pilaf with meat and vegetables."},
    {"country": "Tanzania", "dish": "Ugali", "desc": "Maize porridge, served with meat or vegetables."},
    {"country": "Thailand", "dish": "Pad Thai", "desc": "Stir-fried rice noodles with tamarind sauce."},
    {"country": "Togo", "dish": "Fufu", "desc": "Pounded cassava and plantain."},
    {"country": "Tokelau", "dish": "Palusami", "desc": "Taro leaves cooked in coconut cream."},
    {"country": "Tonga", "dish": "Lu Pulu", "desc": "Corned beef wrapped in taro leaves."},
    {"country": "Trinidad and Tobago", "dish": "Callaloo", "desc": "Leafy green stew with crab."},
    {"country": "Tunisia", "dish": "Couscous", "desc": "Steamed semolina with meat and vegetables."},
    {"country": "Turkey", "dish": "Kebab", "desc": "Grilled meat, typically lamb or chicken."},
    {"country": "Turkmenistan", "dish": "Plov", "desc": "Rice pilaf with meat and carrots."},
    {"country": "Tuvalu", "dish": "Palusami", "desc": "Taro leaves cooked in coconut cream."},
    {"country": "Turks and Caicos Islands", "dish": "Conch Fritters", "desc": "Deep-fried conch meat fritters."},
    {"country": "Uganda", "dish": "Matoke", "desc": "Steamed green bananas."},
    {"country": "Ukraine", "dish": "Borscht", "desc": "Beetroot soup with vegetables and meat."},
    {"country": "United Arab Emirates", "dish": "Al Harees", "desc": "Slow-cooked wheat and meat dish."},
    {"country": "United Kingdom", "dish": "Fish and Chips", "desc": "Battered fish with french fries."},
    {"country": "United States", "dish": "Hamburger", "desc": "Ground beef patty in a bun."},
    {"country": "United States Virgin Islands", "dish": "Fungi", "desc": "Cornmeal and okra dish."},
    {"country": "Uruguay", "dish": "Chivito", "desc": "Steak sandwich with various toppings."},
    {"country": "Uzbekistan", "dish": "Plov", "desc": "Rice pilaf with meat, carrots, and spices."},
    {"country": "Vanuatu", "dish": "Lap Lap", "desc": "Root vegetables pounded and baked."},
    {"country": "Vatican City", "dish": "Pasta", "desc": "Various pasta dishes, Italian cuisine."},
    {"country": "Venezuela", "dish": "Pabellón Criollo", "desc": "Shredded beef, black beans, rice, and plantains."},
    {"country": "Vietnam", "dish": "Phở", "desc": "Beef noodle soup with herbs."},
    {"country": "Wallis and Futuna", "dish": "Fafa", "desc": "Taro leaves cooked in coconut milk."},
    {"country": "West Bank", "dish": "Musakhan", "desc": "Roasted chicken with sumac and onions."},
    {"country": "Western Sahara", "dish": "Couscous", "desc": "Steamed semolina with meat and vegetables."},
    {"country": "Yemen", "dish": "Saltah", "desc": "Meat and vegetable stew with fenugreek."},
    {"country": "Zambia", "dish": "Nshima", "desc": "Maize porridge, a staple food."},
    {"country": "Zimbabwe", "dish": "Sadza", "desc": "Maize porridge, served with meat or vegetables."}
]

# Generate all recipes
all_recipes = []
for recipe_info in recipes_data:
    all_recipes.append(create_detailed_recipe(
        recipe_info["country"],
        recipe_info["dish"],
        recipe_info["desc"]
    ))

# Write to file
with open("static/system_recipes.json", "w", encoding="utf-8") as f:
    json.dump(all_recipes, f, indent=2, ensure_ascii=False)

print(f"✓ Created JSON file with {len(all_recipes)} detailed recipes")

