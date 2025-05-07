<template>
    <div class="slider-container">
      <!-- Range slider -->
      <input
        type="range"
        :min="min"
        :max="max"
        :step="step"
        v-model="rawValue"
        @input="updateValue"
        class="slider"
      />
      <!-- Display value -->
      <span class="slider-value">{{ formattedValue }}</span>
    </div>
  </template>
  
  <script>
  export default {
    name: 'ToolSlider',
    props: {
      modelValue: { // Two-way binding
        type: Number,
        required: true,
      },
      min: {
        type: Number,
        default: 0,
      },
      max: {
        type: Number,
        default: 1, // Default range for floats
      },
      step: {
        type: Number,
        default: 0.1, // Default step for floats
      },
      decimals: {
        type: Number,
        default: 2, // Number of decimal places to display
      },
    },
    data() {
      return {
        rawValue: this.modelValue, // Internal value for the slider
      };
    },
    computed: {
        formattedValue() {
            const value = parseFloat(this.rawValue);

            if (value < this.min || isNaN(value)) {
            return parseFloat(this.min).toFixed(this.decimals);
            }
            if(value > this.max){
            return parseFloat(this.max).toFixed(this.decimals);
            }
            return value.toFixed(this.decimals);
        },
    },
    watch: {
      modelValue(newValue) {
        this.rawValue = newValue; // Sync parent updates
      },
    },
    methods: {
      updateValue() {
        // Emit the value as a float
        this.$emit('update:modelValue', parseFloat(this.rawValue));
      },
    },
  };
  </script>
  
  <style scoped>
  .slider-container {
    display: flex;
    align-items: center;
    gap: 10px;
  }
  
  .slider {
    appearance: none;
    width: 200px;
    height: 6px;
    background: #ddd;
    border-radius: 5px;
    outline: none;
  }
  
  .slider::-webkit-slider-thumb {
    appearance: none;
    width: 20px;
    height: 20px;
    background: #007bff;
    border-radius: 50%;
    cursor: pointer;
    box-shadow: 0 0 5px rgba(0, 0, 0, 0.2);
  }
  
  .slider-value {
    font-size: 14px;
    color: #333;
  }
  </style>
  