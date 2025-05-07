<template>
    <div v-if="show" class="password-modal">
      <ul>
        <li :class="{ valid: passwordLength }">
          <span v-if="passwordLength" class="check">✔</span>
          <span v-else class="cross">✘</span>
          Pelo menos 8 caracteres
        </li>
        <li :class="{ valid: hasUppercase }">
          <span v-if="hasUppercase" class="check">✔</span>
          <span v-else class="cross">✘</span>
          Pelo menos 1 letra maiúscula
        </li>
        <li :class="{ valid: hasNumber }">
          <span v-if="hasNumber" class="check">✔</span>
          <span v-else class="cross">✘</span>
          Pelo menos 1 número
        </li>
        <li :class="{ valid: hasSpecialChar }">
          <span v-if="hasSpecialChar" class="check">✔</span>
          <span v-else class="cross">✘</span>
          Pelo menos 1 caractere especial
        </li>
      </ul>
    </div>
  </template>
  
  <script>
  export default {
    name: "PasswordValidationModal",
    props: {
      show: {
        type: Boolean,
        required: true,
      },
      password: {
        type: String,
        default: "",
      },
    },
    computed: {
      passwordLength() {
        return this.password.length >= 8;
      },
      hasUppercase() {
        return /[A-Z]/.test(this.password);
      },
      hasNumber() {
        return /\d/.test(this.password);
      },
      hasSpecialChar() {
        return /[!@#$%^&*(),.?":{}|<>]/.test(this.password);
      },
    },
  };
  </script>
  
  <style scoped>
  .password-modal {
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
    right: -350px;
    width: 230px;
    padding: 1rem;
    background-color: #ffffff;
    border: 1px solid #ddd;
    border-radius: 1.5em;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    font-size: 0.9rem;
    text-align: left;
  }
  
  .password-modal ul {
    list-style: none;
    padding: 0;
    margin: 0;
  }
  
  .password-modal li {
    display: flex;
    align-items: center;
    margin-bottom: 0.5rem;
    color: #ff4d4f; 
  }
  
  .password-modal li.valid {
    color: #4caf50; 
  }
  
  .password-modal .check {
    margin-right: 0.5rem;
  }
  
  .password-modal .cross {
    margin-right: 0.5rem;
  }
  </style>
  