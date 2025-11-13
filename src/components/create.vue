<template>
  <div class="container">
    <div class="card">
      <h2 class="title">Create Account</h2>

      <form @submit.prevent="handleSubmit" class="form">
        <!-- Name Section -->
        <h3 class="section-title">Enter Name</h3>
        <div class="name-row">
          <div class="input-group">
            <label for="f_name">First Name</label>
            <input v-model="f_name" id="f_name" type="text" />
          </div>
          <div class="input-group">
            <label for="l_name">Last Name</label>
            <input v-model="l_name" id="l_name" type="text" />
          </div>
        </div>

        <!-- Email & Username Section -->
        <h3 class="section-title">Enter Email and Username</h3>
        <div class="name-row">
          <div class="input-group">
            <label for="email">Email</label>
            <input v-model="email" id="email" type="email" />
          </div>
          <div class="input-group">
            <label for="user_name">Username</label>
            <input v-model="user_name" id="user_name" type="text" />
          </div>
        </div>

        <!-- Password Section -->
        <h3 class="section-title">Enter Password</h3>
        <div class="password-group">
          <input
            :type="showPass ? 'text' : 'password'"
            v-model="password"
            id="password"
            placeholder="Enter password"
          />
          <button type="button" @click="togglePass" class="toggle-btn">
            {{ showPass ? 'Hide Password' : 'Show Password' }}
          </button>
        </div>

        <p class="message">{{ message }}</p>

        <button type="submit" class="submit-btn">Finish</button>
      </form>

      <div class="footer">
        <p>Already have a Customer Account?</p>
        <button @click="logIn" class="link-btn">Log In</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      f_name: '',
      l_name: '',
      email: '',
      user_name: '',
      password: '',
      showPass: false,
      message: ''
    };
  },
  methods: {
    togglePass() {
      this.showPass = !this.showPass;
    },
    async handleSubmit() {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

      if (this.password.length < 6) {
        this.message = 'Password must be at least 6 characters long.';
      } else if (this.f_name.length <= 0) {
        this.message = 'First name is required.';
      } else if (this.l_name.length <= 0) {
        this.message = 'Last name is required.';
      } else if (this.user_name.length < 6) {
        this.message = 'Username must be at least 6 characters long.';
      } else if (!emailRegex.test(this.email)) {
        this.message = 'Email address is not in a valid format.';
      } else {
        try {
          const response = await axios.post('http://localhost:30000/create', {
            f_name: this.f_name,
            l_name: this.l_name,
            email: this.email,
            user_name: this.user_name,
            password: this.password
          });
          if (response.data.message === "Account with this username and/or password already exists")
          {
            this.message = response.data.message;
          }
          else {
            this.$router.push({path: '/menu', query: {name: this.f_name+ " " + this.l_name + " (" + this.user_name + ")"}});
          }
        } catch (err) {
          this.message = 'Server error. Please try again later.';
        }
      }
    },
    logIn() {
      this.$router.push({ path: '/' });
    }
  }
};
</script>

<style scoped>
.container {
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f3f4f6;
  height: 100vh;
  width: 100%;
  padding: 1rem;
}

.card {
  background-color: #fff;
  padding: 2rem;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  width: 500px;
  width: 500px;
}

.title {
  text-align: center;
  font-size: 24px;
  font-weight: bold;
  color: #333;
  margin-bottom: 1.5rem;
}

.form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.section-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: #555;
}

.name-row {
  display: flex;
  flex-direction: row;
  gap: 1rem;
  flex-wrap: wrap;
}

.input-group {
  display: flex;
  flex-direction: column;
  flex: 1;
}

.input-group label {
  margin-bottom: 0.4rem;
  color: #444;
  font-weight: 500;
}

.input-group input {
  padding: 0.5rem 0.75rem;
  border: 1px solid #ccc;
  border-radius: 8px;
  font-size: 1rem;
}

.password-group {
  display: flex;
  flex-direction: column;
}

.password-group input {
  padding: 0.5rem 0.75rem;
  border: 1px solid #ccc;
  border-radius: 8px;
  font-size: 1rem;
  margin-bottom: 0.5rem;
}

.toggle-btn {
  background: none;
  border: none;
  color: #0077cc;
  cursor: pointer;
  font-size: 0.9rem;
  padding: 0;
  align-self: flex-start;
}

.toggle-btn:hover {
  text-decoration: underline;
}

.message {
  color: #e11d48;
  min-height: 1.25rem;
  font-size: 0.875rem;
}

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

.footer {
  margin-top: 2rem;
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
