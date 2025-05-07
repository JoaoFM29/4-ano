<template>
    <div class="base-div-inputs">
      <label :for="id">{{ label }}</label>
      <input
      :type="type"
      :id="id"
      :value="modelValue" 
      @input="$emit('update:modelValue', $event.target.value)"
      :placeholder="placeholder"
      :required="required"
      @focus="$emit('focus', $event)" 
      @blur="$emit('blur', $event)"
      class="base-input"
    />
    </div>
  </template>
  
  <script>
  export default {
    name: "Inputs",
    props: {
      id: {
        type: String,
        required: true,
      },
      label: {
        type: String,
        required: true,
      },
      type: {
        type: String,
        default: "text",
      },
      placeholder: {
        type: String,
        default: "",
      },
      modelValue: {
        type: [String, Number],
        default: "",
      },
      required: {
        type: Boolean,
        default: false,
      },
    },
    emits: ["update:modelValue"],
    watch: {
      modelValue(newValue) {
        this.$emit("update:modelValue", newValue);
      },
    },
  };
  </script>
  
  <style scoped>
  
.base-input {
  border: none;
  outline: none;
  border-radius: 15px;
  padding: 1.2em;
  padding-right: 7em;
  background-color: #ccc;
  box-shadow: inset 2px 5px 10px rgba(0,0,0,0.3);
  transition: 300ms ease-in-out;
  margin: 1em 0;
}

.base-input:focus {
  background-color: white;
  transform: scale(1.05);
  box-shadow: 13px 13px 100px #969696,
             -13px -13px 100px #ffffff;
}
  </style>
  