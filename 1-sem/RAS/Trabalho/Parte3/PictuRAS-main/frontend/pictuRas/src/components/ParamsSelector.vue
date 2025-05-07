<template>
    <form v-if="activeTool" class="wrap" @submit.prevent>
      <ul class="params-list">
        <li
          v-for="param in activeTool.parameters"
          :key="param.name"
        >
            <div v-if="param.type === 'float'" class="slide-wraper">
            <h2>{{ param.name }}</h2>
            <input 
                :value="param.value"
                @input="handleInput(param, $event)"
                @blur="handleBlur(param)"
                type="number" 
                :step="0.01" 
                :min="param.min_value" 
                :max="param.max_value"
            />
            <ToolSlider 
                v-model="param.value" 
                :min="param.min_value" 
                :max="param.max_value" 
                :step="0.01" 
            />
            </div>
            <div v-if="param.type === 'int'" class="slide-wraper">
                <h2>{{ param.name }}</h2>
                <input 
                    :value="param.value"
                    @input="handleInput(param, $event)"
                    @blur="handleBlur(param)"
                    type="number" 
                    :step="1" 
                    :min="param.min_value" 
                    :max="param.max_value"
                    :decimals="0"
                />
                <ToolSlider 
                    v-model="param.value" 
                    :min="param.min_value" 
                    :max="param.max_value" 
                    :step="1" 
                    :decimals="0"
                />
            </div>
            <div v-if="param.type === 'hex'" class="hex-wraper">
                <h2>{{ param.name }}</h2>
                <Sketch v-model="param.value"/>
            </div>
        </li>
      </ul>
      <div class="btn-flex">
        
        <button @click="handleActivate">Apply</button>
        <button @click="handleDeactivate">Remove</button>
        <button @click="handleDup">Duplicate</button>
      </div>
      
    </form>
</template>

<script>
import { useEditingToolStore } from '../stores/EditingTool';
import { useProfileStore } from '../stores/ProfileStore'
import { storeToRefs } from 'pinia';
import ToolSlider from './ToolSlider.vue';
import { Sketch } from '@ckpack/vue-color';

export default {
  name: 'ParamsSelector',
  components: {
    ToolSlider,
    Sketch
  },
  setup() {
    const store = useEditingToolStore();
    const profileStore = useProfileStore();
    const { activeTool, tools } = storeToRefs(store);

    const clampValue = (value, min, max, isInt = false) => {
      let numValue = Number(value);

      // Handle NaN case
      if (isNaN(numValue)) {
        return min;
      }

      // Clamp value between min and max
      numValue = Math.min(Math.max(numValue, min), max);

      // Round if integer
      return isInt ? Math.round(numValue) : numValue;
    };

    const handleInput = (param, event) => {
      const value = event.target.value;

      // Allow empty input while typing
      if (value === '') {
        param.value = value;
        return;
      }

      const numValue = Number(value);

      // If the value is not a valid number, don't update
      if (isNaN(numValue)) {
        event.target.value = param.value;
        return;
      }

      // Update the value while typing, only enforcing min/max on blur
      param.value = param.type === 'int' ? Math.round(numValue) : numValue;
    };

    const handleBlur = (param) => {
      // Enforce min/max constraints when the input loses focus
      if (param.value === '' || typeof param.value !== 'number') {
        param.value = param.min_value;
      } else {
        param.value = clampValue(param.value, param.min_value, param.max_value, param.type === 'int');
      }
    };

    const validateList = (tools) => {
       // Filter the list to only include active tools
      const activeTools = tools.filter((tool) => tool.active)

      if (activeTools.length === 0) {
        return true // If no tools are active, the configuration is valid
      }

      // Validate the first active tool
      if (activeTools[0].input_type !== 'image') {
        return false // First active tool must have input_type 'image'
      }

      // Validate subsequent active tools
      for (let i = 1; i < activeTools.length; i++) {
        const prevTool = activeTools[i - 1]
        const currentTool = activeTools[i]

        // Check if the current tool's input_type matches the previous tool's output_type
        if (currentTool.input_type !== prevTool.output_type) {
          return false // Input type does not match previous output type
        }
      }

      return true // All active tools are valid
    }

    const handleActivate = () => {
      const newList = [...tools.value]; // Clone the updated list

      // Find the index of the active tool in the list
      const activeIndex = newList.findIndex((tool) => tool.name === activeTool.value.name);

      if (activeIndex !== -1) {
        // Set the active tool as active in the cloned list
        newList[activeIndex].active = true;

        // Validate the updated list
        if (!validateList(newList)) {
          alert('Invalid tool configuration: output type does not match the required type.');
          newList[activeIndex].active = false;
          return;
        }
        if (newList[activeIndex].premium === true && ( profileStore.userPlanName ==="free" || profileStore.userPlanName ==="basic" )){

          alert('Invalid tool configuration: Basic and free plan does not permit the usage of premium tools.');
          newList[activeIndex].active = false;
          return;

        }
        // Apply changes if the list is valid
        activeTool.value.active = true;
      }
    };

    const handleDeactivate = () => {
      const newList = [...tools.value]; // Clone the updated list

      // Find the index of the active tool in the list
      const activeIndex = newList.findIndex((tool) => tool.name === activeTool.value.name);

      if (activeIndex !== -1) {
        // Set the active tool as inactive in the cloned list
        newList[activeIndex].active = false;

        // Validate the updated list
        if (!validateList(newList)) {
          alert('Invalid tool configuration: input type does not match the required type.');
          newList[activeIndex].active = true;
          return;
        }

        // Apply changes if the list is valid
        activeTool.value.active = false;
      }
    };

    const handleDup = () => {
  if (activeTool.value.name.includes("copy")) {
    alert("You can't duplicate copies!");
    return;
  } if(activeTool.value.output_type !=='image'  ){
    alert("You can't duplicate tools that do not output images");
    return;
  }
    store.addTool();
};

    return {
      activeTool,
      tools,
      handleInput,
      handleBlur,
      handleActivate,
      handleDeactivate,
      handleDup
    };
  }
};

</script>

<style scoped>

.wrap{

    display: flex;
    flex-direction: column;
    height: 100%;
    align-items: center;
}

.params-list{

    display: flex;
    flex-direction: column;
    overflow-y: scroll;
    height: 60%;

}

ul {
    list-style: none;
    padding: 0;
  }
  
li {

    display: flex;
    flex-direction: column;
    align-items: center;

  }

.slide-wraper{

    display: flex;
    flex-direction: column;
    align-items: center;

}

.slide-wraper h2{

    font-size: 20px;
    font-weight: 500;

}

.hex-wraper{

    display: flex;
    flex-direction: column;
    align-items: center;

}

.hex-wraper h2{

    font-size: 20px;
    font-weight: 500;

}

.btn-flex{
    display: flex;
    flex-direction: row;
    gap:10px;

  }

</style>