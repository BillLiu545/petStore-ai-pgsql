<template>
  <div class="container">
    <div class="login">
      <h4>Signed in as {{ name }}</h4>
      <select v-model="path" @change="navigate">
        <option value="/">Sign Out / Switch Customer Account</option>
        <option value="/create">Create New Customer Account</option>
      </select>
    </div>

    <div class="main">
      <div class="myItems">
        <div class="img-field">
          <p>Insert your image of a pet here to look for...</p>
          <input id="imageFile" type="file" accept="image/*" @change="handleFileUpload" />

          <div v-if="img_path" class="preview">
            <img v-if="img_path" :src="img_path" alt="Uploaded Image" />
          </div>
          <p v-else class="placeholder">No image uploaded.</p>

          <button @click="analyze">Analyze</button>
        </div>

        <div class="cart box">
          <p>Product(s) in your cart: </p>
          <ul>
            <li v-for="(item,index) in cartItems" :key="index">
              {{ item.name}} - {{ item.price }}
            </li>
          </ul>
          <p class="total">Total: ${{ totalPrice }}</p>
        </div>

        <div class="cart_buttons box">
          <button @click="add">Add Item(s) to Cart</button>
          <button @click="clearCart">Clear Cart</button>
        </div>

        <div class="checkout">
          <input type="text" v-model="cardNum" placeholder="Enter your card number" />
          <button @click="checkout">Checkout</button>
        </div>
      </div>

      <div class="img_details">
        <p v-if="analysis">Analysis Result: {{ analysis }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  data() {
    return {
      path: '',
      img_path: null,
      analysis: null,
      productList: "",
      cartItems: [],
      num_products: 0,
      cardNum: "",
      totalPrice: 0
    };
  },
  methods: {
    navigate() {
      if (this.path === "/" || this.path === "/create") {
        this.$router.push(this.path);
      } else {
        this.$router.push({ path: this.path, query: { name: this.$route.query.name } });
      }
    },
    handleFileUpload(event) {
      const file = event.target.files[0];
      if (file) {
        this.img_path = URL.createObjectURL(file);
      }
    },
    async analyze() {
      const input = document.getElementById('imageFile');
      if (!input.files.length) {
        alert("Please upload an image of the pet first.");
        return;
      }
      const formData = new FormData();
      formData.append('image', input.files[0]);
      alert("Analyzing image...");
      try {
        const response = await axios.post('http://localhost:30000/analyze', formData);
        this.analysis = response.data.img_details;
      } catch (error) {
        console.error("Error during analysis:", error);
        alert("Error analyzing image. Please try again.");
      }
    },
    add() {
      if (this.analysis && this.analysis.length > 0) {
        const text = this.analysis;
        const index1 = text.match(/Name:\s*(.*?)(?=\s*Price:|$)/);
        const index2 = text.match(/Price:\s*(.*)/);
        this.cartItems.push({ name: index1 ? index1[1].trim() : "Unknown", price: index2 ? index2[1].trim() : "0" });
        alert("Item(s) added to cart successfully.");
        this.analysis = "";
        this.num_products += 1;
        this.totalPrice = this.cartItems.reduce((sum, item) => {
          const price = parseFloat(item.price.toString().replace(/[^0-9.]/g, ""));
          return sum + (isNaN(price) ? 0 : price);
        }, 0).toFixed(2);
      } else {
        alert("No item(s) to add to cart.");
      }
    },
    checkout() {
  const cardRegex = /^\d{16}$/;
  if (!cardRegex.test(this.cardNum)) {
    alert("Please enter a valid 16-digit card number.");
    return;
  }

  if (this.cartItems.length === 0) {
    alert("No item(s) in cart to checkout.");
    return;
  }

  // Clean prices into numbers
  const cleanedCart = this.cartItems.map(item => ({
    name: item.name,
    price: parseFloat(item.price.toString().replace(/[^0-9.]/g, "")) || 0
  }));

  const data = {
    name: this.$route.query.name,
    productList: cleanedCart,
    cardNum: this.cardNum,
    num_products: this.num_products,
    total_price: parseFloat(this.totalPrice) // already numeric from computed
  };

  axios.post('http://localhost:30000/purchase', data)
    .then(response => {
      alert("Purchase successful! Your order has been placed.");
      this.cartItems = [];
      this.num_products = 0;
      this.cardNum = "";
    })
    .catch(error => {
      console.error("Error during purchase:", error);
      alert("Error during purchase. Please try again.");
    });
},
    clearCart() {
      this.productList = "";
      this.num_products = 0;
      alert("Cart cleared successfully.");
    }
  },
  computed: {
    name() {
      return this.$route.query.name;
    },
    totalPrice() {
    return this.cartItems.reduce((sum, item) => {
      // Remove any $ and convert to number
      const price = parseFloat(item.price.toString().replace(/[^0-9.]/g, ""));
      return sum + (isNaN(price) ? 0 : price);
    }, 0).toFixed(2);
  }
  }
};
</script>

<style scoped>
/* Container centers everything with consistent max-width */
.container {
  max-width: 1200px;
  margin: auto;
  padding: 2rem;
  box-sizing: border-box;
}

/* Header row */
.login {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #f5f5f5;
  padding: 1rem;
  border-bottom: 1px solid #ccc;
  border-radius: 8px;
  margin-bottom: 2rem;
}

/* Main section is flexible, not squished */
.main {
  display: flex;
  justify-content: center;
  gap: 2rem;
  flex-wrap: wrap;
}

/* Flexible items that adapt to screen width */
.myItems {
  flex: 1;
  min-width: 300px;
  max-width: 800px;
}

.img_details {
  flex: 1;
  min-width: 300px;
  max-width: 500px;
  padding: 1rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: #f9f9f9;
}

/* Upload box */
.img-field {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  padding: 1.5rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  width: 100%;
  background-color: #fafafa;
}

.preview img {
  max-width: 300px;
  max-height: 300px;
  border-radius: 6px;
}

.placeholder {
  font-style: italic;
  color: #888;
}

/* Cart + checkout sections */
.cart,
.cart_buttons,
.checkout {
  width: 100%;
  padding: 1rem;
  margin-top: 1rem;
  border-radius: 8px;
  border: 1px solid #ccc;
  background-color: #fff;
}

.cart {
  height: 200px;
  overflow-y: auto;
  text-align: left;
}

.cart_buttons {
  display: flex;
  gap: 1rem;
}

.checkout {
  display: flex;
  gap: 1rem;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .main {
    flex-direction: column;
    align-items: center;
  }
}

.cart ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.cart li {
  padding: 0.5rem 0;
  border-bottom: 1px solid #eee;
}

.total
{
  font-weight: bold;
  margin-top: 1rem;
  text-align: right;
}
</style>

