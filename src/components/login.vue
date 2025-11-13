<template>
  <div class="container">
    <div class="card">
      <h2 class="title">Customer Log In</h2>

      <form @submit.prevent="handleSubmit" class="form">
        <div class="form-group">
          <label for="username">Username</label>
          <input
            v-model="user_name"
            id="username"
            type="text"
            placeholder="Enter your username"
          />
        </div>

        <div class="form-group">
          <label for="password">Password</label>
          <input
            :type="showPass ? 'text' : 'password'"
            v-model="password"
            id="password"
            placeholder="Enter your password"
          />
          <button type="button" @click="togglePass" class="toggle-btn">
            {{ showPass ? 'Hide Password' : 'Show Password' }}
          </button>
        </div>

        <p class="message">{{ message }}</p>

        <button type="submit" class="submit-btn">Confirm</button>
      </form>

      <div class="footer">
        <p>Don't have a Customer account?</p>
        <button @click="newAcc" class="link-btn">Create New Account</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      user_name: '',
      password: '',
      message: '',
      showPass: false
    };
  },
  methods: {
    togglePass() {
      this.showPass = !this.showPass;
    },
    newAcc() {
      this.$router.push({ path: '/create' });
    },
    async handleSubmit() {
      if (!this.password) {
        this.message = 'Password is required.';
      } else if (!this.user_name) {
        this.message = 'Username is required.';
      } else {
        try {
          const response = await axios.post('http://localhost:30000/sign', {
            user_name: this.user_name,
            password: this.password
          });
          if (
            response.data.message ===
            'No account associated with this username and/or password'
          ) {
            this.message = response.data.message;
          } else {
            this.$router.push({
              path: '/menu',
              query: { name: response.data.name }
            });
          }
        } catch (err) {
          this.message = 'Server error. Please try again later.';
        }
      }
    }
  }
};
</script>

<style scoped>
/* Layout */
.container {
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f3f4f6;
  height: 100vh;
  padding: 1rem;
}

.card {
  background-color: #fff;
  padding: 2rem;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
}

/* Title */
.title {
  text-align: center;
  font-size: 24px;
  font-weight: bold;
  color: #333;
  margin-bottom: 1.5rem;
}

/* Form */
.form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label {
  margin-bottom: 0.5rem;
  color: #444;
  font-weight: 500;
}

.form-group input {
  padding: 0.5rem 0.75rem;
  border: 1px solid #ccc;
  border-radius: 8px;
  font-size: 1rem;
}

.toggle-btn {
  margin-top: 0.5rem;
  background: none;
  border: none;
  color: #0077cc;
  cursor: pointer;
  font-size: 0.9rem;
  align-self: flex-start;
  padding: 0;
}

.toggle-btn:hover {
  text-decoration: underline;
}

/* Message */
.message {
  color: #e11d48;
  min-height: 1.25rem;
  font-size: 0.875rem;
}

/* Buttons */
.submit-btn {
  padding: 0.75rem;
  background-color: #2563eb;
  color: #fff;
  border: none;
  border-radius: 10px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.submit-btn:hover {
  background-color: #1d4ed8;
}

/* Footer */
.footer {
  margin-top: 1.5rem;
  text-align: center;
}

.footer p {
  margin-bottom: 0.5rem;
  color: #555;
}

.link-btn {
  background: none;
  border: none;
  color: #2563eb;
  font-weight: 600;
  cursor: pointer;
  font-size: 1rem;
}

.link-btn:hover {
  text-decoration: underline;
}
</style>

<!-- Put this in your main.css (global styles) or in App.vue with non-scoped style -->
<style>
html, body, #app {
  margin: 0;
  padding: 0;
  height: 100%;
  font-family: Arial, sans-serif;
  overflow-x: hidden;
}
</style>
