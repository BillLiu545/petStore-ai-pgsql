# petStore-ai-pgsql
In this repository is a sample pet store website created using Vue. The user uploads an image of the pet. AI then analyzes it to generate the description, name, and price so the user can buy the pet. Data for the purchase is then stored in a PostGreSQL database.

# How does it work?
When an image is uploaded, the AI model (Qwen) analyzes to generate the decsription, name, and  price (integration through Flask). When the user selects the option to buy the pet, it is added to the cart. When the user checks out, the data for the purchase in the cart is stored in a PostGreSQL database.
